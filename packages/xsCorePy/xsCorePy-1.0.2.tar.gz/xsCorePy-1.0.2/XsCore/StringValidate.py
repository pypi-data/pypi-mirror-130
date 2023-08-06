
from XsCore import XsRegexUtils


class XsStringValidate:

    @staticmethod
    def IsEmail(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)', txt)

    @staticmethod
    def IsIDCard(txt: str) -> bool:
        return XsRegexUtils.IsMatch(
            r'[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]', txt)

    @staticmethod
    def IsMobile(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'1(3|4|5|6|7|8|9)\d{9}', txt)

    @staticmethod
    def IsTel(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'\d{3}-\d{8}|\d{4}-\d{7}', txt)

    @staticmethod
    def IsIp(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))', txt)

    @staticmethod
    def IsPostCode(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'[1-9]\d{5}(?!\d)', txt)

    @staticmethod
    def IsUrl(txt: str) -> bool:
        return XsRegexUtils.IsMatch(r'[a-zA-z]+://[^\s]*', txt)