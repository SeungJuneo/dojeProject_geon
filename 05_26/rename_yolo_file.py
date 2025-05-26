import os

def rename_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png.json"):
            new_filename = filename.replace(".png.json", ".json")
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Renamed '{filename}' → '{new_filename}'")
            except FileNotFoundError:
                print(f"File not found: '{filename}'")
            except FileExistsError:
                print(f"File already exists: '{new_filename}'")
            except Exception as e:
                print(f"Error while renaming '{filename}': {e}")

if __name__ == "__main__":
    target_directory = "/home/june/ai_hub/labels"  # 대상 디렉토리 이름
    rename_txt_files(target_directory)
    print("Renaming process completed.")