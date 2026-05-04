import os
import shutil
from datetime import datetime

SOURCE_FOLDER = "important_files"
BACKUP_FOLDER = "backup"


def make_backup():
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)

    date = datetime.now().strftime("%Y-%m-%d_%H-%M")

    backup_name = "backup_" + date
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    shutil.copytree(SOURCE_FOLDER, backup_path)

    print("Backup created:")
    print(backup_path)


if __name__ == "__main__":
    make_backup()
