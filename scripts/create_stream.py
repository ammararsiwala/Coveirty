import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
parser.add_argument('--description', required=True)
parser.add_argument('--project', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--apikey', required=True)
args = parser.parse_args()

curl_command = [
    "curl",
    "-X", "POST",
    "https://coverity-dev.eaton.com/api/v2/streams",
    "-H", "Content-Type: application/json",
    "-u", f"{args.username}:{args.apikey}",
    "-d", f'{{"description":"{args.description}","name":"{args.name}","triageStoreName":"Default Triage Store","primaryProjectName":"{args.project}"}}',
    "-w", "\\nHTTP Status: %{http_code}\\n",
    "-s"
]

result = subprocess.run(curl_command, capture_output=True, text=True)

print("Response:")
print(result.stdout)
if result.stderr:
    print("Error:")
    print(result.stderr)
