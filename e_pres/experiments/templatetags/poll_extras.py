from django import template

register = template.Library()

@register.filter
def in_category(things, experiment):
    return things.filter(experiment=experiment)
