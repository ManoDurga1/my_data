from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AddExtraRequirement(models.Model):
    _name = 'sdm.extra.requirement'
    _description = 'Add Extra Requirement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', default='New')
    task_name = fields.Char(string='Task Name', required=True, tracking=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    project_id = fields.Many2one('project.project', string='Project',required=True ,tracking=True)
    consultant_id = fields.Many2one('res.users', string='Requested By' ,required=True,tracking=True)
    evaluated_by_id = fields.Many2one('hr.employee', string='Evaluated By',required=True,tracking=True)
    requested_date = fields.Date(string='Requested Date', default=fields.Date.today, tracking=True)
    expected_completion = fields.Date(string='Expected Completion',required=True, tracking=True)
    dev_hours = fields.Float(string='Dev Hours', required=True ,tracking=True)
    description = fields.Text(string='Requirement description')
    is_billable = fields.Boolean(string='Is Billable', default=False)
    task_count = fields.Integer(string='Task Count', compute='_compute_task_count')
    is_approved = fields.Boolean(string='Is Approved', default=False)

    def _compute_task_count(self):
        for rec in self:
            task_count = self.env['project.task'].search_count([('sequence', '=', rec.name)])
            rec.task_count = task_count

    # @api.constrains('dev_hours')
    # def _check_dev_hours_positive(self):
    #     for record in self:
    #         if record.dev_hours <= 0:
    #             raise ValidationError("Dev Hours must be greater than 0.")



    state = fields.Selection([
        ('new', 'New'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('task_created', 'Task Created'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], default='new', string="Status", tracking=True)

    quotation_ids = fields.One2many('sale.order', 'requirement_id', string="Quotations")
    quotation_count = fields.Integer(compute='_compute_quotation_count', string="Quotation Count")

    def _compute_quotation_count(self):
        for record in self:
            record.quotation_count = len(record.quotation_ids)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for rec in self:
            if rec.project_id:
                rec.customer_id = rec.project_id.partner_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sdm.extra.requirement') or 'New'
        return super().create(vals)


    def action_submit(self):
        for rec in self:
            rec.state = 'waiting'

    def action_approve(self):
        for rec in self:
            if rec.dev_hours <= 0:
                raise ValidationError("Dev Hours must be greater than 0.")
            rec.state = 'approved'
            rec.is_approved = True

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_create_quotation(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'context': {
                'default_requirement_id': self.id,
                'default_partner_id': self.customer_id.id if self.customer_id else False,
            },
            'target': 'current',
        }

    def action_complete(self):
        for rec in self:
            rec.state = 'completed'

    def action_close(self):
        for rec in self:
            rec.state = 'closed'

    # Create a button to create a task from the requirement in project.task model 
    def action_create_task(self):
        Task = self.env['project.task']
        for rec in self:
            if not rec.project_id:
                raise UserError("Please select a Project before creating a task.")

            task = Task.create({
                'name': rec.task_name,
                'sequence': rec.name,
                'project_id': rec.project_id.id,
                'user_ids': [(6, 0, [rec.consultant_id.id])] if rec.consultant_id else False,
                'partner_id': rec.customer_id.id,
                'date_deadline': rec.expected_completion,
                'allocated_hours': rec.dev_hours,
                'description': rec.description or '',
            })
            rec.state = 'task_created'
            return True

    # Create a button to view open tasks related to this requirement
    def action_view_open_tasks(self):
        self.ensure_one()
        task_ids = self.env['project.task'].search([('sequence', '=', self.name)])
        if not task_ids:
            raise UserError("No open tasks found for this project.")
        return {
            'name': 'Open Tasks',
            'view_mode': 'list,form',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', task_ids.ids)],
        }

    def action_view_quotations(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['context'] = {
            'default_requirement_id': self.id,
            'default_partner_id': self.customer_id.id if self.customer_id else False,
            'search_default_draft': 1,
        }
        action['domain'] = [('requirement_id', '=', self.id)]

        quotations = self.quotation_ids
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id

        return action



class ProjectTask(models.Model):
    _inherit = 'project.task'

    sequence = fields.Char(string='Sequence')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    requirement_id = fields.Many2one('sdm.extra.requirement', string='Requirement')