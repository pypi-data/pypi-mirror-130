# -*- coding: utf-8 -*-
from typing import Union



class Findit(object):
    def __init__(self, threshold: Union[int, float] = 0.8, rgb: bool = True):
        """
        初始化构建

        Args:
            threshold: 识别阈值
            rgb: 是否使用rgb通道校验

        Returns:
            None
        """
        self.threshold = threshold
        self.rgb = rgb

    def find_best_result(self, im_source, im_search, threshold: Union[int, float] = None, rgb: bool = None):
        """
        依次运行CVSTRATEGY方法,在im_source中,找到最符合im_search的范围坐标

        Args:
            im_source: 待匹配图像
            im_search: 图片模板
            threshold: 识别阈值(0~1)
            rgb: 是否使用rgb通道进行校验

        Returns:
            None
        """
        # inti params
        threshold = threshold is None and self.threshold or threshold
        rgb = rgb is None and self.rgb or rgb

        