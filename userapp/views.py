from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from admin_side.models import Category
from django.http import HttpResponse
from admin_side.models import Book
from django.shortcuts import get_object_or_404
from .models import Address
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Book, CartItem
from .models import Cart, CartItem, Book

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

def add_address(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        # Perform any additional validation if needed

        # Save the data to the Address model
        address = Address(user=request.user, street=street, city=city, state=state, postal_code=postal_code)
        address.save()

        # Redirect to a success page or any other view
        return redirect('address_list')  # Replace 'address_list' with the URL name for the address list page

    return render(request, 'user/addaddress.html')

def address_list(request):
    # Assuming you have a way to get the current user, you can retrieve their addresses like this:
    user = request.user
    addresses = Address.objects.filter(user=user)

    return render(request, 'user/address_list.html', {'addresses': addresses})


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        address.street = street
        address.city = city
        address.state = state
        address.postal_code = postal_code
        address.save()
        
        return redirect('address_list')

    return render(request, 'user/edit_address.html', {'address': address})

def delete_address(request, address_id):
   
    
    # Get the book object to delete
    address= Address.objects.get(id=address_id)
    # Delete the book
    address.delete()
    # Return a JSON response indicating success
    return redirect('address_list')



@login_required



def add_to_cart(request, book_id):
    # Get the Book object based on the book_id or return a 404 page if not found.
    book = get_object_or_404(Book, pk=book_id)

    # Get the Cart object associated with the current user or create a new one if it doesn't exist.
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the selected Book is already in the user's cart.
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

    # If the item already exists in the cart, increase the quantity by 1.
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Redirect the user to a page indicating the item has been added to the cart.
    # Replace "cart_view" with the name of the view that displays the cart or the desired URL.
    return render(request, 'user/bookdetail.html', {'book': book})

def cart_view(request):
    # Get the CartItem objects related to the current user's cart
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Pass the cart_items to the template for display
    return render(request, 'user/cart.html', {'cart_items': cart_items})

def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity = max(cart_item.quantity - 1, 1)

        cart_item.save()
    
    return redirect('cart')

def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    if request.method == 'POST':
        cart_item.delete()

    return redirect('cart')

