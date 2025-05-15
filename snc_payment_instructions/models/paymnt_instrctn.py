from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, AccessError


class PaymentInstructions(models.Model):
    _name = 'payment.instruction'
    _description = 'Payment Instructions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "create_date DESC"

    name = fields.Char(default=lambda rec: 'New')
    sequence = fields.Char(string='Code', default='New')
    party = fields.Many2one('res.partner', string="Party/Partners", tracking=True, required=True)
    date = fields.Datetime(string="Date", default=fields.Datetime.now, tracking=True)
    release = fields.Float(string="Release Request", tracking=True, digits=(16, 0))
    note = fields.Html(string="Notes")
    # tax_amount = fields.Float(string="Tax Amount", tracking=True,readonly=1)
    amount_pay = fields.Float(string="Amount To Pay", compute='_compute_amount_pay', store=True, digits=(16, 0))
    payment_against = fields.Selection([
        ('advance', 'Advance'),
        ('ledger_balance', 'Ledger Balance'),
        ('bill_in_hand', 'Bill in Hand'),
        ('final_payment', 'Final Payment')
    ],tracking=True)
    payment_against_inst = fields.Selection([
        ('advance', 'Advance'),
        ('ledger_balance', 'Ledger Balance'),
        ('bill_in_hand', 'Bill in Hand'),
        ('final_payment', 'Final Payment')
    ], tracking=True, required=True, string='Payment Against')
    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'),
         ('review', 'Reviewed'), ('audit manager', 'Audit Manager'), ('approved', 'Approved'), ('paid', 'Paid'),
         ('Cancelled', 'Cancelled')],
        default='draft', tracking=True, string='State'
    )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    payee = fields.Boolean(string="Payee Not Registered", tracking=True)
    balance = fields.Float(string="Balance", store=True)
    ntn = fields.Char(string='NTN', store=True)
    account_ids = fields.Many2many(
        comodel_name='custom.accounts'
    )
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    payee_amount = fields.Float(string="Total Amount", compute='_compute_payee_amount', store=True)
    account_lines = fields.One2many('instruction.lines', 'payment_instruction_id', string="Account Lines")
    register_lines = fields.One2many('instruction.lines', 'non_registered_id', string="Non Register Lines")
    ###################################################################################################
    tax = fields.Boolean(string="Tax Deduction", tracking=True)
    tax_rate = fields.Float(string="Tax Rate", digits=(16, 4))
    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount", store=True, tracking=True,
                              readonly=True, digits=(16, 0))
    @api.depends('release', 'tax_rate')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = (record.release * record.tax_rate) / 100 if record.release and record.tax_rate else 0
    ###################################################################################################
    submit_by = fields.Many2one('res.users', string="Submitted By", readonly=True)
    review_by = fields.Many2one('res.users', string="Reviewed By", readonly=True)
    approval_by = fields.Many2one('res.users', string="Approved By", readonly=True)
    approve_by = fields.Many2one('res.users', string="Final Approval By", readonly=True)
    ###################################################################################################
    @api.onchange('party')
    def _onchange_party(self):
        if self.party:
            self.ntn = self.party.ntn
            self.fetch_balance()
            self.account_ids = [(6, 0, self.party.customization_ids.filtered(lambda rec: rec.is_active).account_id.ids)]
    ########################################Calculate Balance############################################################
    def fetch_balance(self):
        for record in self:
            if record.party:
                debit_credit_lines = self.env['account.move.line'].search([
                    ('move_id.state', '=', 'posted'),
                    ('partner_id', '=', record.party.id)
                ])
                pay_recv_accounts = self.env['account.account'].search(
                    [('account_type', 'in', ['asset_receivable', 'liability_payable'])])
                debit_credit_lines = debit_credit_lines.filtered(lambda rec: rec.account_id.id in pay_recv_accounts.ids)
                debit = sum(debit_credit_lines.mapped('debit'))
                credit = sum(debit_credit_lines.mapped('credit'))
                record.balance = debit - credit
            else:
                record.balance = 0.0
    ####################################################################################################
    @api.depends('account_lines.amount')
    def _compute_total_amount(self):
        for instruction in self:
            instruction.total_amount = sum(line.amount for line in instruction.account_lines)

    @api.depends('register_lines.non_payee_amount')
    def _compute_payee_amount(self):
        for instruction in self:
            instruction.payee_amount = sum(line.non_payee_amount for line in instruction.register_lines)

    def _check_amounts_equal(self):
        for record in self:
            if record.amount_pay != record.total_amount:
                if record.amount_pay != record.payee_amount:
                    raise ValidationError("The Amount must be equal !.")

    @api.depends('release', 'tax_amount', 'tax')
    def _compute_amount_pay(self):
        for record in self:
            if record.tax:
                record.amount_pay = record.release - record.tax_amount
            else:
                record.amount_pay = record.release

    def action_draft(self):
        if self.state == 'submitted':
            raise UserError("Cannot changed record once the record is submitted.")
        self.state = 'draft'
        # self.state = False

    def action_submit(self):
        for record in self:
            self._check_amounts_equal()
            record.submit_by = self.env.user.id
        self.state = 'submitted'

    def action_review(self):
        for record in self:
            self._check_amounts_equal()
            record.review_by = self.env.user.id
        self.state = 'review'

    def action_approval(self):
        for record in self:
            self._check_amounts_equal()
            record.approval_by = self.env.user.id
        self.state = 'audit manager'

    def action_approve(self):
        for record in self:
            record.approve_by = self.env.user.id
            self._check_amounts_equal()
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'Cancelled'
    ##############################################New Changing######################################################
    def action_paid(self):
        """Set state to 'paid' if it's currently 'approved'."""
        for record in self:
            if record.state == 'approved':
                record.write({'state': 'paid'})
            else:
                raise UserError("Only approved records can be marked as paid.")

    # def write(self, vals):
    #     if any(record.state == 'approved' for record in self):
    #         if 'state' in vals and vals['state'] == 'paid':
    #             return super(PaymentInstructions, self).write(vals)
    #         raise UserError("Cannot modify a record once it is in the 'approved' state!")
    #     return super(PaymentInstructions, self).write(vals)
    ####################################################################################################

    @api.model
    def create(self, vals):
        if vals.get('name') == 'New':
            seq = self.env['ir.sequence'].next_by_code('payment.instruction.sequence')
            vals['name'] = seq
        return super(PaymentInstructions, self).create(vals)

    def update_payment_against(self):
        for line in self.search([]):
            payment_state = 'advance'
            if line.payment_against == 'advance':
                payment_state = 'advance'
            elif line.payment_against == 'ledger balance':
                payment_state = 'ledger_balance'
            elif line.payment_against == 'bill in hand':
                payment_state = 'bill_in_hand'
            else:
                payment_state = 'final_payment'

            line.payment_against_inst = payment_state

    def update_states_from_logs(self):
        instructions = self.search([('state', '=', False)])

        for record in self:
            state_logs = self.env['mail.message'].search([('res_id', '=', record.id),('model', '=', 'payment.instruction'),], order='create_date desc', limit=1)

            if state_logs:
                state = 'draft'
                if state_logs.tracking_value_ids.new_value_char == 'Draft':
                    state = 'draft'

                elif state_logs.tracking_value_ids.new_value_char == 'Submitted':
                    state = 'submitted'

                elif state_logs.tracking_value_ids.new_value_char == 'Reviewed':
                    state = 'review'

                elif state_logs.tracking_value_ids.new_value_char == 'Manager Approved':
                    state = 'audit manager'

                elif state_logs.tracking_value_ids.new_value_char == 'Paid':
                    state = 'paid'

                elif state_logs.tracking_value_ids.new_value_char == 'Approved':
                    state = 'approved'

                elif state_logs.tracking_value_ids.new_value_char == 'Cancelled':
                    state = 'Cancelled'

                record.state = state

    #function used to open partner ledger wizard
    def open_partner_ledger_wizard(self):
        view_id = self.env.ref('snc_custom_report.partner_ledger_report_form')

        return {
            'name': ('Partner Ledger'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'partner.ledger.report.wizard',
            'view_id': view_id.id,
            'context': {'default_partner_id': self.party.id},
            'target': 'new'
        }

    ##########################################ONE2MANY MODEL##########################################################
class AccountLines(models.Model):
    _name = 'instruction.lines'
    _description = 'Instruction Lines'

    name = fields.Char(string='Account Title')
    payment_instruction_id = fields.Many2one('payment.instruction', string='Payment Instruction')
    non_registered_id = fields.Many2one('payment.instruction', string='Payment Instruction')
    instruction = fields.Many2one('pymnt_instruction.method', string='Payment Method')
    amount = fields.Float(string="Amount")
    non_payee_amount = fields.Float(string="Amount", digits=(16, 0))
    bank = fields.Char(string="Bank", tracking=True, store=True)
    account_no = fields.Char(string="Account Number", tracking=True, store=True)
    account_title = fields.Char(string="Account Title", store=True)
    ntn = fields.Char(string='NTN', store=True)
    account_id = fields.Many2one(
        comodel_name='custom.accounts',
        string="Account"
    )
    ###########################################ACCOUNt id#########################################################
    @api.onchange('account_id')
    def _onchange_partner_customization(self):
        if self.account_id:
            partner_customization = self.env['partners.customization'].search([('account_id', '=', self.account_id.id)],
                                                                              limit=1)
            if partner_customization:
                self.ntn = partner_customization.ntn
                self.bank = partner_customization.bank
                self.account_no = partner_customization.account_no
                self.account_title = partner_customization.account_title
            else:
                self.ntn = self.account_id.ntn if hasattr(self.account_id, 'ntn') else False
                self.bank = self.account_id.bank if hasattr(self.account_id, 'bank') else False
                self.account_no = self.account_id.account_no if hasattr(self.account_id, 'account_no') else False
                self.account_title = self.account_id.account_title if hasattr(self.account_id,
                                                                              'account_title') else False
        else:
            self.ntn = False
            self.bank = False
            self.account_no = False
            self.account_title = False

    ####################################################################################################
class PartnersCustomization(models.Model):
    _name = 'partners.customization'
    _description = 'Customization in partner'
    _rec_name = 'account_title'

    is_active = fields.Boolean(string="Is Active", default=True, store=True)
    account_title = fields.Char(string="Title of Accounts", tracking=True, store=True)
    bank = fields.Char(string="Bank", store=True)
    account_no = fields.Char(string="Account#", store=True)
    pi_id = fields.Many2one('res.partner', string="Partner", required=True, store=True)
    ntn = fields.Char(string='NTN', store=True)
    account_id = fields.Many2one(
        comodel_name='custom.accounts',
        string="Account"
    )
    customization_ids = fields.One2many(
        'partners.customization', 'account_id', string="Customization"
    )

    ##############################################Inherit######################################################
class ResPartner(models.Model):
    _inherit = 'res.partner'

    customization_ids = fields.One2many(
        'partners.customization', 'pi_id', string="Payee Details"
    )
    ####################################################################################################
