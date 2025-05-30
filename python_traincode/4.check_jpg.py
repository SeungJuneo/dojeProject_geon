import os

def delete_unlabeled_images(images_dir, labels_dir):
    deleted_count = 0

    for filename in os.listdir(images_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            name, _ = os.path.splitext(filename)
            txt_path = os.path.join(labels_dir, name + ".txt")

            if not os.path.exists(txt_path):
                img_path = os.path.join(images_dir, filename)
                os.remove(img_path)
                print(f"🗑️ 삭제됨: {img_path}")
                deleted_count += 1

    print(f"\n✅ 삭제 완료: 총 {deleted_count}개의 이미지가 삭제됨.")

# 사용 예시
delete_unlabeled_images(
    images_dir="/home/choi/project_doje/zip1_images",      # 이미지 폴더
    labels_dir="/home/choi/project_doje/zip2_labels"  # 라벨(txt) 폴더
)
