"""Flask API Proxy Module.

This module sets up a Flask application that acts as an API proxy,
handling requests and responses to ensure API credentials remain secure.
"""

import logging
import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load API credentials
API_ENDPOINT = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("API_KEY")


@app.route("/proxy", methods=["GET"])
def proxy_request():
    """Intercepts and forwards requests to the SAM.gov API while injecting the API key."""
    if not API_ENDPOINT or not API_KEY:
        logger.error("Missing API configuration (API_ENDPOINT or API_KEY)")
        return jsonify({"error": "Missing API configuration"}), 500

    # Extract query parameters from the incoming request
    params = request.args.to_dict()

    # Ensure `postedFrom` and `postedTo` are included
    if "postedFrom" not in params or "postedTo" not in params:
        logger.error("Missing required parameters: postedFrom and postedTo")
        return (
            jsonify({"error": "Missing required parameters: postedFrom and postedTo"}),
            400,
        )

    # Inject the API key
    params["api_key"] = API_KEY

    logger.info(
        "Forwarding request to SAM.gov: %s with params %s", API_ENDPOINT, params
    )

    try:
        # Forward the request
        response = requests.get(API_ENDPOINT, params=params)

        logger.info("SAM.gov response status: %s", response.status_code)
        return jsonify(response.json()), response.status_code

    except requests.RequestException as e:
        logger.error("Failed to contact API: %s", str(e))
        return jsonify({"error": "Failed to contact API", "details": str(e)}), 500


@app.route("/", methods=["CONNECT"])
def handle_connect():
    """Handles CONNECT requests to prevent 'curl' from misinterpreting the API proxy as a forward proxy."""
    logger.warning("Received a CONNECT request. This is not a forward proxy.")
    return Response(
        "CONNECT method is not supported. Use direct HTTPS requests.", status=405
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info("Starting Flask API Proxy on port %s", port)
    app.run(host="0.0.0.0", port=port)
