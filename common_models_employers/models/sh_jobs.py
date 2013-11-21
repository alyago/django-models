from django.db import models

from abstract import AbstractEmployer
from employers import Employer

class JobsCompany(AbstractEmployer):
    """
    INSERT INTO jobs_company (normalized_company_name,company_hash,parent,source_type,type,domain,url,page_title,validate,ppr_validated)
    SELECT normalized_company_name,company_hash,parent,source_type,type,domain,url,page_title,validate,ppr_validated
    FROM Companies;
    """
    class Meta(AbstractEmployer.Meta):
        db_table = "jobs_company"
        verbose_name = "jobs_company"
        verbose_name_plural = "jobs_company"
        ordering = ['normalized_company_name']
    
    normalized_company_name = models.CharField(max_length=191, unique=True,
                                               verbose_name="normalized_company_name")
    company_hash = models.CharField(max_length=32, null=True, blank=True,
                                    verbose_name="company_hash")
    parent = models.CharField(max_length=255, null=True, blank=True,
                              verbose_name="parent")
    source_type = models.CharField(max_length=255, null=True, blank=True,
                                   verbose_name="source_type")
    c_type = models.CharField(max_length=1, null=True, blank=True,
                              db_column='type',
                              verbose_name="type")
    domain = models.CharField(max_length=100, null=True, blank=True,
                              db_index=True,
                              verbose_name="domain")
    url = models.CharField(max_length=100, null=True, blank=True,
                           verbose_name="url")
    page_title = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name="page_title")
    validate = models.CharField(max_length=1, null=True, blank=True,
                                verbose_name="validate")
    ppr_validated = models.CharField(max_length=1, null=True, blank=True,
                                     verbose_name="ppr_validated")
    
    canonical_company_name = models.CharField(max_length=191, null=True, blank=True,
                                              db_index=True,
                                              verbose_name="canonical_company_name")
    employer = models.ForeignKey(Employer, null=True, blank=True,
                                 related_name='jobs_companies')
    domain_subdomain = models.CharField(max_length=100, null=True, blank=True,
                                        db_index=True,
                                        verbose_name="domain_subdomain")
    domain_domain = models.CharField(max_length=100, null=True, blank=True,
                                     db_index=True,
                                     verbose_name="domain_domain")
    domain_suffix = models.CharField(max_length=100, null=True, blank=True,
                                     verbose_name="domain_suffix")
    done = models.BooleanField(verbose_name="done")
    
    def __unicode__(self):
        return self.normalized_company_name
    
