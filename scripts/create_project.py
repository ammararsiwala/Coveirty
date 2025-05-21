import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
parser.add_argument('--description', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--apikey', required=True)
args = parser.parse_args()

curl_command = f'''curl --location "https://coverity-dev.eaton.com/api/v2/projects" \
--header "Content-Type: application/json" \
--data '{{"description": "{args.description}", "name": "{args.name}"}}' \
-u "{args.username}:{args.apikey}"'''

result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

print("Response:\n", result.stdout)
if result.stderr:
    print("Errors:\n", result.stderr)

