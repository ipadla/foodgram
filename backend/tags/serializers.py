from rest_framework import serializers

from .models import Tags


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ('__all__',)

    def to_internal_value(self, data):
        # Без этого не срабатывает сериализатор из рецептов.
        if type(data) == int:
            return data
        return super().to_internal_value(data)
