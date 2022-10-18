from django import template


register = template.Library()


@register.filter()
def censor(value):
    cen = ['дурак', 'идиот', 'придурок']
    header_list = value.split()
    new_value = []
    for word in header_list:
        if word.lower() in cen:
            word = '*' * len(word)
            new_value.append(word)
        else:
            new_value.append(word)
    return " ".join(new_value)