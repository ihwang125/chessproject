from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Stockfish API endpoint (replace with actual API if needed)
STOCKFISH_API_URL = "https://stockfish-api.example.com/getBestMove"  # Replace with actual API

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    fen = data.get("fen")

    if not fen:
        return jsonify({"error": "FEN notation missing"}), 400

    # Call Stockfish API
    response = requests.post(STOCKFISH_API_URL, json={"fen": fen})

    if response.status_code == 200:
        stockfish_data = response.json()
        best_move = stockfish_data.get("best_move", "Unknown")
        explanation = stockfish_data.get("explanation", "No explanation available.")
    else:
        best_move = "N/A"
        explanation = "Stockfish API failed."

    return jsonify({"best_move": best_move, "response": explanation})

if __name__ == "__main__":
    app.run(debug=True)

