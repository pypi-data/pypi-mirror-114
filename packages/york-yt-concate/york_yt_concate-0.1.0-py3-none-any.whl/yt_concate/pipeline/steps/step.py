# step 步驟
# 建立 interface 介面
from abc import ABC, abstractmethod  # Abstract Base Class 抽象類別


class Step(ABC):  # Base class
    def __init__(self):
        pass

    @abstractmethod
    def process(self, transporter, inputs, utils):  # 執行
        pass


class StepException(Exception):  # 例外捕捉
    pass
