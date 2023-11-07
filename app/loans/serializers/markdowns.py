from rest_framework import serializers
from app.loans.models import LoanMarkdowns, Loan
from django.utils import timezone

class LoanMarkdownsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanMarkdowns
        fields = ['loan','markdown','apply_to_date']

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        # Get loan markdown if exists
        loan = validated_data['loan']
        markdown_finder = LoanMarkdowns.objects.filter(loan=loan, apply_to_date=timezone.now().date())
        if markdown_finder.exists():
            this_markdown = markdown_finder.first()
            if this_markdown.markdown == True:
                this_markdown.markdown = False
                this_markdown.save()
            else:
                this_markdown.markdown = True
                this_markdown.save()
        else:
            # Create markdown
            this_markdown = LoanMarkdowns.objects.create(loan=loan, markdown=True, apply_to_date=timezone.now().date())
        return this_markdown
    