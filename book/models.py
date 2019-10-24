from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' id=' + str(self.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_name')
        ]

class Phone(models.Model):
    person = models.ForeignKey(Person, related_name='phones', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16)

    def __str__(self):
        return self.phone_number
