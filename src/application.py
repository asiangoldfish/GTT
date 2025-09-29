from os import getenv, path, makedirs
import requests
import pandas as pd
from dotenv import load_dotenv
import json


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

    def show_time_estimate_deviation(self, user: str) -> None:
        """
        For a specific user, compute the time estimate deviation.

        Arguments
        ---------
        user:
            Full name of the user in question.
        """
        if not user or len(user) == 0:
            print("Missing user name")
            return

        if not path.exists('data/gitlab_response.json'):
            if not self.sync():
                print('Failed to synchronise with remote')
                return

        # Gather all issues related to the user
        data = []
        issues = {}
        with open('data/gitlab_response.json') as fp:
            issues = json.load(fp)

        for issue in issues:
            if not issue["assignee"] or issue["assignee"]["name"] != user:
                continue

            stats = issue["time_stats"]

            data.append({
                "estimate": stats["time_estimate"],
                "spent": stats["total_time_spent"],
            })

        if len(data) == 0:
            print("No user was found")
            return

        # Compute the deviation
        total_estimated_time = 0    # in seconds
        total_spent_time = 0        # in seconds
        for d in data:
            total_estimated_time += d.get('estimate')
            total_spent_time += d.get('spent')

        print(f'Total estimated: {total_estimated_time}s')
        print(f'Total spent: {total_spent_time}s')

        print(f'Accuracy: {total_spent_time*100//total_estimated_time}%')
        print(f'Intepretation: <100% means spent less than estimated time. \
>100% means spent more than estimated time.')
