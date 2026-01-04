from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    Dress, DressImage, 
    MenProduct, 
    HandmadeItem
)
from django.contrib import messages
import os


def home(request):
    # ✅ Get category from URL param (women/men/handmade)
    category = request.GET.get('category', 'women')
    
    # ✅ Query appropriate model based on category
    if category == 'women':
        products = Dress.objects.prefetch_related("images", "sizes").order_by("-created_at")
    elif category == 'men':
        products = MenProduct.objects.prefetch_related("sizes").order_by("-created_at")
    elif category == 'handmade':
        products = HandmadeItem.objects.prefetch_related("sizes").order_by("-created_at")
    else:
        # Default to women
        products = Dress.objects.prefetch_related("images", "sizes").order_by("-created_at")
        category = 'women'
    
    # ✅ Organize products by price category (high to low within each)
    price_categories = {
        'budget': [],
        'mid_range': [],
        'premium': [],
        'luxury': []
    }
    
    for product in products:
        if product.price < 500:
            price_categories['budget'].append(product)
        elif product.price < 1000:
            price_categories['mid_range'].append(product)
        elif product.price < 2000:
            price_categories['premium'].append(product)
        else:
            price_categories['luxury'].append(product)
    
    # ✅ Pass unified context
    context = {
        "products": products,  # ✅ Changed from "dresses"
        "price_categories": price_categories,
        "selected_category": category,  # ✅ For dynamic titles & selector
        "categories": [  # ✅ For navbar dropdown
            ("women", "Women Dresses"),
            ("men", "Men Collection"), 
            ("handmade", "Hand Made Items")
        ]
    }
    
    return render(request, "core/home.html", context)


# Optional: Admin-only views (if you want to keep forms later)
@login_required
def add_dress(request):
    """Future use - currently using Django Admin"""
    return redirect("admin:index")


@login_required
def upload_images(request):
    """Future use - currently using Django Admin"""
    return redirect("admin:index")
