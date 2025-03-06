from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
    
    def make_author(
            self,
            first_name ='Dwight',
            last_name = 'Schrute',
            username = 'Manager',
            password = '12345',
            email = 'dwight@dundermifflin.com'):
        return User.objects.create_user(
            first_name =first_name,
            last_name = last_name,
            username = username,
            password = password,
            email = email)
    
    def make_recipe(
            self,
            category_data= None,
            author_data= None,
            title = 'Beet',
            description = 'Just cook the beet',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutes', 
            servings = 5,
            servings_unit = 'Portions',
            preparation_steps = 'Beet preparation steps',
            preparation_steps_is_html = False,
            is_published = True,
            cover = 'beet-img.jpg',
        ):
        
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit, 
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
            cover = cover,
        )