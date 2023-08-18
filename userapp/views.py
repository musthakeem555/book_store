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
from .models import Cart, CartItem ,Order,Address,OrderItem
from admin_side.models import Book


# Create your views here.

def index(request):
    return redirect('booklist')

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

@login_required
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
    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        
        

            # Handle the rest of the logic for placing the order and redirect to the confirmation page
            # (You will need to implement this part based on your requirements)

        return redirect('payment', address_id=address_id)  # Pass the selected_address_id to the order confirmation view

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
def payment(request,address_id):
    # Assuming you have the necessary logic to retrieve the user's cart items and calculate the total price
    if request.method == 'GET':
        cart=Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum( item.book.price * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'address_id' : address_id
        }

        return render(request, 'user/payment.html', context)

    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        address_id = request.POST.get('address_id')

        if address_id:
            address = Address.objects.get(id=address_id)
            payment_method = "Cash on Delivery"
            total_price = sum( item.book.price * item.quantity for item in cart_items)

            # Create an order
            order = Order.objects.create(
                user=user,
                address=address,
                payment_method=payment_method,
                total_amount=total_price
            )
            print(order.id)
            # Create order items from cart items and deduct stock quantities
            for cart_item in cart_items:
                book = cart_item.book
                ordered_quantity = cart_item.quantity
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=ordered_quantity
                )
                book.stock -= ordered_quantity
                book.save()
                cart_item.delete()

            # Clear the cart
            # cart.items.all().delete()

            # Redirect to order confirmation or success page
            return redirect('order_confirmation',order_id=order.id)
        

def order_confirmation(request,order_id):
    # Get the order ID from the request or session

    # Retrieve the order details, including order items
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order_id)
    print(order_items)
    print(order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'user/confirmation.html', context)
@login_required
def user_profile(request):
    user = request.user  # Assuming the user is authenticated
    orders = Order.objects.filter(user=user).order_by('-order_date')
    
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'user/user_profile.html', context)

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Delete the order
    order.delete()

    # After cancellation, redirect the user back to the profile page
    return redirect('user_profile')


def my_orders(request):
    user = request.user
    order_items = OrderItem.objects.filter(order__user=user).order_by('-order__order_date')

    context = {
        'order_items': order_items
    }

    return render(request, 'user/my_orders.html', context)



        





 