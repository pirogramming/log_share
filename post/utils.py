import os
from uuid import uuid4
from django.utils import timezone
from taggit.models import Tag



def date_upload_to(instance, filename):
  # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
  ymd_path = timezone.now().strftime('%Y/%m/%d')
  # 길이 32 인 uuid 값
  uuid_name = uuid4().hex
  # 확장자 추출
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    ymd_path,
    uuid_name + extension,
  ])


def remove_all_tags_without_objects():
  for tag in Tag.objects.all():
    if tag.taggit_taggeditem_items.count() == 0:
      # print(f'Removing: {tag}')
      tag.delete()
    else:
      # print(f'Keeping: {tag}')
      pass

def tag_count_check(request, post):
  # request.POST.get('tags')로 tag를 가져오되, 없을시 None을 할당한다.
  tag_list = request.POST.get('tags')
  # tag들을 10개+나머지로 분리하여 리스트화한다
  tags = [str(tag) for tag in tag_list.split(',', maxsplit=10)]
  # 10개+나머지에서 나머지 제거
  tags = tags[:-1]
  # 하나씩 넣기.
  post.tags.set(*tags)

  return
