import gradio as gr
import cv2
import threading
import time
from PIL import Image
from pathlib import Path


def process_video(video_path):
    # Use threading to run the main code in parallel
    def run_main_code():
        import Speed_Detection  # Import your existing code
        Speed_Detection.trackMultipleObjects()

    # Start the main code in a separate thread
    main_thread = threading.Thread(target=run_main_code)
    main_thread.start()

    # Display images in Gradio as they are saved
    while True:
        # Find the latest image in the output folder (assuming the fixed path)
        output_folder = "overspeeding/cars/"  # Adjust this path as needed
        latest_image_path = max(Path(output_folder).glob('*.jpeg'), key=lambda x: x.stat().st_mtime, default=None)

        if latest_image_path:
            latest_image = Image.open(latest_image_path)
            yield latest_image

        time.sleep(1) 
        
        
iface = gr.Interface(
    fn=process_video,
    inputs=gr.Textbox("START"),
    outputs=gr.Image(type="pil"),
    live=True
)

iface.launch()











