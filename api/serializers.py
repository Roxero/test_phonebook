from rest_framework import serializers
from book.models import Person, Phone
from book.views import validate_names
from rest_framework.validators import UniqueTogetherValidator

class PhoneSerializer(serializers.ModelSerializer):
    phones = serializers.ReadOnlyField
    class Meta:
        model = Phone
        fields = ['phone_number']
    def to_representation(self, obj):
        return obj.phone_number

class PersonSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)
    class Meta:
        model = Person
        fields = ['id', 'last_name', 'first_name', 'phones']
        validators = [UniqueTogetherValidator(
                            queryset=Person.objects.all(),
                            fields=['last_name', 'first_name'],
                            message='Such a user already exists'
                            )]
    def validate(self, data):
        for key,value in data.items():
            if not validate_names(value):
                raise serializers.ValidationError("Wrong name format")
        return data
