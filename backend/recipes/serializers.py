from rest_framework import serializers

from recipes.models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
        read_only_fields = ('__all__',)
