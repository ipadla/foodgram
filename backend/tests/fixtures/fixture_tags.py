import pytest

from tags.models import Tags


@pytest.fixture(autouse=True, scope='package')
def tags(django_db_blocker):
    with django_db_blocker.unblock():
        for i in range(5):
            Tags.objects.create(
                name=f'Tag{i}',
                color=f'#EE00E{i}',
                slug=f'tag_{i}'
            )

        return Tags.objects.all()
