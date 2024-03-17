from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import MemberUser, Profile, Expense, Transaction, Split
from rest_framework.permissions import BasePermission, IsAuthenticated
from decimal import Decimal
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from constants import constant


class PostPermission(BasePermission):
    """Allow access only to the owner of the post."""
    def has_permission(self, request, view):
        SAFE_METHODS = ["GET", "PUT"]
        if request.method in SAFE_METHODS:
            # Allow GET and PUT requests without authentication
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            # Allow POST requests only if the user is authenticated
            return True
        return False


class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            if MemberUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = MemberUser.objects.create_user(email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            Profile(user=user).save()
            data = {"Id": user.pk, "email": user.email, "token": token.key}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'An error occurred while creating the user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            token, _ = Token.objects.get_or_create(user=user)
            data = {"Id": user.pk, "email": user.email, "token": token.key}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordView(APIView):
    permission_classes = (PostPermission,)

    def get(self, request):
        try:
            email = request.GET.get('email')
            if not email:
                return Response({'error': 'Email is required in query parameters'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')

            # Save OTP to user's profile or create a new profile if user does not exist
            try:
                user = MemberUser.objects.get(email=email)
            except MemberUser.DoesNotExist:
                user = MemberUser.objects.create_user(email=email)
            user.profile.otp = otp
            user.profile.save()

            # Send OTP to the user's email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        password1 = request.data.get("password")
        password2 = request.data.get("password_confirm")
        user = request.user
        if user.is_authenticated:
            if password1 == password2:
                user.set_password(password1)
                return Response({"msg": "Password Set Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "Password Mismatch"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unauthenticated Request"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        try:
            email = request.data.get('email')
            otp_entered = request.data.get('otp')
            new_password = request.data.get('new_password')

            user = MemberUser.objects.get(email=email)

            # Verify OTP
            if user.profile.otp != otp_entered:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            # Change password
            user.set_password(new_password)
            user.save()

            # Clear OTP after successful password change
            user.profile.otp = None
            user.profile.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except MemberUser.DoesNotExist:
            return Response({'error': 'MemberUser with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddExpenseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            name = request.data.get('name')
            amount = Decimal(request.data.get('amount'))
            expense_type = request.data.get('type')
            created_by = request.user
            participants = request.data.getlist('participants')
            splits = request.data.getlist('splits')

            # Create the expense
            expense = Expense.objects.create(name=name, amount=amount, type=expense_type, created_by=created_by)

            # Create transactions and splits
            for idx, participant in enumerate(participants):
                user = MemberUser.objects.get(id=participant)
                amount_paid = Decimal(splits[idx])
                transaction = Transaction.objects.create(expense=expense, paid_by=created_by, amount=amount_paid)
                Split.objects.create(transaction=transaction, user=user, amount=amount_paid)

            # Send emails asynchronously
            self.send_email_async(request.user, expense)

            return Response({'message': 'Expense added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def send_email_async(user, expense):
        subject = 'Expense Added'
        html_message = render_to_string('expense_email.html', {'user': user, 'expense': expense})
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, constant.EMAIL_HOST_USER, [user.email], html_message=html_message)


class ShowBalancesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            balances = {}
            splits = Split.objects.filter(user=user)
            for split in splits:
                if split.amount != 0:
                    balances[split.transaction.paid_by.email] = balances.get(split.transaction.paid_by.email, 0) + split.amount
            return Response({'balances': balances}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SimplifyExpensesView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            user = request.user
            splits = Split.objects.filter(user=user)
            for split in splits:
                matching_splits = Split.objects.filter(transaction=split.transaction).exclude(user=user)
                for matching_split in matching_splits:
                    if matching_split.amount > 0:
                        if split.amount >= matching_split.amount:
                            split.amount -= matching_split.amount
                            matching_split.amount = 0
                        else:
                            matching_split.amount -= split.amount
                            split.amount = 0
            return Response({'message': 'Expenses simplified successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShowPassbookView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            transactions = Transaction.objects.filter(expense__created_by=user)
            passbook = {}
            for transaction in transactions:
                splits = Split.objects.filter(transaction=transaction)
                for split in splits:
                    passbook[transaction.created_at] = passbook.get(transaction.created_at, {})
                    passbook[transaction.created_at][split.user.email] = passbook[transaction.created_at].get(split.user.email, 0) + split.amount
            return Response({'passbook': passbook}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
