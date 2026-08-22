from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ========================================== #
# CAR MODEL                                  #
# ========================================== #
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField(help_text="Mileage in km")

    fuel_type = models.CharField(max_length=20, choices=[
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('cng', 'CNG'),
    ], default='petrol')

    transmission = models.CharField(max_length=20, choices=[
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
        ('dsg', 'DSG'),
    ], default='manual')

    body_type = models.CharField(max_length=20, choices=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('hatchback', 'Hatchback'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('luxury', 'Luxury'),
        ('electric', 'Electric'),
    ], default='sedan')

    description = models.TextField()
    # Removed 'image' field - now using CarImage model for multiple images

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    class Meta:
        ordering = ['-created_at']


# ========================================== #
# CAR IMAGE MODEL (Multiple Images)          #
# ========================================== #
class CarImage(models.Model):
    """
    Model for multiple images per car listing.
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    caption = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"


# ========================================== #
# PROFILE MODEL                              #
# ========================================== #
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ========================================== #
# SAVED CAR MODEL (Wishlist)                 #
# ========================================== #
class SavedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_cars')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} saved {self.car}"


# ========================================== #
# SIGNALS                                    #
# ========================================== #
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()