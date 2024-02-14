from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

# Route to serve the HTML interface
@app.route('/analyze_video')
def index():
    return render_template('index.html')

# Route to handle form submission and video analysis
@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    # Get form data sent from the HTML form
    video_file = request.files['video']
    scenario = request.form['scenario']
    duration = request.form['duration']
    emotion = request.form.get('emotion')

    # Process the received data (e.g., save the uploaded video file)
    video_file.save('uploaded_video.mp4')

    # Extract segments from the video
    start_time = 0  # Start time in seconds
    end_time = 2   # End time in seconds
    output_path = "output_segments"
    extract_segments('uploaded_video.mp4', start_time, end_time, output_path)

    # Return a response to the client
    return 'Video analysis completed successfully!'

def extract_segments(video_path, start_time, end_time, output_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        print("Error: Unable to open video file.")
        return
    
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Set the start and end frame numbers based on the start and end times
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Start reading frames and writing segments
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    success, frame = video_capture.read()
    frames_written = 0

    while success and frames_written < (end_frame - start_frame):
        cv2.imwrite(os.path.join(output_path, f"frame_{frames_written}.jpg"), frame)
        success, frame = video_capture.read()
        frames_written += 1

    video_capture.release()

if __name__ == '__main__':
    app.run(debug=True)