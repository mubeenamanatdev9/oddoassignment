from odoo import api, fields, models

class ResUsers(models.Model):
    # _name="ResUsers"
    _inherit="res.users"

    property_ids = fields.One2many("estate.property","user_id_for_resusers")