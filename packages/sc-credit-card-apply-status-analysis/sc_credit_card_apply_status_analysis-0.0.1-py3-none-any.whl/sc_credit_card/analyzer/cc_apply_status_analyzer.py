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
from datetime import datetime

import pandas as pd
from config42 import ConfigManager

from sc_credit_card.analyzer.batch_status import BatchStatus
from sc_credit_card.analyzer.batch_type import BatchType
from sc_credit_card.analyzer.cc_pad_apply_status_analyzer import CcPadApplyStatusAnalyzer
from sc_credit_card.db.cc_sql import *
from sc_credit_card.db.db_module import DBModule


class CcApplyStatusAnalyzer:
    """
    信用卡审批状态基础类
    """

    def __init__(
            self, *,
            config: ConfigManager,
            is_initialize: bool,
            batch_date: datetime,
            is_pad: bool = True
    ):
        # 配置信息
        self._config = config
        # 是否是初始化导入数据
        self._is_initialize = is_initialize
        # 批量日期
        self._batch_date = batch_date
        # 是否是分析PAD网申数据
        self._is_pad = is_pad
        # 业务类型
        self._key_business_type = "credit_card.apply_status.business_type"
        self._business_type = None
        self._read_config(config=self._config)
        # 初始化数据库链接
        self._db_module = DBModule(config=self._config)

    def _read_config(self, *, config: ConfigManager):
        """
        读取配置，初始化相关变量
        """
        # 基础数据文件路径
        self._base_file_filepath = config.get("credit_card.apply_status.base_file_filepath")
        # 每日增量数据文件路径格式
        self._daily_incremental_filepath_format = config.get(
            "credit_card.apply_status.daily_incremental_filepath_format")
        # Sheet名称
        self._sheet_name = config.get("credit_card.apply_status.sheet_name")
        # 表头行索引
        self._header_row = config.get("credit_card.apply_status.sheet_config.header_row")
        # 申请编号列索引
        self._apply_no_column = config.get("credit_card.apply_status.sheet_config.apply_no_column")
        # 客户姓名列索引
        self._client_name_column = config.get("credit_card.apply_status.sheet_config.client_name_column")
        # 客户身份证号码列索引
        self._client_id_no_column = config.get("credit_card.apply_status.sheet_config.client_id_no_column")
        # 申请日期列索引
        self._apply_date_column = config.get("credit_card.apply_status.sheet_config.apply_date_column")
        # 申请编号列索引
        self._card_type_column = config.get("credit_card.apply_status.sheet_config.card_type_column")
        # 卡产品列索引
        self._card_no_column = config.get("credit_card.apply_status.sheet_config.card_no_column")
        # 客户经理名称列索引
        self._manager_name_column = config.get("credit_card.apply_status.sheet_config.manager_name_column")
        # 客户经理工号列索引
        self._manager_no_column = config.get("credit_card.apply_status.sheet_config.manager_no_column")
        # 分支行列索引
        self._branch_column = config.get("credit_card.apply_status.sheet_config.branch_column")
        # 一级支行列索引
        self._sub_branch_column = config.get("credit_card.apply_status.sheet_config.sub_branch_column")
        # 审批状态列索引
        self._apply_status_column = config.get("credit_card.apply_status.sheet_config.apply_status_column")
        # 拒绝原因列索引
        self._reject_reason_column = config.get("credit_card.apply_status.sheet_config.reject_reason_column")

    def _read_src_file(self, *, filepath: str) -> pd.DataFrame:
        """
        读取基础数据文件，获取DataFrame
        :return: DataFrame
        """
        logging.getLogger(__name__).info("读取数据源文件：{}".format(filepath))
        data = pd.read_excel(
            filepath,
            sheet_name=self._sheet_name,
            header=self._header_row,
            parse_dates=[self._apply_date_column],  # 指定申请日期为日期字段
        )
        self._apply_no_column_name = data.columns[self._apply_no_column]
        self._client_name_column_name = data.columns[self._client_name_column]
        self._client_id_no_column_name = data.columns[self._client_id_no_column]
        self._apply_date_column_name = data.columns[self._apply_date_column]
        self._card_type_column_name = data.columns[self._card_type_column]
        self._card_no_column_name = data.columns[self._card_no_column]
        self._manager_name_column_name = data.columns[self._manager_name_column]
        self._manager_no_column_name = data.columns[self._manager_no_column]
        self._branch_column_name = data.columns[self._branch_column]
        self._sub_branch_column_name = data.columns[self._sub_branch_column]
        self._apply_status_column_name = data.columns[self._apply_status_column]
        self._reject_reason_column_name = data.columns[self._reject_reason_column]
        data.fillna('', inplace=True)
        # 申请编号转换为字符串
        data[self._apply_no_column_name] = data[self._apply_no_column_name].astype("str")
        return data

    def _clear_data(self):
        """
        清理数据
        """
        logging.getLogger(__name__).info("清理数据")
        try:
            self._db_module.execute(sql=TRUNCATE_APPLY_STATUS)
        except Exception as e:
            logging.getLogger(__name__).error("清理数据失败：{}".format(e))
            return BatchStatus.CLEAR_DATA_ERROR
        return 0

    def _update_apply_status(
            self, apply_no, apply_date, card_type, card_no, manager_no,
            manager_name, branch, sub_branch, apply_status, reject_reason,
            client_name, client_id_no,
    ) -> (bool, int):
        query_result = self._db_module.select_one(
            sql=CHECK_APPLY_STATUS,
            param=(apply_no,)
        )
        if query_result is not None and len(query_result) > 0 and query_result[0] == apply_no:
            # 记录已经存在
            # 数据库中记录的申请日期
            query_apply_date = query_result[1]
            # 如果数据库中的申请日期日期小于或者等于批量日期，则更新此记录，即数据始终以最新一条为准
            if query_apply_date.date() > apply_date.date():
                logging.getLogger(__name__).info("找到重复记录：{}，无须更新".format(apply_no))
                return True, 0
            if query_result[2] == apply_status:
                logging.getLogger(__name__).info("找到重复记录：{}, 状态一致，无须更新".format(apply_no))
                return True, 0
            logging.getLogger(__name__).info("更新重复记录：{} 原状态为：{} 新状态为：{}".format(
                apply_no, query_result[2], apply_status
            ))
            return True, self._db_module.execute(
                sql=UPDATE_APPLY_STATUS,
                param=(card_no, apply_status, reject_reason, apply_no,),
            )
        # 记录不存在，则插入新数据
        return False, self._db_module.execute(
            sql=INSERT_APPLY_STATUS,
            param=(
                apply_no, apply_date, card_type, card_no, manager_no,
                manager_name, branch, sub_branch, apply_status, reject_reason,
                client_name, client_id_no,
            ),
        )

    def _import_apply_data(self, *, data) -> datetime:
        logging.getLogger(__name__).info("开始导入数据...")
        error_count = 0
        success_count = 0
        duplicated_count = 0
        # 记录数据文件中最后的申请日期
        last_date = datetime.strptime("1970-01-01", "%Y-%m-%d")
        for row_i, row in data.iterrows():
            apply_no = row[self._apply_no_column]
            client_name = row[self._client_name_column]
            client_id_no = row[self._client_id_no_column]
            apply_date = row[self._apply_date_column]
            card_type = row[self._card_type_column]
            card_no = row[self._card_no_column]
            manager_name = row[self._manager_name_column]
            manager_no = row[self._manager_no_column]
            branch = row[self._branch_column]
            sub_branch = row[self._sub_branch_column]
            apply_status = row[self._apply_status_column]
            reject_reason = row[self._reject_reason_column]
            try:
                duplicated, result = self._update_apply_status(
                    apply_no, apply_date, card_type, card_no, manager_no,
                    manager_name, branch, sub_branch, apply_status, reject_reason,
                    client_name, client_id_no
                )
                if apply_date > last_date:
                    last_date = apply_date
                success_count += 1
                if duplicated:
                    duplicated_count += 1
            except Exception as e:
                logging.getLogger(__name__).error("导入数据失败，申请编号：{} 错误信息：{}".format(apply_no, e))
                error_count += 1
        logging.getLogger(__name__).info(f"导入数据，成功：{success_count} 失败 {error_count} 重复 {duplicated_count}")
        return last_date

    def _update_batch_status(self, *, batch_type, batch_status, batch_date, remarks) -> int:
        query_result = self._db_module.select_one(
            sql=CHECK_BATCH_STATUS,
            param=(batch_type,)
        )
        if query_result is not None and len(query_result) > 0 and query_result[0] == batch_type:
            # 记录已经存在
            self._db_module.execute(
                sql=UPDATE_BATCH_STATUS,
                param=(batch_status, batch_date, remarks, batch_type,),
            )
            return 0
        # 记录不存在，则插入新数据
        self._db_module.execute(
            sql=INSERT_BATCH_STATUS,
            param=(batch_type, batch_status, batch_date, remarks,),
        )
        return 0

    def _initialize(self, *, batch_date) -> int:
        """
        如果基础数据不存在，则导入基础数据
        """
        result = self._clear_data()
        if result != 0:
            # 清理数据失败
            self._update_batch_status(
                batch_type=BatchType.CC_BASE_DATA_IMPORT.name,
                batch_status=BatchStatus.CLEAR_DATA_ERROR.value,
                batch_date=batch_date,
                remarks="清理数据失败",
            )
            return result
        filepath = self._base_file_filepath
        return self._run_import_data_batch(filepath=filepath, batch_date=batch_date, is_initialize=True)

    def _run_import_data_batch(self, *, filepath, batch_date, is_initialize: bool = False) -> int:
        batch_type = BatchType.CC_BASE_DATA_IMPORT.name if is_initialize else BatchType.CC_DAILY_IMPORT.name
        try:
            # 读取文件，获取DataFrame
            data = self._read_src_file(filepath=filepath)
        except FileNotFoundError as e:
            logging.getLogger(__name__).error("读取源文件 {} 失败：{}".format(filepath, e))
            # 文件不存在，则直接返回上一次的分析数据
            self._update_batch_status(
                batch_type=batch_type,
                batch_status=BatchStatus.FILE_NOT_FOUND.value,
                batch_date=batch_date,
                remarks="文件不存在",
            )
            return BatchStatus.FILE_NOT_FOUND.value
        last_apply_date = self._import_apply_data(data=data)
        real_batch_date = batch_date
        if is_initialize:
            # 如果是初始化导入，以数据文件中最后的申请日期作为批量日期
            real_batch_date = last_apply_date
        return self._update_batch_status(
            batch_type=batch_type,
            batch_status=BatchStatus.OK.value,
            batch_date=real_batch_date,
            remarks="成功",
        )

    def analysis(self) -> int:
        """
        主分析流程分析
        """
        # 读取业务类型
        self._business_type = self._config.get(self._key_business_type)
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))

        batch_date = datetime.now()
        if self._is_initialize:
            # 导入基础数据，如果没有导入的话
            result = self._initialize(batch_date=batch_date)
            if result != 0:
                logging.getLogger(__name__).error("导入基础数据失败：{}".format(result))
            logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
            return result

        # 批量日期不为空，则是导入新增的审核数据
        if self._batch_date is not None:
            batch_date = self._batch_date
            filepath = batch_date.strftime(self._daily_incremental_filepath_format)
            result = self._run_import_data_batch(filepath=filepath, batch_date=batch_date, is_initialize=False)
            if result != 0:
                logging.getLogger(__name__).error("导入 {} 数据失败：{}".format(batch_date, result))
            logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
            return result
        if self._is_pad:
            result = CcPadApplyStatusAnalyzer(
                config=self._config,
            ).analysis()
            if result != 0:
                logging.getLogger(__name__).error("分析信用卡网申状态失败：{}".format(result))
            logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
            return result
        logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
        return 0
