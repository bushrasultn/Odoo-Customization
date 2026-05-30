from odoo import models, fields, api

# =====================================================
# BOM HEADER MODEL
# This model represents the main BOM Costimator record
# =====================================================
class BillOfMaterialModel(models.Model):
    _name = 'bill.material'
    _description = 'Real-time BOM Cost Calculator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference_name'
    _order = "create_date DESC"


    # Reference number / name of the BOM
    reference_name = fields.Char(string="Reference", tracking=True)

    # Finished product for which cost will be calculated
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        tracking=True
    )

    # Unit of Measure of the finished product
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="UOM",
        tracking=True
    )

    # Quantity of finished product to be produced
    ref_qty = fields.Float(string="Quantity", default=0.0,tracking=True)

    # Company (multi-company support)
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        readonly=1,
        tracking=True,
    default=lambda self: self.env.context.get('company_id', self.env.company.id),
    )

    # One2many relation to BOM lines (raw materials)
    line_ids = fields.One2many(
        'bill.material.lines',
        'bom_id',
        string="Material Lines"
    )

    # -----------------------------------------------------
    # Auto set UOM when finished product is selected
    # -----------------------------------------------------
    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id


# =====================================================
# BOM LINES MODEL
# This model stores raw materials used in manufacturing
# =====================================================
class BillOfMaterialLinesModel(models.Model):
    _name = 'bill.material.lines'
    _description = 'BOM Lines'

    # Many2one link back to BOM header
    bom_id = fields.Many2one(
        'bill.material',
        string="BOM Reference",
        ondelete='cascade'
    )

    # Raw material product
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Components",
        required=True
    )

    # Unit of Measure of raw material
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="UOM"
    )

    # Required quantity of raw material
    ref_line_qty = fields.Float(string="Quantity", default=0.0)
    # label
    label_name = fields.Char(string="Label", tracking=True)
    current_market_cost = fields.Float(
        string="Market Rate",
    )

    current_avg_cost = fields.Float(
        string="Current Average Cost",
        readonly=True,
        compute="_compute_current_avg_cost",
        store=True
    )
    @api.depends('product_id')
    def _compute_current_avg_cost(self):
        for rec in self:
            rec.current_avg_cost = rec.product_id.standard_price or 0.0
            rec.current_market_cost = rec.product_id.standard_price or 0.0

    # -----------------------------------------------------
    # Auto set UOM when raw material product is selected
    # -----------------------------------------------------
    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id