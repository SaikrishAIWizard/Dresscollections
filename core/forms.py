from django import forms
from .models import Dress, Size

# ✅ Custom widget to allow multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=MultipleFileInput(),
        required=False,
        help_text="Max 5 images (JPEG, JPG, PNG - max 5MB each)"
    )


class DressForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Sizes"
    )

    class Meta:
        model = Dress
        fields = ["name", "price", "description", "sizes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Saree, Dress"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price in ₹"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe the dress..."}),
        }
