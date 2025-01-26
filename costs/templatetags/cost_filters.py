from django import template
from django.template.defaultfilters import date as date_filter
from django.conf import settings

register = template.Library()


@register.filter
def sub(value, arg):
    """
    2つの数値の差を計算するフィルター
    使用例: {{ value|sub:arg }}
    """
    try:
        return value - arg
    except (ValueError, TypeError):
        return None


@register.filter
def multiply(value, arg):
    """
    2つの数値の積を計算するフィルター
    使用例: {{ value|multiply:arg }}
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return None


@register.filter
def currency(value):
    """
    数値を通貨形式でフォーマットするフィルター
    使用例: {{ value|currency }}
    """
    try:
        return f"¥{int(value):,}"
    except (ValueError, TypeError):
        return "¥0"


@register.filter
def jp_date(value, arg=None):
    """
    日付を日本語形式でフォーマットするフィルター
    使用例: {{ value|jp_date }} または {{ value|jp_date:"Y年m月d日" }}
    """
    if not value:
        return ""
    if arg is None:
        arg = "Y年m月d日"
    return date_filter(value, arg)
