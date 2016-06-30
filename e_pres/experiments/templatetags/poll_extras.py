from django import template

register = template.Library()

@register.filter
def in_category(things, experiment):
    if things:
        return things.filter(experiment=experiment)
