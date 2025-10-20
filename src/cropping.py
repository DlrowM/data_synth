import os
import cv2
import numpy as np
from typing import List
from .config import Config

class ObjectCropper:
    def __init__(self, config: Config):
        self.config = config
    
    def crop_objects_from_dataset(self):
        """从数据集中提取所有对象并保存到folder_B"""
        dataset_path = self.config['paths']['dataset_path']
        output_folder = self.config['paths']['folder_B']
        
        os.makedirs(output_folder, exist_ok=True)
        
        image_folder = os.path.join(dataset_path, 'images')
        label_folder = os.path.join(dataset_path, 'labels')
        
        for img_name in os.listdir(image_folder):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            self._process_image(img_name, image_folder, label_folder, output_folder)
    
    def _process_image(self, img_name: str, image_folder: str, label_folder: str, output_folder: str):
        img_path = os.path.join(image_folder, img_name)
        label_path = os.path.join(label_folder, os.path.splitext(img_name)[0] + '.txt')
        
        if not os.path.exists(label_path):
            return
            
        img = cv2.imread(img_path)
        if img is None:
            return
            
        h, w = img.shape[:2]
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            self._process_label_line(line, img, h, w, img_name, i, output_folder)
    
    def _process_label_line(self, line: str, img: np.ndarray, h: int, w: int, 
                           img_name: str, idx: int, output_folder: str):
        parts = line.strip().split()
        if len(parts) < 5:
            return
            
        class_id = parts[0]
        x_center, y_center, box_w, box_h = map(float, parts[1:5])
        
        # 转换为像素坐标
        x_center *= w
        y_center *= h
        box_w *= w
        box_h *= h
        
        x1 = int(x_center - box_w/2)
        y1 = int(y_center - box_h/2)
        x2 = int(x_center + box_w/2)
        y2 = int(y_center + box_h/2)
        
        # 确保坐标在图像范围内
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w-1, x2)
        y2 = min(h-1, y2)
        
        if x2 <= x1 or y2 <= y1:
            return
            
        cropped = img[y1:y2, x1:x2]
        
        # 保存抠出的图像
        output_name = f"{os.path.splitext(img_name)[0]}_{idx}_class{class_id}.png"
        cv2.imwrite(os.path.join(output_folder, output_name), cropped)