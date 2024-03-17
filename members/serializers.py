from rest_framework import serializers
from .models import User, Expense, Transaction, Split


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number']


class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = ['id', 'transaction', 'user', 'amount']


class TransactionSerializer(serializers.ModelSerializer):
    splits = SplitSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['id', 'expense', 'paid_by', 'amount', 'splits']


class ExpenseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'created_by', 'created_at', 'type', 'transactions']
