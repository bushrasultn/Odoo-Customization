from odoo import fields, models, api


class QualityControlTemplate(models.Model):
    _name = 'qc.template'


    name = name = fields.Char(string='Name')




# .............................................................................................


class QualityModelPoint(models.Model):
    _name = 'model.points'
    _order = 'create_date desc'


    name = fields.Char(string='Name')
    note = fields.Html(string='Note')
    temp_id = fields.Many2one('qc.template', string='QC Template')


    
