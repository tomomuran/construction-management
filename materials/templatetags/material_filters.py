from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    数値を掛け算するフィルター
    使用例: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
