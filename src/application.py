from os import getenv, path, makedirs
import requests
import pandas as pd
from dotenv import load_dotenv
import json
from tabulate import tabulate


class Application:
    def __init__(self):
        self.debug = False
        self.env_file = path.abspath('.env')
        self.allowed_formats = ['csv']

    def init(self) -> bool:
        self.load_env()
        return True

    def set_format(self, format) -> bool:
        self.format = format
        return format in self.allowed_formats

    def load_env(self) -> bool:
        """
        Load environment variables

        Returns
        -------
        bool
            True if the environment was successfully loaded, otherwise
        """
        if self.debug:
            print("Loading secrets")

        # if os.path.exists()
        if path.exists(".env"):
            load_dotenv()
        else:
            print(f"Failed to environment variables from {self.env_file}")
            return False

        return True

    def sync(self) -> bool:
        print("Synchronising with remote...")

        GITLAB_URL = getenv("VENDOR_URL")
        TOKEN = getenv("TOKEN")
        PROJECT_ID = getenv("PROJECT_ID")

        headers = {"PRIVATE-TOKEN": TOKEN}

        def fetch_all_issues():
            # TODO: Enable caching with CLI arg
            issues = []
            url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues"
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            batch = resp.json()
            issues.extend(batch)
            return issues

        # Collect data
        issues = fetch_all_issues()

        makedirs("data", exist_ok=True)

        # TODO add prefix as CLI arg

        # Export response to JSON
        print("Cache is stored at data/gitlab_response.json.")
        with open('data/gitlab_response.json', 'w') as fp:
            json.dump(issues, fp, indent=2)

    def show(self, format) -> None:
        if format not in self.allowed_formats:
            print(f"Format '{format}' is not supported. Supported formats:")

            for f in self.allowed_formats:
                print(f'\t{f}')

            return

        if not path.exists('data/gitlab_response.json'):
            if not self.sync():
                print('Failed to synchronise with remote')
                return

        # Export to CSV
        print("Exporting time tracking data to data/gitlab_time_tracking.csv..")

        data = []
        issues = {}
        with open('data/gitlab_response.json') as fp:
            issues = json.load(fp)

        for issue in issues:
            stats = issue["time_stats"]

            data.append({
                "issue_id": issue["iid"],
                "title": issue["title"],
                "estimate_human": stats["human_time_estimate"],
                "spent_human": stats["human_total_time_spent"],
                "user": issue["assignee"]["name"] if issue["assignee"] else None
            })

        df = pd.DataFrame(data)
        df.to_csv("data/gitlab_time_tracking.csv", index=False)

    def show_time_estimate_deviation(self, user: str, sprint: int=-1) -> None:
        """
        For a specific user, compute the time estimate deviation.

        Arguments
        ---------
        user:
            Full name of the user in question.
        sprint:
            Include issues only in a specific sprint. Default: all sprints
        """
        if not user or len(user) == 0:
            print('Missing user name')
            return

        if not path.exists('data/gitlab_response.json'):
            if not self.sync():
                print('Failed to synchronise with remote')
                return
            
        # Sprint is parsed from CLI. Check that it's an integer
        try:
            sprint = int(sprint)
        except ValueError:
            print("Argument for --sprint must be an integer")
            return

        # Gather all issues related to the user
        # If a sprint is specified, aka. >= 1, then only inclued issues related
        # that sprint. A sprint is marked by milestone named 'Sprint X'.
        data = []
        issues = {}
        with open('data/gitlab_response.json') as fp:
            issues = json.load(fp)


        # Compute the deviation
        total_estimated_time = 0    # in seconds
        total_spent_time = 0        # in seconds

        for issue in issues:
            if not issue['assignee'] or issue['assignee']['name'] != user:
                continue

            if int(sprint) >= 0:
                milestone = issue.get('milestone')
                # Issue does not have milestone. Skip
                if not milestone or issue.get('milestone').get('title') != f'Sprint {sprint}':
                    continue

            stats = issue['time_stats']

            acc = 0
            if stats['time_estimate'] > 0:
                acc = stats['total_time_spent'] / stats['time_estimate']

            data.append([
                issue["iid"],
                issue["title"],
                stats['human_time_estimate'],
                stats['human_total_time_spent'],
                acc # Accuracy
            ])

            total_estimated_time += stats['time_estimate']
            total_spent_time += stats['total_time_spent']

        if len(data) == 0:
            # No data was found. Compose error message
            print(f'No data was found for user \'{user}\'' , end='')

            if int(sprint) >= 0:
                print(f' on sprint {sprint}')
            return
        
        print(tabulate(data, headers=['issue_id', 'title', 'estimate', 'spent', 'accuracy']))
        acc = 0
        if total_estimated_time > 0:
            acc = total_spent_time * 100 // total_estimated_time
        print(f'\nTotal accuracy: {acc}%')

        # if int(sprint) >= 0:
        #     print(f'Sprint {sprint}:')

        # print(f'Total estimated: {total_estimated_time}s')
        # print(f'Total spent: {total_spent_time}s')

        # if total_estimated_time == 0:
        #     accuracy = 0
        # else:
        #     accuracy = total_spent_time*100//total_estimated_time

        # print(f'Accuracy: {accuracy}%')
        print(f'\nIntepretation: <100% means spent less than estimated time. \
>100% means spent more than estimated time.')
