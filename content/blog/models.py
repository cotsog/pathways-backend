from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class BlogIndexPage(Page):
    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context()
        context['blog_entries'] = BlogPage.objects.child_of(self).live()
        return context


class BlogPage(Page):
    body = RichTextField()
    date = models.DateField('Post date')
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname='full'),
        InlinePanel('related_links', label='Related links'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, 'Common page configuration'),
        ImageChooserPanel('feed_image'),
    ]

    parent_page_types = ['BlogIndexPage']
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
