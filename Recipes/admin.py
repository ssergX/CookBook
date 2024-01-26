from django.contrib import admin
from .models import Product, Recipe, RecipeProduct

class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeProductInline,)

admin.site.register(Product)