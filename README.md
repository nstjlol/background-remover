# Background Remover
This project is a Python script that removes the background from videos and outputs the result in mp4 format. The background is replaced with a green screen, making it suitable for chromakeying in video editing software.

## Features
- Remove background from videos and replace it with a green screen.
- Outputs videos in mp4 format.
- Future plans to support more output formats.

## Requirements
- Python 3.10 or higher
- MediaPipe
- OpenCV
- FFmpeg

## Installation
1. Clone the repository:
```
git clone https://github.com/nstjlol/background-remover.git
cd background-remover
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Download the MediaPipe Selfie Segmentation Model:
```
wget -O models/selfie_segmenter.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite
wget -O models/selfie_segmenter_landscape.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter_landscape/float16/latest/selfie_segmenter_landscape.tflite
```
4. Install FFmpeg
- **Windows**: Download from [FFmpeg website](https://www.ffmpeg.org/download.html) and follow the installation instructions. **Ensure FFmpeg is in your system environment path**
- **Linux**: Install using a package manager, e.g., `sudo apt-get install ffmpeg`.
- **macOS**: Install using Homebrew, e.g., `brew install ffmpeg`.
## Usage
Removing Background from a Video
```
python remove_background.py [input] [output] [options]
```
- `input`: Path to the input video file.
- `output`: Path to the output video file.
- `-o`, `--overwrite`: Force overwrite of the output file if it exists.
- `-s`, `--square`: Process the video using the square selfie data model.

## How It Works
**OpenCV**: Used to load and process the videos.

**MediaPipe Selfie Segment Model**: Used to detect people in the video and create a mask.

**FFmpeg**: Used to extract audo, combine audio with the processed video, and handle video encoding.

**Background Replacement**: The background is replaced with the color green, making it suitable for chromakeying in video editing software.

## Future Plans
- [ ] Add support for more video output formats.
- [ ] Add support for other models.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

This project uses [MediaPipe](https://github.com/google-ai-edge/mediapipe), which is licensed under the Apache License 2.0. You can obtain a copy of the license at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

This project uses [OpenCV](https://opencv.org), which is licensed under the BSD License. You can obtain a copy of the license at [https://opencv.org/license/](https://opencv.org/license/).

This project uses [FFmpeg](https://ffmpeg.org), which is licensed under the LGPL/GPL. You can obtain a copy of the license at [https://ffmpeg.org/legal.html](https://ffmpeg.org/legal.html).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) for providing the core functionality of this project.
- [OpenCV](https://github.com/opencv/opencv) for video processing capabilities.
- [FFmpeg](https://ffmpeg.org) for audio and video processing.
