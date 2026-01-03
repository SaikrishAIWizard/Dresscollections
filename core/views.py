from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DressForm, MultipleImageUploadForm
from .models import Dress, DressImage
from django.contrib import messages
import os


def home(request):
    dresses = Dress.objects.prefetch_related("images", "sizes").order_by("-price")
    
    # Organize dresses by price category (high to low within each)
    price_categories = {
        'budget': [],
        'mid_range': [],
        'premium': [],
        'luxury': []
    }
    
    for dress in dresses:
        if dress.price < 500:
            price_categories['budget'].append(dress)
        elif dress.price < 1000:
            price_categories['mid_range'].append(dress)
        elif dress.price < 2000:
            price_categories['premium'].append(dress)
        else:
            price_categories['luxury'].append(dress)
    
    return render(request, "core/home.html", {
        "dresses": dresses,
        "price_categories": price_categories
    })



