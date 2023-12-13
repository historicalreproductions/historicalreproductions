{
    'name': 'Kiehberg Kardex Connector',
    'version': '14.0.1.0.0',
    'description': 'Kardex stock sync',
    'summary': 'Sending Emails with attachments out of stock moves to Kardex',
    'author': 'Hucke Media GmbH & Co. KG',
    'maintainer': 'Duc Duy Hoang',
    'website': 'https://www.hucke-media.de',
    'license': 'LGPL-3',
    'category': 'Connector',
    'depends': [
        'base',
        'stock',
        'mail',
        'contacts',
    ],
    'data': [
        'views/stock_location.xml',
        'views/stock_picking.xml',
        'views/mail_template.xml',
        'views/ir_config_parameters.xml',
        'views/res_company.xml',
        ],

    'auto_install': False,
    'application': False,
    'assets': {}
}