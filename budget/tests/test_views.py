from django.test import TestCase, Client
from django.urls import reverse
import json
from budget.models import Project, Category, Expense


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')
    
    def test_project_detail_POST_add_new_expense(self):
        # GIVEN
        Category.objects.create(
            project=self.project1,
            name='Development'
        )

        # WHEN
        response = self.client.post(self.detail_url, {
            'title': 'Expense 1',
            'amount': 10000,
            'category': 'Development'
        })

        # THEN
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'Expense 1')

    def test_project_detail_POST_no_data(self):      
        # WHEN
        response = self.client.post(self.detail_url, {})

        # THEN
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.count(), 0)


    def test_project_detail_DELETE_expense(self):
        # GIVEN
        category = Category.objects.create(
            project=self.project1,
            name='Development'
        )

        Expense.objects.create(
            project=self.project1,
            category=category,
            title='title',
            amount=1000
        )

        # WHEN
        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1      
        }))

        # THEN
        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_expense_no_id(self):
        # GIVEN
        category = Category.objects.create(
            project=self.project1,
            name='Development'
        )

        Expense.objects.create(
            project=self.project1,
            category=category,
            title='title',
            amount=1000
        )

        # WHEN
        response = self.client.delete(self.detail_url)

        # THEN
        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)
    
    def test_project_create(self):
        # GIVEN
        url = reverse('add')

        # WHEN
        response = self.client.post(url, {
            'name': 'Project 2',
            'budget': 1000,
            'categoriesString': 'dev,design'
        })

        # THEN
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'Project 2')
        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'dev')