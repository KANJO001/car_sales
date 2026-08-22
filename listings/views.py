

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import models
from .models import Car, CarImage, SavedCar
from .forms import CarForm, CarEditForm, UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from .filters import CarFilter
from .utils import send_email


# ========================================== #
# HOMEPAGE                                   #
# ========================================== #
@login_required
def home(request):
    featured_cars = Car.objects.filter(is_featured=True, is_available=True)[:6]
    latest_cars = Car.objects.filter(is_available=True).order_by('-created_at')[:6]
    return render(request, 'listings/home.html', {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
    })


# ========================================== #
# CAR LISTING WITH SEARCH & FILTER           #
# ========================================== #
@login_required
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    car_filter = CarFilter(request.GET, queryset=cars)
    filtered_cars = car_filter.qs
    
    sort_by = request.GET.get('sort', '-created_at')
    allowed_sorts = ['price', '-price', 'year', '-year', 'mileage', '-mileage', '-created_at', 'created_at']
    if sort_by in allowed_sorts:
        filtered_cars = filtered_cars.order_by(sort_by)
    else:
        filtered_cars = filtered_cars.order_by('-created_at')
    
    paginator = Paginator(filtered_cars, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cars': page_obj,
        'filter': car_filter,
    }
    return render(request, 'listings/car_list.html', context)


# ========================================== #
# CAR DETAIL                                 #
# ========================================== #
@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    return render(request, 'listings/car_detail.html', {'car': car})


# ========================================== #
# SELL CAR                                   #
# ========================================== #
@login_required
def sell_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.is_available = True
            car.save()
            
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                if i < 10:
                    CarImage.objects.create(car=car, image=image, order=i)
            
            messages.success(request, f'✅ Your {car.make} {car.model} has been listed successfully!')
            return redirect('car_detail', car_id=car.id)
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = CarForm()
    
    return render(request, 'listings/sell_car.html', {'form': form})


# ========================================== #
# EDIT CAR                                   #
# ========================================== #
@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    existing_images = car.images.all()
    
    if request.method == 'POST':
        form = CarEditForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            
            images = request.FILES.getlist('images')
            current_count = car.images.count()
            for i, image in enumerate(images):
                if current_count + i < 10:
                    CarImage.objects.create(car=car, image=image, order=current_count + i)
            
            messages.success(request, '✅ Car updated successfully!')
            return redirect('car_detail', car_id=car.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CarEditForm(instance=car)
    
    return render(request, 'listings/edit_car.html', {
        'form': form,
        'car': car,
        'existing_images': existing_images
    })


# ========================================== #
# DELETE CAR IMAGE (AJAX)                    #
# ========================================== #
@login_required
def delete_car_image(request, image_id):
    if request.method == 'DELETE':
        image = get_object_or_404(CarImage, id=image_id)
        if image.car.seller == request.user:
            image.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# ========================================== #
# CONTACT SELLER                             #
# ========================================== #
@login_required
def contact_seller(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')
        
        if not name or not email or not message_text:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'listings/contact_seller.html', {'car': car})
        
        # Send email to seller
        context = {
            'seller': car.seller,
            'car': car,
            'buyer_name': name,
            'buyer_email': email,
            'phone': phone,
            'message_text': message_text,
            'detail_url': request.build_absolute_uri(f'/cars/{car.id}/'),
        }
        send_email(
            subject=f'New message about your {car.make} {car.model}',
            template_name='emails/contact_seller.html',
            context=context,
            recipient_list=[car.seller.email]
        )
        
        messages.success(request, f'✅ Your message has been sent to {car.seller.username}!')
        return redirect('car_detail', car_id=car.id)
    
    return render(request, 'listings/contact_seller.html', {'car': car})


# ========================================== #
# TEST DRIVE                                 #
# ========================================== #
@login_required
def test_drive(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        message_text = request.POST.get('message')
        
        if not name or not email or not preferred_date or not preferred_time:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'listings/test_drive.html', {'car': car})
        
        # Send email to seller
        context = {
            'seller': car.seller,
            'car': car,
            'buyer_name': name,
            'buyer_email': email,
            'phone': phone,
            'preferred_date': preferred_date,
            'preferred_time': preferred_time,
            'message_text': message_text,
            'detail_url': request.build_absolute_uri(f'/cars/{car.id}/'),
        }
        send_email(
            subject=f'Test drive request for your {car.make} {car.model}',
            template_name='emails/test_drive.html',
            context=context,
            recipient_list=[car.seller.email]
        )
        
        messages.success(request, f'✅ Your test drive request for {car.make} {car.model} has been sent to {car.seller.username}!')
        return redirect('car_detail', car_id=car.id)
    
    return render(request, 'listings/test_drive.html', {'car': car})


# ========================================== #
# SAVE / UNSAVE CAR (Wishlist)               #
# ========================================== #
@login_required
def save_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    saved = SavedCar.objects.filter(user=request.user, car=car).first()
    
    if saved:
        saved.delete()
        saved = False
    else:
        SavedCar.objects.create(user=request.user, car=car)
        saved = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'saved': saved,
            'message': f'{car.make} {car.model} {"saved" if saved else "removed"} from wishlist'
        })
    
    return redirect('car_detail', car_id=car.id)


# ========================================== #
# SAVED CARS (Wishlist Page) - FIXED!       #
# ========================================== #
@login_required
def saved_cars(request):
    saved_cars = SavedCar.objects.filter(user=request.user).select_related('car')
    return render(request, 'listings/saved_cars.html', {'saved_cars': saved_cars})


# ========================================== #
# DASHBOARD                                  #
# ========================================== #
@login_required
def dashboard(request):
    user_cars = Car.objects.filter(seller=request.user).order_by('-created_at')
    saved_cars = SavedCar.objects.filter(user=request.user).select_related('car')
    
    context = {
        'user_cars': user_cars,
        'saved_cars': saved_cars,
    }
    return render(request, 'listings/dashboard.html', context)


# ========================================== #
# PROFILE (Edit Profile)                     #
# ========================================== #
@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'listings/profile.html', context)


# ========================================== #
# AUTHENTICATION                             #
# ========================================== #
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Welcome back {user.username}!')
            return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password. Please try again.')
    
    return render(request, 'listings/login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'✅ Welcome {user.username}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'listings/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, '✅ You have been logged out successfully.')
        return redirect('home')
    return render(request, 'listings/logout.html')
