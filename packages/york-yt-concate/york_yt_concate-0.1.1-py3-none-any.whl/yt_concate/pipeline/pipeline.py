# pipeline 生產線
# 裝載著所有步驟
from yt_concate.pipeline.steps.step import StepException


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, inputs, utils):
        transporter = None  # 運輸車，把生產線的東西一個一個傳給亞一個生產線，初始為None代表沒有東西。
        for work in self.steps:
            try:
                transporter = work.process(transporter, inputs, utils)
            except StepException as err:
                print('休士頓，我們發現了一個錯誤！', err)
                break
