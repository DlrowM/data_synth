import os
import cv2
import random
import numpy as np
from typing import List, Tuple
from .config import Config

class ImageSynthesizer:
    def __init__(self, config: Config):
        self.config = config
        self.color_adjustment = self.config['synthesis']['color_adjustment']
        self.rotation_range = self.config['synthesis']['rotation_range']
    
    def synthesize_images(self):
        """合成新图像"""
        folder_A = self.config['paths']['folder_A']
        folder_B = self.config['paths']['folder_B']
        output_folder = self.config['paths']['output_folder']
        num_images = self.config['synthesis']['num_images_to_generate']
        max_objects = self.config['synthesis']['max_objects_per_image']
        
        os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'labels'), exist_ok=True)
        
        b_images = self._get_valid_images(folder_B)
        a_images = self._get_valid_images(folder_A)
        
        for i in range(num_images):
            self._process_single_image(i, a_images, b_images, folder_A, folder_B, output_folder, max_objects)
    
    def _process_single_image(self, idx: int, a_images: List[str], b_images: List[str], 
                             folder_A: str, folder_B: str, output_folder: str, max_objects: int):
        a_img_name = random.choice(a_images)
        a_img_path = os.path.join(folder_A, a_img_name)
        
        try:
            a_img = cv2.imread(a_img_path)
            if a_img is None:
                return
                
            synthesized_img, label_lines = self._synthesize_image_objects(
                a_img, b_images, folder_B, max_objects
            )
            
            if label_lines:
                self._save_output(idx, a_img_name, synthesized_img, label_lines, output_folder)
                
        except Exception as e:
            print(f"Error processing {a_img_name}: {str(e)}")
    
    def _synthesize_image_objects(self, a_img: np.ndarray, b_images: List[str], 
                                folder_B: str, max_objects: int) -> Tuple[np.ndarray, List[str]]:
        a_h, a_w = a_img.shape[:2]
        synthesized_img = a_img.copy()
        existing_boxes = []
        label_lines = []
        
        num_objects = random.randint(1, max_objects)
        
        for _ in range(num_objects):
            b_img_name = random.choice(b_images)
            b_img_path = os.path.join(folder_B, b_img_name)
            b_img = cv2.imread(b_img_path)
            
            if b_img is None:
                continue
                
            result = self._try_place_object(b_img, b_img_name, a_h, a_w, existing_boxes)
            if result:
                pos_img, box_info, label_line = result
                paste_x, paste_y = box_info[:2]
                synthesized_img[paste_y:paste_y+pos_img.shape[0], paste_x:paste_x+pos_img.shape[1]] = pos_img
                existing_boxes.append(box_info)
                label_lines.append(label_line)
        
        return synthesized_img, label_lines
    
    def _try_place_object(self, b_img: np.ndarray, b_img_name: str, 
                         a_h: int, a_w: int, existing_boxes: List[Tuple]) -> Tuple[np.ndarray, Tuple, str]:
        # 计算目标大小
        a_area = a_h * a_w
        b_h, b_w = b_img.shape[:2]
        target_ratio = random.uniform(
            self.config['synthesis']['min_object_area_ratio'],
            self.config['synthesis']['max_object_area_ratio']
        )
        target_area = a_area * target_ratio
        scale_factor = np.sqrt(target_area / (b_h * b_w))
        
        # 应用旋转和颜色调整
        rotated_b = self._apply_transformations(b_img)
        
        # 调整大小
        final_img = self._resize_object(rotated_b, scale_factor, a_w, a_h)
        if final_img is None:
            return None
            
        # 尝试放置
        for _ in range(50):  # 最多尝试50次
            paste_x, paste_y = self._get_random_position(final_img.shape[1], final_img.shape[0], a_w, a_h)
            new_box = (paste_x, paste_y, paste_x + final_img.shape[1], paste_y + final_img.shape[0])
            
            if not self._check_overlap(new_box, existing_boxes):
                # 生成标签信息
                class_id = b_img_name.split('_class')[-1].split('.')[0]
                label_line = self._generate_label_line(new_box, a_w, a_h, class_id)
                return final_img, new_box, label_line
                
        return None
    
    def _apply_transformations(self, img: np.ndarray) -> np.ndarray:
        """应用旋转和颜色调整"""
        # 随机旋转
        angle = random.uniform(self.rotation_range[0], self.rotation_range[1])
        rotated = self._rotate_image(img, angle)
        
        # 随机颜色调整
        adjusted = self._adjust_image_color(rotated)
        return adjusted
    
    def _rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """旋转图像"""
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        rotated = cv2.warpAffine(image, M, (new_w, new_h), borderMode=cv2.BORDER_REPLICATE)
        return rotated
    
    def _adjust_image_color(self, img: np.ndarray) -> np.ndarray:
        """调整图像颜色"""
        # 亮度/对比度
        brightness = random.uniform(self.color_adjustment['brightness_range'][0], 
                                   self.color_adjustment['brightness_range'][1])
        contrast = random.uniform(self.color_adjustment['contrast_range'][0], 
                                 self.color_adjustment['contrast_range'][1])
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=(brightness-1)*255)
        
        # 饱和度 (HSV空间)
        saturation = random.uniform(self.color_adjustment['saturation_range'][0], 
                                  self.color_adjustment['saturation_range'][1])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return img
    
    def _resize_object(self, img: np.ndarray, scale_factor: float, 
                      max_w: int, max_h: int) -> np.ndarray:
        """调整对象大小"""
        h, w = img.shape[:2]
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        
        if new_w < 10 or new_h < 10 or new_w > max_w or new_h > max_h:
            return None
            
        return cv2.resize(img, (new_w, new_h))
    
    def _get_random_position(self, obj_w: int, obj_h: int, 
                           img_w: int, img_h: int) -> Tuple[int, int]:
        """获取随机位置"""
        max_x = img_w - obj_w
        max_y = img_h - obj_h
        return random.randint(0, max_x), random.randint(0, max_y)
    
    def _check_overlap(self, new_box: Tuple, existing_boxes: List[Tuple]) -> bool:
        """检查重叠"""
        new_x1, new_y1, new_x2, new_y2 = new_box
        
        for box in existing_boxes:
            ex_x1, ex_y1, ex_x2, ex_y2 = box
            
            if not (new_x2 < ex_x1 or new_x1 > ex_x2 or new_y2 < ex_y1 or new_y1 > ex_y2):
                return True
        return False
    
    def _generate_label_line(self, box: Tuple, img_w: int, img_h: int, class_id: str) -> str:
        """生成标签行"""
        x1, y1, x2, y2 = box
        x_center = (x1 + x2) / 2 / img_w
        y_center = (y1 + y2) / 2 / img_h
        box_w = (x2 - x1) / img_w
        box_h = (y2 - y1) / img_h
        return f"{class_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\n"
    
    def _save_output(self, idx: int, orig_name: str, img: np.ndarray, 
                    labels: List[str], output_folder: str):
        """保存输出"""
        img_name = f"synthesized_{idx}_{orig_name}"
        label_name = f"synthesized_{idx}_{os.path.splitext(orig_name)[0]}.txt"
        
        cv2.imwrite(os.path.join(output_folder, 'images', img_name), img)
        with open(os.path.join(output_folder, 'labels', label_name), 'w') as f:
            f.writelines(labels)
    
    def _get_valid_images(self, folder: str) -> List[str]:
        """获取有效图像列表"""
        return [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]