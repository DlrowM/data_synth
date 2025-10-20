import argparse
from .config import Config
from .cropping import ObjectCropper
from .synthesis import ImageSynthesizer

def main():
    parser = argparse.ArgumentParser(description="Image Synthesis Tool")
    parser.add_argument('--config', type=str, default=None, help="Path to custom config file")
    args = parser.parse_args()
    
    # 加载配置
    config = Config(args.config)
    
    # 第一步：从数据集中抠出对象
    print("Cropping objects from dataset...")
    cropper = ObjectCropper(config)
    cropper.crop_objects_from_dataset()
    
    # 第二步：合成新图像
    print("Synthesizing new images...")
    synthesizer = ImageSynthesizer(config)
    synthesizer.synthesize_images()
    
    print("All done!")

if __name__ == "__main__":
    main()