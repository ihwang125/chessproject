from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle cross-origin requests
import requests

app = Flask(__name__)
CORS(app)  # Allow all domains for now (development only)

# Stockfish API endpoint
STOCKFISH_API_URL = "https://stockfish.online/api/s/v2.php"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    fen = data.get("fen")

    if not fen:
        return jsonify({"error": "FEN notation missing"}), 400

    # Call Stockfish API with GET request
    params = {"fen": fen, "depth": 15}  # Default depth 15
    response = requests.get(STOCKFISH_API_URL, params=params)

    if response.status_code == 200:
        stockfish_data = response.json()
        if stockfish_data.get("success"):
            best_move_raw = stockfish_data.get("bestmove", "Unknown")
            best_move = best_move_raw.split()[1] if len(best_move_raw.split()) > 1 else "Unknown"
            eval_score = stockfish_data.get("evaluation", "N/A")
            continuation = stockfish_data.get("continuation", "N/A")
            return jsonify({
                "best_move": best_move,
                "evaluation": eval_score,
                "continuation": continuation
            })
        else:
            return jsonify({"error": stockfish_data.get("data", "Unknown error")}), 400
    else:
        return jsonify({"error": "Stockfish API request failed."}), 500

if __name__ == "__main__":
    app.run(debug=True)