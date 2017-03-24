from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class Evidence(models.Model):

    TYPE_CHOICES = (
        ('wit_stat', 'Witness Statement'),
        ('sus_stat', 'Suspect Statement'),
        ('report', 'Report'),
        ('in_note', 'Investigators note'),
        ('unknown', 'Unknown'),
    )

    added_by = models.ForeignKey(User, related_name='new_evidence')
    primary_ID = models.CharField("Primary ID", max_length=36, unique=True)
    secondary_ID = models.CharField("Secondary ID", max_length=96, unique=True)
    document_date = models.DateTimeField("Document Date", blank=True, null=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='unknown')
    verified = models.BooleanField(default=False)
    language = models.ForeignKey('Language')
    title = models.CharField("Document Title", max_length=200)
    description = models.TextField("Description", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField("Language Name", max_length=32, unique=True)
    code = models.CharField("Language Code", max_length=3, unique=True)

    def __str__(self):
        fullname = self.code + " [" + self.name + "]"
        return fullname


class Cell(models.Model):
    cell_id = models.CharField("Cell ID", max_length=5, unique=True)
    name = models.CharField("Cell Name", max_length=64, unique=True)
    evidence = models.ForeignKey('Evidence')
    long = models.DecimalField('Longitude', max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6, null=True, blank=True)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):

    NETWORK_CHOICES = (('mtc', 'MTC'),
                       ('alfa', 'ALFA'),
                       ('other', 'Other'))

    number = models.CharField("Telephone number", max_length=32, unique=True)
    network = models.CharField(max_length=5, choices=NETWORK_CHOICES, default='other')

    # Determine a network from a phone number
    def determine_network(self):

        # Set network number
        if int(self.number[:3]) == 961:
            net_num = int(self.number[4:6])
        else:
            net_num = int(self.number[:2])

        # Determine the network the number belongs to
        if net_num == 30 or 36 <= net_num <= 39:
            return "mtc"
        elif 31 <= net_num <= 35:
            return "alfa"
        else:
            return "other"

    def __str__(self):
        return self.number


class PersonType(models.Model):
    type = models.CharField("Person Type", max_length=64, unique=True)

    def __str__(self):
        return self.type


class Person(models.Model):
    first_name = models.CharField("First Name", max_length=64)
    middle_name = models.CharField("Middle Name(s)", max_length=64, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=64)
    initials = models.CharField("Initials", max_length=4, unique=True)
    date_of_birth = models.DateField("Date of Birth", null=True)
    person_type = models.ForeignKey('PersonType')
    comment = models.TextField("Comment", blank=True, null=True)
    source = models.ManyToManyField(Evidence, blank=True)
    image = models.FileField(blank=True)

    def __str__(self):
        full_name = str.upper(self.last_name) + " " + self.first_name + " " + self.middle_name
        return full_name


class PhoneGroup(models.Model):
    name = models.CharField("Group Name", max_length=64, unique=True)
    description = models.CharField("Description", max_length=1024)
    colour = models.CharField("Colour", max_length=6)
    start_date = models.DateTimeField("Start Date", blank=True, null=True, editable=False)
    end_date = models.DateTimeField("End Date", blank=True, null=True, editable=False)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class PersonGroup(models.Model):
    name = models.CharField("Group Name", max_length=64, unique=True)
    description = models.CharField("Description", max_length=1024)
    colour = models.CharField("Colour", max_length=6)
    start_date = models.DateTimeField("Start Date", blank=True, null=True, editable=False)
    end_date = models.DateTimeField("End Date", blank=True, null=True, editable=False)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Full name", max_length=1024, unique=True)
    short_name = models.CharField("Short Name", max_length=4)
    address1 = models.CharField("Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    postal_code = models.CharField("Postal code", max_length=12, blank=True, null=True)
    city = models.CharField("City", max_length=64, blank=True, null=True)
    country = models.CharField("Country", max_length=32, blank=True, null=True)
    long = models.DecimalField('Longitude', max_digits=9, decimal_places=6, blank=True, null=True)
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6, blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)
    image = models.FileField(blank=True)

    def __str__(self):
        return self.name


