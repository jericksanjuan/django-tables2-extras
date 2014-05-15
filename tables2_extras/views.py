from vanilla import ListView
from extra_views import SearchableListMixin
from django_tables2_reports.views import ReportTableView

from .mixins import ModelSingleTableMixin, DisplaySearchMixin, DefaultTemplateMixin
from .tables import TableReport
from .config import REPORT_TEMPLATE, TABLELIST_TEMPLATE

__all__ = (
    'ModelSingleTableView', 'ModelReportTableView',
)

_PAGINATE_BY = 12


class ModelSingleTableView(DisplaySearchMixin, DefaultTemplateMixin, SearchableListMixin, ModelSingleTableMixin, ListView):
    paginate_by = _PAGINATE_BY
    default_template_name = TABLELIST_TEMPLATE


class ModelReportTableView(DisplaySearchMixin, DefaultTemplateMixin, SearchableListMixin, ModelSingleTableMixin, ReportTableView):

    """
    Add action buttons to export the table to csv and xls.
    """
    default_template_name = TABLELIST_TEMPLATE
    table_parent_class = TableReport
    table_template = REPORT_TEMPLATE
    paginate_by = _PAGINATE_BY


