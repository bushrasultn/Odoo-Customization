from odoo import fields, models, api


class QualityControl(models.Model):
    _inherit = 'quality.point'
    _order = 'create_date desc'


    qc_temp_model_id = fields.Many2one('model.points', 'QC Template')

    @api.onchange('qc_temp_model_id')
    def _onchange_template_id(self):
        if self.qc_temp_model_id:
            self.note = self.qc_temp_model_id.note


                 # MODIFICATION IN QUALITY CHECK FORM

class QualityCheck(models.Model):
    _inherit = "quality.check"
    _order = 'create_date desc'

    mfg = fields.Date(string="Mfg Date")
    exp = fields.Date(string="Exp Date")
    receive = fields.Datetime(string='Sample Receiving Date')
    analysis = fields.Datetime(string='Sample Analysis Date')
    report = fields.Date(string="Report Issue Date")
    temperature = fields.Float(sting="Temperature")
    humidity = fields.Float(sting="Humidity")
    volume = fields.Char(string="Sample Volume")
    method = fields.Char(string="Method")
    crop = fields.Char(string="Crop")
                                          # RELATED FIELDS
    picking_id = fields.Many2one('stock.picking', string="Stock Picking")
    vehicle_no = fields.Char(string="vehicle_no.", related="picking_id.vehicle_no",store=True)
    bilty_no = fields.Char(string="bilty_no.", related="picking_id.bilty_no", store=True)
    origin = fields.Char(string='Source Document', related='picking_id.origin',store=True)
    production_id = fields.Many2one('mrp.production', string="Production Order")
    user_id = fields.Many2one('res.users', string="Requested By", related="production_id.user_id",store=True)
    lot_producing_id = fields.Many2one(string="Batch#",related="production_id.lot_producing_id",store=True)
    quantity = fields.Float(string='Quantity', compute='_compute_quantity', store=True)
    product_id = fields.Many2one('product.product', string="Product")

    @api.depends('picking_id', 'product_id')
    def _compute_quantity(self):
        for rec in self:
            if rec.picking_id and rec.product_id:
                moves = self.env['stock.move'].search([
                    ('picking_id', '=', rec.picking_id.id),
                    ('product_id', '=', rec.product_id.id)
                ])
                rec.quantity = sum(moves.mapped('quantity'))
            else:
                rec.quantity = 0



             # INHERITING THE MODELS FOR PICKING_ID AND PRODUCT_ID
class StockPickin(models.Model):
    _inherit = "stock.picking"



class StockMOve(models.Model):
    _inherit = "stock.move"

