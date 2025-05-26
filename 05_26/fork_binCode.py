import os
import zipfile
import shutil


def create_yolo_config_files(base_path):
    """
    label 폴더안에 obj.names , train.txt , obj.data 생성
    """
    labels_dir = os.path.join(base_path, "short_labels") # 저장 폴더이름 설정(라벨)
    images_dir = os.path.join(base_path, "short_images") # 저장 폴더이름 설정(이미지)
    # 출력 디렉토리 생성 (존재하지 않으면 생성)
    os.makedirs(labels_dir, exist_ok=True)

    # 1. obj.names 파일 생성 (클래스 이름 정의)
    names_path = os.path.join(labels_dir, "obj.names")
    with open(names_path, "w", encoding="utf-8") as f:
        f.write("label\n") # 하나의 클래스: label
        print(f"Created: {names_path}")

    # 2. train.txt 파일 생성 (labels_dir 폴더 안에)
    train_txt_path = os.path.join(labels_dir, "train.txt")
    with open(train_txt_path, "w", encoding="utf-8") as f:
        # 이미지 디렉토리 내의 파일명만 기록
        for img_file in sorted(os.listdir(images_dir)):
            if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                f.write(img_file + "\n")
    print(f"Created: {train_txt_path}")

    # 3. obj.data 파일 생성 (YOLO 학습 설정 파일)
    obj_data_path = os.path.join(labels_dir, "obj.data")
    with open(obj_data_path, "w", encoding="utf-8") as f:
        f.write("classes = 1\n") # 클래스 수
        f.write(f"train = train.txt\n") # 학습 이미지 목록 경로
        f.write(f"names = obj.names\n") # 클래스 이름 파일 경로
    print(f"Created: {obj_data_path}")


def copy_first_1000_files(src_images_dir, src_labels_dir, dst_images_dir, dst_labels_dir, limit):
    """
    이미지 및 라벨 파일을 limit개수로만 복사하는 함수
    src_images_dir : 원본 이미지 폴더
    src_labels_dir : 원본 라벨 폴더
    dst_images_dir : 복사할 이미지 목적지
    dst_labels_dir : 복사할 라벨 목적지
    limit : 복사할 개수
    )
    """
    # 디렉토리 생성 (파일이 존재하면 생성X)
    os.makedirs(dst_images_dir, exist_ok=True)
    os.makedirs(dst_labels_dir, exist_ok=True)
    # 소스 이미지 디렉토리에서 이미지 파일 목록 가져오기 (.jpg, .jpeg, .png 확장자)만
    image_files = sorted([
    f for f in os.listdir(src_images_dir)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    # 소스 라벨 디렉토리에서 라벨 파일 목록 가져오기 (.txt 확장자)만
    label_files = sorted([
    f for f in os.listdir(src_labels_dir)
    if f.lower().endswith('.txt')
    ])
    # 이미지 파일 복사 (앞 limit개)
    for f in image_files[:limit]:
        shutil.copy2(os.path.join(src_images_dir, f), os.path.join(dst_images_dir, f))
        print(f"Copied {min(len(image_files), limit)} images to {dst_images_dir}")
    # 라벨 파일 복사 (앞 limit개)
    for f in label_files[:limit]:
        shutil.copy2(os.path.join(src_labels_dir, f), os.path.join(dst_labels_dir, f))
        print(f"Copied {min(len(label_files), limit)} label files to {dst_labels_dir}")


def zip_folder(folder_path, zip_path):
    """
    지정된 폴더를 압축시켜주는 함수이다.
    :param folder_path : 압축시키고 싶은 폴더
    :param zip_path : 해당폴더의 압축후 이름
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)
                print(f"Zipped: {zip_path}")




create_yolo_config_files("/home/june/ai_hub")

# copy_first_1000_files(
# '/home/june/ai_hub/result_images',
# '/home/june/ai_hub/result_labels',
# '/home/june/ai_hub/short_images',
# '/home/june/ai_hub/short_labels',
# limit=1000
# )



zip_folder("/home/june/ai_hub/short_labels", "/home/june/ai_hub/short_labels.zip")
zip_folder("/home/june/ai_hub/short_images", "/home/june/ai_hub/short_images.zip")
