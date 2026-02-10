import os
import logging


def enter(path: str):
    os.rmdir(path)
    logging.info(f"已删除文件夹 {os.path.abspath(path)}")
    print(f"已删除文件夹 {os.path.abspath(path)}")
