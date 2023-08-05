# -*- coding: utf-8 -*-
{
  'name': "sm_connect",

  'summary': """
    Connect odoo to other apps like wordpress, firbase or carsharing app
  """,

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
  # for the full list
  'category': 'Uncategorized',
  'version': '12.0.0.0.6',

  # any module necessary for this one to work correctly
  'depends': ['base', 'vertical_carsharing'],

  # always loaded
  'data': [
    'views/views_res_config_settings.xml'
  ],
  # only loaded in demonstration mode
  'demo': [],
}
