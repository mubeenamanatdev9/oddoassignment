{
    'name': "real_estate",
    'version': '1.0',
    'sequence': 1,
    'depends': ['base'],
    'author': "Mubeen Amanat",
    'category': 'Accounting/Accounting',
    'description': """
    # This is a test module of Real-Estate Management!
    Written for the Odoo Quickstart Tutorial.
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_property_type.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offer.xml',
        'views/ResUsers.xml'



    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
