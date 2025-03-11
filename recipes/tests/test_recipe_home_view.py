from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):
    
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8')) 

    # Home tests with fixtures
    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Dwight Schrute', content)
        self.assertIn('Just cook the beet', content)
        self.assertIn('5 Portions', content)

        response_recipes = response.context['recipes']
        self.assertEqual(len(response_recipes), 1)
        self.assertEqual(response_recipes.first().title, 'Beet')


    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Dont show test recipe if is_published = False"""
       
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        #check if recipe exist
        self.assertIn(
           '<h1>No recipes found.</h1>',
           response.content.decode('utf-8')
       )