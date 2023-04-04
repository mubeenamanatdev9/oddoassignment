from odoo import api, fields, models
from odoo.exceptions import ValidationError as err
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(String="Name",required=True)
    description = fields.Text(String="Description")
    postcode = fields.Char(String="Char")
    date_availability = fields.Date(String="Date_availability",copy=False, default=lambda self: fields.Date.add(fields.Date.today(),months=+3))
    expected_price = fields.Float(String="expected_price",required=True)
    selling_price = fields.Float(String="selling_price",readonly=True,copy=False)
    bedrooms = fields.Integer(String="bedrooms",default=2)
    living_area = fields.Integer(String="living_area")
    facades = fields.Integer(String="Facades")
    garage = fields.Boolean(String="garage")
    garden = fields.Boolean(string="garden")
    garden_area = fields.Integer(String="garden_area")
    propertytype_id = fields.Many2one("estate.property.type",String="Property Type")
    partner_id = fields.Many2one("res.partner",String="partner")
    salesperson_id = fields.Many2one("res.partner",String="SalesPerson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.users",String="buyer", copy=False)
    garden_orientation = fields.Selection(String="garden_orientation",selection=[("north","North"),("south","South"),("east","East"),("west","West")])
    state = fields.Selection(String="State",default="new",copy=False,
                             selection=[
                                 ("new","new"),
                                 ("offer_recieved","Offer recieved"),
                                 ("offer_accepted","offer accepted"),
                                 ("sold","sold"),
                                 ("cancelled","cancelled")])
    tag_ids = fields.Many2many("estate.property.tags",String="tag ids")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Integer(String="totalarea",compute="_total_area")
    best_price = fields.Integer(string="best_price",compute="_best_price",default=0)
    user_id_for_resusers = fields.Many2one("res.users")
    #constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price must be positive'),
        ('check_selling_price','CHECK(selling_price >= 0','The  selling price must be positive'),

    ]

    #py constraint
    @api.constrains("selling_price")
    def _check_selling_price(self):


        for record in self:
            ninty_percent_of_expected_price = 0.9 * record.expected_price
            if float_is_zero(record.selling_price,precision_digits=3):
                raise err("Selling price Cannot be zero")
            if float_compare(record.selling_price,ninty_percent_of_expected_price,precision_rounding=3) <= 0:
                raise err("selling price cannot be less")




    def sold_btn(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise err("Property Cannot be sold!")
    def cancel_btn(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise err("Cannot be cancelled")

    @api.depends("living_area","garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _best_price(self):
        for record in self:
            if record.offer_ids.mapped('price'):
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
            if self.garden:
                if self.garden_area  < 10 or self.garden_orientation == False:
                    self.garden_area = 10
                    self.garden_orientation = "north"
            elif self.garden == False:
                if self.garden_area < 10 or self.garden_orientation == False:
                    self.garden_area = 0
                    self.garden_orientation = None

