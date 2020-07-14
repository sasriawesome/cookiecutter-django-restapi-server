from __future__ import unicode_literals

DECIMAL_SEPARATOR = ','

THOUSAND_SEPARATOR = '.'

USE_THOUSAND_SEPARATOR = True

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y'  # 'H:i'

DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']
DATETIME_INPUT_FORMATS = ('%d-%m-%Y %H:%M:%S',
                          '%d/%m/%Y %H:%M:%S',
                          '%d-%m-%Y %H:%M',
                          '%d/%m/%Y %H:%M'
                          )
