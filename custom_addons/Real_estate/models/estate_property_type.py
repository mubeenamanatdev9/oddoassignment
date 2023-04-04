from odoo import fields, models

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "define the type of property"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('UNIQUE_NAME', 'name UNIQUE',
         'The Property Type name already exists'),
    ]



