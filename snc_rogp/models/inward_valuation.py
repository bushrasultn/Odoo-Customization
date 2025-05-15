from odoo import models, fields


class InwardValuation(models.Model):
    _name = 'inward.valuation'
    _description = 'Inward Valuation'

    inwardable_id = fields.Many2one(
        comodel_name='gate.pass',
        string='Inward Returnable'
    )
    inward_id = fields.Many2one('gate.pass', string="Inward")
    name = fields.Char(default=lambda rec: 'New')
    cont = fields.Many2one('res.partner', string='Contact')
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse')
    source = fields.Many2one('return.location', string='Source Location')
    destination = fields.Many2one('return.location', string='Destination Location')
    doc_type = fields.Selection(
        [('returnable inward', 'Returnable Inward'), ('returnable outward', 'Returnable Outward')],
        string='Document Type',
        required=True
    )
    date = fields.Date(string='Date')
    remark = fields.Text(string='Remarks')
    state = fields.Selection(
        [('open', 'Open'), ('submitted', 'Submitted')],
        default='open', tracking=True, string='State'
    )
    rigp_state = fields.Selection(
        [('open', 'Open'), ('partially_returned', 'Partially Returned'), ('returned', 'Returned')],
        string='RIGP State', tracking=True
    )
    inward_val_line_ids = fields.One2many('inward.returnable.valuation.line', 'inward_val_id', string="Lines")
    inward_records = fields.Many2one('gate.pass', string='RIGP NO', domain="[('doc_type','=','returnable inward')]")
    sequence = fields.Char(string='Code', default='New')

# ..................................................................................................
class InwardReturnableValuationLines(models.Model):
    _name = 'inward.returnable.valuation.line'
    _description = 'Returnable Valuation Line'

    inward_val_id = fields.Many2one(
        comodel_name='inward.valuation',
        string='Inward Valuation',
        required=True
    )
    inwardable_id = fields.Many2one(
        comodel_name='gate.pass',
        string='Inward Returnable'
    )
    name = fields.Char(default=lambda rec: 'New')
    cont = fields.Many2one('res.partner', string='Contact')
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse')
    source = fields.Many2one('return.location', string='Source Location')
    destination = fields.Many2one('return.location', string='Destination Location')
    date = fields.Date(string='Date')
    remark = fields.Text(string='Remarks')
    state = fields.Selection(
        [('open', 'Open'), ('submitted', 'Submitted')],
        default='open', tracking=True, string='State'
    )
    product_id = fields.Many2one('product.product', string="Product", required=True)
    specify = fields.Text(string='Specification')
    quantity = fields.Float(string='Quantity', default=1, required=True)
    unit_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    doc_type = fields.Selection(
        [('returnable inward', 'Returnable Inward'), ('returnable outward', 'Returnable Outward')],
        string='Document Type',
        required=True
    )
    inward_id = fields.Many2one('gate.pass', string="Outward")
