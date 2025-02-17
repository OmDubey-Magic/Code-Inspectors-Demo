import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import whisper
import os
import google.generativeai as genai
import pyttsx3
import time

gemini_api_key = "AIzaSyD5C8HHzJEe_QDzHfJzT85W4u6TSXx3Qxc"
# Initialize Whisper model
whisper_model = whisper.load_model("medium")

# Transcript list to store interactions
transcript = []


# Function to record audio
# def record_audio(duration=5, fs=16000):
#     print("Recording...")
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
#     sd.wait()  # Wait until recording is finished
#     print("Recording finished.")
#     return np.squeeze(audio)


# Function to transcribe audio with Whisper
# def transcribe_audio(audio):
#     print("transcribe executed")
#     start_time = time.time()
#     try:
#         transcription = whisper_model.transcribe(audio)
#         user_text = transcription["text"]
#         print("User Query:", user_text)

#         return user_text
#     except Exception as e:
#         print("ERROR Error in Function:", str(e))
#         return None
#     finally:
#         elapsed_time = time.time() - start_time
#         print(f"time by transcribe audio: {elapsed_time:.2f} sec")


def get_ai_response(user_text, choice):
    start_time = time.time()
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = f"""The Question is: {user_text}, respond the question like you are answering the question as a human being would do and restrict response to 50 words only, a formal and informative assistant" if {choice} == "male" else "a casual and friendly assistant"""
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    print("Assistant Response:", response_text)
    elapsed_time = time.time() - start_time
    print(f"Time taken by get_ai_response: {elapsed_time:.2f} seconds")
    return response_text


def text_to_speech(text, voice="male"):
    start_time = time.time()
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id if voice == "male" else voices[1].id)
    file_path = "response_files"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_res_path = os.path.join(file_path, "response_audio.wav")
    engine.save_to_file(text, file_res_path)
    engine.runAndWait()
    elapsed_time = time.time() - start_time  # End timer
    print(f"Time taken by text_to_speech: {elapsed_time:.2f} seconds")
    return file_res_path


def male_assistant_interaction(choice, modelSelection, user_text):
    print("Interacting with Male Assistant...")
    # user_text = transcribe_audio(audio)
    response_text = get_ai_response(user_text, choice)

    # Append to transcript
    transcript.append(f"User (Male Assistant): {user_text}")
    transcript.append(f"Male Assistant: {response_text}")

    # Display current transcript
    print("\n--- Transcript ---")
    for line in transcript:
        print(line)
    print("------------------\n")

    # response_audio = text_to_speech(response_text, choice)
    # print("888888888", response_audio)
    return response_text, transcript


# Function for Female Assistant Interaction
def female_assistant_interaction(choice, modelSelection, text_data):
    print("Interacting with Female Assistant...")

    # user_text = transcribe_audio(audio)
    response_text = get_ai_response(text_data, choice)

    # Append to transcript
    transcript.append(f"User (Female Assistant): {text_data}")
    transcript.append(f"Female Assistant: {response_text}")

    # Display current transcript
    print("\n--- Transcript ---")
    for line in transcript:
        print(line)
    print("------------------\n")

    # response_audio = text_to_speech(response_text, choice)
    return response_text, transcript


def voice(choice, modelSelection, text_data):
    print("Welcome to the AI Voice Assistant!")
    print(text_data)
    if choice == "male":
        response_text, transcript_data = male_assistant_interaction(
            choice, modelSelection, text_data
        )
    elif choice == "female":
        response_text, transcript_data = female_assistant_interaction(
            choice, modelSelection, text_data
        )
    else:
        print("Invalid choice. Please select 'male', 'female'")
        return None, []
    return response_text, transcript_data
