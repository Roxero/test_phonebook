from django.urls import path, include
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.query_router, name = 'query_router'),
    path('DELETE=<int:person_id>', views.delete_person),
    path('<int:person_id>/', views.person_card, name = 'person_card'),
]
