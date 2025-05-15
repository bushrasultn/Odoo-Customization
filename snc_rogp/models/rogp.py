import json


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GatePass(models.Model):
    _name = 'gate.pass'
    _description = 'Gate Pass'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'


    name = fields.Char(default=lambda rec: 'New')
    cont = fields.Many2one('res.partner', string='Contact')
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse',
                                default=lambda rec: rec.env.user.property_warehouse_id.id)
    source = fields.Many2one('return.location', string='Source Location', tracking=True, required=True)
    destination = fields.Many2one('return.location', string='Destination Location', tracking=True, required=True, domain=lambda rec: [('id', '=', rec.env['return.location'].search([('warehouse', '=', rec.env.user.property_warehouse_id.id)]))])
    doc_type = fields.Selection(
        [('returnable inward', 'Returnable Inward'), ('returnable outward', 'Returnable Outward')],
        string='Document Type', required=True, tracking=True)
    date = fields.Date(string='Date', required=True)
    remark = fields.Text(string='Remarks')
    state = fields.Selection([('open', 'Open'), ('submitted', 'Submitted')],
                             default='open', tracking=True, string='State')
    rogp_state = fields.Selection(
        [('open', 'Open'), ('partially_returned', 'Partially Returned'), ('returned', 'Returned'),
         ('returnable_out', 'Returnable Out'), ('received', 'Received')],
        string='ROGP State', domain="[('doc_type', '=', 'returnable inward')]", tracking=True)
    product_line_ids = fields.One2many('gate.product', 'gate_pass_id', string="Product Lines")
    outward_records = fields.Many2one('gate.pass', string='ROGP NO',
                                      domain="[('doc_type', '=', 'returnable outward'), ('rogp_state', '!=', 'returned')]")
    sequence = fields.Char(string='Code', default='New')
    product_ids = fields.Many2many(comodel_name='product.product')
    returnable_id = fields.Many2one('gate.pass', string='RIGP NO', domain="[('doc_type','=',' returnable inward')]")
    filter_location = fields.Char(compute='_filter_location', store=True)
    transit_loc_domain = fields.Char()
    not_transit_loc_domain = fields.Char()
    dept = fields.Text(string='Department')
    security = fields.Char(string='Security No.')
    builty_no = fields.Char(string='Builty No.')
    vehicle = fields.Char(string='Veh No.')
    trnsprt = fields.Char(string='Transporter:')
    drvr = fields.Char(string='Driver Name:')
    loc_type = fields.Selection([('vendor', 'Vendor'), ('wh_transfer', 'WH Transfer')], string="Type", required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.context.get('company_id', self.env.company.id)
    )


    @api.onchange('loc_type')
    def _onchange_loc_type(self):
        if self.loc_type == 'vendor' and not self.cont:
            raise ValidationError("Contact is required for vendor location type.")

    # ..........................................NEW CHANGING................................
    inward_records = fields.Many2one('gate.pass', string="RIGP NO.")
    rigp_state = fields.Selection(
        [('open', 'Open'), ('partially_returned', 'Partially Returned'), ('returned', 'Returned'), ],
        string='RIGP State', tracking=True)


    @api.onchange('inward_records')
    def _onchange_inward_records(self):
        if self.inward_records:
            self.source = self.inward_records.destination
            self.product_line_ids = [(5, 0, 0)]
            lines = [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'specify': line.specify,
                    'quantity': line.quantity - line.returned_quantity,
                    'unit_id': line.unit_id.id,
                    'state': line.state,
                })
                for line in self.inward_records.product_line_ids
            ]
            self.product_line_ids = lines

