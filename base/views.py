from itertools import product
from tkinter.messagebox import RETRY
from turtle import title
from urllib import request, response
from django.shortcuts import render, redirect
import requests
from pathlib import Path
import json
import string
import random
from . import models

BASE_DIR = Path(__file__).resolve().parent.parent

def get_color(strtype):
    oldl = strtype.split("'")
    return oldl[3]

def l_form(strt):
    tmp = ""
    nl = []
    incorrect = ["'", "[", " ", "]", ","]
    for x in strt:
        if x not in incorrect:
            tmp += x
        if x =="," or x =="]":
            nl.append(tmp)
            tmp = ""
    return nl

def get_items_l():
    with open(BASE_DIR / "static/dist/items/items.json", "r") as f:
        items = json.load(f)
        
    item_keys = items.keys()
    final = []
    for x in item_keys:
        final.append({
            "id": x,
            "product_id": items[x]["product_id"],
            "image": items[x]["image"],
            "title": items[x]["title"],
            "sizes": items[x]["sizes"],
            "colors": items[x]["colors"]
        })
    return final
    
    
# ISSUE IS HERE \/
def get_items(limit=1000):
    items = models.Product.objects.all()
    final = []
    for x in items.iterator():
        final.append(
            {
            "id": x.product_id,
            "product_id": x.product_id,
            "image": x.image,
            "title": x.title,
            "sizes": l_form(x.sizes),
            "colors": get_color(x.colors),
            "price": x.price
            }
        )
    return final
    
def get_items_d():
    with open(BASE_DIR / "static/dist/items/items.json", "r") as f:
        items = json.load(f)
        
    item_keys = items.keys()
    final = {}
    for x in item_keys:
        final[x] = {
            "id": x,
            "product_id": items[x]["product_id"],
            "image": items[x]["image"],
            "title": items[x]["title"],
            "sizes": items[x]["sizes"],
            "colors": items[x]["colors"]
        }

item_list = get_items()


def load_models_to_db():
    items = item_list
    for x in items:
        models.Product.objects.create(
            product_id=x["id"],
            image=x["image"],
            title=x["title"],
            sizes=x["sizes"],
            colors=x["colors"],
            price=39.99
        )
    
def get_sizes(strtype):
    alphabet = string.ascii_lowercase
    oldl = strtype.split(",")
    nl = []
    tmp = ""
    for x in oldl:
        for i in x:
            if i in alphabet:
                tmp += i
                
        nl.append(tmp)
        tmp = ""
        
    return nl

def get_user_id(request, response):
    alphabet = string.ascii_lowercase
    set_cook_usr = random.choices(alphabet, k=10)
    try:
        user_id = request.COOKIES["user_id"]
    except KeyError:
        response.set_cookies("user_id", set_cook_usr)
        user_id = request.COOKIES["user_id"]

    return user_id, response

def get_cart_count(request):
    user_id = request.COOKIES["user_id"]
    items = models.UserItem.objects.filter(user=user_id)
    cart_count = 0
    for x in items:
        cart_count += x.quantity
    return cart_count
    

def add_to_cart(request, item_id, size):
    user_id = request.COOKIES["user_id"]
    item = models.Product.objects.get(product_id=item_id)
    if models.UserItem.objects.filter(item_id=item_id, user=user_id, sizes=size):
        newquant = models.UserItem.objects.filter(item_id=item_id).get(user=user_id).quantity + 1
        models.UserItem.objects.filter(item_id=item_id).filter(user=user_id).update(quantity=newquant)
        return
    else:
        models.UserItem.objects.create(
            product=item,
            user=user_id,
            name1=item.title,
            price=item.price,
            image=item.image,
            item_id=item_id,
            sizes=size,
            colors=get_color(item.colors)
        )
        return







