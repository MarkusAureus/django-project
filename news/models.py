from django.db import models

class NewsSource(models.Model):
    """Represents a source of news, typically an RSS feed."""
    name = models.CharField(max_length=255)
    rss_url = models.URLField()
    active = models.BooleanField(default=True, help_text="Set to false to stop fetching articles from this source.")

    def __str__(self):
        return self.name

class Article(models.Model):
    """Represents a single article fetched from a NewsSource."""
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=500, unique=True) # unique=True prevents duplicate articles
    published = models.DateTimeField()
    summary = models.TextField()

    class Meta:
        ordering = ['-published'] # Show newest articles first

    def __str__(self):
        return self.title

class Digest(models.Model):
    """A curated collection of articles."""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    articles = models.ManyToManyField(Article, through='DigestArticle', related_name='digests')

    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%Y-%m-%d')})"

class DigestArticle(models.Model):
    """Intermediate model to link Digests and Articles."""
    digest = models.ForeignKey(Digest, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('digest', 'article') # Prevent adding the same article to a digest more than once

    def __str__(self):
        return f"{self.digest.name} - {self.article.title}"

