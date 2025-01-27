from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def create_pagination(main, page):
    paginator = Paginator(main, per_page=13)
    try:
        main = paginator.page(page)
    except EmptyPage:
        main = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        main = paginator.page(1)
    return main
