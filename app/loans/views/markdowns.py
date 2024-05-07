from app.loans.models import LoanMarkdowns, Loan
from app.loans.serializers import LoanMarkdownsSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status

class LoanMarkdownsListAPIView(generics.ListAPIView):
    serializer_class = LoanMarkdownsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        # Search date from query params
        return LoanMarkdowns.objects.filter(loan__collector = self.request.user, markdown=True, apply_to_date=timezone.now().date())
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for markdown in queryset:
            data.append(
                markdown.id,
            )
        return Response(data, status=status.HTTP_200_OK)
    
class LoanMarkdownsCreateAPIView(generics.CreateAPIView):
    serializer_class = LoanMarkdownsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    queryset = LoanMarkdowns.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        markdown = serializer.save()
        return Response({'detail': 'Markdown applied successfully'}, status=status.HTTP_201_CREATED)