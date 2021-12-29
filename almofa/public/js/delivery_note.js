frappe.ui.form.on("Delivery Note", {
	refresh: function (frm) {
		let scan_batch_no_field = frm.get_field('scan_batch_no_cf');
		if (scan_batch_no_field) {
			scan_batch_no_field.set_value("");
			scan_batch_no_field.set_new_description("");

			if (frappe.is_mobile()) {
				if (scan_batch_no_field.$input_wrapper.find('.input-group').length) return;

				let $input_group = $('<div class="input-group">');
				scan_batch_no_field.$input_wrapper.find('.control-input').append($input_group);
				$input_group.append(scan_batch_no_field.$input);
				$(`<span class="input-group-btn" style="vertical-align: top">
						<button class="btn btn-default border" type="button">
							<i class="fa fa-camera text-muted"></i>
						</button>
					</span>`)
					.on('click', '.btn', () => {
						frappe.barcode.scan_batch_no_cf().then(barcode => {
							scan_batch_no_field.set_value(barcode);
						});
					})
					.appendTo($input_group);
			}
		}
	},
	scan_batch_no_cf: function (frm) {
		let scan_batch_no_field = frm.fields_dict["scan_batch_no_cf"];
		let show_description = function (idx = null, item_code = null, batch_no = null, exist) {
			if (exist == 1) {
				let msg = __('Found: Row #{0}: {1}, has scanned batch no {2}.', [idx, item_code, batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.show_alert({
					message: msg,
					indicator: 'green'
				});
			} else if (exist == 2) {
				let msg = __('Scanned barcode {0} doesnot belong to any item below. Check UOM, Batch No field', [batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.msgprint({
					title: __('Not Found'),
					message: msg,
					indicator: 'orange'
				});
			} else if (exist == 0) {
				let msg = __('Cannot find item with {0} barcode', [batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.msgprint({
					title: __('Not Found'),
					message: msg,
					indicator: 'red'
				});
			}
		}

		if (frm.doc.scan_batch_no_cf) {
			frappe.call({
				method: "almofa.api.search_serial_or_batch_or_barcode_number",
				args: {
					scanned_barcode: frm.doc.scan_batch_no_cf
				}
			}).then(r => {
				const data = r && r.message;
				if (!data || Object.keys(data).length === 0) {
					// no match
					show_description(null, null, frm.doc.scan_batch_no_cf, 0);
					scan_batch_no_field.set_value('');
					refresh_field("items");
					return;
				}
				const existing_item_row = frm.doc.items.find(d => (d.batch_no === data.batch_no && d.item_code === data.item_code && d.uom === data.uom));
				if (existing_item_row) {
					// exact match
					frappe.model.set_value(existing_item_row.doctype, existing_item_row.name, {
						scanned_uom_cf: data.uom,
						scanned_batch_no_cf: data.batch_no,
						scanned_barcode_cf: frm.doc.scan_batch_no_cf
					});
					show_description(existing_item_row.idx, existing_item_row.item_code, existing_item_row.batch_no, 1);
					scan_batch_no_field.set_value('');
					refresh_field("items");
					return
				} else {
					// not match with child item table
					show_description(null, null, frm.doc.scan_batch_no_cf, 2);
					scan_batch_no_field.set_value('');
					refresh_field("items");
					return
				}
			})
		}
		return false;
	}
})