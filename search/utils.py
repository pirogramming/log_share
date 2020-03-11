from django.db.models import Q

from post.models import Post


def filter_posts(q, user):
    # print('utils: posts')
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        (Q(title__icontains=q) | Q(contents__icontains=q))
    ).distinct()  # 중복 제거


def filter_tags(q, user):
    # print('utils: tags')
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        Q(tags__name__icontains=q)
    ).distinct()


def filter_users(q, user):
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        (Q(user__user_profile__name__icontains=q) | Q(user__username__icontains=q))
    ).distinct()


def group_id_list(request, user):
    group_list = [id for key, id in request.GET.items() if key[:5] == 'group']
    if not group_list:
        group_list= user.user_groups.all()
    # print(group_list)
    return group_list


def process_category(request, user, qs):
    rq = {}

    for key, value in request.GET.items():
        rq[key] = request.GET.get(key)
    #     print(key, value)
    # print(rq)

    if 'date-start' not in rq.keys() or rq['date-start'] == '':
        rq['date-start'] = '1900-01-01'
    if 'date-end' not in rq.keys() or rq['date-end'] == '':
        rq['date-end'] = '2100-12-31'
    if 'filter-category' not in rq.keys() or rq['filter-category'] == '':
        rq['filter-category'] = (
            '대외활동',
            '공모전',
            '스터디',
            '인턴',
            '강연',
            '기타',
        )

    # print(rq)
    # print(re)
    # print(qs)
    # print('그룹', group_id_list(request, user))
    return qs.filter(
        Q(start_date__gte=rq['date-start']) &
        Q(end_date__lte=rq['date-end']) &
        Q(user__user_groups__id__in=group_id_list(request, user)) &
        (Q(category__in=rq['filter-category']) | Q(category=rq['filter-category']))
    ).distinct().order_by('-start_date', '-end_date')
