from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle cross-origin requests
import requests
import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

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
            explanation = get_gemini_explanation(fen, best_move)
            return jsonify({
                "best_move": best_move,
                "evaluation": eval_score,
                "explanation": explanation
            })
        else:
            return jsonify({"error": stockfish_data.get("data", "Unknown error")}), 400
    else:
        return jsonify({"error": "Stockfish API request failed."}), 500
    
def get_gemini_explanation(fen, best_move):
    """Send the FEN and best move to Gemini for explanation."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"As a chess tutor, explain why {best_move} is the best move in this position: {fen} as briefly as possible", generation_config={"max_output_tokens": 200})

        return response.text if response else "No explanation available."
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Error fetching explanation."

if __name__ == "__main__":
    app.run(debug=True)