# ........................................................................................................................
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'doc_type' in res:
            if res['doc_type'] == 'returnable outward':
                transit_loc_ids = self.source.search([('is_transit', '=', True)])
                normal_loc_ids = self.source.search([('is_transit', '=', False)])
                res['transit_loc_domain'] = json.dumps([('id', 'in', transit_loc_ids.ids)])
                res['not_transit_loc_domain'] = json.dumps([('id', 'in', normal_loc_ids.ids)])
            else:
                transit_loc_ids = self.source.search([('is_transit', '=', True)])
                normal_loc_ids = self.source.search([('is_transit', '=', False)])
                res['not_transit_loc_domain'] = json.dumps([('id', 'in', transit_loc_ids.ids)])
                res['transit_loc_domain'] = json.dumps([('id', 'in', normal_loc_ids.ids)])
        return res

    def _filter_location(self):
        transit_loc_ids = self.source.search([('is_transit', '=', True)])
        normal_loc_ids = self.source.search([('is_transit', '=', False)])
        for line in self:
            if line.doc_type == 'returnable outward':
                return {'domain': {'destination': [('id', 'in', transit_loc_ids.ids)]}}
            else:
                return {'domain': {'source': [('id', 'in', normal_loc_ids.ids)]}}

    @api.model
    def create(self, vals):
        if self.env.user.property_warehouse_id:
            if vals.get('doc_type') == 'returnable outward':
                seq = self.env['ir.sequence'].next_by_code('gate.pass.rogp.sequence')
                vals['name'] = f"{self.env.user.property_warehouse_id.code}/ROGP/{seq}"
            else:
                seq = self.env['ir.sequence'].next_by_code('gate.pass.rigp.sequence')
                vals['name'] = f"{self.env.user.property_warehouse_id.code}/RIGP/{seq}"
        else:
            raise ValidationError('Please select a default warehouse in user profile!')
        return super(GatePass, self).create(vals)

    @api.onchange('outward_records')
    def _onchange_outward_records(self):
        if self.outward_records:
            self.cont = self.outward_records.cont
            if self.doc_type == 'returnable inward' and self.loc_type == 'vendor':
                self.source = self.source.search([('type', '=', 'vendor')])[0].id if self.source.search([('type', '=', 'vendor')]) else False
            else:
                self.source = self.outward_records.destination
                self.destination = self.outward_records.source
            # self.loc_type = self.outward_records.loc_type
            self.product_line_ids = [(5, 0, 0)]
            lines = []

            for line in self.outward_records.product_line_ids:
                outward_valuation = self.env['returnable.valuation'].search(
                    [('outward_id', '=', self.outward_records.id)])
                qty = 0.0
                ret_qty = 0.0
                outward_qty = self.outward_records.product_line_ids.filtered(
                    lambda rec: rec.product_id.id == line.product_id.id)
                outward_valuation = outward_valuation.returnable_val_line_ids.filtered(
                    lambda rec: rec.product_id.id == line.product_id.id and rec.quantity > 0).mapped('quantity')
                if outward_valuation:
                    ret_qty = sum(outward_valuation)
                    qty = line.quantity - sum(outward_valuation)

                if self.outward_records:
                    self.product_line_ids = [(5, 0, 0)]
                    lines = [
                        (0, 0, {
                            'product_id': line.product_id.id,
                            'specify': line.specify,
                            'quantity': line.quantity - line.returned_quantity,
                            'returned_quantity': line.returned_quantity,
                            'unit_id': line.unit_id.id,
                            'state': line.state,
                        })
                        for line in self.outward_records.product_line_ids
                    ]
                    self.product_line_ids = lines

    def action_open(self):
        self.state = 'open'
        self.rogp_state = 'open'
        valuation = self.env['returnable.valuation'].search([('returnable_id', '=', self.id)])
        if valuation:
            for line in valuation.returnable_val_line_ids:
                line.unlink()
            valuation.unlink()

        if self.outward_records:
            if self.loc_type == 'vendor' and self.doc_type == 'returnable inward':
                if self.source.warehouse.id != self.destination.warehouse.id:
                    for line in self.product_line_ids:
                        self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity -= line.quantity
                        self.outward_records.rogp_state = 'partially_returned'

        if self.inward_records:
            if self.loc_type == 'wh_transfer' and self.doc_type == 'returnable outward':
                    for line in self.product_line_ids:
                        self.inward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity -= line.quantity
                        self.inward_records.rigp_state = 'partially_returned'

                    outwards = self.search([('inward_records', '=', self.inward_records.id),
                                            ('doc_type', '=', 'returnable outward')])
                    if outwards:
                        for out in outwards:
                            out.rogp_state = 'returned'

        if self.outward_records:
            if self.loc_type == 'wh_transfer' and self.doc_type == 'returnable inward':
                if self.warehouse.id == self.outward_records.warehouse.id:
                    for line in self.product_line_ids:
                        self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity -= line.quantity
                        self.outward_records.rogp_state = 'partially_returned'

                        inwards = self.search([('outward_records', '=', self.outward_records.id),
                                               ('doc_type', '=', 'returnable inward')])
                        if inwards:
                            for inward in inwards:
                                inward.rigp_state = 'partially_returned'

    def action_return(self):
        if not self.product_line_ids:
            raise ValidationError('Add product lines !')
        self.update_selected_outward()
        if self.doc_type == "returnable outward":
            # self.rogp_state = 'returnable_out'
            for product_line in self.product_line_ids:
                product_line.state = 'done'
        self.state = 'submitted'
        if self.state == 'submitted':
            self.create_valuation()

    def update_selected_outward(self):
        if self.outward_records:
            if self.doc_type == 'returnable inward' and self.loc_type == 'vendor':
                if self.outward_records:
                    for line in self.product_line_ids:
                        self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity += line.quantity
                        if sum(self.outward_records.product_line_ids.mapped('returned_quantity')) == sum(self.outward_records.product_line_ids.mapped('quantity')):
                            self.outward_records.rogp_state = 'returned'
                        else:
                            self.outward_records.rogp_state = 'partially_returned'

        if self.inward_records:
            if self.doc_type == 'returnable outward' and self.loc_type == 'wh_transfer':
                    if not self.source.is_transit and self.destination.is_transit:
                        if self.warehouse.id == self.inward_records.warehouse.id:
                            if self.source.warehouse.id != self.destination.warehouse.id:
                                for line in self.product_line_ids:
                                    return_vals = self.inward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id)
                                    if return_vals.quantity == return_vals.returned_quantity:
                                        raise ValidationError('All quantity returned successfully !')

                                    self.inward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity += line.quantity

                                    if sum(self.inward_records.product_line_ids.mapped('returned_quantity')) == sum(self.inward_records.product_line_ids.mapped('quantity')):
                                        self.inward_records.rigp_state = 'returned'
                                        outwards = self.search([('inward_records', '=', self.inward_records.id),
                                                                ('doc_type', '=', 'returnable outward')])
                                        if outwards:
                                            for out in outwards:
                                                out.rogp_state = 'returned'

                                    elif sum(self.inward_records.product_line_ids.mapped('returned_quantity')) == 0:
                                        self.inward_records.rigp_state = 'open'

                                    else:
                                        self.inward_records.rigp_state = 'partially_returned'

        if self.outward_records:
            if self.doc_type == 'returnable inward' and self.loc_type == 'wh_transfer':
                    if self.source.is_transit:
                        if self.warehouse.id == self.outward_records.warehouse.id:
                            if self.source.warehouse.id != self.destination.warehouse.id:
                                for line in self.product_line_ids:
                                    if self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity  == self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).quantity:
                                        raise ValidationError('All quantity are returned successfully !')
                                    self.outward_records.product_line_ids.filtered(lambda rec: rec.product_id.id == line.product_id.id).returned_quantity += line.quantity
                                    if sum(self.outward_records.product_line_ids.mapped('returned_quantity')) == sum(self.outward_records.product_line_ids.mapped('quantity')):
                                        self.outward_records.rogp_state = 'returned'
                                        inwards = self.search([('outward_records', '=', self.outward_records.id),
                                                                ('doc_type', '=', 'returnable inward')])
                                        if inwards:
                                            for inward in inwards:
                                                inward.rigp_state = 'returned'

                                    elif sum(self.outward_records.product_line_ids.mapped('returned_quantity')) == 0:
                                        self.outward_records.rogp_state = 'returnable_out'
                                    else:
                                        self.outward_records.rogp_state = 'partially_returned'


    def create_valuation(self):
        inward = self.env['returnable.valuation'].create({
            "cont": self.cont.id,
            "warehouse": self.warehouse.id,
            "outward_id": self.outward_records.id,
            "source": self.source.id,
            "destination": self.destination.id,
            "doc_type": self.doc_type,
            "returnable_id": self.id,
            "date": self.date,
            "remark": self.remark,
            "state": self.state,
            "name": self.name,
        })
        lines = []
        for line in self.product_line_ids:
            if line.quantity != 0:
                lines.append((0, 0, {
                    "product_id": line.product_id.id,
                    "quantity": -(line.quantity),
                    "unit_id": line.unit_id.id,
                    "specify": line.specify,
                    "source": self.source.id,
                    "outward_id": self.outward_records.id,
                    "warehouse": self.warehouse.id,
                    "doc_type": self.doc_type,
                    "returnable_id": self.id,
                    "date": self.date,
                    "remark": self.remark,
                    "state": self.state,
                    "name": self.name,
                    "cont": self.cont.id,

                }))
                lines.append((0, 0, {
                    "product_id": line.product_id.id,
                    "quantity": line.quantity,
                    "unit_id": line.unit_id.id,
                    "specify": line.specify,
                    "destination": self.destination.id,
                    "outward_id": self.outward_records.id,
                    "warehouse": self.warehouse.id,
                    "doc_type": self.doc_type,
                    "returnable_id": self.id,
                    "date": self.date,
                    "remark": self.remark,
                    "state": self.state,
                    "name": self.name,
                    "cont": self.cont.id,
                }))
        if inward:
            inward.returnable_val_line_ids = lines
        else:
            raise ValidationError('Inward Against !')


