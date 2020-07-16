from __future__ import unicode_literals

DECIMAL_SEPARATOR = ','

THOUSAND_SEPARATOR = '.'

USE_THOUSAND_SEPARATOR = True

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y'  # 'H:i'

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%Y/%m/%d']
DATETIME_INPUT_FORMATS = ('%Y-%m-%d %H:%M:%S',
                          '%Y/%m/%d %H:%M:%S',
                          '%Y-%m-%d %H:%M',
                          '%Y/%m/%d %H:%M'
                          )
