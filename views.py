from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from .form import *
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

def home(request):
    trendings=Product.objects.filter(trending=1)
    print("this is trending product",trendings)


    return render(request,"index.html",{"trendings":trendings})
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   

 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    print("this is cart",cart)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

    # ]else:
    #     return JsonResponse({'status':'Invalid Access'},status=200)


def logout_page(req):
    if req.user.is_authenticated:
        logout(req)
        messages.success(req,"Logged out Succefully")
    return redirect('/')

def login_page(req):
    if req.user.is_authenticated:
        return redirect('/')
    else:
        if req.method=="POST":
            name=req.POST.get('name')
            pwd=req.POST.get('pwd')
            user=authenticate(req,username=name,password=pwd)

            if user is not None:
                login(req,user)
                messages.success(req,"Login Successfully")
                return redirect('/')

            else:
                messages.error(req,"Invalid Username or Password")
                return redirect('/login')

        return render(req,"login.html")

# def register(request):
#     form=CustomUserForm()
#     if request.method=='POST':
#         form=CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Registration Success")
#             return redirect("login")
            
#     return render(request,"register.html",{"form":form})


def register(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            # Check if the is_superuser checkbox is checked
            if form.cleaned_data['is_superuser']:
                user.is_superuser = True

                # Check if staff_status checkbox is checked for superuser
                if form.cleaned_data['staff_status']:
                    user.is_staff = True

            user.save()

            # Customize messages and redirection based on user role
            if user.is_superuser:
                messages.success(request, "Superuser Registration Success")
                # Redirect to a different URL or render a specific template for superusers
                return redirect("login")
            else:
                messages.success(request, "Normal User Registration Success")
                # Redirect to a different URL or render a specific template for normal users
                return redirect("login")

    return render(request, "register.html", {"form": form})


def collections(request):
    category=Category.objects.filter(status=0)
    print("this is category",category)
    return render(request,"collections.html",{"category":category})


def collections_view(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        print("this is product",products)
        return render(request,"collections_view.html",{"products":products,"name":name})
    
    else:
        messages.warning(request,"Category Does Not Exist")


def product_details(req,cname,pname):
    print("huhuhhu")
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            print("if cond")
            products=Product.objects.filter(name=pname,status=0).first()
            return render(req,"product_details.html",{"products":products})
        
        else:
            messages.error(req,"No Such Product Found")
            return redirect('collections')
    else:
        messages.error(req,"No Such Category Found")
        return redirect('collections')
