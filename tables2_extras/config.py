from django.conf import settings

TABLE_TEMPLATE = getattr(settings, 'TABLES2_DEFAULT_TEMPLATE', 'tables2_extras/table.html')
REPORT_TEMPLATE = getattr(settings, 'TABLES2_REPORT_TEMPLATE', 'tables2_extras/report.html')

TABLELIST_TEMPLATE = getattr(settings, 'TABLES2_TABLELIST_TEMPLATE', 'tables2_extras/base_table_list.html')
