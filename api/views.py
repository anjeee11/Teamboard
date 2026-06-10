from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth        import authenticate
import secrets
from django.db                  import transaction
from django.db.models           import Q, Count

from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models       import Company, KBEntry, QueryLog
from .serializers  import RegisterSerializer, LoginSerializer, KBQuerySerializer
from .permissions  import IsAdminUser


def get_tokens_for_user(user):
    """
    SimpleJWT works with refresh + access token pairs.
    We only return the access token to keep things simple.
    The access token is what the client sends in the Authorization header.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


# ── Register ─────────────────────────────────────────────────────────
class RegisterView(APIView):
    authentication_classes = []   
    permission_classes     = []   

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # 1. Create the Django User
       
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
        )

        # 2. Ensure Company exists and update it with the requested name
        company, created = Company.objects.get_or_create(
            user=user,
            defaults={
                'company_name': data['company_name'],
                'api_key': secrets.token_urlsafe(32),
            }
        )

        if not created:
            company.company_name = data['company_name']
            if not company.api_key:
                company.api_key = secrets.token_urlsafe(32)
            company.save()

        # 3. Generate JWT access token
        access_token = get_tokens_for_user(user)

        return Response({
            'username':     user.username,
            'company_name': company.company_name,
            'api_key':      company.api_key,
            'access':       access_token,
        }, status=status.HTTP_201_CREATED)


# ──  Login ────────────────────────────────────────────────────────────
class LoginView(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if user is None:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        company      = user.company
        access_token = get_tokens_for_user(user)

        return Response({
            'access':       access_token,
            'company_name': company.company_name,
            'api_key':      company.api_key,
        }, status=status.HTTP_200_OK)


# ── KB Query ─────────────────────────────────────────────────────────
class KBQueryView(APIView):

    def post(self, request):
        serializer = KBQuerySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_term = serializer.validated_data['search']
        company     = request.user.company   

        with transaction.atomic():
            results = KBEntry.objects.filter(
                Q(question__icontains=search_term) |
                Q(answer__icontains=search_term)
            )

            count = results.count()

            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=count,
            )

        return Response({
            'search':  search_term,
            'count':   count,
            'results': [
                {
                    'id':       str(entry.id),
                    'question': entry.question,
                    'answer':   entry.answer,
                    'category': entry.category,
                }
                for entry in results
            ]
        }, status=status.HTTP_200_OK)


# ──  Admin Usage Summary ──────────────────────────────────────────────
class UsageSummaryView(APIView):
    permission_classes = [IsAdminUser]   

    def get(self, request):
        
        total_queries = QueryLog.objects.aggregate(
            total=Count('id')
        )['total']

        
        active_companies = QueryLog.objects.values(
            'company'
        ).distinct().count()

        
        top_terms = QueryLog.objects.values(
            'search_term'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        return Response({
            'total_queries':    total_queries,
            'active_companies': active_companies,
            'top_search_terms': list(top_terms),
        }, status=status.HTTP_200_OK)