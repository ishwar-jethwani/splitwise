# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and return a new user instance
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and return a new superuser instance
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class MemberUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(MemberUser, on_delete=models.CASCADE, related_name='profile')
    otp = models.CharField(max_length=6, blank=True, null=True)  # Field to store OTP
    # Add other fields as needed

    def __str__(self):
        return self.user.email


class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent'),
    ]

    name = models.CharField(max_length=255, verbose_name='Name')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Amount')
    created_by = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name='expenses_created', verbose_name='Created By')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES, verbose_name='Type')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'


class Transaction(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='transactions', verbose_name='Expense')
    paid_by = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name='transactions_paid', verbose_name='Paid By')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Amount')

    def __str__(self):
        return f"Transaction {self.id} - {self.paid_by.username} paid {self.amount}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Split(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='splits', verbose_name='Transaction')
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name='splits', verbose_name='User')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Amount')

    def __str__(self):
        return f"{self.user.username} owes {self.amount} in transaction {self.transaction_id}"

    class Meta:
        verbose_name = 'Split'
        verbose_name_plural = 'Splits'
