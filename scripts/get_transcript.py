import whisper
import json
# ffmpeg -i a4Vi7YUp9ws.mp4 a4Vi7YUp9ws.mp3
# Get the transcript of a video
def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

def translate(filename: str = "uMzULsAVh7M.mp3"):
    model = whisper.load_model("medium")
    # options = whisper.DecodingOptions(language="en", without_timestamps=True)
    options = dict(language="Japanese")
    transcribe_options = dict(task="translate", **options)
    result = model.transcribe("kageno.mp3", **transcribe_options)
    return result

def transcribe(filename: str = "uMzULsAVh7M.mp3"):
    model = whisper.load_model("small")
    # options = whisper.DecodingOptions(language="en", without_timestamps=True)
    options = dict(language="Japanese")
    transcribe_options = dict(task="transcribe", **options)
    result = model.transcribe("kageno.mp3", **transcribe_options)
    return result


if __name__ == "__main__":
    # convert this to argparse to eventually write a script to download the video and convert it to mp3
    filename = "kageno.mp3"
    # result = translate(filename)
    # lines = []
    # for count, segment in enumerate(result.get("segments")):
    #     # print(segment)
    #     start = segment.get("start")
    #     end = segment.get("end")
    #     lines.append(f"{count}")
    #     lines.append(f"{second_to_timecode(start)} --> {second_to_timecode(end)}")
    #     lines.append(segment.get("text", "").strip())
    #     lines.append('')
    # words = '\n'.join(lines)
    # base_name = filename.split(".")[0]
    # with open(f"{base_name}_translate.srt", "w") as f:
    #     f.write(words)

    # # dump json to file
    # with open(f"{base_name}_translate.json", "w") as f:
    #     json.dump(result, f, indent=4)

    result = transcribe(filename)
    lines = []
    for count, segment in enumerate(result.get("segments")):
        # print(segment)
        start = segment.get("start")
        end = segment.get("end")
        lines.append(f"{count}")
        lines.append(f"{second_to_timecode(start)} --> {second_to_timecode(end)}")
        lines.append(segment.get("text", "").strip())
        lines.append('')
    words = '\n'.join(lines)
    base_name = filename.split(".")[0]
    with open(f"{base_name}_transcribe.srt", "w") as f:
        f.write(words)

    # dump json to file
    with open(f"{base_name}_transcribe.json", "w") as f:
        json.dump(result, f, indent=4)
    # after writing the transcript.srt file, you can use the following command to convert the original mp4 file to have subtitles
    # ffmpeg -i testing.mp4 -vf subtitles=transcript.srt mysubtitledmovie.mp4
    # pass