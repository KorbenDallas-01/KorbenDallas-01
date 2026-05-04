import os
import shutil
import time

DOWNLOADS_FOLDER = "Downloads"
DAYS_OLD = 30

OLD_FILES_FOLDER = "old_files"


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def clean_downloads():
    create_folder(OLD_FILES_FOLDER)

    current_time = time.time()

    for filename in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, filename)

        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            days = file_age / 86400

            if days > DAYS_OLD:
                destination = os.path.join(OLD_FILES_FOLDER, filename)
                shutil.move(file_path, destination)
                print(f"Moved: {filename}")


if __name__ == "__main__":
    clean_downloads()
