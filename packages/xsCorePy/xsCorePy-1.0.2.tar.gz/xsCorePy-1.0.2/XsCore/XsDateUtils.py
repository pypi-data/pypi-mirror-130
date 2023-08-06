import datetime
import time

"""
时间日期的相关处理
"""
class XsDateUtils:

    @staticmethod
    def getCurrentMilliSecondTime():
        """
         description:  获取当前时间-毫秒级
         return:       1557730376981 -> str
        """
        timestamps = str(round(time.time() * 1000))
        return timestamps

    @staticmethod
    def getCurrentSecondTime():
        """
        description:  获取当前时间-秒级
        return:       1557730377 -> str
        """
        timestamps = str(round(time.time()))
        return timestamps

    @staticmethod
    def getCurrentTimeTuple(times=time.time()):
        """
              description:  接受秒级时间戳并返回时间元组（与mktime(tuple)相反）
             times:        默认当前时间 可传second
             return:       (tm_year=2019, tm_mon=5, tm_mday=13, tm_hour=10, tm_min=9, tm_sec=18, tm_wday=0, tm_yday=133, tm_isdst=0) -> tuple
              tips:         time.localtime() 不传参则取当前时间
         """

        timestamps = time.localtime(times)
        return timestamps

    @staticmethod
    def getTimeByTuple(tupleTime=time.localtime()):
        """
              description:  接受时间元组并返回秒级时间戳（与localtime(sec)相反）
              tupleTime:    默认当前时间的元组 可通过time.localtime() or datetime.datetime.now().timetuple()获取
              return:       1557733061 -> str
              """

        timestamps = str(round(time.mktime(tupleTime)))
        return timestamps

    @staticmethod
    def getCurrentFormatTimeStr(times=time.time()):
        """
              description:  将指定时间元组格式化为字符串
              times:        默认当前时间 可传second
              return:       2019-05-13 15:00:47 -> str
              tips:         %y 两位数的年份表示（00-99）    %Y 四位数的年份表示（000-9999）   %m 月份（01-12）    %d 月内中的一天（0-31）
                            %H 24小时制小时数（0-23）      %I 12小时制小时数（01-12）        %M 分钟数（00=59）  %S 秒（00-59）   %w 星期（0-6）
         """
        timestamps = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(times))
        return timestamps

    @staticmethod
    def getCurrentTimeTupleByFormatStr(time_str=str(datetime.datetime.now()).split(".")[0],
                                       format_type="%Y-%m-%d %H:%M:%S"):
        """
              description:  接受格式化字符串返回时间元组
              time_str:     格式化字符串   如:2019-05-13 15:00:47    默认当前时间
              format_type:  格式化规则    如:%Y-%m-%d %H:%M:%S      默认%Y-%m-%d %H:%M:%S
              return:       (tm_year=2019, tm_mon=5, tm_mday=13, tm_hour=10, tm_min=9, tm_sec=18, tm_wday=0, tm_yday=133, tm_isdst=0) -> tuple
              """

        return time.strptime(time_str, format_type)

    @staticmethod
    def getCurrentTimeStr():
        """
              description:  获取当前时间的可读形式字符串
              return:       Mon May 13 11:27:42 2019 -> str
              """

        return time.ctime()

    @staticmethod
    def getCurrentTimeStrByTuple(tupleTime=time.localtime()):
        """
              description:  获取指定时间的可读形式字符串
              tupleTime:    时间元组 可通过time.localtime() or datetime.datetime.now().timetuple()获取 默认当前时间的元组
              return:       Mon May 13 11:27:42 2019 -> str
              """

        return time.asctime(tupleTime)

    @staticmethod
    def sleepTime(minsecond):
        """
        推迟调用线程的运行
        :param minsecond: 毫秒
        :return:
        """
        time.sleep(minsecond)

    @staticmethod
    def getNowDateTime():
        """
             description:  获取当前日期&时间
             return:       2019-05-13 14:41:15 -> str
             """
        timestamps = str(datetime.datetime.now()).split(".")[0]
        return timestamps

    @staticmethod
    def getNowTime():
        """
             description:  获取当前时间
             return:       14:41:15 -> str
             """

        timestamps = str(datetime.datetime.now().time()).split(".")[0]
        return timestamps

    @staticmethod
    def getTodayDate():
        """
             description:  获取当前日期
             return:       2019-05-13 -> str
             tipe:         datetime.datetime.now().date()有相同效果
             """

        timestamps = str(datetime.date.today())
        return timestamps

    @staticmethod
    def getTimeDate(times=time.time()):
        """
             description:  获取指定时间戳的日期
             time:         秒 默认当前时间
             return:       2019-05-13 -> str
             tips:         一天86400秒
             """

        timestamps = str(datetime.date.fromtimestamp(round(times)))
        return timestamps

    # 获取距离现在时间的任意时间的日期     正数 加,负数 减  return:2019-05-12
    @staticmethod
    def getAnyDateTime(day, hour=0, min=0, sec=0):
        """
             description:  获取距离现在时间的任意时间的日期&时间
             day:          天数 1代表当前时间+1天    -1代表当前时间-1天
             hour:         小时 2代表当前时间+2h     -2代表当前时间-2h     默认=0
             min:          分钟 30代表当前时间+30min -30代表当前时间-30m   默认=0
             sec:          秒   120代表当前时间+120s -120代表当前时间-120s 默认=0
             return:       2019-05-15 15:37:41 -> str
             """

        return \
        str(datetime.datetime.now() + datetime.timedelta(days=day, hours=hour, minutes=min, seconds=sec)).split(".")[0]

    @staticmethod
    def getAnyDateSecondTime(day, hour=0, min=0, sec=0):
        """
             description:  获取距离现在时间的任意时间的秒数
             day:          天数 1代表当前时间+1天    -1代表当前时间-1天
             hour:         小时 2代表当前时间+2h     -2代表当前时间-2h     默认=0
             min:          分钟 30代表当前时间+30min -30代表当前时间-30m   默认=0
             sec:          秒   120代表当前时间+120s -120代表当前时间-120s 默认=0
             return:       1557902182 -> str
             """

        anyDay = datetime.datetime.now() + datetime.timedelta(days=day, hours=hour, minutes=min, seconds=sec)
        return str(round(time.mktime(anyDay.timetuple())))

    @staticmethod
    def getTodayTime():
        """
             description:  获取当天0点的时间戳
             return:       1557676800 -> str
             """

        return str(round(time.mktime(datetime.date.today().timetuple())))

    @staticmethod
    def getCurrentWeekTime():
        """
             description:  获取本周周一0点
             return:       1557676800 -> str
             tips:         可替换成: timestamps = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(times)), "%Y-%m-%d"))
             """

        week = int(time.strftime("%w", time.localtime()))
        times = round(time.time()) - (week - 1) * 86400
        timestamps = time.mktime(datetime.date.fromtimestamp(times).timetuple())
        return str(round(timestamps))
