from django.contrib.sitemaps import Sitemap
from .models import Topic

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Topic.objects.all()
    
    def lastmod(self,obj):
        return obj.last_updated

