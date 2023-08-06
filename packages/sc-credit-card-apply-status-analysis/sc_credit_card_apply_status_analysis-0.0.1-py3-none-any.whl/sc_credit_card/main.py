# The MIT License (MIT)
#
# Copyright (c) 2021 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

from sc_config import ConfigUtils
from .analyzer.cc_apply_status_analyzer import CcApplyStatusAnalyzer
from sc_credit_card import PROJECT_NAME, __version__
import argparse
from datetime import datetime


class Runner(metaclass=Singleton):
    DATE_FORMAT = "%Y%m%d"
    TODAY = datetime.now()

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)

    def run(self, args):
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config.as_dict()))
        logging.getLogger(__name__).info("is initialize {}".format(args.is_initialize))
        if args.is_initialize:
            while True:
                print("导入初始数据将会清空历史数据，确认导入(Y/N)？")
                choice = input("请输入：")
                choice = choice.upper()
                if "Y" == choice:
                    break
                elif "N" == choice:
                    exit(0)
                else:
                    print("您输入的内容有误，请重新输入！")

        logging.getLogger(__name__).info("batch date {}".format(args.batch_date))
        logging.getLogger(__name__).info("is pad {}".format(args.is_pad))
        analyzer = CcApplyStatusAnalyzer(
            config=self._config,
            is_initialize=args.is_initialize,
            batch_date=args.batch_date,
            is_pad=args.is_pad,
        )
        return analyzer.analysis()

    @staticmethod
    def is_valid_date(date_str):
        """
        判断日期格式是不满足要求
        """
        try:
            return datetime.strptime(date_str, Runner.DATE_FORMAT)
        except ValueError:
            raise argparse.ArgumentTypeError("日期格式不符合要求，日期格式应为：" + Runner.get_today_str())

    @staticmethod
    def get_today_str():
        return Runner.TODAY.strftime(Runner.DATE_FORMAT)


def main():
    try:
        parser = argparse.ArgumentParser(description='信用卡审批状态分析工具')
        parser.add_argument(
            "-i", "--init",
            dest='is_initialize',
            action="store_true",
            help="导入初始数据（注意：该操作会清空历史数据，请谨慎操作！）",
        )
        parser.add_argument(
            "-d", "--date",
            type=Runner.is_valid_date,
            dest='batch_date',
            help="分析指定日期的信用卡审批状态文件，日期格式应为：" + Runner.get_today_str(),
        )
        parser.add_argument(
            "-p", "--pad",
            dest='is_pad',
            action="store_true",
            default=True,
            help="分析信用卡网申PAD申请明细数据",
        )
        args = parser.parse_args()
        logging.getLogger(__name__).info("arguments {}".format(args))
        state = Runner().run(args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
