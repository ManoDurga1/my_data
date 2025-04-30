from odoo import models, api

from datetime import datetime


class ReportSalesmanSOA(models.AbstractModel):
    _name = 'report.sdm_salesman_soa_report.salesman_soa_report_template'
    _description = 'Salesman SOA Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get('form', {})
        return {
            'doc_ids': docids,
            'doc_model': 'account.move.report.wizard',
            'data': form,
            'grouped_data': form.get('grouped_data', []),
            'pdc_data': form.get('pdc_data', []),
            'salesperson': form.get('user_name'),
            'date_from': form.get('date_from'),
            'date_to': form.get('date_to'),
            'company': form.get('company'),
            'current_datetime': datetime.now().strftime('%d-%b-%Y %H:%M:%S'),
        }
