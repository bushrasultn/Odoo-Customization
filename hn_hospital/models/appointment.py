from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Hospitalappointment(models.Model):
    _name = "hospital.appointment"
    _description = "hospital appointment"
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'
    _order = 'id desc'
    name = fields.Char(string='Patient Name')
    image = fields.Binary("Image")
    age = fields.Integer("Age")
    reference = fields.Char(string="Reference", default='New', help="Reference of the patient")
    patient_id = fields.Many2one('hospital.patient', string="patient")
    gender = fields.Selection(related='patient_id.gender', selection=[('male', 'Male'), ('female', 'Female')],
                              string="gender", store=True)
    prescription = fields.Html(string='prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    date_appointment = fields.Date(string="Date", default=fields.Date.context_today)
    note = fields.Text(string="Note")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'),
                              ('cancel', 'Cancel')], default='draft')
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string="Lines")
    date_of_birth = fields.Date(related='patient_id.date_of_birth')
    ref = fields.Integer(string='Reference', help="Reference of the patient")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.reference = self.patient_id.ref

    @api.model
    def create(self, vals_list):
        vals_list['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    def action_test(self):
        print("Button Clicked!")
        return {
            'effect': {
                'message': 'Successful',
                'type': 'rainbow_man',
            }
        }

    def _compute_display_name(self):
        for rec in self:
            print("value_is", f"[{rec.reference}]{rec.patient_id.name} ")
            rec.display_name = f"[{rec.reference}]{rec.patient_id.name} "

            # def unlink(self):
            #     print("test")
            #     return super(Hospitalappointment, self).unlink()
            # if self.state =='done':
            #     raise ValidationError("You Cannot delete appointments with 'Done' status!"))
            #     return super((Hospitalappointment,self).create(vals))
from odoo import models, fields, api

class HospitalAppointmentLine(models.Model):
    _name = "hospital.appointment.line"
    _description = "Hospital Appointment Lines"

    sl_no = fields.Integer(string='S.no', readonly=True, default=lambda self: self._get_next_sl_no())
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty = fields.Float(string="QTY")
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    price_unit = fields.Float(related='product_id.list_price', readonly=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', store=True)

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty

    @api.model
    def create(self, vals):
        # Generate and assign sequence number
        vals['sl_no'] = self.env['ir.sequence'].next_by_code('hospital.appointment.line') or 1
        res = super(HospitalAppointmentLine, self).create(vals)
        return res

    def _get_next_sl_no(self):
        # Return next sequence number
        return self.env['ir.sequence'].next_by_code('hospital.appointment.line') or 1
