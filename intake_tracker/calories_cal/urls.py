from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_calorie_intake, name='log_calorie_intake'),
    path('progress/', views.calories_progress, name='calories_progress'),
    path('index/', views.index , name='index'),
    path('signup/', views.signup, name='signup'),
    path('handlelogin/', views.handlelogin, name='handlelogin'),  # Add this line to include the login URL
    path('handlelogout/', views.handlelogout, name='handlelogout'), 
    path('diet_plan_view/',views.diet_plan_view,name="diet_plan_view") ,# Add this line to include the logout URL
    path('index1/',views.diet_plan_view,name="calculate_diet_plan") ,# Add this line to include the
    path('contact',views.contact,name="contact") ,# Add this line to include the
    path('choosed_goal/', views.choosed_goal, name='choosed_goal') ,# Add this line to include the
    path('download_plan/', views.download_plan, name='download_plan'),
    path('update-meal-plan/', views.update_meal_plan, name='update_meal_plan'),

]
