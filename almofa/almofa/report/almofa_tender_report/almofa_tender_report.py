# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict

def execute(filters=None):
	columns, data = [], []
	conditions = []

	columns = [
		{
			"label": _("Tender Ref"),
			"fieldname": "tender_ref",
			"fieldtype": "Link",
			"options": "Tender Info",
			"width": 90
		},
		{
			"label": _("Quot Ref"),
			"fieldname": "quot_ref",
			"fieldtype": "Link",
			"options": "Quotation",
			"width": 90
		},
		{
			"label": _("SO Ref"),
			"fieldname": "so_ref",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 140
		},		
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},		
		{
			"label": _("Total Qtn qty"),
			"fieldname": "total_qtn_qty",
			"fieldtype": "Float",
			'precision': 1,
			"width": 100
		},	
		{
			"label": _("Qtn qty"),
			"fieldname": "qtn_qty",
			"fieldtype": "Float",
			'precision': 1,
			"width": 80
		},		
		{
			"label": _("Total SO qty"),
			"fieldname": "total_so_qty",
			"fieldtype": "Float",
			'precision': 1,
			"width": 90
		},				
		{
			"label": _("SO qty"),
			"fieldname": "so_qty",
			"fieldtype": "Float",
			'precision': 1,
			"width": 80
		},				
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 90
		}
	]


	conditions=" where 1=1"
	if filters.get("tender_name"):
		conditions += " and tender.name= %(tender_name)s"

	if filters.get("from_date"):
		conditions += " and tender.tender_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " and tender.tender_date <= %(to_date)s"		

	data=frappe.db.sql("""SELECT
	tender.name as tender_ref ,
	quot.name as quot_ref,
	so.name as so_ref,
	tender_item.item as item_code,
	tender_item.item_name as item_name,
	tender_item.quoted_qty as total_qtn_qty,
	quot_item.qty as qtn_qty,
	tender_item.ordered_qty as total_so_qty,
	so_item.qty as so_qty,
	IF(tender_item.docstatus = 0,
	'Draft',
	IF(tender_item.docstatus = 1,
	'Submitted',
	'Cancelled')) as status
FROM
	`tabTender Info` as tender
inner join `tabTender Info Item Detail` tender_item on
	tender.name = tender_item.parent
left outer join `tabQuotation` as quot on
	tender.name = quot.tender_info_cf
left outer join `tabQuotation Item` as quot_item on 
	quot_item.parent = quot.name
	and quot_item.item_code = tender_item.item
left outer join `tabSales Order` as so on
	tender.name = so.tender_info_cf
left outer join `tabSales Order Item` as so_item on 
	so_item.parent = so.name
	and so_item.item_code = tender_item.item
	{conditions}
	order by tender.name,tender_item.item,	quot.name,so.name
	""".format(conditions=conditions), filters, as_list=1)
	return columns, data
