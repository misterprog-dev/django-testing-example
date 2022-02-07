from django.test import TestCase
from budget.models import Project, Category, Expense


class TestModel(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(
            name='project 1',
            budget=10000
        )
    
    def test_project_is_assigned_slug_on_creation(self):
        # THEN
        self.assertEquals(self.project1.slug, 'project-1')

    def test_project_budget_left(self):
        # GIVEN
        category1 = Category.objects.create(
            project=self.project1,
            name='Development'
        )

        Expense.objects.create(
            project=self.project1,
            category=category1,
            title='title',
            amount=1000
        )
        Expense.objects.create(
            project=self.project1,
            category=category1,
            title='title2',
            amount=3000
        )

        # WHEN
        response = self.project1.budget_left

        # THEN
        self.assertEquals(response, 6000)
    

    def test_project_total_transactions(self):
        # GIVEN
        category1 = Category.objects.create(
            project=self.project1,
            name='Development'
        )

        Expense.objects.create(
            project=self.project1,
            category=category1,
            title='title',
            amount=1000
        )
        Expense.objects.create(
            project=self.project1,
            category=category1,
            title='title2',
            amount=3000
        )

        # WHEN
        response = self.project1.total_transactions

        # THEN
        self.assertEquals(response, 2)
    
    def test_get_absolute_url(self):
        # WHEN
        url = self.project1.get_absolute_url()

        # THEN
        self.assertEquals(url, '/project-1')


