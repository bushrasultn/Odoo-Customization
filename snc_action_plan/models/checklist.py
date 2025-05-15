from odoo import models, fields, api
class Checklist(models.Model):
    _name = "check.list"
    _description = "Event Checklist"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True, required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.user.company_id.id
    )
    event_type_ids = fields.One2many(
        comodel_name='event.type',
        inverse_name='checklist_id',
        string="Event Types"
    )
class EventTypes(models.Model):
    _inherit = "event.type"

    checklist_id = fields.Many2one(
        comodel_name='check.list',
        string="Checklist"
    )
    checklist_line_ids = fields.One2many(
        comodel_name='check.list.line',
        inverse_name='event_type_id',
        string="Checklist Lines"
    )
class ChecklistLine(models.Model):
    _name = "check.list.line"
    event_type_id = fields.Many2one(comodel_name='event.type',string="Event Type")
    checklist_id = fields.Many2one(comodel_name='check.list',string="Checklist")

    #######################################IN EVENT##################################
class EventEvent(models.Model):
    _inherit = "event.event"
    event_checklist_line_ids = fields.One2many(
        'event.check.list',
        'event_id',
        string="Event Checklist Lines"
    )
    @api.onchange('event_type_id')
    def _onchange_event_type(self):
        if self.event_type_id:
            self.event_checklist_line_ids = [(5, 0, 0)]
            for line in self.event_type_id.checklist_line_ids:
                self.event_checklist_line_ids += self.env['event.check.list'].new({
                    'check_list_id': line.checklist_id.id,
                })
##################################EVENT LIST MODEL ######################################################
class EventCheckLis(models.Model):
    _name = "event.check.list"
    event_id = fields.Many2one('event.event', string="Event")
    name = fields.Char(string="Checklist")
    check_list_id = fields.Many2one(comodel_name="check.list", string="Checklist")
    is_active = fields.Boolean(string="Conducted")
################################CROPS MODELS########################################################
class EventsCrop(models.Model):
    _name = 'event.crop'
    _description = 'Event Crops'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", Tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res
#######################################EVENT REGISTRATION############################
class EventRegistration(models.Model):
   _inherit = 'event.registration'
   land_area = fields.Float(string="Land Area(Acre)")
   phone_no = fields.Char(string="Phone")