import os
from PIL import Image
from ultralytics import YOLO
from collections import defaultdict

def save_yolo_with_class_box_size(folder_path: str,
                                   output_folder: str,
                                   model_path: str
                                   ):
    """
    지정된 폴더(및 하위 폴더) 내 모든 이미지 파일을 YOLO로 분석하고
    YOLO 형식(txt)으로 저장합니다.

    Args:
        folder_path (str): 이미지들이 포함된 상위 폴더 경로
        output_folder (str): 결과 .txt 저장할 폴더 (없으면 원본 이미지 위치)
        model_path (str): YOLOv8 모델 경로
    """
    model = YOLO(model_path)
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(supported_formats):
                img_path = os.path.join(root, file)

                # txt 파일 저장 경로 구성
                relative_path = os.path.relpath(root, folder_path)
                base_name = os.path.splitext(file)[0]
                output_dir = os.path.join(output_folder or root, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                text_path = os.path.join(output_dir, base_name + '.txt')

                # 이미지 처리
                img = Image.open(img_path)
                img_w, img_h = img.size
                results = model(img_path)

                class_boxes = defaultdict(list)
                objects = []

                for box in results[0].boxes:
                    cls = int(box.cls[0])
                    x1, y1, x2, y2 = box.xyxy[0]
                    xc = ((x1 + x2) / 2) / img_w
                    yc = ((y1 + y2) / 2) / img_h
                    objects.append((cls, xc, yc))
                    class_boxes[cls].append((x1, y1, x2, y2))

                class_wh = {}
                for cls, boxes in class_boxes.items():
                    x1s, y1s, x2s, y2s = zip(*boxes)
                    w = (max(x2s) - min(x1s)) / img_w
                    h = (max(y2s) - min(y1s)) / img_h
                    class_wh[cls] = (w, h)

                with open(text_path, 'w') as f:
                    for cls, xc, yc in objects:
                        w, h = class_wh[cls]
                        f.write(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")

                print(f"✔ 저장 완료: {text_path}")



img_dir = "/home/june/model_l/annotated"  # 'imges 폴더
output_dir = "/home/june/model_l/labels"
model_path = "/home/june/best.pt"

save_yolo_with_class_box_size(img_dir, output_dir, model_path)
