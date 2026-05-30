from odoo import models, fields, api


# ======================================================================================
# MAIN MODEL : PRODUCT COST ESTIMATOR
# ======================================================================================
class ProductCostimatorModel(models.Model):
    _name = 'product.costimator'
    _description = 'Product Cost Estimator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "create_date DESC"

    # Company (auto default from current company)
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        readonly=True,
        default=lambda self: self.env.company.id,
    )

    # Finished product
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        tracking=True
    )

    # Reference BOM / Material Reference
    reference_id = fields.Many2one(
        'bill.material',
        string="Reference",
        tracking=True
    )

    # UOM of finished product
    uom_id = fields.Many2one(
        'uom.uom',
        string="UOM"
    )

    # Quantity to produce
    costimator_qty = fields.Float(
        string="Quantity",
        default=0.0
    )

    # Profit margin
    profit_margin = fields.Float(
        string="Profit Margin",
        default=0.0
    )

    # One2many relation with lines
    line_ids = fields.One2many(
        'product.costimator.lines',
        'costimator_id',
        string="Components"
    )

    # ============================================================
    # ONCHANGE: When Reference is selected → auto fill data
    # ============================================================
    @api.onchange('reference_id')
    def _onchange_reference_id(self):
        """
        Auto-fill fields when reference is selected:
        - Product
        - UOM
        - Quantity
        - Component lines
        """

        if not self.reference_id:
            return

        # Main fields
        self.product_id = self.reference_id.product_id.id
        self.uom_id = self.reference_id.uom_id.id
        self.costimator_qty = self.reference_id.ref_qty

        # Clear existing lines
        self.line_ids = [(5, 0, 0)]

        # Load new lines from reference
        self.line_ids = [
            (0, 0, {
                'product_id': l.product_id.id,
                'uom_id': l.uom_id.id,
                'costimator_line_qty': l.ref_line_qty,
                'label_name': l.label_name,
                'current_avg_cost': l.current_avg_cost,
                'current_market_cost': l.current_market_cost,
            }) for l in self.reference_id.line_ids
        ]
    # ======================================================================================
    #                                Onchange Function
    # ======================================================================================
    @api.onchange('costimator_qty')
    def _onchange_costimator_qty(self):
        if not self.costimator_qty or not self.reference_id:
            return

        ref_qty = self.reference_id.ref_qty or 0.0
        costimator_qty = self.costimator_qty

        # update existing lines using reference lines (NOT self.line_ids fields)
        for line, ref_line in zip(self.line_ids, self.reference_id.line_ids):
            line.costimator_line_qty = (
                (ref_line.ref_line_qty / ref_qty) * costimator_qty
                if ref_qty else 0.0
            )
    @api.onchange('profit_margin')
    def _onchange_profit_margin(self):
        """
        When the user enters a profit margin,
        it immediately calls both compute functions.
        """
        if self.profit_margin:
            self._compute_totals()
            self._compute_market_totals()
    # ======================================================================================
    #                                COMPUTED FIELDS
    # ======================================================================================
    total_profit_margin = fields.Float(string="Profit Margin", compute="_compute_totals", store=True)
    total_sale_price = fields.Float(string="Sale Price (Exclusive Taxes)", compute="_compute_totals", store=True)
    cost_per_unit = fields.Float(string="Cost Per Unit", compute="_compute_totals", store=True)
    sale_price_per_unit = fields.Float(string="Sale Price Per Unit", compute="_compute_totals", store=True)

    # ===========================CURRENT AVG COST===========================================================
    @api.depends(
        'line_ids.total_avg_cost',
        'profit_margin',
        'costimator_qty'
    )
    def _compute_totals(self):
        for rec in self:
            # =========================
            # TOTAL COST
            # =========================
            total_cost = sum(rec.line_ids.mapped('total_avg_cost'))

            # =========================
            # QUANTITY
            # =========================
            qty = rec.costimator_qty or 0.0

            # =========================
            # PROFIT MARGIN (your formula fixed only)
            # =========================
            rec.total_profit_margin = (
                (total_cost / (100 - rec.profit_margin) * (rec.profit_margin))
                if rec.profit_margin else 0.0
            )

            # =========================
            # SALE PRICE (EXCLUSIVE TAXES)
            # =========================
            rec.total_sale_price = total_cost + rec.total_profit_margin

            # =========================
            # COST PER UNIT
            # =========================
            rec.cost_per_unit = total_cost / qty if qty else 0.0

            # =========================
            # SALE PRICE PER UNIT
            # =========================
            rec.sale_price_per_unit = (
                rec.total_sale_price / qty if qty else 0.0
            )

    # ===========================MARKET AVG COST===========================================================
    # ==========================================================
    # MARKET COST TOTALS
    # ==========================================================
    market_profit_margin = fields.Float(string="Profit Margin", compute="_compute_market_totals", store=True)
    market_sale_price = fields.Float(string="Sale Price (Exclusive Taxes)", compute="_compute_market_totals",
                                     store=True)
    market_cost_per_unit = fields.Float(string="Cost Per Unit", compute="_compute_market_totals", store=True)
    market_sale_price_per_unit = fields.Float(string="Sale Price Per Unit", compute="_compute_market_totals",
                                              store=True)

    @api.depends(
        'line_ids.total_market_cost',
        'profit_margin',
        'costimator_qty'
    )
    def _compute_market_totals(self):
        for rec in self:
            # =========================
            # TOTAL MARKET COST
            # =========================
            total_cost = sum(rec.line_ids.mapped('total_market_cost'))
            # =========================
            # QUANTITY
            # =========================
            qty = rec.costimator_qty or 0.0
            # =========================
            # PROFIT MARGIN
            # =========================
            rec.market_profit_margin = (
                (total_cost / (100 - rec.profit_margin) * (rec.profit_margin))
                if rec.profit_margin else 0.0
            )
            # =========================
            # MARKET SALE PRICE (EXCLUSIVE TAXES)
            # =========================
            rec.market_sale_price = total_cost + rec.market_profit_margin
            # =========================
            # MARKET COST PER UNIT
            # =========================
            rec.market_cost_per_unit = total_cost / qty if qty else 0.0
            # =========================
            # Market SALE PRICE PER UNIT
            # =========================
            rec.market_sale_price_per_unit = (
                rec.market_sale_price / qty if qty else 0.0
            )


