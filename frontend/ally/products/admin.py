# products/admin.py

from django.contrib import admin
from .models import ProductType, Product, RecipeBundle, VideoContent, DocumentContent, ProductItem
# Ensure Recipe model is importable if needed, e.g.:
# from recipes.models import Recipe

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# This inline might be useful if you want to manage ProductItems
# directly within the Product admin page.
class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1  # Number of empty forms to display
    # Optional: Customize fields shown in the inline
    # fields = ('content_type', 'object_id', 'order')
    # readonly_fields = [...]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'price')
    list_filter = ('type',)
    search_fields = ('title', 'description')
    # If you want to manage ProductItems here using the inline:
    # inlines = [ProductItemInline]

# Updated RecipeBundleAdmin incorporating name, includes_all_recipes, etc.
class RecipeBundleAdmin(admin.ModelAdmin):
    # Updated list_display
    list_display = ('name', 'includes_all_recipes', 'get_recipes_summary', 'description')
    # Updated search_fields (assuming 'description' was added to the RecipeBundle model)
    search_fields = ('name', 'description', 'recipes__name') # Removed recipes__description for brevity, add if needed
    # Updated list_filter
    list_filter = ('includes_all_recipes', 'recipes')
    # Use filter_horizontal for a better ManyToMany selection widget
    filter_horizontal = ('recipes',)

    # Using fieldsets to structure the form
    fieldsets = (
        (None, { # First group without a title
            'fields': ('name', 'description', 'includes_all_recipes')
        }),
        ('Specific Recipes', {
            # This group can optionally be collapsed
            'classes': ('collapse',), # Optional: Collapse group by default
            'description': "This selection is only considered if 'Always include all recipes' above is *not* checked.",
            'fields': ('recipes',),
        }),
    )

    def get_recipes_summary(self, obj):
        """
        Custom display for the list: Shows '(All Recipes)' or a preview.
        'obj' is the RecipeBundle instance.
        """
        if obj.includes_all_recipes:
            return "(All Recipes)"

        # Ensure the related manager can be accessed. Might need prefetching in get_queryset for performance.
        try:
            count = obj.recipes.count()
            if count == 0:
                return "-"
            # Assumption: Your Recipe model has a 'name' field. Adjust if needed (e.g., 'title').
            display_names = ", ".join([r.name for r in obj.recipes.all()[:3]])
            if count > 3:
                display_names += f", ... ({count - 3} more)"
            return display_names
        except Exception: # Catch potential errors if relation is problematic
             return "Error loading recipes"


    get_recipes_summary.short_description = 'Included Recipes' # Column header

class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')
    search_fields = ('title',)

class DocumentContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)

# Register your models with the admin site
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RecipeBundle, RecipeBundleAdmin) # Register with the updated Admin class
admin.site.register(VideoContent, VideoContentAdmin)
admin.site.register(DocumentContent, DocumentContentAdmin)

# Optionally register ProductItem if you need direct admin access to it,
# though managing it via ProductAdmin inline might be sufficient.
# admin.site.register(ProductItem)