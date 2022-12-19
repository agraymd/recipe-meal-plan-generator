from django.contrib import admin
from recipeblog.models import Recipe, Ingredient, RecipeIngredients, MeasurementUnit, MeasurementQuantity, RecipeCategory

# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['ingredient']
    pass

class RecipeInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 0
    autocomplete_fields = ['ingredient']
    
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,    
    ]
    pass



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(MeasurementQuantity)
admin.site.register(MeasurementUnit)
admin.site.register(RecipeCategory)
admin.site.register(Ingredient, IngredientAdmin)


