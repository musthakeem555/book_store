from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,order_status
from django.http import HttpResponse
from .models import Book
from django.shortcuts import get_object_or_404
from userapp.models import OrderItem,Order
from django.utils import timezone
from .models import Coupon
import random
from datetime import date, timedelta

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
    books = Book.objects.filter(category=None)
    for book in books:
        book.featured=False
        book.save()
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
        back_image = request.FILES.get('back_image')
        stock = request.POST.get('stock')
        featured = request.POST.get('featured', False) == 'on'

        # Check if a book with the same title already exists
        if Book.objects.filter(title=title).exists():
            return render(request, 'admin/addbook.html', {'categories': Category.objects.all(), 'error_message': 'A book with this title already exists.'})

        # Create and save the book instance
        book = Book(title=title, author=author, description=description, price=price, category_id=category_id, cover_image=cover_image,back_image=back_image, stock=stock, featured=featured)
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
        back_image = request.FILES.get('back_image')

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
        if back_image:
            book.back_image = back_image
        book.stock = stock
        book.featured = featured  # Assign the boolean value to the 'featured' field
        book.save()

        return redirect('admbooklist')

    else:
        categories = Category.objects.all()
        return render(request, 'admin/editbook.html', {'book': book, 'categories': categories})
    

def order_management(request):
    # Retrieve all order items
    order_items = OrderItem.objects.all().order_by('-id')   
    # Retrieve all order statuses for the drop-down menu
    statuses = order_status.objects.all()
    if request.method == 'POST':
        # Handle form submission for changing order status
        order_item_id = request.POST.get('order_item_id')
        new_status_id = request.POST.get('new_status')
        
        if order_item_id and new_status_id:
            order_item = OrderItem.objects.get(pk=order_item_id)
            new_status = order_status.objects.get(pk=new_status_id)
            order_item.order_status = new_status
            order_item.save()

    context = {
        'order_items': order_items,
        'statuses': statuses,
    }

    return render(request, 'admin/order_management.html', context)


def coupon(request):
    coupons = Coupon.objects.all()
    
    context = {
        'coupons': coupons,
    }
    return render(request, 'admin/coupon.html', context)



def add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        description = request.POST.get('description')
        minimum_amount = int(request.POST.get('minimum_amount'))
        discount_type = request.POST.get('discount_type')
        discount = float(request.POST.get('discount'))
        valid_from_iso = request.POST.get('valid_from')
        valid_from = timezone.datetime.fromisoformat(valid_from_iso)
        
        valid_to_iso = request.POST.get('valid_to')
        valid_to = timezone.datetime.fromisoformat(valid_to_iso)
        active = bool(request.POST.get('active'))

        # Create a new coupon instance
        coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            description=description,
            minimum_amount=minimum_amount,
            discount_type=discount_type,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            active=active
        )

        return redirect('coupon')  # Replace 'coupon_management' with the URL name of the coupon management page

    return render(request, 'admin/add_coupon.html')

def edit_coupon(request, id):
    coupon = get_object_or_404(Coupon, pk=id)

    if request.method == 'POST':
        coupon.coupon_code = request.POST.get('coupon_code')
        coupon.description = request.POST.get('description')
        coupon.minimum_amount = int(request.POST.get('minimum_amount'))
        coupon.discount_type = request.POST.get('discount_type')
        coupon.discount = float(request.POST.get('discount'))
        
        valid_from_iso = request.POST.get('valid_from')
        coupon.valid_from = timezone.datetime.fromisoformat(valid_from_iso)
        
        valid_to_iso = request.POST.get('valid_to')
        coupon.valid_to = timezone.datetime.fromisoformat(valid_to_iso)
        
        coupon.active = request.POST.get('active') == 'on'
        
        coupon.save()
        return redirect('coupon')  # Redirect to the coupon management page after editing
        
    context = {
        'coupon': coupon
    }
    return render(request, 'admin/edit_coupon.html', context)


def delete_coupon(request, id):
    try:
        coupon = Coupon.objects.get(pk=id)
        coupon.delete()
        return redirect('coupon')  # Redirect to the coupon list page
    except Coupon.DoesNotExist:
        return render(request, 'admin/error.html', {'error_message': 'Coupon not found'})  # Handle error case

from django.shortcuts import render

from django.db.models import Sum,Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate

from django.db.models.functions import TruncMonth

def dashboard(request):
    # Calculate the date range for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months = 180 days

    # Query orders within the last 6 months, aggregated by month
    monthly_sales_data = (
        Order.objects
        .filter(order_date__range=(start_date, end_date))
        .annotate(month=TruncMonth('order_date'))  # Use TruncMonth to group by month
        .values('month')
        .annotate(total_sales=Sum('total_amount'))
        .order_by('month')  # Ensure the results are ordered by month
    )

    # Query order items count within the last 6 months, aggregated by month
    monthly_sales_count_data = (
        OrderItem.objects
        .filter(order__order_date__range=(start_date, end_date))
        .annotate(month=TruncMonth('order__order_date'))  # Use TruncMonth to group by month
        .values('month')
        .annotate(total_count=Count('id'))
        .order_by('month')  # Ensure the results are ordered by month
    )

    # Extract the month names and corresponding total sales amounts
    months = [entry['month'].strftime('%B %Y') for entry in monthly_sales_data]
    total_sales = [entry['total_sales'] for entry in monthly_sales_data]

    # Extract the month names and corresponding total sales counts
    counts = [entry['total_count'] for entry in monthly_sales_count_data]

    context = {
        'months': months,
        'total_sales': total_sales,
        'counts': counts,  # Add the counts data to the context
    }

    return render(request, 'admin/dashboard.html', context)





# Sample book titles
books_and_prices = {
    'Crime and Punishment': 20,
    'Dracula': 25,
    'Pride and Prejudice': 30,
    'To Kill a Mockingbird': 35,
    'The Great Gatsby': 40,
}

from datetime import date, timedelta, datetime
import random

def sales_report(request):
    # Get start_date and end_date query parameters from the URL
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    # Convert query parameter strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else date.today() - timedelta(days=365)
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else date.today()

    # Query the OrderItem model to get relevant data
    order_items = OrderItem.objects.filter(
        order__order_date__range=(start_date, end_date)
    ).select_related('order', 'book')

    context = {
        'order_items': order_items,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'admin/sales_report.html', context)




  

    




    
    





    
    
        