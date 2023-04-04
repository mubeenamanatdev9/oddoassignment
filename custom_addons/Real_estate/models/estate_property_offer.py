from odoo import api, fields, models
from odoo.exceptions import ValidationError as err
import datetime


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "for offers"

    price = fields.Integer(String="price")
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partneroffer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    create_date = fields.Date(default=lambda self: fields.Date.today())
    validity_days = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_date_deadline",inverse="_inverse_date_deadline")
    accept_or_refuse_offer = fields.Boolean()

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)',
         'The Offered price must be positive'),


    ]

    def accept_btn(self):
        for record in self:
            if record.accept_or_refuse_offer:
                record.accept_or_refuse_offer = True
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partneroffer_id


    def refuse_btn(self):
        for record in self:
                record.accept_or_refuse_offer = False
                record.status = "refused"

    @api.depends("create_date", "validity_days")
    def _date_deadline(self):
        for record in self:
            record.create_date = datetime.date.today()
            record.date_deadline = fields.Date.add(record.create_date, days=+record.validity_days)

    def _inverse_date_deadline(self):
        for record in self:

          record.validity_days
          record.validity_days= (record.date_deadline-datetime.date.today()).days
