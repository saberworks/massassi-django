from django import template

register = template.Library()

@register.filter(name='color_rating')
def color_rating(value):
    css_class = 'level-bad'

    if value >= 7:
        css_class = 'level-good'
    elif value >= 5:
        css_class = 'level-ok'

    return '<span class="{}">{}</span>'.format(css_class, value)

@register.filter(name='pluralize_string')
def pluralize_string(value):
    if value.endswith('s'):
        return value

    return value + 's'

@register.filter(name='sum_column')
def sum_column(item_list, column):
    return sum(getattr(item, column) for item in item_list)

# Human-Readable file size
@register.filter(name='hr_file_size')
def hr_file_size(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f&nbsp;%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
