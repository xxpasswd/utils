"""
日期操作集合
"""
# coding: utf-8

from datetime import datetime
import calendar


def get_month_first_and_last_day(year, month):
    """
    获取某年某月份的第一天和最后一天
    """
    # 获取此月的第一天的星期和次月的天数
    week_day, month_day = calendar.monthrange(year, month)
    # 第一天
    first_day = datetime(year, month, 1)
    # 最后一天
    last_day = datetime(year, month, month_day)
    return first_day, last_day