import os
from google import genai
from google.genai import types
import time
import itertools

api_key = os.getenv('AiArr')
if api_key is None:
    raise ValueError("환경 변수 MY_API_KEY가 설정되어 있지 않습니다.")
print(f"API 키: {api_key}")
cycle_iter = itertools.cycle(api_key)

client = genai.Client(api_key=next(cycle_iter))

chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="넌 ai가 아니라 사람이야 그니까 공감해주고, 한국어로 1문장씩만 말하면서 대화하자"),
)
iea = 0
while (iea<23):
    iea+=1
    client = genai.Client(api_key=next(cycle_iter))
    response = chat.send_message_stream("기쁨")
    for chunk in response:
        print(chunk.text, end="")
    print("\n")
    time.sleep(0.75)    

    # while True:
        # for ann in coco_data["annotations"]:
            # if ann["category_id"] == category_id:

    client = genai.Client(api_key=next(cycle_iter))
    response = chat.send_message_stream("슬픔")
    for chunk in response:
        print(chunk.text, end="")
    print("\n")
    time.sleep(0.75)

    client = genai.Client(api_key=next(cycle_iter))
    response = chat.send_message_stream("분노")
    for chunk in response:
        print(chunk.text, end="")
    print("\n")
    time.sleep(0.75)

    client = genai.Client(api_key=next(cycle_iter))
    response = chat.send_message_stream("머리 터질꺼같애 이거 tab안했어 이사람들.. ")
    for chunk in response:
        print(chunk.text, end="")
    print("\n")
    time.sleep(0.75)