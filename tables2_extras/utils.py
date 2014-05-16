from django_tables2 import Table
from django_tables2.tables import TableOptions
from .tables import TableReport

from .config import TABLE_TEMPLATE, REPORT_TEMPLATE

__all__ = (
    'model_table_factory', 'create_model_table', 'create_report_table'
)

_PAGINATE_BY = 12


def model_table_factory(
    model, table_parent_class, table_fields=None, table_exclude=None, table_template=TABLE_TEMPLATE,
    paginate_by=_PAGINATE_BY, empty_text='Nothing to display', orderable=True, prefix='', order_by='', convert_to_list=False,
        table_row_url=None, table_update_url=None, table_delete_url=None, table_show_link=True, table_pagination=None):

    name = "{}Table".format(model.__name__)

    meta = dict(model=model, template=table_template, empty_text=empty_text,
                orderable=orderable, prefix=prefix)
    if table_fields:
        meta['fields'] = table_fields
    if table_exclude:
        meta['exclude'] = table_exclude
    if paginate_by:
        meta['per_page'] = paginate_by
    if order_by:
        meta['order_by'] = order_by
    Meta = type(TableOptions)(str('Meta'), (TableOptions,), meta)

    if convert_to_list:
        attrs = dict(Meta=Meta)
    else:
        attrs = dict(
            table_row_url=table_row_url, table_delete_url=table_delete_url, table_show_link=table_show_link,
            table_update_url=table_update_url, Meta=Meta)
    table_class = type(name, (table_parent_class,), attrs)

    return table_class


def create_model_table(model, **kwargs):
    return model_table_factory(model, Table, **kwargs)


def create_report_table(model, **kwargs):
    if not kwargs.get('table_template', None):
        kwargs['table_template'] = REPORT_TEMPLATE
    return model_table_factory(model, TableReport, **kwargs)
