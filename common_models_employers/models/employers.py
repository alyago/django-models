from django.db import models
from django.utils import timezone

from abstract import AbstractEmployer
from src_data import SrcSourceType, SrcBwPublic

### Core identity part: official name and host URL

class Employer(AbstractEmployer):
    class Meta(AbstractEmployer.Meta):
        db_table = 'employers_employer'
        unique_together = (('name', 'dedup'),)
        ordering = ['name']

    name = models.CharField(max_length=180, verbose_name='name',
                            help_text="Full legal name of the employer.")
    dedup = models.CharField(max_length=10, default='', blank=True, verbose_name='dedup',
            help_text="Leave it blank unless there is another employer with the same exact name")

    def __unicode__(self):
        return self.get_unique_name()
    
    def get_unique_name(self):
        dedup = self.dedup
        return "%s%s" % (self.name, dedup if dedup == '' else ' '+dedup)
    get_unique_name.short_description = 'Unique Name'
    
    def get_display_name(self):
        display_name = self.name
        if self.sh_display_name.exists():
            display_name = self.sh_display_name.get().name
        return display_name
    get_display_name.short_description = 'Display Name'

    # DELETE IT!
    def get_host_txt(self):
        if self.host.exists():
            return self.host.get().txt
        return ''
    get_host_txt.short_description = 'Official Website'
    # DELETE IT!
    def get_host_url(self):
        if self.host.exists():
            return self.host.get().url
        return ''

    def get_main_website(self):
        if self.main_website.exists():
            return self.main_website.get()
        return None
    get_main_website.short_description = 'Main Website'
    
    def is_linked(self):
        return self.published_link.exists()

    def get_published_link(self):
        if self.is_linked():
            return self.published_link.get().sh_link.link
        return ''
    get_published_link.short_description = 'Published Link'

    def is_published(self):
        return self.is_linked() and self.published_link.get().is_published
    is_published.boolean = True
    is_published.short_description = 'Published?'

    def is_sh_description(self):
        return self.sh_description.exists()
    is_sh_description.boolean = True
    is_sh_description.short_description = 'Description?'
    
    def get_bw(self):
        try:
            bw = SrcBwPublic.objects.filter(ticker=self.get_bw_id).get()
        except:
            bw = None
        return bw
            
    def get_all_descriptions(self):
        des = []
        bw_display = SrcSourceType.objects.filter(code='bw').get().display
        if self.is_sh_description(): # SH content
            for order in ('1', '2', '3', '4'):
                try:
                    des.append(self.sh_description.get(order=order).paragraph)
                except:
                    pass
        elif self.get_bw_id != '' and bw_display: # BW content
            bw_id = self.get_bw_id
            try:
                bw = SrcBwPublic.objects.filter(ticker=bw_id).get()
                if bw.is_short_description():
                    des.append(bw.description_short)
            except:
                pass
        return des

    def get_ciq_industry(self):
        try:
            industry = self.get_bw().capital_iq_industry
        except:
            industry = ''
        return industry
    
    def get_bw_id(self):
        try:
            bw_id = self.emp_source_ids.filter(source_type__code='bw').get().sid
        except:
            bw_id = ''
        return bw_id
    get_bw_id.short_description = 'BW ID'
    
    def get_bw_url(self):
        url = ''
        if self.emp_webprofiles.filter(webprofile_type__code = 'bw').exists():
            url = self.emp_webprofiles.filter(webprofile_type__code = 'bw').get().url
        return url
        
    def is_mapped(self):
        return self.sh_jobs_map.exists()
    is_mapped.boolean = True
    is_mapped.short_description = 'Mapped?'

    def get_traded_as(self):
        traded_as = ''
        if (self.sh_snapshot_facts.exists() and
            self.sh_snapshot_facts.filter(snapshot_fact_type__title = 'Traded As').exists()):
            traded_as = self.sh_snapshot_facts.\
                        filter(snapshot_fact_type__title = 'Traded As').\
                        get().txt
            
        return traded_as
    get_traded_as.short_description = 'Traded As'
        
    # Check social links
    def is_gplus(self):
        return (self.emp_webprofiles.exists() and
                self.emp_webprofiles.filter(webprofile_type__code = 'gp').exists())
    is_gplus.boolean = True
    is_gplus.short_description = 'G+?'
    
    def is_linkedin(self):
        return (self.emp_webprofiles.exists() and
                self.emp_webprofiles.filter(webprofile_type__code = 'in').exists())
    is_linkedin.boolean = True
    is_linkedin.short_description = 'IN?'
    
    def is_facebook(self):
        return (self.emp_webprofiles.exists() and
                self.emp_webprofiles.filter(webprofile_type__code = 'fb').exists())
    is_facebook.boolean = True
    is_facebook.short_description = 'FB?'
    
    def is_twitter(self):
        return (self.emp_webprofiles.exists() and
                self.emp_webprofiles.filter(webprofile_type__code = 'tw').exists())
    is_twitter.boolean = True
    is_twitter.short_description = 'TW?'
        

