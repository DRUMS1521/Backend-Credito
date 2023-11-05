from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from app.core.serializers import UploadFileSerializer
from app.core.models import UploadedFiles
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

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
        