# ======================================================================================
# LINES MODEL : COMPONENTS
# ======================================================================================
class ProductCostimatorLinesModel(models.Model):
    _name = 'product.costimator.lines'
    _description = 'Product Cost Estimator Lines'

    # Link to main model
    costimator_id = fields.Many2one(
        'product.costimator',
        string="Costimator",
        ondelete='cascade'
    )

    # Component product
    product_id = fields.Many2one(
        'product.product',
        string="Component",
    )

    # UOM
    uom_id = fields.Many2one(
        'uom.uom',
        string="UOM"
    )

    # Quantity
    costimator_line_qty = fields.Float(
        string="Quantity",
        default=0.0
    )

    # Label
    label_name = fields.Char(string="Label")

    # ============================================================
    # COST FIELDS  Standard Price(READONLY)
    # ============================================================
    current_avg_cost = fields.Float(
        string="Average Rate",
        readonly=True,
        compute="_compute_current_avg_cost",
        store=True
    )

    @api.depends('product_id')
    def _compute_current_avg_cost(self):
        for rec in self:
            rec.current_avg_cost = rec.product_id.standard_price or 0.0
            rec.current_market_cost = rec.product_id.standard_price or 0.0

    current_market_cost = fields.Float(
        string="Market Rate",
    )

    # ============================================================
    # COMPUTED TOTALS
    # ============================================================
    total_avg_cost = fields.Float(
        string="Total Average Cost",
        compute="_compute_total_cost",
        store=True
    )

    total_market_cost = fields.Float(
        string="Total Market Cost",
        compute="_compute_total_cost",
        store=True
    )

    # ============================================================
    # COMPUTE LOGIC
    # ============================================================
    @api.depends(
        'costimator_line_qty',
        'current_avg_cost',
        'current_market_cost'
    )
    def _compute_total_cost(self):
        for rec in self:
            qty = rec.costimator_line_qty or 0.0

            # qty * avg cost
            rec.total_avg_cost = qty * rec.current_avg_cost

            # qty * market cost
            rec.total_market_cost = qty * rec.current_market_cost
