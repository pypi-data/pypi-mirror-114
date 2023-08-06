# preflight 前置步驟
from yt_concate.pipeline.steps.step import Step


class Preflight(Step):
    def process(self, transporter, inputs, utils):
        print('前置作業開始......')
        utils.create_dir()
