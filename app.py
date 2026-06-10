from openai import OpenAI
import subprocess
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Get all pods
pods = subprocess.check_output(
    "kubectl get pods -n shine-prod --no-headers",
    shell=True,
    text=True
)

first_pod = pods.split()[0]

# Get logs
logs = subprocess.check_output(
    f"kubectl logs {first_pod} -n shine-prod --tail=100",
    shell=True,
    text=True
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": f"""
Analyze these Kubernetes logs.

Provide:
1. Root Cause
2. Severity
3. Fix

Logs:
{logs}
"""
        }
    ]
)

print(response.choices[0].message.content)