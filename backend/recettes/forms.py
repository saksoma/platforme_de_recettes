from django import forms

from .models import Recipe, WeeklyMenu


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "steps",
            "preparation_time",
            "difficulty",
            "servings",
            "calories",
            "protein",
            "carbs",
            "fat",
            "image",
            "category",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre de la recette"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description"}),
            "ingredients": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Ingredients (un par ligne)"}),
            "steps": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Etapes de preparation"}),
            "preparation_time": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Temps en minutes"}),
            "difficulty": forms.Select(attrs={"class": "form-select"}),
            "servings": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "calories": forms.NumberInput(attrs={"class": "form-control", "min": 0, "placeholder": "kcal"}),
            "protein": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.1", "placeholder": "g"}),
            "carbs": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.1", "placeholder": "g"}),
            "fat": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.1", "placeholder": "g"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        }


class WeeklyMenuForm(forms.ModelForm):
    class Meta:
        model = WeeklyMenu
        fields = ["date", "meal_type", "recipe", "servings"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "meal_type": forms.Select(attrs={"class": "form-select"}),
            "recipe": forms.Select(attrs={"class": "form-select"}),
            "servings": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipe"].queryset = Recipe.objects.filter(status="approved").order_by("title")
