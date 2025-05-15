from odoo import models, fields, api

class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'

    @api.onchange('mail_server_id')
    def _onchange_mail_server_id(self):
        if self.mail_server_id:
            email = self.mail_server_id.from_filter
            name = self.mail_server_id.name
            formatted_email = f'"{name}" <{email}>'
            self.email_from = formatted_email
            self.reply_to = formatted_email
