

{
    'name': 'SDM Tax Invoice Report (Mobile)',
    'version': '18.0.0.1',
    'summary': 'Custom tax invoice report optimized for mobile users',
    'description': """
        This module provides a customized tax invoice PDF report designed
        for better readability on mobile devices.
    """,
    'category': 'Accounting',
    'author': 'Mano Durga',
    'website': 'https://sidmectech.in',
    'depends': ['account', 'web'],
    'data': [
            'report/invoice_tax_view_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
