from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from admin_side.models import Category
from django.http import HttpResponse
from admin_side.models import Book
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Book,Order,Address,OrderItem

# Create your views here.

def index(request):
    return render(request,'user/index.html')

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


def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).order_by('pk')
    
    total_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'user/cart.html', context)



def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            if cart_item.quantity < cart_item.book.stock:
                cart_item.quantity += 1
            else:
                messages.warning(request, "Sorry, you cannot add more of this book to the cart as it exceeds the available stock.")
        elif action == 'decrease':
            cart_item.quantity = max(cart_item.quantity - 1, 1)

        cart_item.save()
    
    return redirect('cart')


def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    if request.method == 'POST':
        cart_item.delete()

    return redirect('cart')


def checkout(request):
    # Get the current user's cart items
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total price
    total_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)

    # Get the user's addresses
    addresses = Address.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'addresses': addresses,
    }

    return render(request, 'user/checkout.html', context)


@login_required
def payment(request):
    # Assuming you have the necessary logic to retrieve the user's cart items and calculate the total price
    cart=Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum( item.book.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'user/payment.html', context)



def place_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    address_id = request.session.get('selected_address_id')

    if address_id:
        address = Address.objects.get(id=address_id)
        payment_method = "Cash on Delivery"
        total_amount = cart.calculate_total_amount()

        # Create an order
        order = Order.objects.create(
            user=user,
            address=address,
            payment_method=payment_method,
            total_amount=total_amount
        )

        # Create order items from cart items and deduct stock quantities
        for cart_item in cart.items.all():
            book = cart_item.book
            ordered_quantity = cart_item.quantity
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=ordered_quantity
            )
            book.stock -= ordered_quantity
            book.save()

        # Clear the cart
        cart.items.all().delete()

        # Redirect to order confirmation or success page
        return redirect('order_confirmation')  # Replace with the appropriate URL name
    else:
        # Redirect back to the payment page with an error message
        messages.error(request, "Please select an address before placing the order.")
        return redirect('payment')  # Replace with the appropriate URL name

    return render(request, 'confirmation.html')  # Create the corresponding template




