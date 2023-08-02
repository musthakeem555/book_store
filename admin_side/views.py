from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category
from django.http import HttpResponse
from .models import Book
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

def admhome(request):
    return render(request,'admin/admbase.html')
@login_required
def userlist(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        k = user_details.objects.exclude(is_superuser=True).order_by("id")
        return render(request, "admin/userlist.html", {"s": k})
    else:
        return render(request, "adminside/adminlogin.html")
# Create your views here.
def blockuser(request,id):
    user=user_details.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect(userlist)

def unblockuser(request,id):
    user=user_details.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect(userlist)

import re
def add_category(request):
    if request.method == 'GET':
        return render(request,'admin/addcategory.html')
    if request.method == 'POST':
        category_name=request.POST.get('category_name')
        
        
        if Category.objects.filter(name__icontains=category_name):
            messages.info(request,"Category Exist")
            return redirect('addcategory')

        # elif Category.objects.filter(category_name__icontains=category_name1):
        #     messages.info(request,'Category is  exist')
        #     return redirect('categorylist')
        cat=Category.objects.create(name=category_name)
        cat.save()
        return redirect ('addcategory')
@login_required   
def categorylist(request):
    # if request.user.is_superuser:
        Categories=Category.objects.all()
        return render(request,'admin/categorylist.html',{'category':Categories})
    
def editcategory(request,id):
    if request.method=='POST':
        name=request.POST.get('name')
        cat=Category.objects.get(id=id)
        cat.name=name
        cat.save()
        return redirect(categorylist)
    data=Category.objects.get(id=id) 
    return render(request,'admin/editcategory.html',{'d':data})   
        
        
def deletecategory(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('categorylist')


def addbook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')

        # Check if a book with the same title already exists
        if Book.objects.filter(title=title).exists():
            return render(request, 'admin/addbook.html', {'categories': Category.objects.all(), 'error_message': 'A book with this title already exists.'})

        # Create and save the book instance
        book = Book(title=title, author=author, description=description, price=price, category_id=category_id, cover_image=cover_image)
        book.save()

        return redirect('addbook')  # Replace 'addbook' with the URL name for the book add page

    # If it's a GET request, render the form
    else:
        categories = Category.objects.all()
        return render(request, 'admin/addbook.html', {'categories': categories})
@login_required
def admbooklist(request):
    books = Book.objects.all()
    return render(request, 'admin/admbooklist.html', {'books': books})    



def deletebook(request, id):
    
        # Get the book object to delete
        book = get_object_or_404(Book, id=id)
        # Delete the book
        book.delete()
        # Return a JSON response indicating success
        return redirect('admbooklist')

    # This view function should not be accessed directly via GET request
def editbook(request, id):
    try:
        book = Book.objects.get(id=id) 
    except Book.DoesNotExist:
        return redirect('booklist')  # Redirect to book list if the book with the specified ID does not exist

    if request.method == 'POST':
        # Get the updated data from the form
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')

        # Update the book instance with the new data
        category = Category.objects.get(id=category_id)
        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.category = category
        if cover_image:
            book.cover_image = cover_image

        book.save()  # Save the updated book instance

        return redirect('admbooklist')  # Redirect to book list page after successful update

    # If it's a GET request, render the edit form
    else:
        categories = Category.objects.all()
        return render(request, 'admin/editbook.html', {'book': book, 'categories': categories})    



    
    





    
    
        