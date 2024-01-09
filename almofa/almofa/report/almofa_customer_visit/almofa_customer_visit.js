// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Almofa Customer Visit"] = {
	"filters": [
		{
			"fieldname": "visit_no",
			"fieldtype": "Link",
			"label": "Visit No",
			"mandatory": 0,
			"options": "Customer Visit",
			"wildcard_filter": 0
		   },
		   {
			"fieldname": "customer",
			"fieldtype": "Link",
			"label": "Customer",
			"mandatory": 0,
			"options": "Customer",
			"wildcard_filter": 0
		   },
		   {
			"fieldname": "sales_partner",
			"fieldtype": "Link",
			"label": "Sales Partner",
			"mandatory": 0,
			"options": "Sales Partner",
			"wildcard_filter": 0
		   },
		   {
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From",
			"mandatory": 0,
			"wildcard_filter": 0,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		   },
		   {
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To",
			"mandatory": 0,
			"wildcard_filter": 0,
			"default":frappe.datetime.get_today()
		   },
		   {
			"fieldname": "status",
			"fieldtype": "Select",
			"label": "Status",
			"mandatory": 0,
			"options": "\nOpen\nCompleted\nCancelled",
			"wildcard_filter": 0
		   }
	]
};
