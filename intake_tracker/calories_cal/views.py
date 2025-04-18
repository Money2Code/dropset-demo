from django.shortcuts import render, redirect
from .models import CaloriesIntake
from .forms import CalorieIntakeForm
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import DietPlanForm
from .models import DietPlan,Contact
from .ai_utils import generate_diet_workout_plan ,generate_updated_meal_plan,calculate_diet_plan
import openai

def log_calorie_intake(request):
    today = timezone.now().date()
    calorie_intake = CaloriesIntake.objects.first()  

    
    print(calorie_intake)

    # print(calorie_intake ,calorie_intake.protein)
    
    if request.method == "POST":
        form = CalorieIntakeForm(request.POST, instance=calorie_intake)
        if form.is_valid():  # Ensure form validation
            form.save()
            return redirect('calories_progress')
        else:
            print(form.errors)  # Print errors if form is invalid (for debugging)
    else:
        form = CalorieIntakeForm(instance=calorie_intake)

    return render(request, 'calorie_intake.html', {'form': form})


def calories_progress(request):
    today = timezone.now().date()
    print(today)
    calorie_intake = CaloriesIntake.objects.first()
    print("-----------",calorie_intake.protein)
    
    if calorie_intake:
        protien_percentage = (calorie_intake.protein / calorie_intake.protein_goal) * 100
        percentage_rounded = round(protien_percentage, 2)
        print(protien_percentage)
        carbs_percentage = (calorie_intake.carbs/ calorie_intake.carbs_goal) * 100
        fat_percentage = (calorie_intake.fats / calorie_intake.fats_goal) * 100
        fibers_percentage = (calorie_intake.fibers / calorie_intake.fibers_goal) * 100
    else:
        percentage = 0

    return render(request, 'calories_progress.html', 
                  {'protien_percentage': percentage_rounded,
                   'carbs_percentage':carbs_percentage,
                   'fat_percentage':fat_percentage,
                   'fibers_percentage':fibers_percentage,
                   'calorie_intake': calorie_intake})


def index(request):
    return render(request, 'index.html')



def signup(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
      
        if len(username)>10 or len(username)<10:
            messages.info(request,"Phone Number Must be 10 Digits")
            return redirect('/signup')

        if pass1!=pass2:
            messages.info(request,"Password is not Matching")
            return redirect('/signup')
       
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Phone Number is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/handlelogin')
        
        
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        password=request.POST.get('pass1')
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successful")
            return redirect('/index')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/handlelogin')
        
    return render(request, 'handlelogin.html')



def handlelogout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('/index')



# views.py


from django.shortcuts import redirect

def choosed_goal(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        print("-------- this is the choose goal",goal)
        # Store the goal in the session or pass it directly to the next view
        request.session['goal'] = goal  # Using session to carry the goal across views
        return redirect('diet_plan_view')  # Redirect to the diet plan form view
    else:
        return redirect('index')  # Redirect to home or another page if accessed via GET

import openai  # Assuming Gemini API is accessible via OpenAI-like interface
import json



def diet_plan_view(request):
    goal = request.session['goal']
    print(goal) # Retrieve the goal from session
    if not goal:
        # If no goal is found, handle it (redirect or show an error)
        return redirect('index')  
    if request.method == 'POST':
        print(request.POST)
        print("----------the goal --------",goal)
        print("in the form ")
        form = DietPlanForm(request.POST)
        print("-----------------------")
        if form.is_valid():
            print("-------------------- the form is valid")
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            meal = form.cleaned_data['meal_choice']
            activity_level = form.cleaned_data['activity_level']

            # Calculate diet details
            calories, proteins, carbs, fats, fibers, water ,ai_diet_text= calculate_diet_plan(
 
                weight, height, age, gender,activity_level,goal
            )
            print("------------------------",print(calories))
            # Save to the database
            diet_plan = form.save(commit=False)
            diet_plan.user = request.user
            diet_plan.calories = calories
            diet_plan.proteins = proteins
            diet_plan.carbs = carbs
            diet_plan.fats = fats
            diet_plan.fibers = fibers
            diet_plan.water = water/1000
            diet_plan.save()
            

            ai_generated_plan ,meal_descriptions  = generate_diet_workout_plan(
                weight=weight,
                height=height,
                age=age,
                gender=gender,
                meal=meal,
                activity_level=activity_level,
                goal=goal 
            )
            # print("GOAL ", goal)
            # print(ai_generated_plan)
            print("------------------",meal_descriptions)

            # meal_images = []
            # for meal_desc in meal_descriptions:
            #     image_data = generate_image(meal_desc)
                
            #     print(image_data)
            #     meal_images.append({"description": meal_desc, "image_data": image_data})


            request.session['ai_generated_plan'] = ai_generated_plan
            # Redirect to a results page or render the result
            return render(request, 'index1.html', {
                'form': form,
                'calories': calories,
                'proteins': proteins,
                'carbs': carbs,
                'fats': fats,
                'fibers': fibers,
                'water': water/1000,
                'ai_generated_plan': ai_generated_plan,
                # 'meal_images': meal_images
            })
    else:
        form = DietPlanForm()

    return render(request, 'index1.html', {'form': form,'goal': goal})
    


def contact(request):
    if request.method == 'POST':
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        description=request.POST.get('desc')
        myquery = Contact(name=name, email=email, phone=number, description=description)
        myquery.save()

        messages.info(request,'Thanks for contacting , will get back to you')

        return redirect('/contact')


    return render(request, 'contact.html')


def download_plan(request):
    ai_generated_plan = request.session.get('ai_generated_plan')  # Retrieve from session if stored
    print()
    if not ai_generated_plan:
        return redirect('diet_plan_view')
    return render(request, 'download_plan.html', {'ai_generated_plan': ai_generated_plan,
    
        })

def update_meal_plan(request):
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type')  # e.g., "breakfast"
        custom_meal = request.POST.get('custom_meal')  # e.g., "Oatmeal with nuts"
        
        # Call your AI function to generate an updated plan
        updated_plan = generate_updated_meal_plan(meal_type, custom_meal,)
        
        print("--------------------",updated_plan)
        # Pass the updated plan back to the template
        return render(request, 'diet_plan.html', {
            'upated_ai_generated_plan': updated_plan,
        })
    
    return redirect('home')
