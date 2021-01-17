import requests


url = "http://localhost:8080"
r = requests.post(
    url,
    params={'user': 'bruno'},
    data={'number': [12524, 356, 42357, 467], 'type': 'issue', 'action': 'show'}
)

print("DONE")
