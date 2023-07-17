# encoding=utf-8
import re


def decompose_date(date):
    """
    Gives tuple of year, month, day if format is valid else raise InvalidFormatException
    :param date:
    :return:
    """
    re_date_format = r"(\d{4})[\-\/](\d{1,2})[\-\/](\d{1,2})"

    valid_date = re.match(re_date_format, date)
    if not valid_date:
        raise ValueError(
            "Invalid date format! Date should be of format yyyy-mm-dd")

    year, month, day = map(int, valid_date.groups())

    return year, month, day


number_map = {
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}
nepali_to_english_digit = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9",
}


def to_nepali_numbers(number):
    number = str(number)
    return "".join([number_map[i] for i in number])


# Getting nepali year and return english
def get_nepali_digit(year, month, day):
    year = str(year)
    month = str(month)
    day = str(day)
    year_value = "".join([nepali_to_english_digit[i] for i in year])
    month_value = "".join([nepali_to_english_digit[i] for i in month])
    day_value = "".join([nepali_to_english_digit[i] for i in day])
    return year_value, month_value, day_value


def weekday_abbr__a(date_obj, lang="en"):
    en = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    np = ["सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि", "आइत"]

    if lang == "en":
        return en[date_obj.weekday()]
    return np[date_obj.weekday()]


def weekday__A(date_obj, lang="en"):
    en = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"]
    np = [
        "सोमबार",
        "मंगलबार",
        "बुधबार",
        "बिहिबार",
        "शुक्रबार",
        "शनिबार",
        "आइतबार"]

    if lang == "en":
        return en[date_obj.weekday()]
    return np[date_obj.weekday()]


def weekday_as_dec__w(date_obj, lang="en"):
    if lang == "en":
        return str(date_obj.weekday())
    return to_nepali_numbers(str(date_obj.weekday()))


def day_of_month__d(date_obj, lang="en"):
    en = "%02d" % date_obj.day
    if lang == "en":
        return en
    return to_nepali_numbers(en)


def month_abbr__b(date_obj, lang="en"):
    en = [
        "Bai",
        "Jes",
        "Ashr",
        "Shr",
        "Bha",
        "Asho",
        "Kar",
        "Man",
        "Pou",
        "Mag",
        "Fal",
        "Chai",
    ]
    ne = [
        "बै",
        "जेष्",
        "आष",
        "श्रा",
        "भा",
        "असो",
        "कार्",
        "मं",
        "पौ",
        "माघ",
        "फा",
        "चै",
    ]
    if lang == "en":
        return en[date_obj.month - 1]
    return ne[date_obj.month - 1]


def month__B(date_obj, lang="en"):
    en = [
        "Baisakh",
        "Jestha",
        "Ashar",
        "Shrawan",
        "Bhadra",
        "Ashoj",
        "Kartik",
        "Mangsir",
        "Poush",
        "Magh",
        "Falgun",
        "Chait",
    ]
    ne = [
        "बैशाख",
        "जेष्ठ",
        "आषाढ",
        "श्रावन",
        "भाद्र",
        "असोज",
        "कार्तिक",
        "मंसिर",
        "पौष",
        "माघ",
        "फागुन",
        "चैत्र",
    ]
    if lang == "en":
        return en[date_obj.month - 1]
    return ne[date_obj.month - 1]


def month_as_int__m(date_obj, lang="en"):
    en = "%02d" % date_obj.month
    if lang == "en":
        return en
    return to_nepali_numbers(en)


def year_without_century__y(date_obj, lang="en"):
    if lang == "en":
        return str(date_obj.year)[2:]
    return to_nepali_numbers(str(date_obj.year)[2:])


def year__Y(date_obj, lang="en"):
    if lang == "en":
        return str(date_obj.year)
    return to_nepali_numbers(str(date_obj.year))


def am_pm__p(date_obj, lang="en"):
    return "AM"


def UTC_offset__z(date_obj, lang="en"):
    raise NotImplementedError


def timezone_name__Z(date_obj, lang="en"):
    raise NotImplementedError


def day_of_the_year__j(date_obj, lang="en"):
    raise NotImplementedError


def week_of_year_sunday__U(date_obj, lang="en"):
    raise NotImplementedError


def week_of_year_sunday__W(date_obj, lang="en"):
    raise NotImplementedError


def locale_appropriate_datetime__c(date_obj, lang="en"):
    raise NotImplementedError


def locale_appropriate_date__x(date_obj, lang="en"):
    raise NotImplementedError


def not_implemented_yet(date_obj, lang="en"):
    raise NotImplementedError


format_functions = {
    "%a": weekday_abbr__a,
    "%A": weekday__A,
    "%w": weekday_as_dec__w,
    "%d": day_of_month__d,
    "%b": month_abbr__b,
    "%B": month__B,
    "%m": month_as_int__m,
    "%y": year_without_century__y,
    "%Y": year__Y,
    "%H": lambda _, __: "00",
    "%I": lambda _, __: "00",
    "%p": am_pm__p,
    "%M": lambda _, __: "00",
    "%S": lambda _, __: "00",
    "%f": lambda _, __: "000000",
    "%z": not_implemented_yet,
    "%Z": not_implemented_yet,
    "%j": not_implemented_yet,
    "%U": not_implemented_yet,
    "%W": not_implemented_yet,
    "%c": not_implemented_yet,
    "%x": not_implemented_yet,
    "%X": lambda _, __: "00:00:00",
    "%%": lambda _, __: "%",
}
