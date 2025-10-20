
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
# Congfiguration Guide
## Default Configuration
```yaml
# configs/default.yaml
paths:
  dataset_path: "./data/raw_dataset"  # Source dataset path
  folder_A: "./data/folder_A"        # Background images directory
  folder_B: "./data/folder_B"        # Extracted objects directory
  output_folder: "./data/output"     # Synthesis output directory

synthesis:
  num_images_to_generate: 100        # Number of images to generate
  max_objects_per_image: 5           # Maximum objects per image
  min_object_area_ratio: 0.01        # Min object area (1% of background)
  max_object_area_ratio: 0.1         # Max object area (10% of background)
  rotation_range: [-30, 30]          # Rotation angle range (degrees)
  color_adjustment:
    brightness_range: [0.7, 1.3]     # Brightness adjustment range
    contrast_range: [0.7, 1.3]       # Contrast adjustment range
    saturation_range: [0.7, 1.3]    # Saturation adjustment range
```

# Custom Configuration Example
## Create configs/custom.yaml:
```yaml
# High-volume configuration for large datasets
synthesis:
  num_images_to_generate: 1000
  max_objects_per_image: 8
  min_object_area_ratio: 0.005      # 0.5% of background
  max_object_area_ratio: 0.15       # 15% of background
```

# Advanced Usage
## Batch Processing
```bash
# Generate 5000 images with custom settings
python -m src.main --config configs/batch_config.yaml
```

## Integration with Training Pipelines
```python
# Example: Integrate with PyTorch data loader
from src.synthesis import ImageSynthesizer
from src.config import Config

config = Config("configs/training.yaml")
synthesizer = ImageSynthesizer(config)

# Generate synthetic data on-the-fly
def augment_dataset(original_images):
    return synthesizer.augment_batch(original_images)
```

# Output Format
## Generated Images
+ Location: data/output/images/
+ Naming: synthesized_{index}_{original_name}.jpg

## Annotation Files
+ Location: data/output/labels/
+ Format: YOLO format (class_id x_center y_center width height)
+ Example:
```
0 0.453125 0.623438 0.125000 0.187500
1 0.712500 0.334375 0.093750 0.156250
```
# Development
## Running Tests
```bash
# Run all tests
pytest tests/

# With coverage report
pytest --cov=src tests/

# Specific module tests
pytest tests/test_synthesis.py -v
```
## Adding New Features
1. __Create new module​​ in__ src/(e.g., perspective.py)
2. __Update exports​​ in__ src/__init__.py.
3. __Add tests​​ in__ tests/test_perspective.py
4. __Update documentation​​ in__ relevant sections

# Debug Mode  
Enable debug output by setting environment variable:
```bash
export SYNTHESIS_DEBUG=1
python -m src.main
```
Or use the built-in debug configuration:
``` bash
python -m src.main --config configs/debug.yaml
```

# API Reference
## Core Classes
### 1. Config
```
from src.config import Config
config = Config("path/to/config.yaml")
dataset_path = config['paths']['dataset_path']
```
### 2. ObjectCropper
```
from src.cropping import ObjectCropper
cropper = ObjectCropper(config)
cropper.crop_objects_from_dataset()
```
### 3. ImageSynthesizer
```
from src.synthesis import ImageSynthesizer
synthesizer = ImageSynthesizer(config)
synthesizer.synthesize_images()
```

# Performance Tips
## For Large Datasets
+ Use max_objects_per_image: 3-5for optimal performance
+ Set num_images_to_generatebased on available storage
+ Consider using SSD storage for temporary files
## Memory Optimization
+ Process images in batches for large-scale synthesis
+ Use appropriate image compression settings

# Citation
If you use this tool in your research, please cite:
```
@software{image_synthesis_tool,
  title = {Image Synthesis Tool for Object Detection},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/image-synthesis-tool}
}
```
