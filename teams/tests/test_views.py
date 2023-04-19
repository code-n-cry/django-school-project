import django.test
import django.urls


class TeamsViewsTestCase(django.test.TestCase):
    fixtures = ('skills_fixture.json', 'team_fixture.json',)

    def test_create_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:create')
        )

        self.assertEqual(response.status_code, 302)

    def test_detail_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:detail', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:list')
        )

        self.assertEqual(response.status_code, 200)

    def test_edit_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:edit', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_yours_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:yours')
        )

        self.assertEqual(response.status_code, 302)

    def test_members_view(self):
        response = django.test.Client().get(
            django.urls.reverse_lazy('teams:members', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
