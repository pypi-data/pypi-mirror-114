# utils 實用程式，屬於工具箱，裝著一些通用型小型def
import os
from yt_concate.settings import DOWNLOADS_DIR, CAPTIONS_DIR, VIDEOS_DIR, OUTPUT_DIR


class Utils:
    def __init__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def get_videos_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + '.txt')

    def videos_list_file_exists(self, channel_id):
        path = self.get_videos_list_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def caption_file_exists(self, yto):
        filepath = yto.get_caption_filepath()
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    def videos_file_exists(self, yto):
        filepath = yto.get_video_filepath()
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    def edit_videos_file_exists(self, inputs):
        filepath = self.get_output_filename(inputs['channel_id'], inputs['search_word'])
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    def get_output_filename(self, channel_id, search_word):
        filename = channel_id + '_' + search_word + '.mp4'
        return os.path.join(OUTPUT_DIR, filename)
