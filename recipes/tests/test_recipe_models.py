from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe

class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category= self.make_category(name='Test Default Category'),
            author= self.make_author(username='new_user'),
            title = 'Beet',
            description = 'Just cook the beet',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutes', 
            servings = 5,
            servings_unit = 'Portions',
            preparation_steps = 'Beet preparation steps',
            cover = 'beet-img.jpg',
        )

        recipe.full_clean()
        recipe.save()

        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)
        ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):

        setattr(self.recipe, field, 'A' * (max_lenght + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults() 

        self.assertFalse(recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False')
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults() 

        self.assertFalse(recipe.is_published,
            msg='Recipe is_published is not False')
        
    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), 'Testing Representation')