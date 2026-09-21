from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    prep_time = models.CharField(max_length=50, default='15 mins')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    is_veg = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    image = models.URLField(blank=True, default='')
    is_in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    @property
    def category_name(self):
        return self.category.name

    @property
    def status(self):
        return 'In Stock' if self.is_in_stock else 'Out of Stock'

    def __str__(self):
        return f"{self.name} (₹{self.price})"