class CallSequence(models.Model):

    CALL_TYPE_CHOICES = (('sms', 'SMS'),
                         ('call', 'Call'),
                         ('undefined', 'Undefined'))

    DIRECTION_CHOICES = (('in', 'Incoming'),
                         ('out', 'Outgoing'))

    call_datetime = models.DateTimeField("Call Date")
    outgoing_number = models.ForeignKey('Subscription', related_name='call_seq_out')
    incoming_number = models.ForeignKey('Subscription', related_name='call_seq_in')
    type = models.CharField(max_length=4, choices=CALL_TYPE_CHOICES, default='undefined')
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES, default='out')
    is_roaming = models.BooleanField("Roaming")
    duration = models.IntegerField("Duration in seconds")
    start_cell = models.ForeignKey('Cell', related_name='call_seq_start', blank=True, null=True)
    end_cell = models.ForeignKey('Cell', related_name='call_seq_end', blank=True, null=True)
    evidence = models.ForeignKey('Evidence')

    def __str__(self):
        return ", ".join([str(self.call_datetime)[:19], str(self.outgoing_number),
                          str(self.incoming_number), str.upper(self.direction)])


class Call(models.Model):

    outgoing = models.ForeignKey('CallSequence', related_name='call_out', null=True)
    incoming = models.ForeignKey('CallSequence', related_name='call_in', null=True)
    time_diff = None

    # Check if call is a pair
    def is_pair(self):
        return not (self.outgoing is None or self.incoming is None)

    def has_outgoing(self):
        return not (self.outgoing is None)

    def calculate_time_diff(self):
        out_time = dt.datetime(self.outgoing.call_datetime)
        in_time = dt.datetime(self.incoming.call_datetime)
        self.time_diff = abs((out_time-in_time).total_seconds())

    # Returns call time of outgoing call if available, otherwise return time of incoming call
    def get_call_time(self):
        if not (self.outgoing is None):
            return self.outgoing.call_datetime
        else:
            return self.incoming.call_datetime

    def parse_call(self):

        # Parse call if outgoing call exists
        if self.has_outgoing():
            d_time = self.outgoing.call_datetime
            out_number = self.outgoing.outgoing_number
            out_cell = self.outgoing.start_cell
            in_number = self.outgoing.incoming_number
            if self.is_pair():
                in_cell = self.incoming.start_cell
            else:
                in_cell = None
            c_type = self.outgoing.type
            c_duration = self.outgoing.duration

        # Parse call if outgoing does nto exits
        else:
            d_time = self.incoming.call_datetime
            out_number = self.incoming.outgoing_number
            in_cell = None
            out_cell = self.incoming.start_cell
            in_number = self.incoming.incoming_number
            c_type = self.incoming.type
            c_duration = self.incoming.duration

        return ", ".join([str(d_time)[:19], str(out_number), str(out_cell), str(in_number), str(in_cell),
                          str(c_type), str(c_duration)])

    def __str__(self):
        return self.parse_call()


class PersonGroupAttribution(models.Model):
    person = models.ForeignKey('Person')
    group = models.ForeignKey('PersonGroup')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        formatted_str = ", ".join([str(self.group), str(self.person)])
        return formatted_str


class PhoneGroupAttribution(models.Model):
    phone = models.ForeignKey('Subscription')
    group = models.ForeignKey('PhoneGroup')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        formatted_str = ", ".join([str(self.group), str(self.phone)])
        return formatted_str


class PersonPhoneAttribution(models.Model):
    phone = models.ForeignKey('Subscription')
    person = models.ForeignKey('Person')
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", blank=True, null=True)
    comment = models.TextField("Comment", blank=True, null=True)

    def __str__(self):
        formatted_str = ", ".join([str(self.person), str(self.phone)])
        return formatted_str