# ...................................................................................................
class GatePassProduct(models.Model):
    _name = 'gate.product'
    _description = 'Gate Pass Product'

    gate_pass_id = fields.Many2one('gate.pass', string="Gate Pass", tracking=True)
    product_id = fields.Many2one('product.product', string="Product", required=True, tracking=True)
    specify = fields.Text(string='Specification')
    quantity = fields.Float(string='Quantity', default=1, required=True, tracking=True)
    returned_quantity = fields.Float(string='Ret Quantity', default=0, store=True)
    unit_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='Status', default='draft')
    remaining_quantity = fields.Float(string='Remaining Quantity', compute='_compute_remaining_quantity', store=True)

    @api.depends('quantity', 'returned_quantity')
    def _compute_remaining_quantity(self):
        for line in self:
            line.remaining_quantity = line.quantity - line.returned_quantity

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.unit_id = line.product_id.uom_id.id

    @api.onchange('quantity')
    def _onchange_qty(self):
        for line in self:
            outward_qty = line.gate_pass_id.outward_records.product_line_ids.filtered(
                lambda rec: rec.product_id.id == line.product_id.id
            )

            if outward_qty:
                total_outward_qty = sum(outward_qty.mapped('quantity'))

                if (total_outward_qty - line.returned_quantity) < line.quantity:
                    raise ValidationError("Quantity exceeds available quantity. You cannot submit.")
