import argparse
import os
import cv2 as cv
import numpy as np
import mediapipe as mp
import subprocess
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input video file")
parser.add_argument("output", type=str, help="Output video file")
parser.add_argument("-o", "--overwrite", action="store_true", help="Force overwrite of output file if it exists.")
parser.add_argument("-s", "--square", action="store_true")
args = parser.parse_args()

BG_COLOR = (0, 255, 0) # green
MASK_COLOR = (255, 255, 255) # white

landscape_model_dir = os.path.join(os.path.abspath(os.path.curdir),'util/models/selfie_segmenter_landscape.tflite')
square_model_dir = os.path.join(os.path.abspath(os.path.curdir),'util/models/selfie_segmenter.tflite')

def remove_background(i_dir, o_dir, square):
    model_dir = square_model_dir if square else landscape_model_dir
    
    base_options = mp.tasks.BaseOptions
    image_segmenter = mp.tasks.vision.ImageSegmenter
    image_segmenter_options = mp.tasks.vision.ImageSegmenterOptions
    vision_running_mode = mp.tasks.vision.RunningMode
    
    # Create an image segmenter instance with the video mode:
    options = image_segmenter_options(
        base_options = base_options(model_asset_path=model_dir),
        running_mode = vision_running_mode.VIDEO,
        output_category_mask = True)
    
    frames, timestamps, fps = video_to_mediapipe(i_dir)
    
    with image_segmenter.create_from_options(options) as segmenter:
        segmented_frames = []
        for frame, timestamp in zip(frames, timestamps):
            # Retrieve the masks for the segmented image
            segmentation_result = segmenter.segment_for_video(frame, timestamp)
            category_mask = segmentation_result.category_mask
            
            # Generate solid color images for showing the output segmentation mask.
            frame_data = frame.numpy_view()
            fg_image = frame_data.copy()
            bg_image = np.zeros(frame_data.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            
            condition = np.stack((category_mask.numpy_view(),) * 3, axis = -1) > 0.2
            output_frame = np.where(condition, bg_image, fg_image)
            segmented_frames.append(output_frame)
        
        temp_video_path = "temp.mp4"
        save_video(segmented_frames, fps, temp_video_path)
        
        reencode_video(temp_video_path, o_dir, fps)
        
        os.remove(temp_video_path)
    
def video_to_mediapipe(i_dir):
    frames = []
    timestamps = []
    
    cap = cv.VideoCapture(i_dir)
    fps = cap.get(cv.CAP_PROP_FPS)
    ret = True
    timestamp = 0
    
    while ret:
        ret, img = cap.read()
        if ret:
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            frames.append(mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb))
            timestamps.append(int(timestamp * 1e6)) # convert to microseconds
            timestamp += 1/fps
    
    cap.release()
        
    return frames, timestamps, fps

def save_video(frames, fps, temp_path):
    height, width, _ = frames[0].shape
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(temp_path, fourcc, fps, (width, height))
    
    for frame in frames:
        out.write(cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        
    out.release()
    
def reencode_video(temp_path, output_path, fps):
    command = [
        'ffmpeg', '-y', '-i', temp_path, '-c:v', 'libx264', '-r', str(fps), output_path
    ]
    subprocess.run(command)

if __name__ == "__main__":
    input_dir = os.path.relpath(args.input)
    output_dir = os.path.relpath(args.output)
    overwrite = args.overwrite
    square = args.square
    
    if not os.path.isfile(input_dir):
        print(f"{input_dir} does not exist. Exiting...")
        exit(2)
    if os.path.isfile(output_dir) and not overwrite:
        print(f"{output_dir} already exist, use '-o to overwrite the file.")
        exit(3)
        
    vid = remove_background(input_dir, output_dir, square)