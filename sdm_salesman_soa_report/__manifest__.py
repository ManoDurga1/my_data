{
    'name': 'Salesman report SOA',
    'version': '18.0.0.0',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_action.xml',
        'report/salesman_report_soa_template.xml',
        'wizard/salesman_report_wizard.xml',
    ],
    'installable': True,
    'application': False,
}
