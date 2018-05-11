import logging
from django.conf import settings
from django.db import models
from django.utils import timezone

from tracking.managers import VisitorManager, PageviewManager
from tracking.settings import TRACK_USING_GEOIP

from django.contrib.gis.geoip import HAS_GEOIP
from django.utils.encoding import python_2_unicode_compatible
from jsonfield.fields import JSONField
if HAS_GEOIP:
    from django.contrib.gis.geoip import GeoIP, GeoIPException

log = logging.getLogger(__file__)


@python_2_unicode_compatible
class Visitor(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='visit_history',
        null=True,
        editable=False,
        on_delete=models.CASCADE,
    )
    # Update to GenericIPAddress in Django 1.4
    ip_address = models.CharField(max_length=39, editable=False)
    user_agent = models.TextField(null=True, editable=False)
    start_time = models.DateTimeField(default=timezone.now, editable=False)
    expiry_age = models.IntegerField(null=True, editable=False)
    expiry_time = models.DateTimeField(null=True, editable=False)
    time_on_site = models.IntegerField(null=True, editable=False)
    end_time = models.DateTimeField(null=True, editable=False)
    geoip_data = JSONField(null=True, editable=False)
    

    objects = VisitorManager()
    
    def __str__(self):
        return self.user.__str__() if self.user else self.session_key

    def session_expired(self):
        """The session has ended due to session expiration."""
        if self.expiry_time:
            return self.expiry_time <= timezone.now()
        return False
    session_expired.boolean = True

    def session_ended(self):
        """The session has ended due to an explicit logout."""
        return bool(self.end_time)
    session_ended.boolean = True

    def get_geoip_data(self):
        """Attempt to retrieve MaxMind GeoIP data based on visitor's IP."""
        return self.geoip_data

    class Meta(object):
        ordering = ('-start_time',)
        permissions = (
            ('view_visitor', 'Can view visitor'),
        )


class Pageview(models.Model):
    visitor = models.ForeignKey(
        Visitor,
        related_name='pageviews',
        on_delete=models.CASCADE,
    )
    url = models.TextField(null=False, editable=False)
    referer = models.TextField(null=True, editable=False)
    query_string = models.TextField(null=True, editable=False)
    method = models.CharField(max_length=20, null=True)
    view_time = models.DateTimeField()

    objects = PageviewManager()

    class Meta(object):
        ordering = ('-view_time',)
