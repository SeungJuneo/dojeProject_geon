import os
import shutil

labels_dir = '/home/choi/project_doje/ttx'
images_dir = '/home/choi/project_doje/zip1_images'
result_images_dir = '/home/choi/project_doje/zip2_images'
result_labels_dir = '/home/choi/project_doje/zip2_labels'

# 결과 폴더가 없다면 생성
os.makedirs(result_images_dir, exist_ok=True)
os.makedirs(result_labels_dir, exist_ok=True)

# labels 폴더 내의 모든 txt 파일을 반복
for txt_filename in os.listdir(labels_dir):
    if not txt_filename.endswith('.txt'):
        continue

    # txt에서 고유 식별자 추출
    identifier = txt_filename.split('_')[-1].replace('.txt', '')

    # images 폴더에서 해당 identifier를 포함하는 jpg 찾기
    for img_filename in os.listdir(images_dir):
        if identifier in img_filename and img_filename.endswith('.jpg'):
            # 새로운 이미지 이름은 txt 이름에서 .txt -> .jpg로 변경
            new_img_filename = txt_filename.replace('.txt', '.jpg')

            # 파일 복사 및 이름 변경
            shutil.copyfile(os.path.join(images_dir, img_filename),
                            os.path.join(result_images_dir, new_img_filename))

            shutil.copyfile(os.path.join(labels_dir, txt_filename),
                            os.path.join(result_labels_dir, txt_filename))
            break  # 같은 identifier의 이미지가 하나만 있다고 가정
