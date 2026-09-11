"""Sentinel — Security Awareness Chatbot.

A self-contained Flask app: serves a chat UI and a single /api/chat
endpoint backed by a local security knowledge base. No API keys or
external LLM required — it runs anywhere Python runs.
"""
import os

from flask import Flask, jsonify, request, send_from_directory

from chatbot.engine import get_response

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(reply="Ask me anything about staying secure online.")
    return jsonify(reply=get_response(message))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
