import os

start_frame = 0
end_frame = 843

prefix = "2025-05-13_10-59-19_frame"
suffix = ".jpg"

root_dir = "/home/june/model_n/images"

output_file = "/home/june/model_n/train.txt"

with open(output_file, "w") as f_out:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for i in range(start_frame, end_frame + 1):
            filename = f"{prefix}{i:05d}{suffix}"
            if filename in filenames:
                # images/파일이름 형식으로 작성
                f_out.write(f"images/{filename}\n")