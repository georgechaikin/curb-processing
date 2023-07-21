# curb-processing
The script for curb processing. It tries to extract ground plane, then extracts curb.

# Requirements
See [requirements.txt](https://github.com/georgechaikin/curb-processing/blob/main/requirements.txt)

# Example
Red color: curb

<img src="https://github.com/georgechaikin/curb-processing/blob/main/images/curb_example.png"/>

# Installation
```bash
>>> git clone https://github.com/georgechaikin/curb-processing.git
>>> cd curb-processing
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
>>> python __main__.py --input_path [ply_filepath]
```
There are extra parameters:
- --output_dir: output dir path
- --show_points: the script will show three plots with point clouds
