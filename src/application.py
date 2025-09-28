from os import getenv, path, makedirs
import requests
import pandas as pd
from dotenv import load_dotenv
import json


class Application:
    def __init__(self):
        self.debug = False
        self.env_file = path.abspath('.env')
        self.format = ''
        self.allowed_formats = ['json', 'table']

    def init(self) -> bool:
        if len(self.format) == 0:
            print("No format was specified.")
            return False
        else:
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

    def show_time_table(self) -> None:

        load_dotenv()

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
        data = []
        for issue in issues:
            stats = issue["time_stats"]
            data.append({
                "issue_id": issue["iid"],
                "title": issue["title"],
                "estimate_sec": stats["time_estimate"],
                "spent_sec": stats["total_time_spent"],
                "estimate_human": stats["human_time_estimate"],
                "spent_human": stats["human_total_time_spent"],
                "user": issue["assignee"]["name"] if issue["assignee"] else None
            })

        makedirs("data", exist_ok=True)

        # TODO add prefix as CLI arg

        # Export to CSV
        print("Exporting time tracking data to data/gitlab_time_tracking.csv..")
        df = pd.DataFrame(data)
        df.to_csv("data/gitlab_time_tracking.csv", index=False)

        # Export response to JSON
        print("Exporting response to data/gitlab_response.json..")
        with open('data/gitlab_response.json', 'w') as fp:
            json.dump(issues, fp, indent=2)
