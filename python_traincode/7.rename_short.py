import os
import random
import shutil

def split_dataset(base_dir, image_folder='ima', label_folder='lab', train_ratio=0.8):
    image_dir = os.path.join(base_dir, image_folder)
    label_dir = os.path.join(base_dir, label_folder)

    # 훈련/검증 경로 생성
    train_img_dir = os.path.join(image_dir, 'train')
    val_img_dir = os.path.join(image_dir, 'val')
    train_label_dir = os.path.join(label_dir, 'train')
    val_label_dir = os.path.join(label_dir, 'val')

    for d in [train_img_dir, val_img_dir, train_label_dir, val_label_dir]:
        os.makedirs(d, exist_ok=True)

    # 이미지 목록 가져오기
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

    # 파일 무작위 섞기
    random.shuffle(image_files)
    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]

    # 복사 함수
    def move_files(file_list, img_src, lbl_src, img_dst, lbl_dst):
        for img_file in file_list:
            name, _ = os.path.splitext(img_file)
            label_file = name + '.txt'
            # 이미지 복사
            shutil.copy2(os.path.join(img_src, img_file), os.path.join(img_dst, img_file))
            # 라벨 복사
            shutil.copy2(os.path.join(lbl_src, label_file), os.path.join(lbl_dst, label_file))

    # 실제 복사 실행
    move_files(train_files, image_dir, label_dir, train_img_dir, train_label_dir)
    move_files(val_files, image_dir, label_dir, val_img_dir, val_label_dir)

    print(f"✅ 분할 완료: {len(train_files)}개는 학습용, {len(val_files)}개는 검증용입니다.")

# 예시 호출
split_dataset(base_dir='/home/choi/project_doje')










from ultralytics import YOLO
model = YOLO('yolov8n.pt') #.YOLO8n모델을 쓰겠다는 것
model.train(data='/home/choi/project_doje/data/data.yaml', epochs=300, imgsz=640)
