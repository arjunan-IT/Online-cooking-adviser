from django.db import models

# Recipe Model
class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    category = models.CharField(max_length=100)
    ratings = models.FloatField(default=0.0)
    how_to_cook=models.TextField(default='nothing')

    def __str__(self):
        return self.recipe_name

# Feedback Model
class Feedback(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.recipe.recipe_name}"

class UserRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
