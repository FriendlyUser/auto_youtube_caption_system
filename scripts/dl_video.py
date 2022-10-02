import youtube_dl 
import ffmpeg
import argparse
from utils import youtube_livestream_codes, youtube_mp4_codes

def get_video_metadata(video_url: str = "https://www.youtube.com/watch?v=21X5lGlDOfg&ab_channel=NASA")-> dict:
    with youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'}) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title', None)
        uploader_id = info_dict.get('uploader_id', None)
        print(f"[youtube] {video_title}: {uploader_id}")
    return info_dict


def parse_metadata(metadata) -> dict:
    """
    Parse metadata and send to discord.
    After a video is done recording, 
    it will have both the livestream format and the mp4 format.
    """
    # send metadata to discord
    formats = metadata.get("formats", [])
    # filter for ext = mp4
    mp4_formats = [f for f in formats if f.get("ext", "") == "mp4"]
    format_ids = [int(f.get("format_id", 0)) for f in mp4_formats]
    if livestream_entries := list(
        set(format_ids).intersection(youtube_livestream_codes)
    ):
        # get the first one
        livestream_entries.sort()
        selected_id = livestream_entries[0]

    video_entries = sorted(set(format_ids).intersection(youtube_mp4_codes))

    is_livestream = True
    if len(video_entries) > 0:
        # use video format id over livestream id if available
        selected_id = video_entries[0]
        is_livestream = False

    # TODO use video format if available


    return {
        "selected_id": selected_id,
        "is_livestream": is_livestream,
    }

def get_video(url: str, config: dict):
    """
    Get video from start time.
    """
    # result = subprocess.run()
    # could delay start time by a few seconds to just sync up and capture the full video length
    # but would need to time how long it takes to fetch the video using youtube-dl and other adjustments and start a bit before
    filename = config.get("filename", "livestream01.mp4")
    end = config.get("end", "00:00:10")
    overlay_file = ffmpeg.input(filename)
    (
        ffmpeg
        .input(url, t=end)
        .output(filename)
        .run()
    )

def get_all_files(url: str, end: str = "00:01:30"):
    metadata = get_video_metadata(url)
    temp_dict = parse_metadata(metadata)
    selected_id = temp_dict.get("selected_id", 0)
    formats = metadata.get("formats", [])
    selected_format = [f for f in formats if f.get("format_id", "") == str(selected_id)][0]
    format_url = selected_format.get("url", "")
    filename = f"{metadata.get('id', '')}.mp4"
    filename = filename.replace("-", "")
    get_video(format_url, {"filename": filename, "end": "00:01:30"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://www.youtube.com/watch?v=21X5lGlDOfg&ab_channel=NASA")
    parser.add_argument("--end", type=str, default="00:01:30")
    args = parser.parse_args()
    get_all_files(args.url, args.end)
