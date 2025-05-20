import os
import cv2
from ultralytics import YOLO

def run_yolo_on_videos(video_dir : str, output_dir : str, model_path : str):
    """
     YOLO 추론 수행, 결과 영상 저장하는 함수입니다.
    """

    os.makedirs(output_dir, exist_ok=True)
    model = YOLO(model_path)

    valid_exts = (".mp4", ".avi", ".mov", ".mkv")

    for file_name in os.listdir(video_dir): #디렉토리 아래 파일들 전부 file_name으로 불러옴
        file_path = os.path.join(video_dir, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(valid_exts): #파일이고, 확장자가 영상일 경우
            print(f"Processing: {file_name}")
        
            cap = cv2.VideoCapture(file_path) #영상 읽어오기
            width, height = int(cap.get(3)), int(cap.get(4))
            fps = cap.get(cv2.CAP_PROP_FPS)

            output_path = os.path.join(output_dir, f"detected_{file_name}") #영상 이름 지정
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height)) #탐지된 영상 제작

            while cap.isOpened(): #영상이 열렸다면
                ret, frame = cap.read() #정상 유무, 프레임을 받아와 저장
                if not ret: # 올바르지 않다면 멈춤
                    break

                results = model(frame)
                annotated_frame = results[0].plot() #결과를 프레임별로 저장
                out.write(annotated_frame) #라벨을 영상에 삽입함

            cap.release() #비디오 읽기 작업 종료
            out.release() #비디오 출력 작업 종료
            print(f"✅ Saved: {output_path}")

    print("🎉 모든 유효한 영상 처리 완료!")

video_dir = "/home/june/result"
output_dir = "/home/june/result_videos"
model_path = "/home/june/Downloads/project_roadsign_class4 only-2025_05_14_04_20_40-yolo 1.1/runs/detect/train3/weights/best.pt"

run_yolo_on_videos(video_dir,output_dir,model_path)