from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def search_serial_or_batch_or_barcode_number(search_value):
	# search batch no
	batch_no_data = frappe.db.get_value('Batch', search_value, ['name as batch_no', 'item as item_code'], as_dict=True)
	if batch_no_data:
		return batch_no_data

	return {}


def scanned_batch_no_validation(self,method):
	for item in self.items:
		if item.batch_no and item.batch_no!=item.scanned_batch_no_cf:
			frappe.throw
			frappe.throw(_("Row #{0}: Scanned batch no field is empty. Please correct it to submit").format(item.idx))
