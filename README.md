
Image Synthesis Tool for Object Detection


🚀 A professional image synthesis tool for data augmentation in object detection tasks. Extracts objects from annotated datasets and synthesizes them onto background images with realistic transformations.


Features
​​Precise Object Extraction​​: Accurately crops objects from YOLO-format annotated datasets
​​Realistic Synthesis​​: Naturally blends objects onto background images with intelligent placement
​​Anti-overlap System​​: Automatically detects and prevents object overlapping
​​Advanced Augmentation​​: Supports random rotation (-30° to 30°) and color adjustments (brightness/contrast/saturation)
​​YOLO-Compatible​​: Automatically generates annotations in standard YOLO format
​​Multi-Object Support​​: Configurable number of objects per image (1-10+)


Project Structure
ImageSynthesisTool/
├── configs/                 # Configuration files
├── data/                   # Data directories (symlink to actual data)
├── src/                    # Source code
│   ├── config.py           # Configuration management
│   ├── cropping.py         # Object extraction logic
│   ├── synthesis.py        # Image synthesis engine
│   ├── utils.py            # Utility functions
│   └── main.py            # Main entry point
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── setup.py               # Installation script


Quick Start
installation

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .


Data Preparation
1.​​Prepare Source Dataset​​: Place your YOLO-format dataset in data/raw_dataset/with images/and labels/subdirectories
2.​​Prepare Background Images​​: Place background images in data/folder_A/

