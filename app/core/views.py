from rest_framework.generics import CreateAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from app.core.serializers import UploadFileSerializer, InfoAndRulesSerializer
from app.core.models import UploadedFiles, InfoAndRules
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class healthCheckAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
    

class uploadFileAPIView(CreateAPIView):
    queryset = UploadedFiles.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadFileSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['uploaded_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class InfoAndRulesAPIView(ListCreateAPIView):
    queryset = InfoAndRules.objects.all()
    serializer_class = InfoAndRulesSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() > 0:
            serializer = self.get_serializer(queryset[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

