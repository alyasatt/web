from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Book, CartItem, Order, OrderItem
from .forms import BookForm, CustomUserRegistrationForm, LoginForm
from django.contrib.auth import update_session_auth_hash

# Проверка на администратора
def is_admin(user):
    return user.is_authenticated and user.user_role == 'admin'

# Проверка на авторизованного пользователя (любой роли)
def is_authenticated_user(user):
    return user.is_authenticated

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                user.last_login = timezone.now()
                user.save(update_fields=["last_login"])
                login(request, user)
                return redirect('book_list')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# Выход
def logout_view(request):
    logout(request)
    return redirect('book_list')

# Просмотр книг — доступен всем
def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    return render(request, 'book_list.html', {'books': books_page})

# Добавление книги — только авторизованным
@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

# Редактирование книги — только админам
@login_required
@user_passes_test(is_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'book': book})

# Удаление книги — только админам
@login_required
@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})

# Личный кабинет
@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.full_name = full_name
        user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Чтобы не выкидывало из сессии

        user.save()
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

# Корзина
@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()


    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('view_cart')

# Оформление заказа
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
        cart_items.delete()
        return redirect('orders')
    return redirect('view_cart')

# Страница заказа
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})
