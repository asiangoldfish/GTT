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

            ## Show time in hour or minute if applicable
            # Estimated time
            time_estimate_min = stats['time_estimate'] // 60 % 60
            time_estimate_hour = stats['time_estimate'] // 3600
            time_estimate_show = ''

            if time_estimate_hour > 0:
                time_estimate_show = f'{time_estimate_hour}h'
            if time_estimate_min > 0 :
                time_estimate_show += f'{time_estimate_min}m'
            
            # Time spent            
            time_spent_min = stats['total_time_spent'] // 60 % 60
            time_spent_hour = time_estimate_min // 60
            time_spent_show = ''

            if time_spent_hour > 0:
                time_spent_show = f'{time_spent_hour}h'
            if time_spent_min >0 :
                time_spent_show += f'{time_spent_min}m'

            data.append({
                "issue_id": issue["iid"],
                "title": issue["title"],
                "estimate": time_estimate_show,
                "spent": time_spent_show,
                "estimate_human": stats["human_time_estimate"],
                "spent_human": stats["human_total_time_spent"],
                "user": issue["assignee"]["name"] if issue["assignee"] else None
            })

        df = pd.DataFrame(data)
        df.to_csv("data/gitlab_time_tracking.csv", index=False)
