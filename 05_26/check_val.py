import os

# 각자 폴더 경로 지정
txt_folder = "/home/june/ai_hub/short_labels"  # 예: "./txt_files"
png_folder = "/home/june/ai_hub/short_images"  # 예: "./png_files"

# 폴더 내 파일 리스트
txt_files = os.listdir(txt_folder)
png_files = os.listdir(png_folder)

# 기본 이름 추출
txt_names = set()
png_names = set()

for f in txt_files:
    if f.endswith('.png.txt'):
        base_name = f[:-8]  # '.png.txt' 제거
        txt_names.add(base_name)

for f in png_files:
    if f.endswith('.png'):
        base_name = f[:-4]  # '.png' 제거
        png_names.add(base_name)

# 비교
only_in_txt = txt_names - png_names
only_in_png = png_names - txt_names

if not only_in_txt and not only_in_png:
    print("모든 기본 이름이 두 폴더에 완전히 일치합니다.")
else:
    if only_in_txt:
        print("PNG 파일이 없는 TXT 파일 기본 이름:")
        for name in sorted(only_in_txt):
            print(name)
    if only_in_png:
        print("TXT 파일이 없는 PNG 파일 기본 이름:")
        for name in sorted(only_in_png):
            print(name)
