from django.contrib import admin
from .models import NewsSource, Article, Digest, DigestArticle

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    """Admin view for NewsSource."""
    list_display = ('name', 'rss_url', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'rss_url')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin view for Article."""
    list_display = ('title', 'source', 'published')
    list_filter = ('source', 'published')
    search_fields = ('title', 'summary')
    date_hierarchy = 'published'

class DigestArticleInline(admin.TabularInline):
    """Allows adding articles to a digest directly in the digest admin page."""
    model = DigestArticle
    extra = 1 # Show one extra slot for adding an article
    raw_id_fields = ('article',) # Use a popup to select articles, better for performance

@admin.register(Digest)
class DigestAdmin(admin.ModelAdmin):
    """Admin view for Digest."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    inlines = (DigestArticleInline,)

