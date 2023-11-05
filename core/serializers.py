from rest_framework import serializers
from staff.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    overdue_task = serializers.IntegerField()

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'overdue_task')
