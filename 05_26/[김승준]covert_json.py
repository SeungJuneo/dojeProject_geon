import json
import os
import shutil

def save_yolo_annotations_for_category(json_dir: str, output_dir: str, image_dir: str, image_output: str, category_id: int):
    """"
    COCO 형식의 어노테이션(JSON 파일들)에서 특정 category_id에 해당하는 객체만 추출하여,
    YOLO 형식으로 라벨링 파일을 저장하고, 해당 이미지도 함께 복사합니다.

    Parameters:
        json_dir (str): COCO 어노테이션 JSON 파일들이 위치한 디렉토리
        output_dir (str): YOLO 형식 라벨 파일(.txt)을 저장할 디렉토리
        image_dir (str): 원본 이미지들이 저장된 디렉토리
        image_output (str): 라벨에 해당하는 이미지를 복사할 디렉토리
        category_id (int): 변환할 대상 카테고리 ID
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(image_output, exist_ok=True)
    images_copied = set()

    for root, _, files in os.walk(json_dir):
        for file in files:
            if not file.endswith(".json"):
                continue

            json_path = os.path.join(root, file)
            print(f"📄 Processing: {json_path}")

            with open(json_path, "r") as f:
                coco_data = json.load(f)

            image_sizes = {img["id"]: (img["width"], img["height"]) for img in coco_data["images"]}
            image_filenames = {img["id"]: img["file_name"] for img in coco_data["images"]}

            # annotation 별로 묶기: image_id -> list of anns
            anns_per_image = {}
            for ann in coco_data["annotations"]:
                if ann["category_id"] == category_id:
                    anns_per_image.setdefault(ann["image_id"], []).append(ann)

            for image_id, anns in anns_per_image.items():
                img_w, img_h = image_sizes[image_id]
                image_filename = image_filenames[image_id]
                base_filename = os.path.splitext(os.path.basename(image_filename))[0]

                # 이미지 경로 (png 확장자 고정)
                src_img_path = os.path.join(image_dir, f"{base_filename}.png")
                if not os.path.exists(src_img_path):
                    print(f"⚠️ 이미지 파일을 찾을 수 없습니다: {src_img_path}")
                    continue  # 이미지 없으면 라벨 파일 생성하지 않음

                # 이미지 복사
                if base_filename not in images_copied:
                    dst_img_path = os.path.join(image_output, f"{base_filename}.png")
                    shutil.copy2(src_img_path, dst_img_path)
                    images_copied.add(base_filename)

                # 라벨 파일 경로
                txt_filename = f"{base_filename}.txt"
                txt_path = os.path.join(output_dir, txt_filename)

                # 기존에 내용이 있으면 덮어쓰는 형태로 열기
                with open(txt_path, "w") as txt_file:
                    for ann in anns:
                        x_min, y_min, width, height = ann["bbox"]
                        x_center = (x_min + width / 2) / img_w
                        y_center = (y_min + height / 2) / img_h
                        w_norm = width / img_w
                        h_norm = height / img_h
                        txt_file.write(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")

    print(f"\n✅ YOLO 라벨과 이미지들이 '{output_dir}' 와 '{image_output}' 에 저장되었습니다.")



coco_json_path = "/home/june/ai_hub/labels"
output_dir = "/home/june/ai_hub/result_labels"
image_dir = "/home/june/ai_hub/images"
image_output = "/home/june/ai_hub/result_images"

category_id = 12

save_yolo_annotations_for_category(coco_json_path,output_dir,image_dir,image_output,category_id)