import requests
import os 
import json

# get gladia api key
apiKey = os.getenv("GLADIA_API_KEY")
headers = {
    'x-gladia-key': apiKey,
}
file_path = "dQw4w9WgXcQ.mp4"
file_name, file_extension = os.path.splitext(file_path) # Get your audio file name + extension
with open(file_path, 'rb') as f:
    files = {
        'audio': ("dQw4w9WgXcQ.mp4", f, 'audio/'+file_extension[1:]),
        'toggle_diarization': (None, 'true'),
    }

    try:
        response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
    # Parse JSON error response
        error_json = response.json() 
        print(error_json)

    else:
        # Success
        data = response.json()

def seconds_to_timecode(x: float) -> str:
    """
    Convert a given number of seconds to a timecode string.

    Parameters:
        x (float): The number of seconds to convert.

    Returns:
        str: The timecode string in the format HH:MM:SS.mmm.
    """
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

segments = data['prediction']

lines = []
for count, segment in enumerate(segments):

    start = segment['time_begin']
    end = segment['time_end']
    
    text = segment['transcription'].replace('\n', ' ')

    lines.append(str(count + 1))
    lines.append(f"{seconds_to_timecode(start)} --> {seconds_to_timecode(end)}") 
    lines.append(text)
    lines.append('')

srt_text = '\n'.join(lines)

with open('video_transcription.srt', 'w') as srt:
    srt.write(srt_text)