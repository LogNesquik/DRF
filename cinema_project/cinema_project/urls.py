from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from films import views

router = DefaultRouter()
router.register(
    "filmes", views.FilmViewSet
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/films/', views.film_list_api_view), # GET -> list, POST -> create
    path('api/v1/films/<int:id>/', views.film_detail_api_view),
    path('api/v2/', include(router.urls)), # GET ->item, PUT->update,DELETETE->destroy
    path('api/v1/users/', include("users.urls"))
]

