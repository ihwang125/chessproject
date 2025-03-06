import requests

# Define API endpoint and parameters
url = "https://stockfish.online/api/s/v2.php"
params = {
    "fen": "rnbqkb1r/pppppppp/5n2/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 1",
    "depth": 15
}

# Send GET request
response = requests.get(url, params=params)

# Print response
print(response.json())  # Assumes the response is JSON
print(response.json()['bestmove'].split(" ")[1])

