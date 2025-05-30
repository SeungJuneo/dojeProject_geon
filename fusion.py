from ultralytics import YOLO
import cv2
import math

import os
from google import genai
from google.genai import types
import time
import itertools

from collections import deque
import threading

from dotenv import load_dotenv
load_dotenv()

st_api_key = os.getenv('AiArr')
if st_api_key is None:
    raise ValueError("환경 변수 MY_API_KEY가 설정되어 있지 않습니다.")

api_key = st_api_key.split(',')
cycle_iter = itertools.cycle(api_key)
client = genai.Client(api_key=next(cycle_iter))

chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="넌 ai가 아니라 사람이야 그니까 공감해주고, 한국어로 1문장씩만 말하면서 대화하자"),
)


def send_emotion_message(emotion_text):
    response = chat.send_message_stream(emotion_text)
    for chunk in response:
        if len(chunk.text) == 1:
            continue
        print(chunk.text, end="")
    print("\n")

cap=cv2.VideoCapture("http://111.111.111.27:8080/video")

frame_width=int(cap.get(3))
frame_height = int(cap.get(4))

# 녹화 기능
# out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))


model=YOLO("../best.pt")
classNames = ["happy","sad","angry","neutrality"]
display_width, display_height = 1080, 920

API_WINDOW_SECONDS = 5  
MAX_CALLS_PER_WINDOW = 1  # 원하는 호출 횟수로 조절
api_call_timestamps = deque()


last_emotion = None
last_response_time = 0
cooldown_seconds = 7
frame_count = 0
frame_skip = 3  # 3프레임에 1번만 YOLO 추론

def can_call_api():
    current_time = time.time()
    while api_call_timestamps and current_time - api_call_timestamps[0] > API_WINDOW_SECONDS:
        api_call_timestamps.popleft()
    return len(api_call_timestamps) < MAX_CALLS_PER_WINDOW

korean_emotion = {
    "happy": "기쁨",
    "sad": "슬픔",
    "angry": "분노",
    "neutrality": "무표정"
}
colors = {
    "happy": ([255, 255, 0], [255, 255, 255]),
    "sad": ([255, 0, 0], [255, 255, 255]),
    "angry": ([0, 0, 255], [255, 255, 255]),
    "neutrality": ([128, 128, 128], [255, 255, 255])
}
while True:
    success, img = cap.read()
    if not success:
        break
    
    frame_count += 1

    if frame_count % frame_skip == 0:
        # Doing detections using YOLOv8 frame by frame
        results=model(img,stream=True, verbose=False)

        # we will loop through each of the bouning box
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                # print(x1,y1,x2,y2)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]


                label=f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3

                
                current_time = time.time()

                if class_name != last_emotion or (current_time - last_response_time > cooldown_seconds):
                    last_emotion = class_name
                    last_response_time = current_time

                    # 감정별 색상 지정
                    
                    bg_color, text_color = colors.get(class_name, ([0, 0, 0], [255, 255, 255]))

                    # 라벨 배경과 텍스트 출력
                    cv2.rectangle(img, (x1, y1), (x2, y2), bg_color, 3)
                    cv2.rectangle(img, (x1, y1), c2, bg_color, -1, cv2.LINE_AA)
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, text_color, thickness=1, lineType=cv2.LINE_AA)

                    # API 호출 제한 확인
                    if can_call_api():
                        api_call_timestamps.append(time.time())  # 호출 시간 기록

                        # Google GenAI에 감정명 전달 후 출력
                        korean_emotion_text = korean_emotion.get(class_name, "무표정")
                        threading.Thread(target=send_emotion_message, args=(korean_emotion_text,), daemon=True).start()
                else:
                    # 감정 같고 쿨다운 안 지났으면 라벨만 그림 (속도 향상)
                    bg_color, text_color = colors.get(class_name, ([0, 0, 0], [255, 255, 255]))
                    cv2.rectangle(img, (x1, y1), (x2, y2), bg_color, 3)
                    cv2.rectangle(img, (x1, y1), c2, bg_color, -1, cv2.LINE_AA)
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, text_color, thickness=1, lineType=cv2.LINE_AA)
    else:
        pass 

    # out.write(img)
    resized_img = cv2.resize(img, (display_width, display_height))
    cv2.imshow("Image", resized_img)
    if cv2.waitKey(1) & 0xFF==ord('1'):
        break
# out.release()