from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from admin_side.models import Category
from django.http import HttpResponse
from admin_side.models import Book
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    return render(request,'user/base.html')
def book_list(request):
    # Get the list of books from the database
    books = Book.objects.all()

    # Pass the list of books to the template
    return render(request, 'user/booklist.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'user/bookdetail.html', {'book': book})