from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import Person
import re

# Routing GET and POST queries for site
# GET for / requests are routed to printing all the entries in phonebook
# POST for / requests are routed to view for adding a new person into Book
# all other methods are denied and redirected for common list of entries
def query_router(request):
    if request.method == 'GET':
        return list_entries(request)
    elif request.method == 'POST':
        return add_person(request)
    else:
        return HttpResponseRedirect (reverse('book:query_router'))

# Function for listing all the queries or limited by search
# search parameter comes in from site header form field
def list_entries(request):
    if request.GET.get('search'):
        search_persons = Person.objects.filter(deleted = False).filter(Q(first_name__icontains=request.GET.get('search'))|Q(last_name__icontains=request.GET.get('search'))).distinct().order_by('last_name')
        return render(request, 'phonebook/addressbook_list.html', {'all_persons': search_persons })
    else:
        all_persons = Person.objects.filter(deleted = False).order_by('last_name')
        return render(request, 'phonebook/addressbook_list.html', {'all_persons': all_persons })

# Function for adding a person into phonebook
def add_person(request):
    # getting the POST method params of last and first name
    first_name = request.POST.get('first_name').strip().title()
    last_name = request.POST.get('last_name').strip().title()
    #checking validity and nonemptiness of both fields
    if first_name and last_name and validate_names(first_name) and validate_names(last_name):
       try:
           # trying add a valid new person
           query = Person(first_name, last_name)
           query.save()
       except:
           # if addition failed, it means such a person is already added in the book
           messages.error(request, 'Person with such name already exists.')
           return HttpResponseRedirect (reverse('book:query_router'))
       # all ok, person added
       messages.success(request, 'Profile successfully added.')
       return HttpResponseRedirect (reverse('book:query_router'))
    else:
        # name(s) are non-valid or empty
        messages.error(request, 'Invalid name entered.')
        return HttpResponseRedirect (reverse('book:query_router'))

# function for deleting a person
# indeed it's just marking person as deleted without real erasing from DB
def delete_person(request, person_id=None):
    #checking whether or not a person exists
    person = Person.objects.filter(deleted = False).get(id = person_id)
    if person:
        #person exists, marking him as deleted
        person.deleted=True
        person.save()
        messages.success(request, 'Person deleted successfully.')
        return HttpResponseRedirect (reverse('book:query_router'))
    else:
        # wrong given id, returning back with error
        messages.error(request, 'There is no person with given id.')
        return HttpResponseRedirect (reverse('book:query_router'))

# function for representing person card with his phones
# also for addition and deleting phone number for exact person by person id
# Queries comming here from url /book/<id>
def person_card(request, person_id):
    # checking whether person with given id exists
    try:
        person = Person.objects.filter(deleted = False).get(id = person_id)
    except:
        # if person with given id doesn't exist, returning to all the list
        messages.error(request, 'There is no person with given id.')
        return HttpResponseRedirect (reverse('book:query_router') )
    # getting person's phone list
    phones = [str(phone) for phone in person.phones.all()]
    # collecting POST params
    # phone_for_add - number candidate to be added
    # phone_for_del - number candidate to be deleted
    phone_for_add = request.POST.get('phone_for_add')
    phone_for_del = request.POST.get('phone_for_del')
    # routing queries by query params
    # going to add a new number
    if phone_for_add:
        return addphone(request, person_id)
    # going to delete an exact phone from phone list for the person
    elif phone_for_del:
        return del_phone(request, person_id)
    # no extraparams, only rendering a page with person card info
    else:
        return render(request, 'phonebook/person_card.html', {'person': person, 'phones':phones})

# function for adding a phone into persons phone list
def addphone(request, person_id):
    # collecting a phone number from query
    phone_for_add = request.POST.get('phone_for_add')
    # checking existency of person by given id
    if Person.objects.filter(deleted = False).filter(id = person_id):
        # person id exists in DB
        person = Person.objects.filter(deleted = False).get(id = person_id)
        # getting all the phones for person
        phones = [str(phone) for phone in person.phones.all()]
        # checking phonenumber validity and non-existency in the phone list
        if phone_for_add and validate_phonenumber(phone_for_add):
            # all ok, adding new phone into phones table
            if phone_for_add not in phones:
                person.phones.create(phone_number = phone_for_add)
                person.save()
                messages.success(request, 'Phone added successfully.')
                return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )
            # phone format is valid, but number is already in phone list of person
            else:
                messages.error(request, 'Given phone number already in list')
                return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )
        else:
            messages.error(request, 'Given phone number incorrect. Expecting +7-XXX-XXX-XX-XX ')
            return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )
    else:
        # wrong given id, returning back with error
        messages.error(request, 'There is no person with given id.')
        return HttpResponseRedirect (reverse('book:query_router', args = (person.id,)) )

# function for deleting a phone number from person's list
def del_phone(request, person_id):
    # collecting a phone number to be deleted from query
    phone_for_del = request.POST.get('phone_for_del')
    # checking existency of person by given id
    if Person.objects.filter(deleted = False).get(id = person_id):
        # person id exists in DB
        person = Person.objects.filter(deleted = False).get(id = person_id)
        phones = [str(phone) for phone in person.phones.all()]
        # checking if the given phone to be deleted is in person's phone list
        if phone_for_del not in phones:
            # if not exists, redirecting back with an error
            messages.error(request, 'There is no such a phone in list.')
            return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )
        else:
            # if exists, removing it
            person.phones.filter(phone_number=phone_for_del).delete()
            person.save()
            messages.success(request, 'Phone deleted successfully.')
            return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )
    else:
        # wrong given id, returning back with error
        messages.error(request, 'There is no person with given id.')
        return HttpResponseRedirect (reverse('book:person_card', args = (person.id,)) )

# function for validation names according to common sense
# returns Bool
def validate_names(name):
    rex = re.compile("^[а-яА-ЯёЁa-zA-Z-]{1,30}$")
    return True if rex.match(name) else False

# function for validation phonenumber according to requirements
# returns Bool
def validate_phonenumber(phone_number):
    rex = re.compile("^\+7\-[0-9]{3}\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}$")
    return True if rex.match(phone_number) else False
