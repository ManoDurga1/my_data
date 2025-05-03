from odoo import models, fields

class InvoiceXlsxWizard(models.TransientModel):
    _name = 'invoice.xlsx.wizard'
    _description = 'Invoice XLSX Report Wizard'

    partner_id = fields.Many2one('res.partner', string="Customer")
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    company_id = fields.Many2one('res.company', string="Company")

    def action_generate_report(self):
        return self.env.ref('sdm_invoice_xlsx.action_invoice_xlsx_report').report_action(self)
