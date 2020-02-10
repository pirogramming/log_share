from django.core.management.base import BaseCommand
from taggit.models import Tag

class Command(BaseCommand):
    help = 'Delete unused(non-related with any objects) tags in DB'

    def remove_all_tags_without_objects(self):
        for tag in Tag.objects.all():
            if tag.taggit_taggeditem_items.count() == 0:
                print(f'Removing: {tag}')
                tag.delete()
            else:
                print(f'Keeping: {tag}')

