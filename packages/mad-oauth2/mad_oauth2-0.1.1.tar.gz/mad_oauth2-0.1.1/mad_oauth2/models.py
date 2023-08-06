from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.db import models
from django.utils.text import slugify
from random import randint
from multiselectfield import MultiSelectField
from oauth2_provider.models import AbstractApplication
from mad_oauth2.settings import oauth2_settings


# Create your models here.


class Throttle(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    throttling = models.CharField(max_length=255, blank=False, null=False, help_text="Example: 100/day</br>Options: sec, min, hour, day, month, year")

    class Meta:
        ordering = ['-id']

class Scope(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    key = models.CharField(max_length=255, blank=False, null=False, help_text="View name, must match a valid name in View, see documentation.")
    throttling = models.ForeignKey(Throttle, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True, help_text="Detailed Description for this scope you might want show to the user.")
    admin_note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']


class Oauth2ApplicationAbstract(AbstractApplication):
    namespace = models.CharField(max_length=255, blank=True, null=True, unique=True)
    allowed_scopes = models.ManyToManyField(Scope, related_name="%(app_label)s_%(class)s_allowed_scopes")
    allowed_schemes = models.TextField(_("Allowed Schemes"), blank=True, null=True, help_text="list of allowed schemes, seperated by new line.")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-id']
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return str(self.id) + " - " + str(self.name)

    def save(self, *args, **kwargs):
        if self.namespace is None or self.namespace == "":
            self.namespace = slugify(self.name)
        else:
            self.namespace = slugify(self.namespace)

        if self._state.adding is True:
            self.namespace = self.namespace + "-"+ str(randint(0,9999999))

        super().save(*args, **kwargs)

    def get_allowed_schemes(self):
        if self.allowed_schemes is None or self.allowed_schemes == "":
            return super().get_allowed_schemes()
        else:
            # get content seperated by new line and convert to list
            return self.allowed_schemes.splitlines()


class Application(Oauth2ApplicationAbstract):
    pass
