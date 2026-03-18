from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Director
from .serializers import FilmListSerializers, FilmDetailSerializers, FilmValidateSerializers
from rest_framework.viewsets import ModelViewSet

class FilmViewSet(ModelViewSet):
    queryset = Film.objects.prefetch_related("genres").select_related('director')

    def get_serializer_class(self):
        if self.action == 'list':
            return FilmListSerializers
        return FilmDetailSerializers

@api_view(['GET', 'POST'])
def film_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        films = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()
        data = FilmListSerializers(films, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Получаем данные из запроса
        
        serializer = FilmValidateSerializers(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        realease_date = serializer.validated_data.get('realease_date')  # Исправил опечатку
        ratting = serializer.validated_data.get('ratting')  # Исправил опечатку
        is_hit = serializer.validated_data.get('is_hit')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        
        # Создаем фильм с экземпляром Director
        film = Film.objects.create(
            title=title,
            text=text,
            realease_date=realease_date,
            ratting=ratting,
            is_hit=is_hit,
            director_id=director_id  # Передаем объект, а не ID
        )
        film.genres.set(genres)

        return Response(
            data=FilmDetailSerializers(film).data,
            status=status.HTTP_201_CREATED
        )

@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        films = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data={'error': 'film does not exsist'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializers(films).data
        return Response(data=data)
    elif request.method == 'DELETE':
        films.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        films.title = request.data.get('title')
        films.text = request.data.get('text')
        films.realease_date = request.data.get('realease_date')  # Исправил опечатку
        films.ratting = request.data.get('ratting')  # Исправил опечатку
        films.is_hit = request.data.get('is_hit')
        films.director_id = request.data.get('director')
        films.save()
        return Response(status=status.HTTP_201_CREATED)

