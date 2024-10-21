import os
import subprocess
import sys
import logging
from flask import Flask, request, render_template, send_file, redirect, url_for, flash

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Determine the base path for the executable or script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    logging.debug(f"Entered URL: {url}")

    if not url:
        return "Please enter a YouTube URL.", 400

    youtubedl_path = os.path.join(base_path, "youtube-dl.exe")
    if not os.path.exists(youtubedl_path):
        logging.error("youtube-dl.exe not found.")
        return "youtube-dl.exe not found.", 500

    output_dir = base_path
    command = [youtubedl_path, '-v', '-f', 'bestvideo+bestaudio/best', '-o', os.path.join(output_dir, '%(title)s.%(ext)s'), url]

    try:
        logging.info(f"Running command: {' '.join(command)}")
        run_subprocess(command)

        video_files = [f for f in os.listdir(output_dir) if f.endswith(('.mp4', '.webm'))]
        if not video_files:
            raise FileNotFoundError("No video files found in the output directory.")

        video_path = os.path.join(output_dir, video_files[0])
        logging.debug(f"Found video file: {video_path}")
        mp3_path = convert_to_mp3(video_path)

        return send_file(mp3_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Error during download or conversion: {str(e)}")
        return str(e), 500

def convert_to_mp3(video_path):
    mp3_save_path = os.path.splitext(video_path)[0] + ".mp3"
    ffmpeg_path = os.path.join(base_path, "tuner.exe")
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError("tuner.exe not found in the same folder as this script.")

    command = [ffmpeg_path, '-i', video_path, '-b:a', '320k', '-q:a', '0', mp3_save_path]
    logging.info(f"Running command: {' '.join(command)}")
    run_subprocess(command)

    return mp3_save_path

def run_subprocess(command):
    """Helper function to run a subprocess command and log output."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.debug(f"stdout: {result.stdout}")
        logging.debug(f"stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e.stderr}")
        raise

if __name__ == '__main__':
    app.run(debug=True)  # Runs on localhost:5000 by default
