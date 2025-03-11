from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewsTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=So para ter o search')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search')  + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title_1 = 'This is recipe one'
        title_2 = 'This is recipe two'

        recipe_1 = self.make_recipe(
            slug = 'one',
            title = title_1,
            author_data =  {'username': 'one'}
        )

        recipe_2 = self.make_recipe(
            slug = 'two',
            title = title_2,
            author_data =  {'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response_1 = self.client.get(f'{search_url}?q={title_1}')
        response_2 = self.client.get(f'{search_url}?q={title_2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe_1, response_1.context['recipes'])
        self.assertNotIn(recipe_2, response_1.context['recipes'])

        self.assertIn(recipe_2, response_2.context['recipes'])
        self.assertNotIn(recipe_1, response_2.context['recipes'])

        self.assertIn(recipe_1, response_both.context['recipes'])
        self.assertIn(recipe_2, response_both.context['recipes'])    