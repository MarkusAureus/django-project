import feedparser
from celery import shared_task
from datetime import datetime
from time import mktime
from django.utils import timezone
from .models import NewsSource, Article
import logging

# Set up a logger for this task
logger = logging.getLogger(__name__)

@shared_task
def fetch_rss_feeds():
    """
    A Celery task that fetches articles from all active NewsSource RSS feeds.
    """
    active_sources = NewsSource.objects.filter(active=True)
    logger.info(f"Starting RSS feed fetch for {active_sources.count()} active sources.")
    
    for source in active_sources:
        try:
            feed = feedparser.parse(source.rss_url)
            
            # Check for common feed errors
            if feed.bozo:
                logger.warning(f"Feed for '{source.name}' is not well-formed. Bozo bit set. Reason: {feed.bozo_exception}")
                # Continue to the next source, but you might want to handle this differently
                # e.g., by deactivating the source after several failed attempts.
                
            new_articles_count = 0
            for entry in feed.entries:
                # Check if an article with the same link already exists
                if not Article.objects.filter(link=entry.link).exists():
                    
                    # Parse the published date
                    published_time_struct = entry.get('published_parsed', None)
                    if published_time_struct:
                        published_datetime = datetime.fromtimestamp(mktime(published_time_struct))
                        # Make the datetime timezone-aware
                        published_datetime = timezone.make_aware(published_datetime, timezone.get_current_timezone())
                    else:
                        # Fallback if no published date is available
                        published_datetime = timezone.now()

                    Article.objects.create(
                        source=source,
                        title=entry.title,
                        link=entry.link,
                        summary=entry.get('summary', ''),
                        published=published_datetime,
                    )
                    new_articles_count += 1
            
            if new_articles_count > 0:
                logger.info(f"Successfully fetched {new_articles_count} new articles from '{source.name}'.")
        
        except Exception as e:
            logger.error(f"An error occurred while fetching feed for '{source.name}': {e}", exc_info=True)
            
    return f"RSS feed fetch completed for {active_sources.count()} sources."

