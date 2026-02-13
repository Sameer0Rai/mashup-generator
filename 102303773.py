import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
TRIMMED_DIR = "trimmed"
OUTPUT_DIR = "output"


def download_audios(singer_name, num_videos):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer_name}"])


def trim_audios(duration):
    os.makedirs(TRIMMED_DIR, exist_ok=True)

    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith(".mp3"):
            input_path = os.path.join(DOWNLOAD_DIR, file)
            audio = AudioSegment.from_mp3(input_path)

            trimmed_audio = audio[:duration * 1000]
            output_path = os.path.join(TRIMMED_DIR, file)

            trimmed_audio.export(output_path, format="mp3")


def merge_audios(output_file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    final_audio = AudioSegment.empty()

    for file in sorted(os.listdir(TRIMMED_DIR)):
        if file.endswith(".mp3"):
            audio_path = os.path.join(TRIMMED_DIR, file)
            audio = AudioSegment.from_mp3(audio_path)
            final_audio += audio

    output_path = os.path.join(OUTPUT_DIR, output_file)
    final_audio.export(output_path, format="mp3")


def main():
    if len(sys.argv) != 5:
        print("Usage: python 102303773.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    print("🎵 Downloading audios...")
    download_audios(singer_name, num_videos)

    print("✂️ Trimming audios...")
    trim_audios(duration)

    print("🎼 Merging audios...")
    merge_audios(output_file)

    print(f"✅ Mashup created successfully: output/{output_file}")


if __name__ == "__main__":
    main()
