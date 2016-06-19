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


def gregorian_to_jalali(_date, format_split='-'):
    """
        Convert Gregorian date to Jalali date into Template
    """
    if format_split == '-':
        text_date = "{0:04d}-{1:02d}-{2:02d}"

    elif format_split == '/':
        text_date = "{0:04d}/{1:02d}/{2:02d}"

    if isinstance(_date, str):
        _date = _date.strip()

        if len(_date) <= 11:
            _date = parser.parse(_date).date()

        else:
            _date = parser.parse(_date)

    if isinstance(_date, unicode):
        _date = str(_date).strip()

        if len(_date) <= 11:
            _date = parser.parse(_date).date()

        else:
            _date = parser.parse(_date)

    if isinstance(_date, datetime.datetime):
        with_time = True

    elif isinstance(_date, datetime.date):
        with_time = False

    year = _date.year
    month = _date.month
    day = _date.day
    date = jdatetime.GregorianToJalali(year, month, day)

    if with_time:
        _datetime = text_date.format(date.jyear, date.jmonth, date.jday)
        _datetime += ' {0:02d}:{1:02d}:{2:02d}'.format(
            _date.hour,
            _date.minute,
            _date.second
        )

        return _datetime

    else:
        _date = text_date.format(date.jyear, date.jmonth, date.jday)

        return _date


def jalali_to_gregorian(year, month, day):
    gregorian = jdatetime.JalaliToGregorian(year, month, day)
    gyear, gmonth, gday = gregorian.getGregorianList()
    _date = datetime.date(gyear, gmonth, gday)
    return _date
