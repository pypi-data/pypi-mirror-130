#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import logging
import os

import pandas as pd
from config42 import ConfigManager

from sc_credit_card.db.cc_sql import *
from sc_credit_card.db.db_module import DBModule


class CcPadApplyStatusAnalyzer:
    """
    从数据库读取审批状态更新生成新的网申文件
    """

    def __init__(
            self, *,
            config: ConfigManager,
    ):
        # 配置信息
        self._config = config
        self._key_business_type = "credit_card.apply_status.business_type"
        self._business_type = None
        self._read_config(config=self._config)
        # 初始化数据库链接
        self._db_module = DBModule(config=self._config)

    def _read_config(self, *, config: ConfigManager):
        """
        读取配置，初始化相关变量
        """
        # 生成的目标Excel文件存放路径
        self._target_directory = self._config.get("credit_card.pad.target_directory")
        # 目标文件名称
        self._target_filename = self._config.get("credit_card.pad.target_filename")
        # 数据文件路径
        self._src_filepath = config.get("credit_card.pad.src_filepath")
        # Sheet名称
        self._sheet_name = config.get("credit_card.pad.sheet_name")
        # 表头行索引
        self._header_row = config.get("credit_card.pad.sheet_config.header_row")
        # 申请书条形码列索引
        self._apply_no_column = config.get("credit_card.pad.sheet_config.apply_no_column")
        # 申请书条形码列名称
        self._apply_no_column_name = config.get("credit_card.pad.sheet_config.apply_no_column_name")
        # 审批结果列索引
        self._apply_result_column = config.get("credit_card.pad.sheet_config.apply_result_column")
        # 生成的Excel中审批状态列名称
        self._target_apply_status_column_name = config.get(
            "credit_card.pad.sheet_config.target_apply_status_column_name")
        # 生成的Excel中拒绝原因列名称
        self._target_reject_reason_column_name = config.get(
            "credit_card.pad.sheet_config.target_reject_reason_column_name")

    def _read_src_file(self, *, filepath: str) -> pd.DataFrame:
        """
        读取数据文件，获取DataFrame
        :return: DataFrame
        """
        logging.getLogger(__name__).info("读取数据源文件：{}".format(filepath))
        data = pd.read_excel(
            filepath,
            sheet_name=self._sheet_name,
            header=self._header_row,
            dtype={self._apply_no_column_name: "str"},
        )
        self._apply_result_column_name = data.columns[self._apply_result_column]
        # 申请编号转换为字符串
        data[self._apply_no_column_name] = data[self._apply_no_column_name].astype("str")
        return data

    def _read_apply_status_from_db(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        从数据库中更新审批状态及拒绝原因
        :return: DataFrame
        """
        # 添加审批状态列
        data[self._target_apply_status_column_name] = data[self._apply_result_column_name]
        # 添加拒绝原因列
        data[self._target_reject_reason_column_name] = ""
        for row_i, row in data.iterrows():
            apply_no = row[self._apply_no_column]
            try:
                query_result = self._db_module.select_one(
                    sql=CHECK_APPLY_STATUS,
                    param=(apply_no,)
                )
                if query_result is not None and len(query_result) > 0 and query_result[0] == apply_no:
                    apply_status = query_result[2]
                    reject_reason = query_result[3]
                    data.at[row_i, self._target_apply_status_column_name] = apply_status
                    data.at[row_i, self._target_reject_reason_column_name] = reject_reason
            except Exception as e:
                logging.getLogger(__name__).error("查询数据失败，申请编号：{} 错误信息：{}".format(apply_no, e))
        return data

    def analysis(self) -> int:
        self._business_type = self._config.get(self._key_business_type)
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))
        data = self._read_src_file(filepath=self._src_filepath)
        data = self._read_apply_status_from_db(data=data)
        return self._write_new_apply_status_report(data=data)

    def _write_new_apply_status_report(self, *, data) -> int:
        """
        将结果写到新的文件中
        """
        target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename_full_path):
            logging.getLogger(__name__).info("删除输出文件：{} ".format(target_filename_full_path))
            try:
                os.remove(target_filename_full_path)
            except Exception as e:
                logging.getLogger(__name__).error("删除文件 {} 失败：{} ".format(target_filename_full_path, e))
                return 1
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename_full_path))
        # 读取源文件失败
        if data is None:
            logging.getLogger(__name__).error("写结果文件失败：无结果集")
            return 1

        with pd.ExcelWriter(target_filename_full_path) as excel_writer:
            data.to_excel(
                excel_writer=excel_writer,
                index=False,
                sheet_name=self._business_type,
            )
        return 0
