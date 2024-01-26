from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Recipe, Product, RecipeProduct

def add_product_to_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    # Получаем рецепт и продукт по их идентификаторам
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    # Проверяем, существует ли уже такой продукт в рецепте
    try:
        recipe_product = RecipeProduct.objects.get(recipe=recipe, product=product)
        # Если продукт уже есть в рецепте, обновляем его вес
        recipe_product.weight = weight
        recipe_product.save()
    except RecipeProduct.DoesNotExist:
        # Если продукта нет в рецепте, создаем новую связь
        recipe_product = RecipeProduct(recipe=recipe, product=product, weight=weight)
        recipe_product.save()

    return HttpResponse("Product added/updated successfully")

def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id')

    # Получаем рецепт по его идентификатору
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Получаем все ингредиенты (RecipeProduct), входящие в данный рецепт
    recipe_products = RecipeProduct.objects.filter(recipe=recipe)

    # Обновляем количество приготовленных блюд для каждого продукта
    for rp in recipe_products:
        rp.product.times_used += 1  # Увеличиваем количество использований продукта на 1
        rp.product.save()  # Сохраняем изменения в базе данных

    return HttpResponse("Recipe cooked successfully")


def show_recipes_without_product(request, product_id):
    # Получаем рецепты, в которых указанный продукт отсутствует или его количество меньше 10 грамм
    recipes_without_product = Recipe.objects.exclude(recipeproduct__product_id=product_id)

    context = {
        'recipes': recipes_without_product,
        'product_id': product_id
    }

    return render(request, 'Recipes/recipes_without_product.html', context)