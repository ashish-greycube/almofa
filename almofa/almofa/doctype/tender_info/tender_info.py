# -*- coding: utf-8 -*-
# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe, erpnext, json
from frappe import _, scrub, ValidationError
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_link_to_form,flt

class TenderInfo(Document):
	def validate(self):
		self.validate_for_duplicate_items()			

	def on_update_after_submit(self):
		for ti_item in self.tender_info_item_detail:
			if ti_item.quoted_qty and ti_item.quoted_qty>ti_item.qty:
				msg = _('Row #{0} : {1} item, "quoted qty" cannot be greater than <b>{2}</b> "qty" for tender info {3}.'.format(ti_item.idx,ti_item.item,ti_item.quoted_qty-ti_item.qty,frappe.bold(get_link_to_form('Tender Info',self.name))))
				frappe.throw(msg)					

			if ti_item.ordered_qty and ti_item.ordered_qty>ti_item.qty:
				msg = _('Row #{0} : {1} item, "ordered qty" cannot be greater than <b>{2}</b> "qty" for tender info {3}.'.format(ti_item.idx,ti_item.item,ti_item.ordered_qty-ti_item.qty,frappe.bold(get_link_to_form('Tender Info',self.name))))
				frappe.throw(msg)	

	def validate_for_duplicate_items(self):
		chk_dupl_itm = []
		for d in self.get('tender_info_item_detail'):
			if d.item in chk_dupl_itm:
				frappe.throw(_("Note: Item {0} entered multiple times").format(d.item))
			else:
				chk_dupl_itm.append(d.item)


@frappe.whitelist()
def create_sales_order_from_tender_info(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.customer=source.customer

	def update_item(source_doc, target_doc, source_parent):
		target_qty=(source_doc.qty-source_doc.ordered_qty)
		target_doc.item_code = source_doc.item
		target_doc.item_name = source_doc.item_name
		target_doc.qty = target_qty

	ti=frappe.get_doc('Tender Info',source_name)
	eligible_item=False
	for item in ti.tender_info_item_detail:
		if item.ordered_qty < item.qty:
			eligible_item=True
			break

	if	eligible_item==False:
		frappe.msgprint(_('No eligible items for making sales order'))
		return	

	doc = get_mapped_doc('Tender Info', source_name, {
		'Tender Info': {
			'doctype': 'Sales Order',
			'field_map': {
				'tender_info_cf':'name',
			},			
			'validation': {
				'docstatus': ['!=', 2]
			}
		},
		"Tender Info Item Detail": {
			"doctype": "Sales Order Item",
			"postprocess": update_item,
			"condition": lambda doc: (doc.qty-doc.ordered_qty)>0
		},		
	}, target_doc,set_missing_values)
	doc.run_method('set_missing_values')
	return doc


@frappe.whitelist()
def create_quotation_from_tender_info(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.quotation_to = "Customer"
		target.party_name=source.customer

	def update_item(source_doc, target_doc, source_parent):
		target_qty=(source_doc.qty-source_doc.quoted_qty)
		target_doc.item_code = source_doc.item
		target_doc.item_name = source_doc.item_name
		target_doc.qty = target_qty

	ti=frappe.get_doc('Tender Info',source_name)
	eligible_item=False
	for item in ti.tender_info_item_detail:
		if item.quoted_qty < item.qty:
			eligible_item=True
			break

	if	eligible_item==False:
		frappe.msgprint(_('No eligible items for making quotation'))
		return	

	doc = get_mapped_doc('Tender Info', source_name, {
		'Tender Info': {
			'doctype': 'Quotation',
			'field_map': {
				'tender_info_cf':'name',
			},			
			'validation': {
				'docstatus': ['!=', 2]
			}
		},
		"Tender Info Item Detail": {
			"doctype": "Quotation Item",
			"postprocess": update_item,
			"condition": lambda doc: (doc.qty-doc.quoted_qty)>0
		},		
	}, target_doc,set_missing_values)
	doc.run_method('set_missing_values')
	return doc


def update_quoted_qty_of_tender_info(self,method):
	if self.tender_info_cf:
		ti=frappe.get_doc('Tender Info',self.tender_info_cf)
		qo_item_found=False
		msg=''
		for item in self.items:
			for ti_item in ti.tender_info_item_detail:
				if item.item_code == ti_item.item:
					if self.doctype=='Quotation' and method=='on_submit':
						ti_item.quoted_qty=ti_item.quoted_qty+item.qty
						msg += _('Row #{0} : {1} item quoted qty is updated for tender info {2}. <br>'.format(ti_item.idx,ti_item.item,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
						qo_item_found=True
					elif self.doctype=='Quotation' and method=='on_cancel':
						ti_item.quoted_qty=ti_item.quoted_qty-item.qty
						msg += _('Row #{0} : {1} item quoted qty is updated for tender info {2}. <br>'.format(ti_item.idx,ti_item.item,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
						qo_item_found=True
					elif self.doctype=='Sales Order' and method=='on_submit':
						ti_item.ordered_qty=ti_item.ordered_qty+item.qty
						msg += _('Row #{0} : {1} item ordered qty is updated for tender info {2}. <br>'.format(ti_item.idx,ti_item.item,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
						qo_item_found=True
					elif self.doctype=='Sales Order' and method=='on_update_after_submit':
						existing_qty=sum_of_existing_so(self.tender_info_cf,item.item_code,self.name)
						ti_item.ordered_qty=existing_qty+item.qty
						msg += _('Row #{0} : {1} item ordered qty is updated for tender info {2}. <br>'.format(ti_item.idx,ti_item.item,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
						qo_item_found=True						
					elif self.doctype=='Sales Order' and method=='on_cancel':
						ti_item.ordered_qty=ti_item.ordered_qty-item.qty
						msg += _('Row #{0} : {1} item ordered qty is updated for tender info {2}. <br>'.format(ti_item.idx,ti_item.item,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
						qo_item_found=True						
		if qo_item_found==True:
			ti.save(ignore_permissions=True)
			if len(msg)>0:
				frappe.msgprint(msg)

def sum_of_existing_so(tender_info,item_code,so_name):
	existing_qty = frappe.db.sql("""
SELECT  sum(sot.qty)  FROM  `tabSales Order` so inner join `tabSales Order Item` sot 
on so.name=sot.parent 
where so.tender_info_cf = %s
and sot.item_code = %s
and so.docstatus = 1
and so.name != %s
	""", (tender_info,item_code, so_name))
	return flt(existing_qty[0][0]) if existing_qty else 0	

def validate_against_tender_info(self,method):
	if self.tender_info_cf:
		ti=frappe.get_doc('Tender Info',self.tender_info_cf)
		for item in self.items:
			qo_item_found=False
			for ti_item in ti.tender_info_item_detail:
				if item.item_code == ti_item.item:
					qo_item_found=True
					break
			if qo_item_found == False:
				msg = _('Row #{0} : {1} item is not part of tender info {2}. <br>Please remove item to proceed.'.format(item.idx,item.item_code,frappe.bold(get_link_to_form('Tender Info',self.tender_info_cf))))
				frappe.throw(msg)				


