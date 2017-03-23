from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Evidence)
admin.site.register(Language)
admin.site.register(Cell)
admin.site.register(Subscription)
admin.site.register(PersonType)
admin.site.register(Person)
admin.site.register(PhoneGroup)
admin.site.register(PersonGroup)
admin.site.register(Location)
admin.site.register(CallSequence)
admin.site.register(Call)
admin.site.register(PersonGroupAttribution)
admin.site.register(PhoneGroupAttribution)
admin.site.register(PersonPhoneAttribution)
