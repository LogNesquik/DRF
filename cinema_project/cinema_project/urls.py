from django.contrib import admin
from django.urls import path
from films import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/films/', views.film_list_api_view), # GET -> list, POST -> create
    path('api/v1/films/<int:id>/', views.film_detail_api_view) # GET ->item, PUT->update,DELETETE->destroy
]
