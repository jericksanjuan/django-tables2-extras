from django_tables2_reports.tables import TableReport


class TableReport(TableReport):
    """
    Extend TableReport to use prioritize meta.template over self._template
    """

    @property
    def template(self):
        return (self._meta.template if self._meta.template is not None
                else self._template)

    @template.setter
    def template(self, value):
        self._template = value
