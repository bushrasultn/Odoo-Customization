from odoo import models, fields, api
from datetime import datetime


class IPOReg(models.Model):
    _name = 'ipo.reg'
    _description = 'Ipo  Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(default=lambda rec: 'New')
    product = fields.Many2one('product.product', string='Product', Tracking=True)
    brand = fields.Char(string="Brand", Tracking=True)
    app = fields.Char(string="Application #:", Tracking=True)
    reg_no = fields.Char(string="Registration #", Tracking=True)
    undertaking = fields.Many2one('res.company', string="Name Undertaking", Tracking=True)
    reg_date = fields.Date(string="Registration Date", Tracking=True)
    sealed_date = fields.Date(string="Sealed Date", Tracking=True)
    apply_date = fields.Date(string="Apply Date", Tracking=True)
    expiry_date = fields.Date(string="Expiry Date", Tracking=True)
    sent_date = fields.Date(string="Renewal Sent Date", Tracking=True)
    payment_date = fields.Date(string="Payment Date", Tracking=True)
    rcv_date = fields.Date(string="Renewal Received Date", Tracking=True)
    next_date = fields.Date(string=" Next Renewal Date", Tracking=True)
    stages = fields.Many2one('stage.ipo', string=" Stages", Tracking=True)
    ipo_class = fields.Many2one('depart.reg', string="Class", Tracking="True")
    note = fields.Html(string="Notes")
    description = fields.Char(string="Description")
    sequence = fields.Char(string='Code', default='New')
    state = fields.Selection(
        [('draft', 'Draft'), ('applied', 'Applied'),('registered', 'Registered'),
         ('renewal', 'Renewal'),
         ('expired', 'Expired'),], default='draft', tracking=True, string='State')

    @api.onchange('product')
    def _onchange_product(self):
        if self.product:
            self.brand = self.product.brand_id.name or ''

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('ipo.reg.sequence')
            vals['sequence'] = seq
        return super(IPOReg, self).create(vals)

    @api.onchange('reg_date')
    def _onchange_reg_date(self):
        if self.reg_date:
            reg_date = fields.Date.from_string(self.reg_date)
            next_date = reg_date.replace(year=reg_date.year + 10)
            self.next_date = fields.Date.to_string(next_date)
