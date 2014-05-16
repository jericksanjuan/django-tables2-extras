from django.core.exceptions import ImproperlyConfigured
from django_tables2 import SingleTableMixin, Table
from django_tables2 import RequestConfig

from .utils import model_table_factory, create_model_table, create_report_table
from .config import TABLE_TEMPLATE

__all__ = (
    'ModelSingleTableMixin', 'TableHelperMixin', 'DisplaySearchMixin', 'DefaultTemplateMixin'
)


class ModelSingleTableMixin(SingleTableMixin):

    """
    Automagically create a Table from the Model Info.

    Fields:
    table_fields = list or tuple of fields to display
    table_template = the template to use for rendering the table
    table_show_link = if true, make first column a link based on table_row_url
    table_row_url = urlname to use for row with object pk as param.
        If not defined, use get_absolute_url
    table_delete_url = urlname for the delete view of the model.
        If present, this will add a column for delete buttons.
    table_parent_class = the base Table model, used by subclasses.
    paginate_by = number of objects per page
    """

    table_fields = []
    table_exclude = []
    table_template = TABLE_TEMPLATE
    table_parent_class = Table
    table_show_link = True
    table_row_url = None
    table_update_url = None
    table_delete_url = None
    empty_text = 'Nothing to display'
    orderable = True
    prefix = ''
    order_by = None

    def get_table_class(self):
        if self.table_class:
            return self.table_class

        if self.model is not None:
            return model_table_factory(
                self.model, self.table_parent_class, table_fields=self.table_fields, table_exclude=self.table_exclude, table_template=self.table_template,
                table_show_link=self.table_show_link, table_row_url=self.table_row_url, table_delete_url=self.table_delete_url, empty_text=self.empty_text,
                paginate_by=self.paginate_by, orderable=self.orderable, prefix=self.prefix, order_by=self.order_by)

        msg = "'%s' must either define 'table_class' or both 'model' and " \
            "'fields', or override 'get_table_class()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)


class TableHelperMixin(object):

    """
    provide a function add_table that you can call in a get_context_data to add and configure tables from querysets
    """

    table_context_name_base = 'mtable'
    mtables = 0
    tconfig = None

    def get_new_table_context_name(self):
        return '{}{}'.format(self.table_context_name_base, self.mtables)

    def add_table(self, context, qs, table_class=None, with_report=False, context_name=None, **kwargs):
        """
        context = context from  get_context_data (dict)
        qs = the qs for the table
        table_class = Table class to use, auto generated from model if not provided.
            kwargs = will be used in the auto generation table class.
        with_report = FIXME: not showing export buttons right now.
        context_name = specify context name for the table
        """
        if not self.mtables:
            self.mtables = 0
        if not self.tconfig:
            self.config = RequestConfig(self.request)

        convert_to_list = kwargs.get('convert_to_list')
        if not table_class:
            if with_report:
                table_class = create_report_table(qs.model, **kwargs)
            else:
                table_class = create_model_table(qs.model, **kwargs)

        if convert_to_list:
            table_fields = kwargs.get('table_fields', [])
            if table_fields:
                qs_list = self.convert_qs_to_list(qs, table_fields)
            else:
                qs_list = qs.values()
            qs_list = list(qs_list)
            table = table_class(qs_list)
        else:
            table = table_class(qs)
        self.config.configure(table)
        self.mtables = self.mtables + 1
        context[context_name or self.get_new_table_context_name()] = table

    def convert_qs_to_list(self, qs, table_fields):
        qs_list = []
        for obj in qs:
            obj_dict = {}
            for f in table_fields:
                x = getattr(obj, f)
                if hasattr(x, '__call__'):
                    x = x()
                obj_dict[f] = x
            qs_list.append(obj_dict)
        return qs_list


class DisplaySearchMixin(object):
    """
    Set display_search to True if search_fields is defined.
    """
    display_search = False
    search_fields = []

    def get_display_search(self):
        if getattr(self, 'search_fields', False):
            self.display_search = True
        return self.display_search

    def get_context_data(self, **kwargs):
        ctx = super(DisplaySearchMixin, self).get_context_data(**kwargs)
        ctx['display_search'] = self.get_display_search()
        return ctx


class DefaultTemplateMixin(object):
    default_template_name = None

    def get_default_template_name(self):
        return self.default_template_name

    def get_template_names(self):
        templates = super(DefaultTemplateMixin, self).get_template_names()
        default_template = self.get_default_template_name()
        if default_template:
            templates.append(default_template)
            return templates
        return templates
