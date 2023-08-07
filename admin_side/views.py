from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category
from django.http import HttpResponse
from .models import Book
from django.shortcuts import get_object_or_404

def admhome(request):
    return render(request,'admin/admbase.html')

def userlist(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    k = user_details.objects.exclude(is_superuser=True).order_by("id")
    return render(request, "admin/userlist.html", {"s": k})
    
    
# Create your views here.
def blockuser(request,id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    user=user_details.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect(userlist)

def unblockuser(request,id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    user=user_details.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect(userlist)

import re
def add_category(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    if request.method == 'GET':
        return render(request,'admin/addcategory.html')
    if request.method == 'POST':
        category_name=request.POST.get('category_name')
        
        
        if Category.objects.filter(name__icontains=category_name):
            messages.info(request,"Category Exist")
            return redirect('addcategory')

        cat=Category.objects.create(name=category_name)
        cat.save()
        return redirect ('addcategory')
    
def categorylist(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    # if request.user.is_superuser:
    Categories=Category.objects.all()
    return render(request,'admin/categorylist.html',{'category':Categories})
    
def editcategory(request,id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    if request.method=='POST':
        name=request.POST.get('name')
        cat=Category.objects.get(id=id)
        cat.name=name
        cat.save()
        return redirect(categorylist)
    data=Category.objects.get(id=id) 
    return render(request,'admin/editcategory.html',{'d':data})   
        
        
def deletecategory(request,id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('categorylist')


def addbook(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        featured = request.POST.get('featured')

        # Check if a book with the same title already exists
        if Book.objects.filter(title=title).exists():
            return render(request, 'admin/addbook.html', {'categories': Category.objects.all(), 'error_message': 'A book with this title already exists.'})

        # Create and save the book instance
        book = Book(title=title, author=author, description=description, price=price, category_id=category_id, cover_image=cover_image, stock=stock, featured=featured)
        book.save()

        return redirect('addbook')  # Replace 'addbook' with the URL name for the book add page

    # If it's a GET request, render the form
    else:
        categories = Category.objects.all()
        return render(request, 'admin/addbook.html', {'categories': categories})


def admbooklist(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    books = Book.objects.all()
    return render(request, 'admin/admbooklist.html', {'books': books})    



def deletebook(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admlogin')
    
    # Get the book object to delete
    book = get_object_or_404(Book, id=id)
    # Delete the book
    book.delete()
    # Return a JSON response indicating success
    return redirect('admbooklist')

def editbook(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        featured = request.POST.get('featured')  # Get the checkbox value as string

        # Convert the string value of 'featured' to boolean
        featured = featured.lower() == 'true'

        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.category_id = category_id
        if cover_image:
            book.cover_image = cover_image
        book.stock = stock
        book.featured = featured  # Assign the boolean value to the 'featured' field
        book.save()

        return redirect('admbooklist')

    else:
        categories = Category.objects.all()
        return render(request, 'admin/editbook.html', {'book': book, 'categories': categories})




    
    





    
    
        