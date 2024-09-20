# Create a flask app with a page that has a form that accepts and returns json

from flask import Flask, request, jsonify, render_template
import requests, json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.identity import AzureCliCredential, ManagedIdentityCredential, AzureDeveloperCliCredential
import os

app = Flask(__name__)

print(app.name)

def run_code(code, token):
    AZURE_TENANT_ID = "b834794e-212a-4d12-81d1-c4b80e81bde0"
    credential = AzureDeveloperCliCredential(tenant_id=AZURE_TENANT_ID, process_timeout=60)
    token = credential.get_token("https://dynamicsessions.io/.default")

    session_id = "abc123"
    url = "https://eastasia.dynamicsessions.io/subscriptions/d90264b1-74b1-44b6-af25-a420cf18c61c/resourceGroups/rn-hack-containerapps/sessionPools/test-session1/code/execute?api-version=2024-02-02-preview&identifier=" + session_id
    # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2R5bmFtaWNzZXNzaW9ucy5pbyIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2I4MzQ3OTRlLTIxMmEtNGQxMi04MWQxLWM0YjgwZTgxYmRlMC8iLCJpYXQiOjE3MjY3MjMwNzgsIm5iZiI6MTcyNjcyMzA3OCwiZXhwIjoxNzI2NzI4MDQ0LCJhY3IiOiIxIiwiYWlvIjoiQWRRQUsvOFhBQUFBVkVJQW9qTHVXVGhtN2E0NmJmdldIbHlwRHhLa1ZGWmU3QkVxem1tWURCaHJLS29FNHlsT1pzMmhaMFBQYWtOOThPMVkyTlE3MGVmWUI4eUo5TDlFaFpJUUErR2RTdVNyYVVaODRMMjRlNGtJU2ZsQXJGQ210dHB4RklwR0tWemI4RUFqYjZ6VUVjeHRXbjN3ZkhDaGphWmZiQzkzMEpUY0hPcUorWll0VGRRN2tUQXN3Q1lVbEFINmpLV2tEejRINU1UdXplaWJWS2dwNWpEalZQM0J0Nk5aQ2dLa0YxSWxLU2ltM0pMeS8vV2NTT2ErZ2l4NTc1OU9RTTg5NFhsK3RYVlNRR0VjM2c5MEhEU2JFbFEvMFE9PSIsImFsdHNlY2lkIjoiNTo6MTAwMzIwMDFBMUU0OTAxOCIsImFtciI6WyJyc2EiLCJtZmEiXSwiYXBwaWQiOiJmNjQwNzFiOS1hNzliLTQ2NTUtOWRhZC0zYjM1MzVlMDBiODQiLCJhcHBpZGFjciI6IjAiLCJlbWFpbCI6InJlbmVlbm9ibGVAbWljcm9zb2Z0LmNvbSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxMTkuMTguMC4yMzMiLCJuYW1lIjoiUmVuZWUgTm9ibGUiLCJvaWQiOiJmZmViNTg2NC01ZTA0LTQyODAtYTRkZi04Y2QwYTc2MzFhM2QiLCJwdWlkIjoiMTAwMzIwMDNBRTQwRTAyOCIsInJoIjoiMC5BYmNBVG5rMHVDb2hFazJCMGNTNERvRzk0RF9YZlN3aGVsdEl1WDJpVUktaFVzUDhBRFkuIiwic2NwIjoiU2Vzc2lvbnMuUmVhZFdyaXRlLkFsbCIsInN1YiI6InBDamtoZDhWNF9XcHlMOUdUSllTeXpZZEJlU2VSaFlNZjFSSVhSZGZUdTgiLCJ0aWQiOiJiODM0Nzk0ZS0yMTJhLTRkMTItODFkMS1jNGI4MGU4MWJkZTAiLCJ1bmlxdWVfbmFtZSI6InJlbmVlbm9ibGVAbWljcm9zb2Z0LmNvbSIsInV0aSI6IjFoLUdVZVc5QlVpNkZjYmF5Rm9FQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfaWRyZWwiOiIxIDEwIn0.QJo4H2CJnfwkP4Cj1_jC6IwaYtgclq3QTkGGkFBQpmOlqfu0K4_zBM_9-2Uxs2GU4lzSNOlUo6cPreNbr-NH8xtXzKB7lNh-VbjI2HG5_HWAN3_XhoZW_FQVkXtv6gg35V_4rjRLer0DPF9qd-9YN_5JYYlyFEltsrw3cY_X7svEGhe9ue0_FS8xYg0ihjCOgm4ZF3r6uha79YbuuzVeOE8OXzbWgE8ppgMlJPccSjH7e6Kvz7g676qPwcog5_4HxmyArJCF9m4rYvNxdMtr-c-GQcClw3RrdCV0qH8a4_GnmZcoC7fckXiq_pocIy0f_xd7uvwPCtF33tD8aRVHBQ"
    print(code)
    body = {
            "properties": {
                "code": code,
                "codeInputType": "inline",
                "executionType": "synchronous",
                "timeoutInSeconds": 60,
                "enableEgress": True
            }
            }

    response = requests.post(url, json=body, headers={"Authorization": "Bearer " + token.token, "Content-Type": "application/json"})
    json_response = response.json()
    if json_response.get("properties", {}).get("stdout"):
        return json_response.get("properties").get("stdout")
    else:
        return "Empty response"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify(request.json)
    return 'Hello, World!'


@app.get('/code')
def chat():
    return render_template('code.html')

@app.route("/post-code", methods=["GET", "POST"])
def context_message():
    code = request.json["code"]
    print(code)
    # session_id = request.json["session_id"]
    session_id = "abc123"
    resp = run_code(code, session_id)
    return {"resp": resp}


if __name__ == '__main__':
    app.run(debug=True)
