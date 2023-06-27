from curriculum.models import Lesson,Standard,Subject
from rest_framework import serializers

class standardserializer(serializers.HyperlinkedModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Standard
        fields="__all__"

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    options = serializers.HyperlinkedRelatedField(
    view_name='standard-detail',
    lookup_field = 'slug',
    many=True,
    read_only=True)
    class Meta:
        model=Subject
        fields="__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }