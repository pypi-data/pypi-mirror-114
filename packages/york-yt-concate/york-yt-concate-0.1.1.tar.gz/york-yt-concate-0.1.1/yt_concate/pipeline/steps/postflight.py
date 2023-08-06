# post flight 後至步驟
from yt_concate.pipeline.steps.step import Step


class Postflight(Step):
    def process(self, transporter, inputs, utils):
        print('後製作業開始，準備結束程式。')
        pass
