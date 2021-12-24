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

		let show_description = function (idx = null, item_code = null, batch_no = null, exist = null) {
			if (exist) {
				let msg=__('Found: Row #{0}: {1}, has scanned batch no {2}.', [idx, item_code, batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.show_alert({ message: msg, indicator: 'green' });
			} else {
				let msg=__('Not Found: Batch no {0} doesnot belong to any item below.', [batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.show_alert({ message: msg, indicator: 'orange' });
			}
		}

		if (frm.doc.scan_batch_no_cf) {
			frappe.call({
				method: "almofa.api.search_serial_or_batch_or_barcode_number",
				args: {
					search_value: frm.doc.scan_batch_no_cf
				}
			}).then(r => {
				const data = r && r.message;
				if (!data || Object.keys(data).length === 0) {
					let msg=__('Cannot find Item with this batch no in system.')
					scan_batch_no_field.set_new_description(msg);
					frappe.show_alert({ message: msg, indicator: 'red' });
					return;
				}
				let row_to_modify = null;
				const existing_item_row = frm.doc.items.find(d => d.batch_no === data.batch_no);
				const blank_item_row = frm.doc.items.find(d => !d.batch_no);

				if (existing_item_row) {
					row_to_modify = existing_item_row;
					show_description(row_to_modify.idx, row_to_modify.item_code, row_to_modify.batch_no, true);
					frm.from_barcode = true;
					frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, {
						scanned_batch_no_cf: data.batch_no,
					});
				} else {
					show_description(null, null, frm.doc.scan_batch_no_cf, null);
				}
				scan_batch_no_field.set_value('');
				refresh_field("items");
			});
		}
		return false;
	},
})