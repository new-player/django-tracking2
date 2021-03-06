from datetime import timedelta
from django.contrib import admin
from tracking.models import Visitor, Pageview
from tracking.settings import TRACK_PAGEVIEWS, TRACK_USING_GEOIP

class VisitorAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'

    list_display = ('session_key', 'user', 'start_time', 'session_over',
        'pretty_time_on_site', 'ip_address', 'user_agent')
    list_filter = ('user',)
    search_fields = ('session_key', 'user__email', 'user__username', 'user_agent', )

    readonly_fields=('user_agent', 'ip_address', 'start_time', 'expiry_age',\
                     'expiry_time', 'time_on_site', 'end_time', 'geoip_data', )
    

    def session_over(self, obj):
        return obj.session_ended() or obj.session_expired()
    session_over.boolean = True

    def pretty_time_on_site(self, obj):
        if obj.time_on_site is not None:
            return timedelta(seconds=obj.time_on_site)
    pretty_time_on_site.short_description = 'Time on site'
    
    
    def get_list_display(self, request):
        list_display = super(VisitorAdmin, self).get_list_display(request)
        if TRACK_USING_GEOIP:
            list_display += ('geoip_data',)
        return list_display
        
    def get_search_fields(self, request):
        search_fields = super(VisitorAdmin, self).get_search_fields(request)
        if TRACK_USING_GEOIP:
            search_fields += ('geoip_data',)
        return search_fields

admin.site.register(Visitor, VisitorAdmin)


class PageviewAdmin(admin.ModelAdmin):
    date_hierarchy = 'view_time'
    raw_id_fields = ['visitor',]
    search_fields = ('visitor__session_key', 'visitor__user__email', 'visitor__user__username', 'url', 'referer', 'query_string', 'method',)
    list_display = ('visitor', 'url', 'view_time', 'query_string','referer',)
    readonly_fields = ('query_string', 'referer', 'url', )


if TRACK_PAGEVIEWS:
    admin.site.register(Pageview, PageviewAdmin)
