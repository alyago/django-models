from django.db import models

from abstract import AbstractEmployer

### Support and general reference data

class USState(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'ref_us_state'
        verbose_name = "US State"
        verbose_name_plural = "US States"
        ordering = ['code']
        
    name = models.CharField(max_length=25, unique=True)
    code = models.CharField(max_length=2, unique=True)
    capital = models.CharField(max_length=25)
    largest_city = models.CharField(max_length=25)
    status = models.CharField(max_length=25,
                              help_text="State, Federal district or Territory")
    founded = models.DateField(null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s: %s" % (self.code, self.name)
    
    def get_link(self):
        if self.link.exists():
            return self.link.get().link
        return ''
    get_link.short_description = 'SH Link for US State'