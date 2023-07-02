import os
import re
import pytube
from pytube import YouTube
from moviepy.editor import AudioFileClip
import moviepy.editor as mp
import os
def download_youtube_video(url, output_path):
    #try:
    #    yt = YouTube(url)
    #    video = yt.streams.filter(only_audio=True).first()
    #    video.download(output_path=output_path)
    #    file_name = video.default_filename
    #    return os.path.join(output_path, file_name)
    #except pytube.exceptions.PytubeError:
    #    return None

    yt = YouTube(url)
    filename= url.rsplit('/', 1)[-1].replace("?", "!")
    print(
        "filename", filename
    )

    yt.streams.get_highest_resolution().download(output_path=output_path, filename=filename + ".mp4")
    video_path = output_path + f"/{filename}" + ".mp4"
    
    audio_path = output_path + f"/{filename}" + ".wav"

    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    video.close()
    #video.reader.close()
    #3video.audio.reader.close_proc()

    return audio_path

def convert_to_wav(file_path, output_path):
    try:
        clip = AudioFileClip(file_path)
       # wav_file = os.path.splitext(os.path.basename(file_path))[0] + ".wav"
        wav_file = f"{file_path[:-4]}.wav"
        print(wav_file)
    
        #print("wav_file", wav_file)
        #print("os_stuff", os.path.splitext(os.path.basename(file_path))[0])
        print("ef")
        wav_path = os.path.join(output_path, wav_file)
        print(wav_path)
       # print("wav_path", wav_path)
        clip.write_audiofile(wav_path)
        print("rgvsgf")
        return wav_path
    except Exception as e:
        print(e)
        return None

def check_file_type(input_path):
    file_extension = os.path.splitext(input_path)[1].lower()

    if file_extension == ".mp4":
        return "MP4"
    elif file_extension == ".mp3":
        return "MP3"
    else:
        return None

def process_input(input_path, output_path):
    file_type = check_file_type(input_path)

    if file_type == "MP4":
        wav_path = convert_to_wav(input_path, output_path)
        if wav_path:
            print("MP4 file converted to WAV successfully!")
            print("WAV file path:", wav_path)
            return wav_path
        else:
            print("Failed to convert MP4 file to WAV.")
            return 0
    elif file_type == "MP3":
        wav_path = convert_to_wav(input_path, output_path)
        if wav_path:
            print("MP3 file converted to WAV successfully!")
            print("WAV file path:", wav_path)
            return wav_path
        else:
            print("Failed to convert MP3 file to WAV.")
            return 0
    else:
        youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        if re.match(youtube_regex, input_path):
            wav_path = download_youtube_video(input_path, output_path)
            if wav_path:
                print("YouTube video downloaded and converted to WAV successfully!")
                print("WAV file path:", wav_path)
                return wav_path
            else:
                print("Failed to download and convert YouTube video to WAV.")
                return 0
        else:
            print("Invalid input file or YouTube URL.")
            return 0

# Example usage
#input_path = "john.mp3"
#output_path = ""
#process_input(input_path, output_path)
