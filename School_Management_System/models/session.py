from odoo import fields, models, api


class SchoolSession(models.Model):
    _name = "school.session"
    _description = "School Session"
    _rec_name = 'year'

    year = fields.Char(string='Year')
    session_id = fields.Many2one('school.sheet', string='Session')
    fee_ids = fields.One2many('student.fee', 'session_id', string='Fees')
    active = fields.Boolean(string='Active', default=True)
    price = fields.Float(string="Price")
    quantity = fields.Integer(string="Quantity")
    discount = fields.Integer(string="Discount")
    total_discount = fields.Float(string="Total Discount", compute='_compute_total_discount', store=True)
    total = fields.Float(string="Total", compute='_compute_total', store=True)

    @api.onchange('price', 'quantity', 'discount')
    def _onchange_price_quantity_discount(self):
        self.total_discount = (self.price * self.quantity) * self.discount/100
        self.total = (self.price * self.quantity) - self.total_discount
    # for record in self: 2nd month to calculate the discount
    #     if record.price and record.quantity and record.discount is not None:
    #         total_price = record.price * record.quantity
    #         total_discount = total_price * (record.discount / 100*2)
    #         record.total_discount = total_discount
    #         record.total = total_price - total_discount
    #     else:
    #         record.total_discount = 0.0
    #         record.total = 0.0


@api.depends('price', 'quantity', 'discount')
def _compute_total_discount_compute_total (self):
    for record in self:
        if record.price and record.quantity and record.discount:
            total_price = record.price * record.quantity
            record.total_discount = total_price * (record.discount / 100)
            record.total = total_price - record.total_discount

        else:
            record.total_discount = 0.0
            record.total = 0.0

# @api.depends('price', 'quantity', 'discount')
# def _compute_total(self):
#     for record in self:
#         if record.price and record.quantity and record.discount:
#             total_price = record.price * record.quantity
#             total_discount = total_price * (record.discount / 100)
#             record.total = total_price - total_discount
#         else:
#             record.total = 0.0
