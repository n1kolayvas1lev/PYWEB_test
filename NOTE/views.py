from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from NOTE import filters, permissions, serializers
from NOTE.models import Note


class NoteListCreateAPIView(generics.ListCreateAPIView):
    """
    Вывод списка заметок и создание заметки
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter

    def get_queryset(self):
        """
        Получения доступа только к заметкам пользователя,
        а также заметкам других пользователей, которые отмечены как публичные
        """
        queryset = super().get_queryset()
        return queryset.filter(Q(author=self.request.user) | Q(public=True))

    def perform_create(self, serializer):
        """
        Передача данных пользователя как автора заметки
        """
        serializer.save(author=self.request.user)
        return serializer


class NoteDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для вывода данных о конкретной заметке, ее изменения и удаления
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated & permissions.GetPublicNote]

    def perform_update(self, serializer):
        """
        Изменения разрешено вносить только автору заметки
        """
        author = self.get_object().author_id
        user = self.request.user.id
        if author == user:
            serializer.save()
            return serializer
        else:
            raise PermissionError('Denied.')
