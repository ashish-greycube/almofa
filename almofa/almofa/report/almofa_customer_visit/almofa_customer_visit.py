# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
 columns= [
  {
   "fieldname": "visit_no",
  "fieldtype": "Link",
   "label": "Visit No",
   "options": "Customer Visit",
   "width": 80
  },
  {
   "fieldname": "sales_partner",
   "fieldtype": "Link",
   "label": "Sales Partner",
   "options": "Sales Partner",
   "width": 150
  },
  {
   "fieldname": "planned_date",
   "fieldtype": "Date",
   "label": "Planned Date",
   "width": 100
  },
  {
   "fieldname": "status",
   "fieldtype": "Data",
   "label": "Status",
   "width": 100
  },
  {
   "fieldname": "visit_conclusion",
   "fieldtype": "Small Text",
   "label": "Visit Conclusion",
   "width": 470
  },
  {
   "fieldname": "customer",
   "fieldtype": "Link",
   "label": "Customer",
   "options": "Customer",
   "width": 220
  },
  {
   "fieldname": "sample",
   "fieldtype": "Data",
   "label": "Sample",
   "width": 80
  }
 ]
 return columns

def get_data(filters):
	conditions = get_conditions(filters)
	data = frappe.db.sql(
		"""
SELECT
	cv.name as visit_no,
	cv.sales_partner,
	cv.planned_date,
	cv.status,
	cv.custom_visit_conclusion as visit_conclusion,
	cv.customer,
	IFNULL(
	(SELECT
		IF (count(cvi.name)>0,'Yes','No')
	from
		`tabCustomer Visit Item` as cvi
	where
		cvi.parent = cv.name
	group by
		cvi.parent),'No') as sample
FROM
	`tabCustomer Visit` as cv
WHERE 
	{0}
		""".format(conditions),filters,as_dict=1,debug=0
	)	
	return data

def get_conditions(filters):
	
	conditions ="1=1 "

	if filters.get("visit_no"):
		conditions += " and cv.name = %(visit_no)s"

	if filters.get("customer"):
		conditions += " and cv.customer = %(customer)s"

	if filters.get("sales_partner"):
		conditions += " and cv.sales_partner = %(sales_partner)s"

	if filters.get("status"):
		conditions += " and cv.status = %(status)s"
		

	if filters.get("from_date"):
			conditions += " and cv.planned_date between {0} and {1}".format(
        		frappe.db.escape(filters["from_date"]),
        		frappe.db.escape(filters["to_date"]),
    )


	return conditions
