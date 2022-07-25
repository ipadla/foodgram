import pytest

from tags.models import Tags


@pytest.mark.django_db(transaction=True)
class TestTagsModel:
    def test_tags_api(self, client):
        Tags.objects.create(id=0, name='One', color='#ee00ee', slug='tag_1')
        Tags.objects.create(name='Two', color='#EE00E1', slug='tag_2')
        Tags.objects.create(name='Three', color='EE00E2', slug='tag_3')

        response = client.get('/api/tags/')
        assert response.status_code == 200
        # TODO: Check response length

        response = client.get('/api/tags/0/')
        assert response.status_code == 200
        # TODO: Check response dict
