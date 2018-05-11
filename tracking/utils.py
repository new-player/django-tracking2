from __future__ import division

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.contrib.gis.geoip import HAS_GEOIP
from tracking.settings import TRACK_USING_GEOIP
if HAS_GEOIP:
    from django.contrib.gis.geoip import GeoIP, GeoIPException


GEOIP_CACHE_TYPE = getattr(settings, 'GEOIP_CACHE_TYPE', 4)

headers = (
    'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTERED_CLIENT_IP', 'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED',
    'REMOTE_ADDR'
)


def get_ip_address(request):
    for header in headers:
        if request.META.get(header, None):
            ip = request.META[header].split(',')[0]

            try:
                validate_ipv46_address(ip)
                return ip
            except ValidationError:
                pass


def get_geo_ip_data(ip_address):
    if not HAS_GEOIP or not TRACK_USING_GEOIP:
        return
    
    geoip_data = None
    try:
        gip = GeoIP(cache=GEOIP_CACHE_TYPE)
        geoip_data = gip.city(ip_address)
    except GeoIPException as e:
        msg = 'Error getting GeoIP data for IP "{0}"'.format(
            ip_address)
        log.exception(msg)

    return geoip_data


def total_seconds(delta):
    day_seconds = (delta.days * 24 * 3600) + delta.seconds
    return (delta.microseconds + day_seconds * 10**6) / 10**6
