from django.contrib import admin
from .models import Car, CarImage, Profile, SavedCar


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ('image', 'caption', 'order')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'seller', 'is_available')
    list_filter = ('make', 'year', 'is_available', 'fuel_type', 'transmission')
    search_fields = ('make', 'model', 'description')
    inlines = [CarImageInline]


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'image', 'caption', 'order', 'uploaded_at')
    list_filter = ('car',)
    search_fields = ('car__make', 'car__model', 'caption')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'updated_at')
    search_fields = ('user__username', 'phone')


@admin.register(SavedCar)
class SavedCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'car__make', 'car__model')