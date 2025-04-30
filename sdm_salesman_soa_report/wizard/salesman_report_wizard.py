from odoo import models, fields, api, _
from datetime import datetime

class AccountMoveReportWizard(models.TransientModel):
    _name = 'account.move.report.wizard'
    _description = 'Account Move Report Wizard'

    user_id = fields.Many2one('res.users', string='Salesperson', required=True)
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    def _get_pdc_details(self,partner_ids):


        pdc_lines = self.env['pdc.wizard'].search([('partner_id', 'in', partner_ids), ('state', '=', 'done')])
        res = []

        for line in pdc_lines:
            res.append({
                'reference': line.reference or '',
                'cheque_no': line.name or '',
                'cheque_date': line.done_date.strftime('%d/%m/%Y') if line.done_date else '',
                'amount': line.cheque_amount or 0.0,
            })
        return res

    def _get_grouped_invoice_data(self):
        domain = [
            ('responsible_id', '=', self.user_id.id),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('move_type', '=', 'out_invoice'),
        ]

        grouped_data = self.env['account.move'].read_group(
            domain=domain,
            fields=['amount_total_in_currency_signed', 'amount_residual_signed', 'partner_id'],
            groupby=['partner_id']
        )
        partner_ids = []
        partner_ids = self.env['account.move'].search(domain).filtered(lambda x: x.partner_id).mapped('partner_id.id')

        pdc_data = self._get_pdc_details(partner_ids)
        result = []
        for group in grouped_data:
            result.append({
                'partner_name': group['partner_id'][1] if group['partner_id'] else 'Undefined Partner',
                'total_amount': group.get('amount_total_in_currency_signed', 0.0),
                'residual_amount': group.get('amount_residual_signed', 0.0),
            })
        return result,pdc_data



    def action_print_report(self):
        report_data = {
            'form': {
                'user_id': self.user_id.id,
                'user_name': self.user_id.name,
                'date_from': self.date_from.strftime('%d-%m-%Y'),
                'date_to': self.date_to.strftime('%d-%m-%Y'),
                'grouped_data': self._get_grouped_invoice_data()[0],
                'pdc_data': self._get_grouped_invoice_data()[1],
                'company': {
                    'name': self.env.company.name,
                    'logo': self.env.company.logo.decode('utf-8') if self.env.company.logo else '',
                    'street': self.env.company.street,
                    'street2': self.env.company.street2,
                    'city': self.env.company.city,
                    'state': self.env.company.state_id.name if self.env.company.state_id else '',
                    'country': self.env.company.country_id.name if self.env.company.country_id else '',
                    'phone': self.env.company.phone,
                    'email': self.env.company.email,
                    'vat': self.env.company.vat,
                    'website': self.env.company.website,
                }
            }
        }


        return self.env.ref('sdm_salesman_soa_report.salesman_soa_report').report_action(self, data=report_data)
