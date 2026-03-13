from rest_framework import serializers
from django.utils import timezone
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'id name'.split()

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio'.split()


class FilmDetailSerializers(serializers.ModelSerializer):
    class Meta():
        model = Film
        fields = '__all__'


class FilmListSerializers(serializers.ModelSerializer):
    director = DirectorSerializer()
    # genres = GenreSerializer(many=True) 
    genres = serializers.SerializerMethodField()


    class Meta():
        model = Film
        fields = 'director genres id title ratting is_hit reviews'.split()
        depth = 1

    def get_genres(self, film):
        return film.genre_names()
    

class FilmValidateSerializers(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=3)
    text = serializers.CharField(required=False)
    realease_date = serializers.IntegerField(min_value=1900, max_value=timezone.now().year + 10)
    ratting = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField()
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exsist!')
        return director_id

    def validate_genres(self, genres):
        genres = list(set(genres))
        genres_from_db = Genre.objects.filter(id__in=genres)
        if len(genres) != len(genres_from_db):
            raise ValidationError("Genre does not exsist")
        return genres

    # one sposob
    # def validate(self, attrs):
    #     director_id = attrs.get('director_id')
    #     try:
    #         Director.objects.get(id=director_id)
    #     except Director.DoesNotExist:
    #         raise ValidationError('Director does not exsist!')
    #     return attrs