from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Страница администратора


    # Аутентификация
    path('register/', views.register_view, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),  # Вход
    path('logout/', views.logout_view, name='logout'),  # Выход

    path('profile/', views.profile_view, name='profile'), # Личный кабинет
    path('cart/', views.view_cart, name='view_cart'), # Просмотр корзины
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'), # Добавление книги в корзину
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), # Удаление из корзины
    path('order/place/', views.place_order, name='place_order'), # Оформление заказа
    path('orders/', views.orders_view, name='orders'), # Страница со списком заказов

    # Книги
    path('', views.book_list, name='book_list'),  # Список книг
    path('book/create/', views.book_create, name='book_create'),  # Создание книги
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),  # Редактирование книги
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),  # Удаление книги
]
