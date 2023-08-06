from django.db.models import Q, F, CharField, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator


def objects_page(objects, pages, page):
    paginator = Paginator(objects, pages)
    return paginator.get_page(page)


def search_user(object_list, search):
    return object_list.annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(full_name__icontains=search) |
        Q(username__icontains=search))


def search_post(object_list, search):
    return object_list.filter(title__icontains=search)
