import io
import base64
from odoo import models

class InvoiceXlsxReport(models.AbstractModel):
    _name = 'report.sdm_invoice_xlsx.invoice_xlsx_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizards):
        wizard = wizards[0] if wizards else None
        sheet = workbook.add_worksheet('Invoices')
        bold = workbook.add_format({'bold': True})

        title_format = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#F5F5F5'})
        text_format = workbook.add_format({'font_size': 11})
        amount_format = workbook.add_format({'font_size': 11, 'num_format': '#,##0.00', 'align': 'right'})

        row = 0
        column = 0

        company = wizard.company_id if wizard and wizard.company_id else self.env.company
        logo = company.logo or company.parent_id.logo
        if logo:
            logo_data = io.BytesIO(base64.b64decode(logo))
            sheet.insert_image(row, 0, "logo.png", {'image_data': logo_data, 'x_scale': 0.5, 'y_scale': 0.5})

        row = 1
        sheet.merge_range(column, 2, row, 5, 'INVOICE REPORT', title_format)
        row += 2


        domain = [('move_type', '=', 'out_invoice')]

        if wizard:
            if wizard.partner_id:
                domain.append(('partner_id', '=', wizard.partner_id.id))
            if wizard.date_from:
                domain.append(('invoice_date', '>=', wizard.date_from))
            if wizard.date_to:
                domain.append(('invoice_date', '<=', wizard.date_to))
            if wizard.company_id:
                domain.append(('company_id', '=', wizard.company_id.id))

        invoices = self.env['account.move'].search(domain, order='invoice_date asc')


        sheet.set_column(0, 0, 9)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 18)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 10)


        row += 2
        sheet.write(row, 0, "Sl.No", header_format)
        sheet.write(row, 1, "Invoice No", header_format)
        sheet.write(row, 2, "Customer", header_format)
        sheet.write(row, 3, "Reference", header_format)
        sheet.write(row, 4, "Product", header_format)
        sheet.write(row, 5, "Amount", header_format)


        serial = 1
        row += 1
        for inv in invoices:
            for line in inv.invoice_line_ids:
                sheet.write(row, 0, serial, text_format)
                sheet.write(row, 1, inv.name or '', text_format)
                sheet.write(row, 2, inv.partner_id.name or '', text_format)
                sheet.write(row, 3, inv.invoice_origin or '', text_format)
                sheet.write(row, 4, line.product_id.display_name or '', text_format)
                sheet.write(row, 5, line.price_subtotal or 0.0, amount_format)
                row += 1
                serial += 1
