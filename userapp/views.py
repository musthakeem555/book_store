from django.shortcuts import render
from accounts.models import user_details
from django.shortcuts import render,redirect
from django.contrib import messages
from admin_side.models import Category
from django.http import HttpResponse
from admin_side.models import Book,order_status,Coupon
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem ,Order,Address,OrderItem
from admin_side.models import Book,Coupon
import razorpay
from django.conf import settings
from django.utils import timezone
from userapp.models import wallet
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.

def index(request):
    return redirect('booklist')

def book_list(request):
    # Get the sorting criteria from the query parameters
    categories=Category.objects.all()
    sort_criteria = request.GET.get('sort', 'default')
    category_filter = request.GET.get('category')
    # Define a dictionary to map sorting criteria to database fields
    sort_mapping = {
        'default': 'id',  # Change 'id' to the default sorting field
        'newness': '-created_at',  # Replace 'created_at' with your date field
        'price_low_to_high': 'price',
        'price_high_to_low': '-price',
    }

    # Get the corresponding database field for the selected sorting criteria
    sort_field = sort_mapping.get(sort_criteria, 'id')



    # Query the books and apply sorting
    books = Book.objects.all().order_by(sort_field)
    if category_filter:
    # Filter products by category
        books = Book.objects.filter(category=category_filter)

    context = {
        'books': books,
        'sort_criteria': sort_criteria, 
        'categories':categories
        # Pass the selected criteria to the template
    }

    return render(request, 'user/booklist.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'user/bookdetail.html', {'book': book})

def catgry_search(request,id):
    books=Book.objects.filter(Category=id)
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
        next_url = request.GET.get('next', None)
        if next_url:
            return redirect(next_url)
        else:
            return redirect('address_list')
        # Redirect to a success page or any other view
        # return redirect('address_list')  # Replace 'address_list' with the URL name for the address list page

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
        next_url = request.GET.get('next', None)
        if next_url:
            return redirect(next_url)
        else:
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
    # Create and save instances

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
                return JsonResponse({'error': "Sorry, you cannot add more of this book to the cart as it exceeds the available stock."})
        elif action == 'decrease':
            cart_item.quantity = max(cart_item.quantity - 1, 1)

        cart_item.save()
    
    data = {
        'new_quantity': cart_item.quantity,
        'new_total_price': cart_item.book.price * cart_item.quantity,
    }
    return JsonResponse(data)



def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if request.method == 'POST':
        cart_item.delete()
        return JsonResponse({'message': 'Cart item deleted successfully.'})
    
    return JsonResponse({'message': 'Invalid request.'}, status=400)



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
        if total_price<1:
            return redirect('cart')
        
        client=razorpay.Client(auth=("rzp_test_VDPQPNxYzpv9RG","qHyItpczSI5AHn5zzD3vlBbn"))
        amount=int(total_price * 100)
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'address_id' : address_id,
            'payment':payment,
            'new_total_price':total_price,
            'discount':0
            
        }
        
        print(payment)
        return render(request, 'user/payment.html', context)

    if request.method == 'POST':
        
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        address_id = request.POST.get('address_id')
        discount = request.POST.get('discount')

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

            # context=
            # Redirect to order confirmation or success page
            return redirect('order_confirmation',order_id=order.id,discount=discount)


def apply_coupon(request, address_id):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_price = sum(item.book.price * item.quantity for item in cart_items)
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, active=True,
                                        valid_from__lte=timezone.now(),
                                        valid_to__gte=timezone.now())
            
            # Check if the total price is above the minimum amount required for the coupon
            if total_price < coupon.minimum_amount:
                return render(request, 'user/payment.html', {'error_message': 'Total price is less than the minimum amount required for this coupon', 'address_id': address_id})
            
            # Calculate the discount amount based on coupon details
            if coupon.discount_type == 'amount':
                discount = coupon.discount
            elif coupon.discount_type == 'percentage':
                discount = (coupon.discount / 100) * total_price
            else:
                discount = 0
            
            # Calculate the new total price after applying the discount
            new_total_price = total_price - discount
            
            # Render the template with the new total price and discount
            return render(request, 'user/payment.html', {'total_price': total_price, 'new_total_price': new_total_price, 'discount': discount, 'address_id': address_id})
        
        except Coupon.DoesNotExist:
            # Coupon is not valid, render template with an error message
            return render(request, 'user/payment.html', {'error_message': 'Invalid coupon code', 'address_id': address_id})


        
