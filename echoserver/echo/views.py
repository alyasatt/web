from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 5)  # 5 книг на страницу
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    return render(request, 'book_list.html', {'books': books_page})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

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

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})
