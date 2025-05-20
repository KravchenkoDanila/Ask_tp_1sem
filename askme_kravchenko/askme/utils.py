from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects_list, request, per_page=3):
    page = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    # print(page_obj, paginator, paginator.num_pages > 1)
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
    }

# def paginate(objects_list, request, per_page=3):
#     page_number = request.GET.get('page')
#
#     paginator = Paginator(objects_list, per_page)
#
#     try:
#         page = paginator.page(page_number)
#     except PageNotAnInteger:
#         page = paginator.page(1)
#     except EmptyPage:
#         page = paginator.page(paginator.num_pages)
#
#     return page
