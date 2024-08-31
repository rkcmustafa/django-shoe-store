from django.shortcuts import render
from django.http import JsonResponse
from .models import Shoe, Favorite, Basket
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
# def shoes(request):
#     all_shoes = Shoe.objects.all()
#     favorite_shoe_ids = []
    
#     if request.user.is_authenticated:
#         favorite_shoe_ids = list(Favorite.objects.filter(user=request.user).values_list('id', flat=True))
#         print("###################################################", favorite_shoe_ids)
#     return render(request, "products.html", {"shoes": all_shoes, "ids": favorite_shoe_ids})

def shoes(request):
    all_shoes = Shoe.objects.all()
    favorite_shoe_ids = []
    
    if request.user.is_authenticated:
        favorite_shoe_ids = list(Favorite.objects.filter(user=request.user).values_list('shoe__id', flat=True))
    
    return render(request, "products.html", {"shoes": all_shoes, "ids": favorite_shoe_ids})


@login_required(login_url="login")
def favorites(request):
    if request.method == "GET":
        favorite_shoes = Favorite.objects.filter(user=request.user)
        print("###############################################",favorite_shoes)
        return render(request, "favorites.html", { "favorites": favorite_shoes})
    elif request.method == "POST":
        shoe_id = int(json.loads(request.body)["shoe_id"])
        try:
            shoe = Shoe.objects.get(id=shoe_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, shoe=shoe)
            
            if not created:
                favorite.delete()
                return JsonResponse({"message": "Shoe removed from favorites", "status": "success"})
            return JsonResponse({"message": "Shoe added to favorites.", "status": "success"})
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Shoe is not found.", "status": "error"})

@login_required(login_url="login")
def basket(request):
    if request.method == "GET":
        shoes_in_basket = Basket.objects.filter(user=request.user)

        return render(request, "basket.html", {"basket": list(shoes_in_basket)})
    
    elif request.method == "POST":
        shoe_id = int(json.loads(request.body)["shoe_id"])
        amount = int(json.loads(request.body)["amount"])
        try:
            shoe = Shoe.objects.get(id=shoe_id)
            basket_shoe, created = Basket.objects.get_or_create(user=request.user, shoe=shoe, defaults={'amount': amount})
            
            if not created:
                basket_shoe.amount += amount
            else:
                basket_shoe.amount = amount
            
            basket_shoe.save()
            return JsonResponse({"message": "Basket updated successfully.", "status": "success"})
        
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Shoe not found.", "status": "error"})
    
    elif request.method == "DELETE":
        shoe_id = int(json.loads(request.body)["shoe_id"])
        try:
            shoe = Shoe.objects.get(id=shoe_id)
            basket_shoe = Basket.objects.filter(user=request.user, shoe=shoe).first()
            
            if basket_shoe is None:
                return JsonResponse({"message": "Shoe is not in basket.", "status": "error"})
            else:
                basket_shoe.delete()
                return JsonResponse({"message": "Shoe removed from basket.", "status": "success"})
        
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Shoe not found.", "status": "error"})
    
    elif request.method == "PUT":
        shoe_id = int(json.loads(request.body)["shoe_id"])
        amount = int(json.loads(request.body)["amount"])
        
        try:
            shoe = Shoe.objects.get(id=shoe_id)
            basket_shoe = Basket.objects.filter(user=request.user, shoe=shoe).first()
            
            if basket_shoe is None:
                return JsonResponse({"message": "Shoe is not in basket.", "status": "error"})
            else:
                basket_shoe.amount = amount
                basket_shoe.save()
                return JsonResponse({"message": "Basket updated successfully.", "status": "success"})
        
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Shoe not found.", "status": "error"})


def shoe(request, slug):
    shoe = Shoe.objects.get(slug=slug)
    return render(request, "shoe.html", {'shoe': shoe})
