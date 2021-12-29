from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def search_serial_or_batch_or_barcode_number(scanned_barcode):
	# search batch no
		data= frappe.db.sql("""select batch.name as batch_no, batch.item as item_code , BBU.uom as uom
		from `tabBatch` as batch inner join `tabBatch Barcode UOM` BBU on batch.name=BBU.parent 
		where BBU.barcode = %s
		""",scanned_barcode, as_dict=1)
		if len(data)>0:
			batch_no_data=data[0]
			return batch_no_data
		else:
			return {}

def scanned_batch_no_validation(self,method):
	for item in self.items:
		if item.batch_no and item.batch_no!=item.scanned_batch_no_cf and item.uom!=item.scanned_uom_cf:
			frappe.throw(_("Row #{0}: Scanned fields are incorrect. Please correct it to submit").format(item.idx))
