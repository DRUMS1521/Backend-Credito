from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from app.loans.models import Loan
from rest_framework.response import Response
from rest_framework import status

class UpdateLoanOrderingAPIView(UpdateAPIView):
    queryset = Loan.objects.all()
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Actual ids ordering comes from request data
        ordering = request.data.get('ordering', None)
        if ordering is None:
            return Response({'detail': 'Ordering not found'}, status=status.HTTP_404_NOT_FOUND)
        # Action to perform comes from kwargs
        action = kwargs.get('action', None)
        if action is None:
            return Response({'detail': 'Action not found'}, status=status.HTTP_404_NOT_FOUND)
        # Actions could be 'up' or 'down'
        # Refactor al ordering on each action
        # Locate the element to move in the ordering list
        index = ordering.index(instance.id)
        # If the element is the first, it can't go up
        if index == 0 and action == 'up':
            return Response({'detail': 'Can\'t move up'}, status=status.HTTP_400_BAD_REQUEST)
        # If the element is the last, it can't go down
        if index == len(ordering) - 1 and action == 'down':
            return Response({'detail': 'Can\'t move down'}, status=status.HTTP_400_BAD_REQUEST)
        # Update ordering list
        # check if is the first time the ordering is updated
        for element in ordering:
            this_object = Loan.objects.get(id=element)
            this_object.ordering = ordering.index(element)
            this_object.save()
        # Update ordering of the instance swapping with the previous or next element
        if action == 'up':
            previous_element = Loan.objects.get(id=ordering[index - 1])
            previous_element.ordering = index
            previous_element.save()
            instance.ordering = index - 1
        elif action == 'down':
            next_element = Loan.objects.get(id=ordering[index + 1])
            next_element.ordering = index
            next_element.save()
            instance.ordering = index + 1
        instance.save()
        return Response({'detail': 'Ordering updated successfully'}, status=status.HTTP_200_OK)
