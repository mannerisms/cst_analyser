from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Evidence(models.Model):
    """Model for the source document representing evidence"""
    created_date = models.DateTimeField(auto_now=True, editable=False)
    added_by = models.ForeignKey('auth.User')
    primary_ID = models.CharField("Primary ID", max_length=36)
    secondary_ID = models.CharField("Secondary ID", max_length=96)
    title = models.CharField("Document Title", max_length=200)
    document_date = models.DateTimeField("Document Date", blank=True, null=True)
    language = models.ForeignKey('Language')
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField("Language Name", max_length=32)
    code = models.CharField("Language Code", max_length=3)

    def __str__(self):
        fullname = self.code + " [" + self.name + "]"
        return fullname


class Cell(models.Model):
    cell_id = models.CharField("ID", max_length=5)
    name = models.CharField("Name", max_length=64)
    evidence = models.ForeignKey('Evidence')
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    number = models.CharField("Telephone number", max_length=32)

    def __str__(self):
        return self.number


class PersonType(models.Model):
    type = models.CharField("Person Type", max_length=64)

    def __str__(self):
        return self.type


class Person(models.Model):
    first_name = models.CharField("First Name", max_length=64)
    middle_name = models.CharField("Middle Name(s)", max_length=64)
    last_name = models.CharField("Last Name", max_length=64)
    initials = models.CharField("Initials", max_length=3)
    date_of_birth = models.DateField("Date of Birth", null=True)
    person_type = models.ForeignKey('PersonType')
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class PhoneGroup(models.Model):
    name = models.CharField("Group Name", max_length=64)
    description = models.CharField("Description", max_length=1024)
    colour = models.CharField("Colour", max_length=6)
    start_date = models.DateTimeField("Start Date", blank=True, null=True, editable=False)
    end_date = models.DateTimeField("End Date", blank=True, null=True, editable=False)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class PersonGroup(models.Model):
    name = models.CharField("Group Name", max_length=64)
    description = models.CharField("Description", max_length=1024)
    colour = models.CharField("Colour", max_length=6)
    start_date = models.DateTimeField("Start Date", blank=True, null=True, editable=False)
    end_date = models.DateTimeField("End Date", blank=True, null=True, editable=False)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Full name", max_length=1024)
    short_name = models.CharField("Short Name", max_length=4)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024)
    postal_code = models.CharField("Postal code", max_length=12)
    city = models.CharField("City", max_length=64)
    country = models.CharField("Country", max_length=32)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class CallSequence(models.Model):
    call_datetime = models.DateTimeField("Call Date")
    outgoing = models.ForeignKey('Subscription', related_name='Outgoing_number')
    incoming = models.ForeignKey('Subscription', related_name='Incoming_number')
    is_txt = models.BooleanField("SMS")
    is_outgoing = models.BooleanField("Outgoing")
    is_roaming = models.BooleanField("Roaming")
    duration = models.IntegerField("Duration in seconds")
    start_cell = models.ForeignKey('Cell', related_name='Start_cell')
    end_cell = models.ForeignKey('Cell', related_name='End_cell', blank=True, null=True)
    evidence = models.ForeignKey('Evidence')


class Call(models.Model):

    outgoing = models.ForeignKey('CallSequence', related_name='Outgoing_call', null=True)
    incoming = models.ForeignKey('CallSequence', related_name='Incoming_call', null=True)

    # Check if call is a pair
    def is_pair(self):
        return not (self.outgoing is None or self.incoming is None)

    def has_outgoing(self):
        return not (self.outgoing is None)

    # Returns call time of outgoing call if available, otherwise return time of incoming call
    def get_call_time(self):
        if not (self.outgoing is None):
            return self.outgoing.call_datetime
        else:
            return self.incoming.call_datetime


class PersonGroupAttribution(models.Model):
    person = models.ForeignKey('Person')
    group = models.ForeignKey('PersonGroup')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)


class PhoneGroupAttribution(models.Model):
    phone = models.ForeignKey('Subscription')
    group = models.ForeignKey('PhoneGroup')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)


class PersonPhoneAttribution(models.Model):
    phone = models.ForeignKey('Subscription')
    person = models.ForeignKey('Person')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)