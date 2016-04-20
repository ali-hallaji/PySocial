# -*- coding: utf-8 -*-
# Python Import
import calendar
import datetime
import jdatetime
from dateutil import parser


def translate_ago_date(_date):

    now = datetime.datetime.now()
    diff = (now - _date)
    sec = int(diff.total_seconds())

    end_month = calendar.monthrange(now.year, now.month)[1]

    if sec <= 59:
        result = int(sec), 'seconds'

    elif 60 <= sec <= 3599:
        result = int(sec / 60), 'minutes'

    elif 3600 <= sec <= 86399:
        result = int(sec / 3600), 'hours'

    elif sec >= 86400:
        if diff.days <= 6:
            result = diff.days, 'days'

        elif 7 <= diff.days <= end_month:
            result = (diff.days / 7), 'weeks'

        elif (end_month + 1) <= diff.days <= 365:
            result = (diff.days / end_month), 'months'

        elif diff.days >= 366:
            result = (diff.days / 365), 'years'

    return result


def last_persian_date(_date):
    _tuple = translate_ago_date(_date)

    translate = {
        'seconds': 'ثانیه',
        'minutes': 'دقیقه',
        'hours': 'ساعت',
        'days': 'روز',
        'months': 'ماه',
        'years': 'سال'
    }

    text = "{0} {1} پیش".format(_tuple[0], translate[_tuple[1]])

    return text


def gregorian_to_jalali(_date):
    """
        Convert Gregorian date to Jalali date into Template
    """
    if isinstance(_date, datetime.datetime):
        with_time = True
    elif isinstance(_date, datetime.date):
        with_time = False

    if isinstance(_date, str):
        _date = parser.parse(_date)

    year = _date.year
    month = _date.month
    day = _date.day
    date = jdatetime.GregorianToJalali(year, month, day)

    if with_time:
        _datetime = '{0}/{1}/{2}'.format(date.jyear, date.jmonth, date.jday)
        _datetime += ' {0}:{1}:{2}'.format(
            _date.hour,
            _date.minute,
            _date.second
        )

        return _datetime

    else:
        _date = '{0}/{1}/{2}'.format(date.jyear, date.jmonth, date.jday)

        return _date
