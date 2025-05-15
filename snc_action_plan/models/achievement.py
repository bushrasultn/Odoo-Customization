from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrExpenseInherit(models.Model):
    _inherit = 'hr.expense'

    event_id = fields.Many2one(comodel_name='event.event', string='Event')


class Expense(models.Model):
    _name = 'nap.expense.lines'
    _description = 'NAP Expense Lines'

    nap_target_id = fields.Many2one('event.event', string="Target")
    expense_category_id = fields.Many2one('product.product', string="Expense Category")
    amount = fields.Float(string="Amount")
    description = fields.Char(string="Description")
    attach_link = fields.Char(string="File Link")

class Achievement(models.Model):
    _inherit = 'event.event'
    _description = 'NAP Achievements'

    event_id = fields.Many2one('event.event', string='Event')
    emp_id = fields.Many2one('hr.employee', string='Organized By')
    region_id = fields.Many2one('customer.region', string='Region')
    territory_id = fields.Many2one('customer.territory', string='Territory')

    mng_level = fields.Selection([('tm', 'TM'), ('rsm', 'RSM')], string='Team Level')
    verify = fields.Boolean(string='Verified', default=False)
    nap_expense_ids = fields.One2many('nap.expense.lines', 'nap_target_id', string="Expenses")
    expense_id = fields.Many2one(comodel_name='hr.expense')
    total_expense = fields.Float(string="Total Expense", compute='_compute_total_expense', store=True)
###########################################Modification in it########################
    rsm_id = fields.Many2one('hr.employee', string='RSM')
    rsm_verify = fields.Boolean(string='RSM Verification', default=False)
    demo_product_ids = fields.Many2many('product.brand', string="Demo Product")
    event_crop_ids = fields.Many2many('event.crop', string="Crop")
    cpo_name = fields.Char(string="CPO Name")

    @api.onchange('emp_id')
    def _onchange_emp_id(self):
        if self.emp_id:
            self.territory_id = self.emp_id.territory_id
            self.region_id = self.emp_id.region_id
        else:
            self.territory_id = False
            self.region_id = False

    def submit_expense(self):
        if not self.emp_id:
            raise ValidationError(_('Organized by is required!'))

        HrExpense = self.env['hr.expense']

        existing_expenses = HrExpense.search([('event_id', '=', self.id)])

        if existing_expenses:
            raise ValidationError(_('Expenses already created!'))

        for line in self.nap_expense_ids:
            if not line.expense_category_id:
                raise ValidationError(_('Expense Category is required for all expense lines!'))

            HrExpense.create({
                'name': self.name + ' - ' + (line.description or _('Event Expense')),
                'product_id': line.expense_category_id.id,
                'total_amount_currency': line.amount,
                'employee_id': self.emp_id.id,
                'payment_mode': 'own_account',
                'tax_ids': False,
                'company_id': self.company_id.id,
                'date': self.date_begin.date() if self.date_begin else fields.Date.context_today(self),
                'event_id': self.id,
            })

    def display_expenses(self):
        exp_ids = self.expense_id.search([('event_id', '=', self.id)])
        if exp_ids:
            return {
                'name': 'Expenses',
                'type': 'ir.actions.act_window',
                'res_model': 'hr.expense',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', exp_ids.ids)]
            }

    @api.depends('nap_expense_ids.amount')
    def _compute_total_expense(self):
        for event in self:
            event.total_expense = sum(line.amount for line in event.nap_expense_ids)
