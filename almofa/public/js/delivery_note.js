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
				let msg = __('Found: Row #{0}: {1}, has scanned batch no {2}.', [idx, item_code, batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.show_alert({
					message: msg,
					indicator: 'green'
				});
			} else {
				let msg = __('Scanned batch no {0} doesnot belong to any item below.', [batch_no])
				scan_batch_no_field.set_new_description(msg);
				frappe.msgprint({
					title: __('Not Found'),
					message: msg,
					indicator: 'red'
				});
			}
		}

		if (frm.doc.scan_batch_no_cf) {
			let existing_item_row = false
			$.each(frm.doc.items || [], function (i, item) {
				if (item.batch_no) {
					if (!item.scanned_batch_no_cf) {
						if (item.batch_no == frm.doc.scan_batch_no_cf) {
							show_description(item.idx, item.item_code, item.batch_no, true);
							frappe.model.set_value(item.doctype, item.name, {
								scanned_batch_no_cf: item.batch_no
							});
							existing_item_row = true
						}
					}
				}
			});

			if (existing_item_row == false) {
				show_description(null, null, frm.doc.scan_batch_no_cf, null);
			}

			scan_batch_no_field.set_value('');
			refresh_field("items");
		}
		return false;
	}
})