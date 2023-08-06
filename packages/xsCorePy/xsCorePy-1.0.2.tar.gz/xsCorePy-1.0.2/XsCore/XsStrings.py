from typing import Any

from XsCore import XsRegexUtils


class XsStrings:

    @staticmethod
    def clearHtml(html):
        """
        将内容里的html标签清除
        :param html:带有html标签的内容
        :return:
        """
        rz = XsRegexUtils.ReplaceAll(r'[<].*?[>]', html)
        return rz

    @staticmethod
    def cutStartEndList(txt: str, start: str, end: str) -> list[str]:
        """
        指定起始字符，截取中间的字符，将所有匹配到的字符并返回一个列表
        :param txt:要截取的内容
        :param start:开始标记
        :param end: 结束标记
        :return: 返回列表
        """
        rz = XsRegexUtils.FindStrToList(r'(?<=(' + start + '))[.\s\S]*?(?=(' + end + '))', txt)
        return rz

    @staticmethod
    def cutStartEndFirst(txt: str, start: str, end: str) -> str:
        """
        指定起始字符，截取中间的字符，返回第一个
        :param txt:要截取的内容
        :param start:开始标记
        :param end:结束标记
        :return: 返回第一个匹配到的字符
        """
        rz = XsRegexUtils.FindOne(r'(?<=(' + start + '))[.\s\S]*?(?=(' + end + '))', txt)
        return rz

    @staticmethod
    def splitLines(txt: str) -> list[str]:
        """
        将字符分割成列表,分割符为各种换行包括回车
        :param txt: 要分割的字符
        :return:
        """
        return txt.splitlines()

    @staticmethod
    def split(txt: str, strSplit: str = ',') -> list[str]:
        """
        将字符分割成列表,默认以,号分割，可以自定义分割符号
        :param txt: 要分割的字符
        :param strSplit: 分割符号
        :return:
        """
        return txt.split(strSplit)

    @staticmethod
    def getChinese(txt) -> list[str]:
        """
        提取内容中的中文
        :param txt: 内容
        :return:
        """
        rzs = XsRegexUtils.FindStrToList(r'[\u4e00-\u9fa5]+', txt)
        return rzs

    @staticmethod
    def getHtmlUrls(html: str) -> list[str]:
        """
        提取html中的网址，包括非a标签内容
        :param html:
        :return:
        """
        rzs = XsRegexUtils.FindStrToList(
            r'(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)', html)
        return rzs

    @staticmethod
    def isString(obj: Any) -> bool:
        """
        判断对象是否为字符串
        :param obj:
        :return:
        """
        return isinstance(obj, str)

    @staticmethod
    def is_empty(input_string: str) -> bool:
        """
        检查字符串是否为空（它必须至少包含一个非空格字符）
        *Examples:*

        >>> is_full_string(None) # returns false
        >>> is_full_string('') # returns false
        >>> is_full_string(' ') # returns false
        >>> is_full_string('hello') # returns true

        :param input_string: String to check.
        :type input_string: str
        :return: True if not empty, false otherwise.
        """
        return input_string.strip() == ''

    @staticmethod
    def is_number(input_string: str) -> bool:
        """
        判断字符是否为数字
        :param input_string:
        :return:
        """
        try:
            float(input_string)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(input_string)
            return True
        except (TypeError, ValueError):
            pass

        return False

    @staticmethod
    def is_integer(input_string: str) -> bool:
        """
        判断字符是否为整数
        >>> is_integer('42') # returns true
        >>> is_integer('42.0') # returns false

        :param input_string: String to check
        :type input_string: str
        :return: True if integer, false otherwise
        """
        return XsStrings.is_number(input_string) and '.' not in input_string

    @staticmethod
    def is_decimal(input_string: str) -> bool:
        """
         判断字符是否为decimal
        >>> is_decimal('42.0') # returns true
        >>> is_decimal('42') # returns false

        :param input_string: String to check
        :type input_string: str
        :return: True if integer, false otherwise
        """
        return XsStrings.is_number(input_string) and '.' in input_string
