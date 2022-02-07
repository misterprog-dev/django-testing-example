from django.test import SimpleTestCase
from budget.forms import ExpenseForm

class TestForm(SimpleTestCase):
    def test_expenses_form_valid_data(self):
        # WHEN
        expense = ExpenseForm(data = {
            'title': 'Title 1',
            'amount': 1000,
            'category': 'Dev'
        })

        # THEN
        self.assertTrue(expense.is_valid())

    def test_expenses_form_invalid_data(self):
        # WHEN
        expense = ExpenseForm(data = {
            'title': 'Title 1',
            'amount': '100n0',
            'category': 'Dev'
        })

        # THEN
        self.assertFalse(expense.is_valid())
        self.assertEquals(len(expense.errors), 1)
