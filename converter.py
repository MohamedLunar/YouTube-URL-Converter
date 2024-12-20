from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

def handler(request):
    try:
        # Parse the URL from the incoming request
        request_data = request.json
        url = request_data.get("url")
        
        if not url:
            return {
                "status": "error",
                "message": "URL is required."
            }
        
        # Download video using pytube
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        video_path = video_stream.download(filename="video.mp4")

        # Convert to MP3 using moviepy
        video_clip = VideoFileClip(video_path)
        audio_path = video_path.replace(".mp4", ".mp3")
        video_clip.audio.write_audiofile(audio_path)

        # Clean up the downloaded video file after conversion
        os.remove(video_path)

        # Return the paths to the converted files
        return {
            "status": "success",
            "mp3": audio_path,
            "mp4": video_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
