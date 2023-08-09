from django.template import Library

register = Library()


@register.filter()
def get_companion(obj, request):
    return obj.recipient if obj.sender == request.user else obj.sender
