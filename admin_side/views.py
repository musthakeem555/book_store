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

def dashboard(request):
    # Replace the following with your actual data retrieval logic
    monthly_sales = [1000, 1500, 2000, 1800, 2200, 2500, 2800, 3000]
    yearly_sales = [12000, 14500, 17500, 19800, 22000]

    monthly_sales_total = sum(monthly_sales)
    yearly_sales_total = sum(yearly_sales)
    last_month_total = monthly_sales[-2] if len(monthly_sales) >= 2 else 0
    last_year_total = yearly_sales[-2] if len(yearly_sales) >= 2 else 0

    if last_month_total > 0:
        monthly_change_percentage = ((monthly_sales[-1] - last_month_total) / last_month_total) * 100
    else:
        monthly_change_percentage = 0

    if last_year_total > 0:
        yearly_change_percentage = ((yearly_sales[-1] - last_year_total) / last_year_total) * 100
    else:
        yearly_change_percentage = 0

    context = {
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
        'monthly_sales_total': monthly_sales_total,
        'yearly_sales_total': yearly_sales_total,
        'monthly_change_percentage': monthly_change_percentage,
        'yearly_change_percentage': yearly_change_percentage,
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

    # Generate sample order data for the specified date range
    orders = []
    for order_id in range(1, 30):  # Adding an order_id field
        order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        book = random.choice(list(books_and_prices.keys()))  # Choose a book title randomly
        quantity = random.randint(1, 10)
        price = books_and_prices[book]  # Retrieve the price for the chosen book
        discount = random.choice([0, 10, 20])  # Adding a discount field
        total = quantity * price * (1 - discount / 100)  # Calculate total after applying discount
        orders.append({
            'order_id': order_id,
            'order_date': order_date,
            'book': book,
            'quantity': quantity,
            'price': price,
            'discount': discount,
            'total': int(total),  # Convert total to an integer to remove decimal values
        })

    # Sort orders by order date
    orders.sort(key=lambda x: x['order_date'])

    context = {
        'orders': orders,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'admin/sales_report.html', context)




  

    




    
    





    
    
        