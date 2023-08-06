from yt_concate.pipeline.steps.step import Step
import pickle


class ReadCaptions(Step):
    def process(self, transporter, inputs, utils):
        print('處理字幕中......')
        for yto in transporter:
            try:
                with open(yto.caption_filepath, 'rb') as f:
                    yto.captions = pickle.load(f)
            except FileNotFoundError:
                print('未找到此檔案', yto.v_id)
                continue
        return transporter
