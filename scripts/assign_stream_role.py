import subprocess
import json
import argparse

# Define the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--stream', required=True, help='Stream name')
parser.add_argument('--role', required=True, help='Role to assign')
parser.add_argument('--scope', required=True, help='Scope of the role')
parser.add_argument('--username', required=False, help='Username to assign the role to')
parser.add_argument('--group', required=False, help='Group name to assign the role to')
parser.add_argument('--description', required=True, help='Stream description')
parser.add_argument('--name', required=True, help='Stream name (for update)')
parser.add_argument('--primary_project_name', required=True, help='Primary project name')
parser.add_argument('--apiuser', required=True, help='Coverity API username')
parser.add_argument('--apikey', required=True, help='Coverity API key')
args = parser.parse_args()

# Step 1: Fetch current stream configuration
get_command = [
    "curl",
    "-X", "GET",
    f"https://coverity-dev.eaton.com/api/v2/streams/{args.stream}",
    "-H", "Content-Type: application/json",
    "-u", f"{args.apiuser}:{args.apikey}",
    "-s"
]

get_result = subprocess.run(get_command, capture_output=True, text=True)

if get_result.returncode != 0 or not get_result.stdout:
    print("Failed to fetch stream details.")
    print("STDERR:", get_result.stderr)
    print("STDOUT:", get_result.stdout)
    exit(1)

# Parse the JSON response
stream_data = json.loads(get_result.stdout)
stream = stream_data.get("streams", [])[0]

# Step 2: Append the new role assignment
if args.username:
    new_assignment = {
        "group": None,
        "roleAssignmentType": "user",
        "roleName": args.role,
        "scope": args.scope,
        "username": args.username
    }
elif args.group:
    new_assignment = {
        "group": {"name": args.group},
        "roleAssignmentType": "group",
        "roleName": args.role,
        "scope": args.scope
    }
else:
    print("Error: Either --username or --group must be provided.")
    exit(1)

# Ensure roleAssignments exists
if "roleAssignments" not in stream:
    stream["roleAssignments"] = []

stream["roleAssignments"].append(new_assignment)

# Step 3: Update other fields
stream["name"] = args.name
stream["description"] = args.description
stream["primaryProjectName"] = args.primary_project_name

# Step 4: Send updated stream configuration
updated_payload = json.dumps(stream)

put_command = [
    "curl",
    "-X", "PUT",
    f"https://coverity-dev.eaton.com/api/v2/streams/{args.stream}",
    "-H", "Content-Type: application/json",
    "-u", f"{args.apiuser}:{args.apikey}",
    "-d", updated_payload,
    "-w", "\\nHTTP Status: %{http_code}\\n",
    "-s"
]

put_result = subprocess.run(put_command, capture_output=True, text=True)

# Print the response
print("Response:")
print(put_result.stdout)
if put_result.stderr:
    print("Error:")
    print(put_result.stderr)
