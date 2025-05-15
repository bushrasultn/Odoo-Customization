from odoo import models, fields, api


class FertilizerReg(models.Model):
    _name = 'fertilizer.reg'
    _description = 'Fertilizer Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(default=lambda rec: 'New')
    reg_type = fields.Selection(
        [('MNF', 'Manufacturer'), ('IPM', 'Importer'), ('DIST', 'Distributor')],
        string='Registration Type', Tracking=True)
    reg_no = fields.Char(string="Registration #", Tracking=True)
    reg_date = fields.Date(string="Registration Date", Tracking=True)
    brand = fields.Char(string="Brand", Tracking=True)
    product = fields.Many2one('product.product', string='Product', Tracking=True)
    undertaking = fields.Many2one('fertilizer.undertaking', string="Name Undertaking", Tracking=True)
    province = fields.Many2one('fertilizer.dept', string='Province/Department', Tracking=True)
    expiry_date = fields.Date(string="Expiry Date", Tracking=True)
    apply_date = fields.Date(string="Renewal Apply Date", Tracking=True)
    renewal_date = fields.Date(string="Renewal Date", Tracking=True)
    rcv_date = fields.Date(string="Renewal Received Date", Tracking=True)
    composition = fields.Char(string="Composition", Tracking=True)
    sequence = fields.Char(string='Code', default='New')
    note = fields.Html(string="Notes")
    state = fields.Selection(
        [('draft', 'Draft'), ('applied', 'Applied'),
         ('registered', 'Registered'), ('expired', 'Expired'),
         ('renewal', 'Renewal'), ], string='State',
        default='draft', Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('fertilizer.reg.sequence')
            vals['sequence'] = seq or 'New'
        return super(FertilizerReg, self).create(vals)

    @api.onchange('product')
    def _onchange_product(self):
        if self.product:
            self.brand = self.product.brand_id.name or ''
