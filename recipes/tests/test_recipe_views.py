from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    
    # Home tests
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


    # Category tests
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    # Category tests with fixtures
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category' , args=(1,)))
        content = response.content.decode('utf-8')
        response_recipes = response.context['recipes']

        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Dont show test recipe if is_published = False"""
        
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id':recipe.category.id,
            }))

        self.assertEqual(response.status_code, 404)


    # Detail tests
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    # Detail tests with fixtures
    def test_recipe_detail_template_loads_recipes(self):
        needed_title = 'This is a detail page - it load one recipe'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe' , kwargs={
            'id':1,
            }))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Dont show test recipe if is_published = False"""
        
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id':recipe.id,
            }))

        self.assertEqual(response.status_code, 404)

    # Search Tests
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)