from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from NOTE.models import Note
from . import serializers, filters, permissions


class NoteListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей и добавить новую запись. """

    def get(self, request: Request):
        objects = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        # Передаем в сериалайзер (валидатор) данные из запроса
        serializer = serializers.NoteSerializer(data=request.data)

        # Проверка параметров
        if not serializer.is_valid():  # serializer.is_valid(raise_exception=True)
            return Response(
                serializer.errors,  # serializer.errors будут все ошибки
                status=status.HTTP_400_BAD_REQUEST
            )

        # Записываем новую статью и добавляем текущего пользователя как автора
        serializer.save(author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.note_filter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .filter(public=True) \
            .order_by("-created_at", "-important")\
            .prefetch_related("authors",)


class NoteDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс представления для вывода данных о конкретной заметке, ее изменения и удаления"""
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated & permissions.GetPublicNote]

    def perform_update(self, serializer):
        """Переопределение метода update, которым изменения разрешено вносить только автору заметки"""
        author = self.get_object().author_id
        user = self.request.user.id
        if author == user:
            serializer.save()
            return serializer
        raise PermissionError('Невозможно изменить. (Недостаточно прав.)')