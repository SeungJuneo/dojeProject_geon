from ultralytics import YOLO
import cv2
import math

import os
from google import genai
from google.genai import types
import time
import itertools

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



cap=cv2.VideoCapture("http://111.111.111.27:8080/video")

frame_width=int(cap.get(3))
frame_height = int(cap.get(4))

out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))


model=YOLO("../best.pt")
classNames = ["happy","sad","angry","neutrality"]
display_width, display_height = 1080, 920

while True:
    success, img = cap.read()
    # Doing detections using YOLOv8 frame by frame
    results=model(img,stream=True, verbose=False)

    # we will loop through each of the bouning box
    for r in results:
        boxes=r.boxes
        for box in boxes:
            x1,y1,x2,y2=box.xyxy[0]
            x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
            # print(x1,y1,x2,y2)
            cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
            conf=math.ceil((box.conf[0]*100))/100
            cls=int(box.cls[0])
            class_name=classNames[cls]


            label=f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)



            if class_name=="happy":
                client = genai.Client(api_key=next(cycle_iter))
                response = chat.send_message_stream("기쁨")
                for chunk in response:
                    print(chunk.text, end="")
                print("\n")
                time.sleep(1.3)    
            elif class_name=="sad":
                client = genai.Client(api_key=next(cycle_iter))
                response = chat.send_message_stream("슬픔")
                for chunk in response:
                    print(chunk.text, end="")
                print("\n")
                time.sleep(1.3)   
            elif class_name=="angry":
                client = genai.Client(api_key=next(cycle_iter))
                response = chat.send_message_stream("화남")
                for chunk in response:
                    print(chunk.text, end="")
                print("\n")
                time.sleep(1.3)   
            elif class_name=="neutrality":
                client = genai.Client(api_key=next(cycle_iter))
                response = chat.send_message_stream("무표정")
                for chunk in response:
                    print(chunk.text, end="")
                print("\n")
                time.sleep(1.3)   

    # out.write(img)
    resized_img = cv2.resize(img, (display_width, display_height))
    cv2.imshow("Image", resized_img)
    if cv2.waitKey(1) & 0xFF==ord('1'):
        break
out.release()