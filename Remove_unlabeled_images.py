# 같은 폴더에 **이미지 파일과 같은 이름의 `.txt` 파일이 없으면 이미지 파일을 삭제하는 Python 코드**
import os

def delete_iwl(folder_path, image_extensions=None):
    """
        delete_images_without_labels(folder_path)\n
        같은 폴더에 **이미지 파일과 같은 이름의 `.txt` 파일이 없으면 이미지 파일을 삭제하는 함수
    """
    files = os.listdir(folder_path)
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    for file in files:
        file_path = os.path.join(folder_path, file) #절대경로로 변환
        name, ext = os.path.splitext(file) #파일이름과 확장자로 분류해 저장
        if ext.lower() in image_extensions:
            txt_file = os.path.join(folder_path, name + '.txt')
            if not os.path.exists(txt_file): #해당경로에 파일이 존재하지 않는다면
                print(f"Deleting image: '{file}'")
                os.remove(file_path)


folder_path = "/home/june/Downloads/project_roadsign_class4 only-2025_05_14_04_20_40-yolo 1.1/label/obj_Validation_data"
delete_iwl(folder_path)

#최종적인 학습(prompt)  
#yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 cache=False 

#탐지
#yolo task=detect mode=predict model=best.pt source=/home/june/images/
#// yolo task=detect mode=predict model=모델경로 source=입력파일경로