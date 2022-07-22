import pytest

from tags.models import Tags


@pytest.mark.django_db(transaction=True)
class TestTagsModel:
    def test_tags_creation(self):
        tag = Tags.objects.create(
            name='Tag One',
            color='#ee00ee',
            slug='tag_1'
        )

        assert tag is not None

        tag = Tags.objects.create(
            name='Tag Two',
            color='#EE00E1',
            slug='tag_2'
        )

        assert tag.color == '#ee00e1'

        tag = Tags.objects.create(
            name='Tag Three',
            color='EE00E2',
            slug='tag_3'
        )

        assert tag.color == '#ee00e2'
