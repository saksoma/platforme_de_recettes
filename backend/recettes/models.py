from django.db import models
from django.contrib.auth.models import User
from category.models import Category


# -------------------------
# RECIPE
# -------------------------
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente'),
        ('approved', 'Approuvee'),
        ('rejected', 'Rejetee'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()

    preparation_time = models.PositiveIntegerField(help_text="Temps en minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    servings = models.PositiveIntegerField(default=4, help_text="Nombre de portions")

    calories = models.PositiveIntegerField(null=True, blank=True, help_text="Calories par portion")
    protein = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Proteines par portion")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Glucides par portion")
    fat = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Lipides par portion")

    image = models.ImageField(upload_to='recipes/', null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField('tag.Tag', related_name='recipes', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    is_featured = models.BooleanField(default=False, verbose_name="Mise en avant")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -------------------------
# FAVORITE
# -------------------------
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"


# -------------------------
# RATING
# -------------------------
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.score} stars"


# -------------------------
# COMMENT
# -------------------------
class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuve'),
        ('rejected', 'Rejete'),
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"


# -------------------------
# WEEKLY MENU
# -------------------------
class WeeklyMenu(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Petit-dejeuner'),
        ('lunch', 'Dejeuner'),
        ('dinner', 'Diner'),
        ('snack', 'Collation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_menus")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="menu_items")
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    servings = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'meal_type']
        unique_together = ('user', 'date', 'meal_type')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.recipe.title}"
