from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Dress(models.Model):
    name = models.CharField(max_length=100, default="Dress")
    price = models.IntegerField()
    description = models.TextField()
    sizes = models.ManyToManyField(Size, blank=True, related_name="dresses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    def get_sizes_list(self):
        sizes_list = self.sizes.all()
        if not sizes_list:
            return []
        return [s.name for s in sizes_list]


class DressImage(models.Model):
    dress = models.ForeignKey(
        Dress,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.dress}"
