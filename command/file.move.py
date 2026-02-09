import os
import shutil
import logging


def enterance(path: str, newPath: str):
    shutil.move(path, newPath)
    logging.info(f"已移动文件 {os.path.abspath(path)} 到 {os.path.abspath(newPath)}")
    print(f"已移动文件 {os.path.abspath(path)} 到 {os.path.abspath(newPath)}")
