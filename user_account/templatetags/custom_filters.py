from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.encoding import force_str

register = template.Library()
user = get_user_model()

@register.filter
def user_display(user):
    if isinstance(user, User):
        return f"{user.username}"
    return ''

@register.filter
def str(value):
    return force_str(value)