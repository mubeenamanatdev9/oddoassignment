from odoo import fields, models

class estatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description  = "for tags "

    name = fields.Char(required=True)
    _sql_constraints = [
        ('UNIQUE_name', 'name UNIQUE',
         'The Tag name already exists'),


    ]

