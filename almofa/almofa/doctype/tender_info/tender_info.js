// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tender Info', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1 && frm.doc.tender_info_item_detail && frm.doc.tender_info_item_detail.length>0) {
			frm.add_custom_button(__('Quotation'), () => create_quotation_from_tender_info(), __('Create'));
			frm.add_custom_button(__('Sales Order'), () => create_sales_order_from_tender_info(), __('Create'));
		}
	}
});

frappe.ui.form.on('Tender Info Item Detail', {
	qty: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn]
		if (row.quoted_qty && row.qty< row.quoted_qty) {
			frappe.throw(__('Qty entered cannot be less than quoted qty'))
		}
		if (row.ordered_qty && row.qty< row.ordered_qty) {
			frappe.throw(__('Qty entered cannot be less than ordered qty'))
		}		
	}
});

function create_quotation_from_tender_info() {
	frappe.model.open_mapped_doc({
		method: "almofa.almofa.doctype.tender_info.tender_info.create_quotation_from_tender_info",
		frm: cur_frm
	})
}

function create_sales_order_from_tender_info() {
	frappe.model.open_mapped_doc({
		method: "almofa.almofa.doctype.tender_info.tender_info.create_sales_order_from_tender_info",
		frm: cur_frm
	})
}