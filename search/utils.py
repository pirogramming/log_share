from django.db.models import Q

from post.models import Post


def filter_posts(q, user):
    print('utils: posts')
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        (Q(title__icontains=q) | Q(contents__icontains=q))
    ).distinct()  # 중복 제거


def filter_tags(q, user):
    print('utils: tags')
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        Q(tags__name__icontains=q)
    ).distinct()


def filter_users(q, user):
    return Post.objects.filter(
        Q(user__user_groups__in=user.user_groups.all()) &  # 나와 관련된 유저들
        (Q(user__user_profile__name__icontains=q) | Q(user__username__icontains=q))
    ).distinct()
