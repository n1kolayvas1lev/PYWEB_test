from django_filters import rest_framework as filters
from NOTE.models import Note


class NoteFilter(filters.FilterSet):
    """Фильтрация заметок"""

    class Meta:
        model = Note
        fields = ['status', 'important', 'public']

