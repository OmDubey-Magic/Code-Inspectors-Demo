"""This is the main flask api module where we call all the function.
"""

import warnings

warnings.filterwarnings("ignore")
from flask import Flask, request, jsonification
from flask_cors import CORS
from main import voice
import os, json
from pydub import AudioSegment

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# ---------------------------------------------------------------------------------


# ------------------------------------------------------------
@app.route("/callview", methods=["POST"])
def callview_class():
    try:
        # Retrieve model selection as a string and parse it
        data = request.get_json()
        modelSelection = request.form.get("modelSelection", "[]")
        modelSelection = json.loads(modelSelection)  # Convert string to a list
        choice = data.get("choice", "")
        text_data = data.get("text_data")

        if not text_data:
            return jsonify({"sts": 0, "msg": "No text data provided"})

        result, transcript_data = voice(choice, modelSelection, text_data)
        print("result", result)

        return jsonify(
            {
                "sts": 1,
                "msg": "Audio processed successfully",
                "response_text": result,
                "transcript": transcript_data,
            }
        )

    except Exception as e:
        print("ERROR", f"Error in Function: {str(e)}")
        return jsonify({"sts": 0, "msg": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
