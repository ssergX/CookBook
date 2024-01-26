from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return self.name

class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.weight}g'