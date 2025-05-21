import subprocess
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--project', required=True)
parser.add_argument('--role', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--apikey', required=True)
parser.add_argument('--assignee', required=True)
parser.add_argument('--scope', required=True)
args = parser.parse_args()

get_command = [
    "curl",
    "-X", "GET",
    f"https://coverity-dev.eaton.com/api/v2/projects/{args.project}",
    "-H", "Content-Type: application/json",
    "-u", f"{args.username}:{args.apikey}",
    "-s"
]

get_result = subprocess.run(get_command, capture_output=True, text=True)

if get_result.returncode != 0 or not get_result.stdout:
    print("Failed to fetch project details.")
    print("STDERR:", get_result.stderr)
    print("STDOUT:", get_result.stdout)
    exit(1)

project_data = json.loads(get_result.stdout)
project = project_data.get("projects", [])[0]

new_assignment = {
    "roleAssignmentType": "user",
    "roleName": args.role,
    "scope": args.scope,
    "username": args.assignee
}

if "roleAssignments" not in project:
    project["roleAssignments"] = []

project["roleAssignments"].append(new_assignment)
updated_payload = json.dumps(project)

put_command = [
    "curl",
    "-X", "PUT",
    f"https://coverity-dev.eaton.com/api/v2/projects/{args.project}",
    "-H", "Content-Type: application/json",
    "-u", f"{args.username}:{args.apikey}",
    "-d", updated_payload,
    "-w", "\\nHTTP Status: %{http_code}\\n",
    "-s"
]

put_result = subprocess.run(put_command, capture_output=True, text=True)

print("Response:")
print(put_result.stdout)
if put_result.stderr:
    print("Error:")
    print(put_result.stderr)
