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


@login_required
def upload_dress(request):
    if request.method == "POST":
        dress_form = DressForm(request.POST)
        image_form = MultipleImageUploadForm(request.POST, request.FILES)

        if dress_form.is_valid():
            # Validate images before saving
            images = request.FILES.getlist('images')
            
            # Check if images exist
            if not images or all(img.name == '' for img in images):
                messages.error(request, "❌ Please select at least one image.")
            else:
                # Validate files
                allowed_extensions = {'.jpg', '.jpeg', '.png'}
                max_size = 5 * 1024 * 1024  # 5MB
                valid_images = []
                has_error = False
                
                for img in images:
                    if not img or img.name == '':
                        continue
                    
                    # Check extension
                    ext = os.path.splitext(img.name)[1].lower()
                    if ext not in allowed_extensions:
                        messages.error(request, f"❌ Invalid file type: {img.name}. Only JPG, JPEG, PNG allowed.")
                        has_error = True
                    # Check size
                    elif img.size > max_size:
                        messages.error(request, f"❌ File {img.name} is too large (max 5MB).")
                        has_error = True
                    else:
                        valid_images.append(img)
                
                # Check max 5 images
                if len(valid_images) > 5:
                    messages.error(request, "❌ Maximum 5 images allowed.")
                    has_error = True
                elif len(valid_images) == 0:
                    messages.error(request, "❌ No valid images to upload.")
                    has_error = True
                elif not has_error:
                    # Save dress
                    try:
                        dress = dress_form.save()
                        
                        # Save images
                        for img in valid_images:
                            DressImage.objects.create(dress=dress, image=img)
                        
                        messages.success(request, f"✅ Dress '{dress.name}' uploaded with {len(valid_images)} images! You can add more images below.")
                        return redirect("upload_dress")
                    except Exception as e:
                        messages.error(request, f"❌ Error saving: {str(e)}")
        else:
            # Dress form validation errors
            for field, errors in dress_form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {field}: {error}")
    else:
        dress_form = DressForm()
        image_form = MultipleImageUploadForm()

    return render(request, "core/upload.html", {
        "dress_form": dress_form,
        "image_form": image_form
    })

