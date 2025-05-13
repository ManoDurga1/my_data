{
    'name': 'Invoice XLSX Report',
    'version': '18.0.1.0',
    'category': 'Accounting',
    'summary': 'Generate XLSX reports for customer invoices',
    'description': """
        This module allows you to export customer invoices to XLSX format from the Invoices menu.
        """,
    'author': 'Mano Durga',
    'website': 'https://sidmectech.com',
    'depends': ['account','report_xlsx','sale','mail','base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_xlsx_wizard_view.xml',
        'report/report_view.xml',
        'views/student_course_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
