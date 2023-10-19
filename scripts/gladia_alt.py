import requests
import os 

# get gladia api key
apiKey = os.getenv("GLADIA_API_KEY")

headers = {
    'x-gladia-key': apiKey,
}

files = {
    'audio_url': (None, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'),
    'toggle_diarization': (None, 'true'),
}

response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)

data = response.json()