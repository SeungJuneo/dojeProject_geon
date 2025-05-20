import os
import zipfile

def extract_zip(zip_path, extract_dir):
    """
        zip파일 압축해제 함수
    """
    if os.path.exists(zip_path): 
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir) #압축해제
            print(f"Extracted {os.path.basename(zip_path)} to {extract_dir}")
    else:
        print(f"Zip not found: {zip_path}")

def delete_files(lbl_file_path, img_file_path):
    """
        img, label 삭제 함수
    """
    for file_path in [lbl_file_path, img_file_path]:
        if os.path.exists(file_path): #해당경로에 파일이 있다면
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

def process_file(lbl_file_path, img_folder_path):
    """
        한 줄에서 4로 시작하는 줄만 남기는 알고리즘 함수
    """
    with open(lbl_file_path, 'r', encoding='utf-8') as f:
        new_lines = [line for line in f if line.strip().split() and line.strip().split()[0].isdigit() and line.strip().split()[0].startswith('4')]
        #파일이 비어있지 않고, 파일에서 첫번째 단어가 숫자이며, 그숫자가 4로 시작하는 경우를 저장
    if new_lines:
        with open(lbl_file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    else:
        img_file_path = os.path.join(img_folder_path, os.path.basename(lbl_file_path).replace('.txt', '.jpg'))
        delete_files(lbl_file_path, img_file_path) #txt와 jpg 확장자만 바꿔 삭제

base_path = '/home/june/RoadSign(copy)/val/'
for file_index in range(1, 16):
    img_extract_dir = os.path.join(base_path, 'img', f'img_validation{str(file_index).zfill(3)}')
    lbl_extract_dir = os.path.join(base_path, 'lbl', f'lbl_validation{str(file_index).zfill(3)}')
    #압축 풀기
    extract_zip(os.path.join(base_path, f'img_validation{str(file_index).zfill(3)}.zip'), img_extract_dir)
    extract_zip(os.path.join(base_path, f'lbl_validation{str(file_index).zfill(3)}.zip'), lbl_extract_dir)
    for file in os.listdir(lbl_extract_dir):
        if file.endswith('.txt'):
            process_file(os.path.join(lbl_extract_dir, file), img_extract_dir) #프로세스 진행
