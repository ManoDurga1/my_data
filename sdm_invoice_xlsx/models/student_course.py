from odoo import models, fields, api
from odoo.tools import html2plaintext


class Student(models.Model):
    _name = 'academy.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables Chatter
    _description = 'Student'

    name = fields.Char(string='Student Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    father_name = fields.Char(string='Father Name', required=True, tracking=True)
    mother_name = fields.Char(string='Mother Name', required=True, tracking=True)
    mobile = fields.Char(string='Mobile Number', required=True, tracking=True)
    course_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='draft', string='Course Status', tracking=True)

    def start_course(self):
        for rec in self:
            rec.course_state = 'in_progress'

            message_body = f"📘 Course started for <b>{rec.name}</b>."
            # rec.message_post(
            #     body=message_body,
            #     message_type='notification',
            #     subtype_xmlid='mail.mt_note',
            #     partner_ids=[rec.user_id.partner_id.id],  # Notify the student user
            #     body_is_html=True
            # )

            # Optionally, send an email notification (if you want to notify via email)
            rec.message_post(
                body=f"Course has started for {rec.name}.",
                message_type='email',
                email_from=self.env.user.email,
                subject="Course Started"
            )

    def complete_course(self):
        for rec in self:
            rec.course_state = 'completed'

            message_body = f"🎓 Course completed for <b>{rec.name}</b>."
            # rec.message_post(
            #     body=message_body,
            #     message_type='notification',
            #     subtype_xmlid='mail.mt_note',
            #     partner_ids=[rec.user_id.partner_id.id],  # Notify the student user
            #     body_is_html=True  # Allow HTML content
            # )

            # Optionally, send an email notification
            rec.message_post(
                body=f"The course has been completed for {rec.name}.",
                message_type='email',
                email_from=self.env.user.email,
                subject="Course Completed"
            )
