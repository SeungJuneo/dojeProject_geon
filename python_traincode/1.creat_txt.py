from PIL import Image
import os
import json

def convert_json_to_yolo(json_path, output_dir="yolo_labels", images_dir=None):
    expression_map = {
        "기쁨": 0,
        "분노": 1,
        "슬픔": 2,
        "중립": 3
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        image_name = item.get("filename")
        if not image_name:
            continue

        # 이미지 크기 읽기 (images_dir 경로와 결합해서)
        if images_dir is not None:
            image_path = os.path.join(images_dir, image_name)
            if not os.path.isfile(image_path):
                print(f"⚠️ 이미지 파일 없음, 건너뜀: {image_path}")
                continue  # 이미지가 없으면 건너뜀

            try:
                with Image.open(image_path) as img:
                    IMG_WIDTH, IMG_HEIGHT = img.size
            except Exception as e:
                print(f"이미지 열기 실패: {image_path}, 기본 크기 사용 (2592x1944)")
                IMG_WIDTH, IMG_HEIGHT = 2592, 1944
        else:
            IMG_WIDTH, IMG_HEIGHT = 2592, 1944

        frame_name = os.path.splitext(image_name)[0] + ".txt"
        output_path = os.path.join(output_dir, frame_name)
        yolo_lines = []

        for annot_key in ["annot_A", "annot_B", "annot_C"]:
            annot = item.get(annot_key)
            if annot is None:
                continue

            label = annot.get("faceExp")
            boxes = annot.get("boxes")
            if boxes is None or label not in expression_map:
                continue

            class_id = expression_map[label]
            minX, minY, maxX, maxY = boxes["minX"], boxes["minY"], boxes["maxX"], boxes["maxY"]
            center_x = ((minX + maxX) / 2) / IMG_WIDTH
            center_y = ((minY + maxY) / 2) / IMG_HEIGHT
            width = (maxX - minX) / IMG_WIDTH
            height = (maxY - minY) / IMG_HEIGHT
            yolo_line = f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
            yolo_lines.append(yolo_line)

        if yolo_lines:
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write("\n".join(yolo_lines))

def convert_json_to_yolo_dir(json_dir, output_dir="yolo_labels", images_dir=None):
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(json_dir, filename)
            convert_json_to_yolo(json_path, output_dir, images_dir)
    print(f"✅ 모든 JSON 변환 완료! 결과가 '{output_dir}'에 저장됨.")


convert_json_to_yolo_dir(
    "/home/choi/Downloads/한국인 감정인식을 위한 복합 영상/Validation/labels",
    output_dir="/home/choi/project_doje/ttx",
    images_dir="/home/choi/project_doje/result_images"
)

# 또는 특정 매핑을 지정할 경우
# expression_map = {"기쁨": 0, "분노": 1, "슬픔": 2, "중립": 3}
# convert_json_to_yolo(json_path, output_dir, expression_map=expression_map)
