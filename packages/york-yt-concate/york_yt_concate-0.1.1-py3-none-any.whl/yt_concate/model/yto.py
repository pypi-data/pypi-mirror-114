# yto YouTube object
import os
from yt_concate.settings import CAPTIONS_DIR, VIDEOS_DIR


class YTO:
    def __init__(self, url):
        self.url = url
        self.v_id = self.get_video_id_from_url(url)
        self.caption_filepath = self.get_caption_filepath()
        self.video_filepath = self.get_video_filepath()
        self.captions = None
        self.time_start = None
        self.time_duration = None
        self.download_or_not = False


    @staticmethod
    def get_video_id_from_url(url):  # 擷取影片網址代號的部分，當作video_id
        return url.split('watch?v=')[-1]

    def get_caption_filepath(self):
        return os.path.join(CAPTIONS_DIR, self.v_id + '.txt')

    def get_video_filepath(self):
        return os.path.join(VIDEOS_DIR, self.v_id + '.mp4')

