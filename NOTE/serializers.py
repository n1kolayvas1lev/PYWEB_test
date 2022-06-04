from rest_framework import serializers
from NOTE.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('author',)


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at',  # из модели
            'author',  # из сериализатора
        )