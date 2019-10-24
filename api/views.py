from book.models import Person
from .serializers import PersonSerializer
from book.views import validate_phonenumber
from rest_framework.response import Response
from rest_framework import generics


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all().filter(deleted=False).order_by('last_name')
    serializer_class = PersonSerializer

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def put(self, request, pk):
        person = Person.objects.filter(deleted = False).filter(id = pk)
        if person:
            person = person[0]
            phones = [item.phone_number for item in person.phones.all()]
            new_phone = request.data.get('phone')
            if not new_phone:
                return Response({"fail": {
                                "message":"Malformed request"
                                }
                            }, status=400)
            else:
                print(new_phone)
                if validate_phonenumber(new_phone):
                    if new_phone not in phones:
                        person.phones.create(phone_number=new_phone)
                        person.save()
                        return Response({"success": {
                                          "message":"Phone successfully added"
                                          }
                                    }, status=201)
                    else:
                        return Response({"fail": {
                                        "message":"Phone already exists"
                                        }
                                    }, status=400)
                else:
                    return Response({"fail": {
                                    "message":"Wrong phone format. Use +7-XXX-XXX-XX-XX"
                                    }
                                }, status=400)
        else:
            return Response({"fail": {
                            "message":"No person with id {}".format(pk)
                            }
                        }, status=404)
