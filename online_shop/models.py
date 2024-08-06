from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,
                                              null=True, blank=True)
    discount = models.PositiveSmallIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


class Comment(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    is_provide = models.BooleanField(default=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.created_at = None

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class Order(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.phone}'
