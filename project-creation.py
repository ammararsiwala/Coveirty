import subprocess

description = input("Enter the description: ")
name = input("Enter the name: ")

curl_command = f'curl --location "https://coverity-dev.eaton.com/api/v2/projects" --header "Content-Type: application/json" --data "{{\\"description\\": \\"{description}\\", \\"name\\": \\"{name}\\"}}" -u "ammararsiwala@eaton.com:9268BFC6A5A1BEE79B2DD3346CAC86C8"'

result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

print("Response:\n", result.stdout)
if result.stderr:
    print("Errors:\n", result.stderr)



