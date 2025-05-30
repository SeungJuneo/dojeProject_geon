import os

def delete_orphan_txt_files(labels_dir, images_dir):
    deleted_count = 0
    image_extensions = [".jpg", ".jpeg", ".png"]

    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            name = os.path.splitext(filename)[0]

            # 같은 이름의 이미지가 존재하는지 확인
            image_exists = any(
                os.path.exists(os.path.join(images_dir, name + ext))
                for ext in image_extensions
            )

            if not image_exists:
                txt_path = os.path.join(labels_dir, filename)
                os.remove(txt_path)
                print(f"🗑️ 삭제됨: {txt_path}")
                deleted_count += 1

    print(f"\n✅ 삭제 완료: 총 {deleted_count}개의 .txt 파일이 삭제됨.")

# 사용 예시
delete_orphan_txt_files(
    images_dir="/home/choi/project_doje/zip1_images",      # 이미지 폴더
    labels_dir="/home/choi/project_doje/zip2_labels"  # 라벨(txt) 폴더                               # 이미지 폴더
)
