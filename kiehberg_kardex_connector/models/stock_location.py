from odoo import models,fields, _


class Location(models.Model):
    _inherit = "stock.location"
    
    is_kardex_location = fields.Boolean(string="Kardex Location", default=False)
    
