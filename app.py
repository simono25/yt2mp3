import os
import subprocess
import sys
import logging
from flask import Flask, request, render_template, send_file

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

    youtubedl_path = os.path.join(base_path, "yt-dlp.exe")  # Updated to yt-dlp
    if not os.path.exists(youtubedl_path):
        logging.error("yt-dlp.exe not found.")
        return "yt-dlp.exe not found.", 500

    output_dir = base_path
    command = [
        youtubedl_path, 
        '-v', 
        '-x', 
        '--audio-format', 'mp3', 
        '--audio-quality', '0',  # Highest audio quality
        '-o', os.path.join(output_dir, '%(title)s.%(ext)s'), 
        url
    ]

    try:
        logging.info(f"Running command: {' '.join(command)}")
        run_subprocess(command)

        mp3_files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]
        if not mp3_files:
            raise FileNotFoundError("No MP3 files found in the output directory.")

        mp3_path = os.path.join(output_dir, mp3_files[0])
        logging.debug(f"Found MP3 file: {mp3_path}")

        return send_file(mp3_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return str(e), 500

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
