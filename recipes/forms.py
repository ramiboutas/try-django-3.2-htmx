from django import forms

from .models import Recipe, Ingredient, RecipeImage

class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = RecipeImage
        fields = ['image']


class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update() # very powerfull
        for field in self.fields:
            new_data = {
                "placeholder": f"Recipe {field}",
                "class": "form-control"
            }
            self.fields[str(field)].widget.attrs.update(new_data)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
