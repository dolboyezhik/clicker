from .serializers import NoteSerializer  # Импортируем сериалайзер, который мы написали
from django.contrib.auth import login
from django.shortcuts import render, redirect
from docutils.parsers.rst.directives.admonitions import Note
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response

# from clicker.backend.forms import UserForm

from rest_framework.views import APIView
from rest_framework.response import Response

...


class NoteView(APIView):
    def get(self, request):
        id = request.query_params.get("id")
        if id:
            note = Note.objects.get(pk=id)  # Получаем заметку из базы по primary key
            serializer = NoteSerializer(note)  # Засовываем заметку в сериализатор, преобразуем данные
            return Response(serializer.data)  # serializer.data вернет красивый json на фронт

        notes = Note.objects.all()  # Получаем все заметки из базы данных

        # Засовываем полученные данные в сериалайзер, чтобы
        # он автоматически превратил все данные в красивый json формат
        # и ставим аргумент many=True, чтобы он достал множество заметок, а не одну
        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data)  # serializer.data вернет красивый json на фронт

    def post(self, request):
        title = request.data.get('title')
        text = request.data.get('text')
        note = Note.objects.create(title=title, text=text)

        return Response({
            "id": note.id,
            "title": note.title,
            "text": note.text
        })

    def put(self, request):
        id = request.data.get('id')  # Получение id из тела запроса
        if not id:
            return Response({"error": 'Нету id'})

        """
        Поиск заметки.
        Метод filter используется потому, что метод update (ниже) работает только по списку объектов.
        """
        note = Note.objects.filter(pk=id)
        if not note:
            return Response({"error": 'Нету такой заметки'})
        title = request.data.get('title')
        text = request.data.get('text')
        note.update(title=title, text=text)  # Обновление заметки

        updated_note = Note.objects.get(pk=id)  # Получение обновленной заметки
        return Response({
            "id": updated_note.id,
            "title": updated_note.title,
            "text": updated_note.text
        })

    def delete(self, request):
        id = request.query_params.get('id')  # Получение id из параметров запроса
        if not id:
            return Response({"error": 'Нету id'})
        note = Note.objects.get(pk=id)  # Получение заметки
        if not note:
            return Response({"error": 'Нету такой заметки'})
        note.delete()  # Удаление заметки

        return Response({
            "success": 'Заметка успешно удалена'
        })


# Или более реальный пример. Переписанная функция регистрации из прошлой лекции.
class Register(APIView):
    def get(self, request):
        from project.backend.forms import UserForm
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        from project.backend.forms import UserForm
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {'form': form})


def notes_list(request):
    pass


@api_view(['GET', 'POST', 'DELETE'])
def notes_list(request):
    if request.method == 'GET':
        return ...

    if request.method == 'POST':
        return ...

    if request.method == 'DELETE':
        return ...
