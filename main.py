import os
import requests
import pandas as pd
from dotenv import load_dotenv
import json

# Load variables from .env
load_dotenv()

GITLAB_URL = os.getenv("VENDOR_URL")
TOKEN = os.getenv("TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")

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

os.makedirs("data", exist_ok=True)

# TODO add prefix as CLI arg

# Export to CSV
print("Exporting time tracking data to data/gitlab_time_tracking.csv..")
df = pd.DataFrame(data)
df.to_csv("data/gitlab_time_tracking.csv", index=False)

# Export response to JSON
print("Exporting response to data/gitlab_response.json..")
with open('data/gitlab_response.json', 'w') as fp:
    json.dump(issues, fp, indent=2)

