from django.db import models

from abstract import AbstractEmployer
from employers import Employer
from src_data import SrcSourceType

class EmpSourceId(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_source_id'
        unique_together = (('employer', 'source_type'),
                           ('sid', 'source_type'),)
        
    employer = models.ForeignKey(Employer, related_name='emp_source_ids')
    source_type = models.ForeignKey(SrcSourceType, related_name='emp_source_ids')
    sid = models.CharField(max_length=20, verbose_name='sid')

    def __unicode__(self):
        return "%s: %s" % (self.source_type.code, self.sid)

class EmpWebsiteType(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_website_type'
        ordering = ['code']

    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=50, unique=True,
                                   help_text="Brief description of the website type.")

    def __unicode__(self):
        return "%s: %s" % (self.code, self.description)


class EmpWebsite(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_website'
        unique_together = (('url', 'dedup'),
                           ('employer', 'url'),)
        ordering = ['employer', 'txt']

    employer = models.ForeignKey(Employer, related_name='emp_websites')
    url = models.URLField(max_length=100,
                          help_text="URL of this web site.")
    dedup = models.CharField(max_length=15, default='', blank=True, verbose_name='dedup' ,
            help_text="Leave it blank unless there is another website with the same exact url")
    txt = models.CharField(max_length=100, null=True, blank=True,
            help_text="How do you want to display it? Recommended format: www.example.com")
    description = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Brief description of the website.")
    website_type = models.ForeignKey(EmpWebsiteType, null=True, blank=True,
                                     related_name='emp_websites')
    url_subdomain = models.CharField(max_length=50, null=True, blank=True,
                                     verbose_name="url_subdomain")
    url_domain = models.CharField(max_length=50, null=True, blank=True,
                                  verbose_name="url_domain")
    url_suffix = models.CharField(max_length=50, null=True, blank=True,
                                  verbose_name="url_suffix")

    def __unicode__(self):
        return "%s %s" % (self.url, self.dedup if self.dedup else '')
    
    def is_marked_as_main(self):
        return self.main_website.exists()
    is_marked_as_main.boolean = True
    is_marked_as_main.short_description = 'Is Main?'
    
    def mark_as_main(self):
        mw, created = self.employer.main_website.get_or_create(defaults={'website': self})
        if not created:
            mw.website = self
            mw.save()

class EmpWebsiteMain(AbstractEmployer):
    """
    Main Website - unique for employer.
    Used when there are multiple domains for employer
    to mark the one which is "main official"
    """
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_website_main'

    employer = models.ForeignKey(Employer, unique=True, related_name='main_website')
    website = models.ForeignKey(EmpWebsite, unique=True, related_name='main_website')

    def __unicode__(self):
        return "%s | %s" % (self.website, self.website.txt)
    
    
class EmpWebprofileType(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_webprofile_type'
        ordering = ['code']

    TIER_CHOICES = (
        ('1', '1 - Social'),
        ('2', '2 - Social'),
        ('3', '3 - Other'),
    )
    
    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=50, unique=True,
                                   help_text="Brief description of the webprofile type, like 'LinkedIn'")
    display = models.BooleanField(default=True)    
    order = models.PositiveSmallIntegerField(unique=True,
                                             help_text="Order in a snapshot")
    tier = models.CharField(max_length=1, choices=TIER_CHOICES,
                                             help_text="Grouping in a snapshot")

    def __unicode__(self):
        return "%s %s: %s - %s - %s" % ('+' if self.display else '-', self.code,
                                   self.description, self.tier, self.order)


class EmpWebprofile(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'emp_webprofile'
        ordering = ['webprofile_type']

    employer = models.ForeignKey(Employer, related_name='emp_webprofiles')
    webprofile_type = models.ForeignKey(EmpWebprofileType, related_name='emp_webprofiles')
    url = models.URLField(max_length=100, unique=True, help_text="URL of this webprofile.")
    description = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Brief description of the webprofile.")

    def __unicode__(self):
        return "%s: %s" % (self.webprofile_type.code, self.url)
