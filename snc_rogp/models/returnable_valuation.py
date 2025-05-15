from odoo import models, fields


class ReturnableValuation(models.Model):
    _name = 'returnable.valuation'
    _description = 'Returnable Valuation'


    returnable_id = fields.Many2one(
        comodel_name='gate.pass',
        string='Returnable'
    )
    outward_id = fields.Many2one('gate.pass', string="Outward")
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
    rogp_state = fields.Selection(
        [
            ('open', 'Open'),
            ('partially_returned', 'Partially Returned'),
            ('returned', 'Returned'),
            ('returnable_out', 'Returnable Out')
        ],
        string='ROGP State',
        domain="[('doc_type', '=', 'returnable inward')]"
    )
    returnable_val_line_ids = fields.One2many('returnable.valuation.line', 'returnable_val_id', string="Lines")
    outward_records = fields.Many2one('gate.pass', string='ROGP NO', domain="[('doc_type','=','returnable outward')]")
    sequence = fields.Char(string='Code', default='New')


class ReturnableValuationLines(models.Model):
    _name = 'returnable.valuation.line'
    _description = 'Returnable Valuation Line'

    returnable_id = fields.Many2one(
        comodel_name='gate.pass',
        string='Returnable'
    )
    returnable_val_id = fields.Many2one(
        comodel_name='returnable.valuation',
        string='Returnable Valuation'
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
    state = fields.Selection(
        [('open', 'Open'), ('submitted', 'Submitted')],
        default='open', tracking=True, string='State'
    )
    doc_type = fields.Selection(
        [('returnable inward', 'returnable Inward'), ('returnable outward', 'returnable Outward')],
        string='Document Type',
        required=True
    )
    outward_id = fields.Many2one('gate.pass', string="Outward")
