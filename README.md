
# Image Synthesis Tool for Object Detection

🚀 A professional image synthesis tool for data augmentation in object detection tasks. Extracts objects from annotated datasets and synthesizes them onto background images with realistic transformations.


# Features

1. ​​Precise Object Extraction​​: Accurately crops objects from YOLO-format annotated datasets
2. ​​Realistic Synthesis​​: Naturally blends objects onto background images with intelligent placement
3. ​​Anti-overlap System​​: Automatically detects and prevents object overlapping
4. ​​Advanced Augmentation​​: Supports random rotation (-30° to 30°) and color adjustments (brightness/contrast/saturation)
5. ​​YOLO-Compatible​​: Automatically generates annotations in standard YOLO format
​​6. Multi-Object Support​​: Configurable number of objects per image (1-10+)



# Quick Start
installation

1. Install dependencies

`pip install -r requirements.txt`


2. Or install in development mode

`pip install -e .`



# Data Preparation
1. ​​Prepare Source Dataset​​: Place your YOLO-format dataset in data/raw_dataset/with images/and labels/subdirectories  

2.​​ Prepare Background Images​​: Place background images in data/folder_A/  

# Basic Usage
```python
# Run with default configuration
python -m src.main
# Run with custom configuration
python -m src.main --config configs/custom.yaml
```
