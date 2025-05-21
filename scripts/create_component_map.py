import subprocess
import argparse

# Define the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True, help='Component Map name')
parser.add_argument('--description', required=True, help='Component Map description')
parser.add_argument('--username', required=True, help='Coverity API username')
parser.add_argument('--apikey', required=True, help='Coverity API key')
args = parser.parse_args()

# Define the curl command
curl_command = f'''curl --location "https://coverity-dev.eaton.com/api/v2/componentMaps" \
--header "Content-Type: application/json" \
--data "{{\\"description\\": \\"{args.description}\\", \\"name\\": \\"{args.name}\\"}}" \
-u "{args.username}:{args.apikey}"'''

# Run the curl command and capture output
result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

# Print the response
print("Response:\n", result.stdout)
if result.stderr:
    print("Errors:\n", result.stderr)
