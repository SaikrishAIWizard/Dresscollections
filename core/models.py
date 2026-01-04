from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# ========= COMMON BASE =========
class BaseProduct(models.Model):
    name = models.CharField(max_length=100, default="Product")
    price = models.IntegerField()
    description = models.TextField()
    sizes = models.ManyToManyField(
        Size,
        blank=True,
        related_name="%(class)s_sizes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    def get_sizes_list(self):
        sizes_list = self.sizes.all()
        if not sizes_list:
            return []
        return [s.name for s in sizes_list]

# ========= WOMEN (UNCHANGED) =========
class Dress(BaseProduct):
    class Meta:
        verbose_name = "Women Dress"
        verbose_name_plural = "Women Dresses"

class DressImage(models.Model):
    dress = models.ForeignKey(
        Dress,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.dress}"

# ========= MEN (TEXTFIELD) =========
class MenProduct(BaseProduct):
    image_urls_text = models.TextField(  # ✅ No validation issues!
        blank=True,
        help_text="Paste URLs one per line"
    )
    
    @property
    def image_urls(self):  # ✅ Templates use this
        if not self.image_urls_text:
            return []
        return [url.strip() for url in self.image_urls_text.split('\n') if url.strip()]

    class Meta:
        verbose_name = "Men Product"
        verbose_name_plural = "Men Products"

# ========= HANDMADE (TEXTFIELD) =========
class HandmadeItem(BaseProduct):
    image_urls_text = models.TextField(
        blank=True,
        help_text="Paste URLs one per line"
    )
    
    @property
    def image_urls(self):
        if not self.image_urls_text:
            return []
        return [url.strip() for url in self.image_urls_text.split('\n') if url.strip()]

    class Meta:
        verbose_name = "Handmade Item"
        verbose_name_plural = "Handmade Items"
