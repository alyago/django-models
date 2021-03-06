from django.db import models
from django.utils import timezone

from abstract import AbstractEmployer
from employers import Employer
from ref_data import USState

### Data specific to Simply Hired: linking, publishing, content


### Linking and Publishing
class ShDisplayName(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = "sh_display_name"
        ordering = ['name']

    name = models.CharField(max_length=150,
                            help_text="Reader friendly name of the employer.")
    employer = models.ForeignKey(Employer, unique=True, related_name='sh_display_name')
    
    def __unicode__(self):
        return self.name

### Internal rating of employers      
class ShRating(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = "sh_rating"
        ordering = ['employer']
        verbose_name = "Employer With Rating"
        verbose_name_plural = "Employers With Rating"

    RATING_CHOICES = (
        ('0', "Don't display"),
        ('1', '1 star'),
        ('2', '2 stars'),
        ('3', '3 stars'),
    )
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    employer = models.ForeignKey(Employer, unique=True, related_name='sh_rating')
    
    def __unicode__(self):
        return self.rating
    
    def get_rating_stars(self):
        r = int(self.rating)
        stars = ''.join(r*[u'\u2605'])
        return stars
  
class ShLink(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = "sh_link"
        verbose_name = "SH Link"

    link = models.CharField(max_length=100, unique=True,
                            help_text="Unique identifier. To be used in URLs.")
    employer = models.ForeignKey(Employer, related_name='links')
    datetime_created = models.DateTimeField(default=timezone.now())


    def __unicode__(self):
        return self.link

    def is_published(self):
        return self.published_link.exists() and self.published_link.get().is_published
    is_published.boolean = True
    is_published.short_description = 'Is Published?'

    def publish(self):
        pl, created = self.employer.published_link.get_or_create(defaults={'sh_link': self})
        pl.sh_link = self
        pl.is_published = True
        pl.datetime_last_published = timezone.now()
        pl.save()

class ShPublishedLink(AbstractEmployer):
    """
    Published link - unique for employer.
    Used as a part of the permalink url of the employer page,
    like: http://www.simplyhired.com/employer-info-<published_link>.html
    """
    class Meta(AbstractEmployer.Meta):
        db_table = 'sh_published_link'

    employer = models.ForeignKey(Employer, unique=True, related_name='published_link')
    sh_link = models.ForeignKey(ShLink, unique=True, related_name='published_link')
    is_published = models.BooleanField(default=False)
    datetime_last_published = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return "%s | %s | %s | %s" % (self.employer.name, self.sh_link.link,
                                      str(self.datetime_last_published), str(self.is_published))
    
class ShLinkUSState(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = "sh_link_us_state"
        verbose_name = "SH Link for US State"
        ordering = ['us_state']
    
    link = models.CharField(max_length=25, unique=True,
                            help_text="Unique identifier. To be used in URLs.")
    us_state = models.ForeignKey(USState, unique=True, related_name='link')


    def __unicode__(self):
        return "%s: %s" % (self.us_state.code, self.link)


### Mapping to SimplyHired's jobs database

class ShJobsMap(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'sh_jobs_map'
        verbose_name = 'SH Jobs Database Mapping'
        
    employer = models.ForeignKey(Employer, related_name='sh_jobs_map')
    normalized_company_name = models.CharField(max_length=150, unique=True,
                                               help_text="Normalized company name in SH jobs DB.")

    def __unicode__(self):
        return self.normalized_company_name

### Content generated by SH

class ShDescription(AbstractEmployer):
    """
    4 (or less) paragraphs describing employer. Original text created by Simplyhired.
    """
    class Meta(AbstractEmployer.Meta):
        db_table = 'sh_description'
        verbose_name = 'SH Description'
        unique_together = (("employer", "order"),)
        ordering = ['order']

    PARAGRAPH_ORDER_CHOICES = (
        ('1', '1st paragraph'),
        ('2', '2nd paragraph'),
        ('3', '3rd paragraph'),
        ('4', '4th paragraph'),
    )
    order = models.CharField(max_length=1, choices=PARAGRAPH_ORDER_CHOICES)
    paragraph = models.TextField()
    employer = models.ForeignKey(Employer, related_name='sh_description')


class ShSnapshotFactType(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'sh_snapshot_fact_type'
        ordering = ['order']
        
    order = models.PositiveSmallIntegerField(unique=True,
                                             help_text="Order in a snapshot")
    title = models.CharField(max_length=50, unique=True,
                             help_text="Title in a snapshot")

    def __unicode__(self):
        return "%s: %s" % (self.order, self.title)


class ShSnapshotFact(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'sh_snapshot_fact'
        ordering = ['snapshot_fact_type']
        verbose_name = 'SH Snapshot Fact'
        unique_together = (("employer", "snapshot_fact_type"),)
        
    employer = models.ForeignKey(Employer, related_name='sh_snapshot_facts')
    snapshot_fact_type = models.ForeignKey(ShSnapshotFactType)
    txt = models.TextField()

    def __unicode__(self):
        return "%s: %s ..." % (self.snapshot_fact_type.title, self.txt[:10])