def shop_main(request):
    main = (item_list[::-1])[:32]
    context = {
        "items": main[:32]
    }
    
    
    response = render(request,"base/index.html", context)
    user_id, response = get_user_id(request, response)
    cart_count = get_cart_count(request)
    context["cart_count"] = cart_count
    response = render(request,"base/index.html", context)
    if request.method == "POST":
        if "add_cart" in request.POST:
            name1 = request.POST.get("item_id")
            for x in l_form(models.Product.objects.get(product_id=name1).sizes):
                if request.POST.get(x) == "on":
                    size = x
                    break
            add_to_cart(request, request.POST.get("item_id"), size)
            return redirect("shop")
            
    
    return response

def shop_all(request):
    response = render(request, "base/index.html", {})
    user_id, response = get_user_id(request, response)

    context = {
        "items": item_list[::-1],
        "cart_count": get_cart_count(request)
    }
    response =  render(request, "base/index.html", context)
    if request.method == "POST":
        if "add_cart" in request.POST:
            name1 = request.POST.get("item_id")
            for x in l_form(models.Product.objects.get(product_id=name1).sizes):
                if request.POST.get(x) == "on":
                    size = x
                    break
            add_to_cart(request, request.POST.get("item_id"), size)
            return redirect("shopAll")
    return response



def new_arrival(request):
    new_arrivals = item_list[:32]
    context = {
        "items": new_arrivals,
        "cart_count": get_cart_count(request)
    }
    if request.method == "POST":
        if "add_cart" in request.POST:
            name1 = request.POST.get("item_id")
            for x in l_form(models.Product.objects.get(product_id=name1).sizes):
                if request.POST.get(x) == "on":
                    size = x
                    break
            add_to_cart(request, request.POST.get("item_id"), size)
            return redirect("newArrivals")
    
    return render(request, "base/index.html", context)

def cart(request):
    response = render(request, "base/cart.html", {})
    user_id, response = get_user_id(request, response)
    items = models.UserItem.objects.filter(user=user_id)
    shipping = 9.99
    cart_count = 0
    item_total = 0.0
    for x in items:
        item_total += float(x.price)
        cart_count += int(x.quantity)
    n_item_total = round(item_total, 2)
    shipping = shipping * float(cart_count)
    total = item_total + shipping
    total = format(total, '.2f')
    shipping = format(shipping, '.2f')
    context = {
        "items": items,
        "items_total": n_item_total,
        "shipping": shipping,
        "cart_count": cart_count,
        "total": total
    }
    if request.method == "POST":
        size = request.POST.get("item_size")
        quantity = request.POST.get("quantity")
        item_id = request.POST.get("user_item_id")
        quantity = int(quantity)

        if quantity == 0:
            models.UserItem.objects.filter(user=user_id, item_id=item_id).delete()
            print("done")
        else:
            models.UserItem.objects.filter(user=user_id, sizes=size, item_id=item_id).update(quantity=quantity)
        
        response = render(request, "base/cart.html", {})
        user_id, response = get_user_id(request, response)
        items = models.UserItem.objects.filter(user=user_id)
        shipping = 9.99
        cart_count = 0
        item_total = 0.0
        for x in items:
            item_total += float(x.price)
            cart_count += int(x.quantity)
        n_item_total = round(item_total, 2)
        shipping = shipping * float(cart_count)
        total = item_total + shipping
        total = format(total, '.2f')
        shipping = format(shipping, '.2f')
        context = {
            "items": items,
            "items_total": n_item_total,
            "shipping": shipping,
            "cart_count": cart_count,
            "total": total
        }
        return render(request, "base/cart.html", context)
        


    return render(request, "base/cart.html", context)







# using printful api:

    # return :
    # id
    # product id
    # image
    # title
    # colors
    # url = "https://api.printful.com/product-templates"
    # token = "token here"
    # payload = {
    #     "Authorization": f'Bearer {token}'
    # }
    # rules = {
    #     "limit": "100"
    # }
    # r = requests.get(url, headers=payload, params=rules)
    # dict_type = r.json()
    # items = dict_type["result"]["items"]