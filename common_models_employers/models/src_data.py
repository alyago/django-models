from django.db import models

from abstract import AbstractEmployer

class SrcSourceType(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = "src_source_type"
        ordering = ['code']

    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=50, unique=True,
                                   help_text="Brief description of the source type")
    url = models.URLField(max_length=100, unique=True,
                          help_text="URL base.")
    display = models.BooleanField(verbose_name="display")

    def __unicode__(self):
        return "%s: %s" % (self.code, self.description)

class SrcBwPublic(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'src_bw_public'
        unique_together = (('name', 'dedup'),)
        verbose_name = 'BW Public'
        ordering = ['name']
        
    capital_iq_industry = models.CharField(max_length=50, verbose_name="capital_iq_industry")
    country = models.CharField(max_length=50, verbose_name="country")
    description_short = models.TextField(null=True, blank=True, verbose_name="description_short")
    employees_date = models.DateField(null=True, blank=True, verbose_name="employees_date")
    employees_num = models.PositiveIntegerField(null=True, blank=True, verbose_name="employees_num")
    exchange = models.CharField(max_length=50, null=True, blank=True, verbose_name="exchange")
    hq_address = models.TextField(null=True, blank=True, verbose_name="hq_address")
    industry = models.CharField(max_length=50, null=True, blank=True, verbose_name="industry")
    industry_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="industry_code")
    is_public = models.BooleanField(verbose_name="is_public")
    letter_in = models.CharField(max_length=1, verbose_name="letter_in")
    lookup_page = models.PositiveSmallIntegerField(verbose_name="lookup_page")
    lookup_row = models.PositiveSmallIntegerField(verbose_name="lookup_row")
    
    # unique together
    name = models.CharField(max_length=180, verbose_name="name")
    dedup = models.CharField(max_length=10, default='', blank=True, verbose_name="dedup")
    
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="phone")
    region = models.CharField(max_length=10, verbose_name="region")
    sector = models.CharField(max_length=50, null=True, blank=True, verbose_name="sector")
    sector_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="sector_code")
    
    # unique
    ticker = models.CharField(max_length=20, unique=True, verbose_name="ticker")
    ticker_t = models.CharField(max_length=20, null=True, blank=True, verbose_name="ticker_t")
    ticker_e = models.CharField(max_length=20, null=True, blank=True, verbose_name="ticker_e")
    
    web_txt = models.CharField(max_length=150, null=True, blank=True, verbose_name="web_txt")
    web_url = models.URLField(max_length=150, null=True, blank=True, verbose_name="web_url")
    web_url_subdomain = models.CharField(max_length=100, null=True, blank=True, verbose_name="web_url_subdomain")
    web_url_domain = models.CharField(max_length=50, null=True, blank=True, verbose_name="web_url_domain")
    web_url_suffix = models.CharField(max_length=50, null=True, blank=True, verbose_name="web_url_suffix")
    year_founded = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="year_founded")
    
    def __unicode__(self):
        return "%s | %s | %s" % (self.name, self.country, self.ticker)
    
    def is_short_description(self):
        return self.description_short is not None
    is_short_description.boolean = True
    is_short_description.short_description = 'Description?'
