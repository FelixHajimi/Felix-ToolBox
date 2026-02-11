import os
import logging


def enter(path: str):
    os.mkdir(path)
    logging.info(f"已创建文件夹至 {os.path.abspath(path)}")
    print(f"已创建文件夹至 {os.path.abspath(path)}")