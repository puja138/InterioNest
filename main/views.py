from django.shortcuts import render, get_object_or_404
from .models import Product
from . import views
from .models import ContactMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import OrderForm  # if you're using a form
from .models import Order, ContactMessage
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Make sure this is imported
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator      # admin-dashbord 
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt     #payment getway

from django.conf import settings
import razorpay



def home_view(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, 'main/about.html')


def shop_view(request):
    premium_products = Product.objects.all()[:10]
    latest_products = Product.objects.filter(is_latest=True)
    offer_products = Product.objects.filter(is_offer=True)  # ✅ Get offer products

    print("Latest Products:", latest_products)  # ✅ DEBUG line

    return render(request, 'main/shop.html', {
        'premium_products': premium_products,
        'latest_products': latest_products,
        'Offer_products': offer_products,  # ✅ passed to template
    })


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
 

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )


        messages.success(request, 'Thank you for contacting us! We will get back to you shortly.')
        return redirect('contact')  # 👈 Redirect to avoid resubmission on refresh

    return render(request, 'main/contact.html')



def order_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        otp = request.POST.get('otp')
        payment_id = request.POST.get('razorpay_payment_id')

        print("👉 Form Data:")
        print("Full Name:", full_name)
        print("Email:", email)
        print("Phone:", phone)
        print("Address:", address)
        print("Product Name:", product_name)
        print("Quantity:", quantity)
        print("OTP:", otp)
        print("Payment ID:", payment_id)


        if all([full_name, email, phone, address, product_name, quantity, otp, payment_id]):
            print("✅ All fields + Payment ID received. Saving order...")

            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                product_name=product_name,
                quantity=quantity,
                otp=otp,
                payment_id=payment_id
            )

            expected_date = (datetime.date.today() + datetime.timedelta(days=5)).strftime("%B %d, %Y")

            print("✅ Order Saved. Showing success page.")
            return render(request, 'main/order_success.html', {
                'order': order,
                'expected_date': expected_date
            })
        else:
            print("❌ Missing field! Not saving.")

    print("📄 Rendering order form page")
    return render(request, 'main/order.html')

def payment_view(request):
    if request.method == "POST":
        amount = 50000  # Amount in paise (500.00 INR)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
        context = {
            'amount': amount,
            'api_key': settings.RAZORPAY_KEY_ID,
            'order_id': payment['id']
        }
        return render(request, 'main/payment.html', context)

    return render(request, 'main/order_form.html')

def search_view(request):
    query = request.GET.get('query')
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'main/search.html', {
        'query': query,
        'results': results
    })

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})

    
def blog_view(request):
    return render(request, 'main/blog.html')

def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
@user_passes_test(is_admin)

def admin_dashboard(request):
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    user_count = ContactMessage.objects.count()  # Using contact form as customer
    recent_orders = Order.objects.order_by('-order_date')[:5]
    recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]

    return render(request, 'main/admin_dashboard.html', {
        'product_count': product_count,
        'order_count': order_count,
        'user_count': user_count,
        'recent_orders': recent_orders,
        'recent_contacts': recent_contacts,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')  # Change if your dashboard URL name is different
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Product.objects.create(name=name, price=price, description=description, image=image)
        return redirect('product_list')

    return render(request, 'main/add_product.html')


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_dashboard')


# ✅ Customer List View
@login_required
def customer_list(request):
    customers = User.objects.all()
    return render(request, 'main/customer_list.html', {'customers': customers})

# ✅ Export Orders to CSV
@login_required
def export_orders(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Product', 'Quantity', 'Date'])

    for order in Order.objects.all():
        writer.writerow([order.full_name, order.product_name, order.quantity, order.order_date])

    return response

# ✅ Search Orders by Customer/Product Name
@login_required
def search_orders(request):
    query = request.GET.get('query')
    orders = Order.objects.all()
    if query:
        orders = orders.filter(full_name__icontains=query) | orders.filter(product_name__icontains=query)

    return render(request, 'main/search_orders.html', {'orders': orders, 'query': query})

def join_now_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Ya kisi aur page par
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'main/join_now.html')