def razor(request,address_id,new_total_price):
    # Assuming you have the necessary logic to retrieve the user's cart items and calculate the total price

        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        new_total_price=float(new_total_price)
        discount=float(discount)

        if address_id:
            address = Address.objects.get(id=address_id)
            # Create an order
            order = Order.objects.create(
                user=user,
                address=address,
                payment_method='Razor Pay',
                total_amount=new_total_price
            )
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

            # context=
            # Redirect to order confirmation or success page
            return redirect('order_confirmation',order_id=order.id,)
        

def get_coupon_details(request, coupon_code):
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        coupon_details = {
            'discount_type': coupon.discount_type,
            'discount_amount': coupon.discount,
        }
        return JsonResponse(coupon_details)
    except Coupon.DoesNotExist:
        return JsonResponse({'error': 'Coupon not found'}, status=400)


def order_confirmation(request,order_id,discount):
    # Get the order ID from the request or session

    # Retrieve the order details, including order items
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order_id)
    discount=float(discount)

    context = {
        'order': order,
        'order_items': order_items,
        'discount' :discount
    }

    return render(request, 'user/confirmation.html', context)
@login_required
def user_profile(request):
    user = request.user  # Assuming the user is authenticated
    orders = Order.objects.filter(user=user).order_by('-order_date')
    
    # Check if the user has a wallet
    
    wallet_balance = None
    walet= wallet.objects.get(user=user)
    if walet:
        wallet_balance=walet.balance
    
    print(wallet_balance)
    context = {
        'user': user,
        'orders': orders,
        'wallet_balance': wallet_balance,  # Include wallet balance in the context
    }
    return render(request, 'user/user_profile.html', context)


  # Import the Wallet model

def cancel_order(request, order_id):
    try:
        order_item = OrderItem.objects.get(id=order_id)
        if order_item.order_status.order_status == 'Order Placed' or order_item.order_status.order_status == 'Order Shipped':
            # Increase the book's stock by the quantity of the canceled order item
            book = order_item.book
            book.stock += order_item.quantity
            book.save()

            # Delete the order item
            status=order_status.objects.get(order_status='Cancelled')
            order_item.order_status = status
            print(order_item.order_status)
            order_item.save()

            messages.success(request, 'Order item canceled successfully.')
            wallet_balance = 0
            # Check if the payment method is Razor Pay
            if order_item.order.payment_method == 'Razor Pay':
                user = request.user
                # Check if the user has a wallet; create one if not
                user_wallet, created = wallet.objects.get_or_create(user=user)
                # Add the price of the canceled item to the user's wallet
                user_wallet.balance += order_item.book.price * order_item.quantity
                user_wallet.save()
                wallet_balance=user_wallet.balance

        else:
            messages.error(request, 'Cannot cancel this order item.')

    except OrderItem.DoesNotExist:
        messages.error(request, 'Order item not found.')

    return redirect('my_orders')  # Redirect to the order items page




def my_orders(request):
    user = request.user
    order_items = OrderItem.objects.filter(order__user=user).order_by('-order__order_date')

    context = {
        'order_items': order_items
    }
    return render(request, 'user/my_orders.html', context)

def search(request):
    # Get the search query from the URL's query parameters
    search_query = request.GET.get('q', '')

    # Implement your search logic here using Q objects
    search_results = Book.objects.filter(
        Q(title__icontains=search_query) |
        Q(author__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(category__name__icontains=search_query)  # If you want to search by category name
    )

    context = {
        'books': search_results,
        'search_query': search_query,
    }

    return render(request, 'user/booklist.html', context)


        





 