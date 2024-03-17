from django.urls import path
from .views import AddExpenseView, ShowBalancesView, SimplifyExpensesView, ShowPassbookView


urlpatterns = [
    path('add-expense/', AddExpenseView.as_view(), name='add_expense'),
    path('show-balances/', ShowBalancesView.as_view(), name='show_balances'),
    path('simplify-expenses/', SimplifyExpensesView.as_view(), name='simplify_expenses'),
    path('show-passbook/', ShowPassbookView.as_view(), name='show_passbook'),
]
