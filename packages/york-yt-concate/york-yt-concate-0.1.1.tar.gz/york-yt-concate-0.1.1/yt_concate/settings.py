import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_KEY = os.getenv('API_KEY')

# 把CAP跟VID加進DOW裡面
DOWNLOADS_DIR = 'downloads'  # 下載資料夾
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR, 'videos')  # 影片資料夾
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR, 'captions')  # 字幕資料夾
OUTPUT_DIR = 'output'
