import os
import cv2
from ultralytics import YOLO

def save_detected_frames_only(video_dir: str, output_dir: str, model_path: str):
    """
    YOLOv8 추론 후 객체가 감지된 프레임만 저장:
    - 원본 이미지: (output_dir)/non_annotated
    - 라벨이 시각화된 이미지: (output_dir)/annotated
    """

    #annotated 파일과 non_annotated 파일 생성
    annotated_dir = os.path.join(output_dir, "annotated")
    raw_dir = os.path.join(output_dir, "non_annotated")
    labels_dir = os.path.join(output_dir, "labels")
    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    model = YOLO(model_path)
    saved_count = 0
    cap = cv2.VideoCapture(video_dir)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps / 5))
    frame_count = 0
    # valid_exts = (".mp4", ".avi", ".mov", ".mkv")

    # 'am'과 'pm' 디렉토리 내 파일 처리
    # for time_of_day in ["am", "pm"]: 
    #     time_dir = os.path.join(video_dir, time_of_day) #경로를 am 폴더 하나, pm 폴더 하나로 바꿈
        
    #     if not os.path.exists(time_dir):
    #         print(f"{time_of_day} 디렉토리가 존재하지 않습니다. 건너뛰기...")
    #         continue
        
        
        #경로 하위 파일들을 전부 불러옴
        # for file_name in os.listdir(time_dir):
        #     file_path = os.path.join(time_dir, file_name)
    if not os.path.isfile(video_dir):
            print(f"❌ 입력된 영상 경로가 잘못되었습니다: {video_dir}")
            return

    print(f"🎬 영상 처리 시작: {os.path.basename(video_dir)}")
    if os.path.isfile(video_dir): #and file_name.lower().endswith(valid_exts)
        #동영상 파일 이름 맨 앞을 불러옴
        base_name = os.path.splitext(os.path.basename(video_dir))[0]
        
        
        #영상이 열렸는지 확인
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                results = model(frame)[0]

            # 감지된 객체가 하나라도 있을 때만 저장
                if len(results.boxes) > 0:
                    img_h, img_w = frame.shape[:2]

                    labeled_frame = results.plot()
                    #:05d = 5자리 공간 확보
                    frame_name = f"{base_name}_frame{saved_count:05d}.jpg"

                    # mp4 저장
                    raw_path = os.path.join(raw_dir, frame_name)
                    labeled_path = os.path.join(annotated_dir, frame_name)

                    cv2.imwrite(raw_path, frame)
                    cv2.imwrite(labeled_path, labeled_frame)

                    # 라벨 저장
                    label_txt_path = os.path.join(labels_dir, frame_name.replace(".jpg", ".txt"))
                    with open(label_txt_path, "w") as f:
                        for box in results.boxes:
                            cls = int(box.cls[0])
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            xc = ((x1 + x2) / 2) / img_w
                            yc = ((y1 + y2) / 2) / img_h
                            w = (x2 - x1) / img_w
                            h = (y2 - y1) / img_h
                            f.write(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")


                    saved_count += 1

            frame_count += 1

        cap.release()
        print(f"✅ 감지된 프레임 {saved_count}개 저장 완료")

    print("🎉 모든 영상 처리 완료!")

# 사용 예시
video_dir = "/home/june/2025.05.15_record_video/am/2025-05-13_10-59-19.mp4"  # 'am'과 'pm' 폴더가 여기에 있음
output_dir = "/home/june/model_l"
model_path = "/home/june/best.pt"

save_detected_frames_only(video_dir, output_dir, model_path)
