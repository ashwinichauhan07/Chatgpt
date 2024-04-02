import assemblyai as aai

# replace with your API token
aai.settings.api_key = f"795d6163420748d8b72a2c6a6da14be0"

# URL of the file to transcribe
FILE_URL = "C:/Users/Ashwini/Downloads/harvard.wav"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

print(transcript.text)