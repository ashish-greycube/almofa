from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'name',
		'non_standard_fieldnames': {
			'Sales Order': 'tender_info_cf',
			'Quotation': 'tender_info_cf',
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Quotation', 'Sales Order']
			}
		]
	}