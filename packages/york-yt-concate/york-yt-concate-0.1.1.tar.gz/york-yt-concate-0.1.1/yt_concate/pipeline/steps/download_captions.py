# 下載字幕
from youtube_transcript_api import YouTubeTranscriptApi
from yt_concate.pipeline.steps.step import Step
import pickle


class DownloadCaptions(Step):
    def process(self, transporter, inputs, utils):
        print('下載字幕中')
        for yto in transporter:
            if utils.caption_file_exists(yto):
                print('已經下載過了喔:', yto.v_id)
                continue
            try:
                # 使用 srt 變量和 .get_transcript() 函數獲得的字典列表
                srt = YouTubeTranscriptApi.get_transcript(yto.v_id)
            except:
                print('非英文或無字幕，網址: ', yto.url)
                continue
            print('寫入中', yto.url)
            with open(yto.get_caption_filepath(), 'wb', ) as f:
                pickle.dump(srt, f)
        return transporter
