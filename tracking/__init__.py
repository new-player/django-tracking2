__version_info__ = {
    'major': 0,
    'minor': 4,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 1
}

def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i.%(micro)i" % __version_info__]
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(vers)

__version__ = get_version()
default_app_config = 'tracking.apps.TrackingConfig'


import os

def geoip_data_download_location():
    from django.conf import settings
    if not settings.GEOIP_PATH:
        directory = os.path.abspath(os.path.join(f, 'data'))
    else:
        directory = settings.GEOIP_PATH
    
    return directory

    
