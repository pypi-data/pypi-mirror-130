# -*- coding: utf-8 -*-
{
    'name': "vertical-habitatge-invoicing",

    'summary': """
        Invoicing process for habitatge.""",

    'author': "Coopdevs",
    'website': "http://coopdevs.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'vertical-habitatge',
    'version': '12.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}
