from django.urls import path
from . import views

urlpatterns = [
    # ========================================== #
    # HOMEPAGE = REGISTRATION PAGE               #
    # ========================================== #
    path('', views.register_view, name='register'),  # Homepage is registration
    
    # ========================================== #
    # HOME (for logged-in users)                 #
    # ========================================== #
    path('home/', views.home, name='home'),         # Actual homepage after login
    
    # ========================================== #
    # CAR LISTING & DETAILS                      #
    # ========================================== #
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    
    # ========================================== #
    # SELL CAR                                   #
    # ========================================== #
    path('sell-car/', views.sell_car, name='sell_car'),
    
    # ========================================== #
    # EDIT CAR                                   #
    # ========================================== #
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    
    # ========================================== #
    # DELETE CAR IMAGE (AJAX)                    #
    # ========================================== #
    path('cars/image/<int:image_id>/delete/', views.delete_car_image, name='delete_car_image'),
    
    # ========================================== #
    # CONTACT SELLER                             #
    # ========================================== #
    path('cars/<int:car_id>/contact/', views.contact_seller, name='contact_seller'),
    
    # ========================================== #
    # TEST DRIVE                                 #
    # ========================================== #
    path('cars/<int:car_id>/test-drive/', views.test_drive, name='test_drive'),
    
    # ========================================== #
    # SAVE CAR (Wishlist)                        #
    # ========================================== #
    path('cars/<int:car_id>/save/', views.save_car, name='save_car'),
    
    # ========================================== #
    # SAVED CARS PAGE                            #
    # ========================================== #
    path('saved-cars/', views.saved_cars, name='saved_cars'),
    
    # ========================================== #
    # DASHBOARD                                  #
    # ========================================== #
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ========================================== #
    # PROFILE                                    #
    # ========================================== #
    path('profile/', views.profile_view, name='profile'),
    
    # ========================================== #
    # AUTHENTICATION                             #
    # ========================================== #
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),  # Also accessible here
    path('logout/', views.logout_view, name='logout'),
        path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
        path('cars/<int:car_id>/save/', views.save_car, name='save_car'),

]
