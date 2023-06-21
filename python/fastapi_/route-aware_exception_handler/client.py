import requests



for _ in range(4):
    anvil_response = requests.post("http://localhost:8000/anvil", json={"weight": 100})
    print(f"anvil response: HTTP {anvil_response.status_code} {anvil_response.json()}")

    tnt_response = requests.post("http://localhost:8000/tnt", json={"yield": 100})
    print(f"TNT response:   HTTP {tnt_response.status_code} {tnt_response.json()}")
    print('---\n')
