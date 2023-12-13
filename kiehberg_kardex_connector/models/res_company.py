from odoo import models,fields, _


class ResCompany(models.Model):
    _inherit = "res.company"
    
    is_mandant_01 = fields.Boolean(string="Is Kardex Company 1")
    is_mandant_02 = fields.Boolean(string="Is Kardex Company 2")