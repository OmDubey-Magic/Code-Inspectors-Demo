import requests
import os
import urllib.parse

# from playsound import playsound
import subprocess
import time

# import subprocess

# Define the URL of your PDF file
SOURCE_FILE_URL = "https://venturebeat.com/wp-content/uploads/2010/09/amzn_shareholder-letter-20072.pdf"

# PlayNote API URL
url = "https://api.play.ai/api/v1/playnotes"

# Retrieve API key and User ID from environment variables
api_key = "ak-750f896380344ec5b36c51d38c233f46"
# Set this in your environment variables
user_id = "Xiy8aPZr7Dd1htPUUM44MPBCT6A3"
# Set this in your environment variables

if not api_key or not user_id:
    raise ValueError(
        "API key or User ID is missing. Set them as environment variables."
    )

headers = {
    "content-type": "application/json",
    "AUTHORIZATION": api_key,
    "X-USER-ID": user_id,
}
# Set up headers with authorization details
# headers = {"AUTHORIZATION": api_key, "X-USER-ID": user_id, "accept": "application/json"}

# Configure the request parameters
files = {
    "sourceFileUrl": (None, SOURCE_FILE_URL),
    "synthesisStyle": (None, "podcast"),
    "voice1": (
        None,
        "s3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json",
    ),
    "voice1Name": (None, "Angelo"),
    "voice2": (
        None,
        "s3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json",
    ),
    "voice2Name": (None, "Deedee"),
}

# Send the POST request
response = requests.post(url, headers=headers, files=files)

print("************", response)
print("************", response.text)
# Check the response
if response.status_code == 201:
    print("Request sent successfully!")
    playNoteId = response.json().get("id")
    print(f"Generated PlayNote ID: {playNoteId}")
else:
    print(f"Failed to generate PlayNote: {response.text}")
    exit()

# Double encode the PlayNoteId
double_encoded_id = urllib.parse.quote(playNoteId, safe="")

# Construct the final URL
url = f"https://api.play.ai/api/v1/playnotes/{double_encoded_id}"

MAX_RETRIES = 3  # Maximum retries before giving up
RETRY_DELAY = 10  # Delay in seconds between retries

audio_url = None  # Initialize audio_url

for attempt in range(MAX_RETRIES):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get("status")
        if status == "completed":
            audio_url = response.json().get("audioUrl")
            print(f"Audio URL: {audio_url}")
            break
        elif status == "generating":
            print(
                f"Attempt {attempt + 1}/{MAX_RETRIES}: PlayNote is still generating. Retrying in {RETRY_DELAY} seconds..."
            )
            time.sleep(RETRY_DELAY)
        else:
            print("PlayNote creation was not successful. Please try again.")
            exit()
    else:
        print(f"Error fetching PlayNote status: {response.text}")
        exit()

# Ensure we have a valid audio URL before proceeding
if not audio_url:
    print("PlayNote generation failed or did not complete within the retry limit.")
    exit()


# Download the audio file
audio_filename = "output.wav"
response = requests.get(audio_url, stream=True)
if response.status_code == 200:
    with open(audio_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Audio file downloaded as {audio_filename}")
else:
    print(f"Failed to download audio file: {response.text}")
    exit()

# Play the audio file
try:
    subprocess.run(["ffplay", "-nodisp", "-autoexit", audio_filename], check=True)
except FileNotFoundError:
    print("Please install ffplay (part of FFmpeg) to play the audio.")

# try:
#     print("Playing audio...")
#     playsound(audio_filename)
# except Exception as e:
#     print(f"Error playing audio: {e}")
