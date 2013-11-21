
#DATABASES['employers'] =
EMPLOYERS_DATABASES = {
    'employers': {
        # DROP DATABASE IF EXISTS employer_pages;
        # CREATE DATABASE IF NOT EXISTS employer_pages
        # DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
        
        # mysql -u readonly -preadonly -h db-jobs-100.ksjc.sh.colo
        # mysql -u emppages_rw -pPixiyuhO -h employerpages-jobs-rw.ksjc.sh.colo employer_pages
        
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employer_pages',
        'USER': 'readonly',
        'PASSWORD': 'readonly',
        'HOST': 'employerpages-jobs-rw.ksjc.sh.colo',           
        'PORT': '',          
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB, \
                            character_set_connection=utf8mb4, \
                            collation_connection=utf8mb4_unicode_ci;',
        }
    },
}
