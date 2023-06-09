// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Schedule', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("Home","Shift Schedule");
		frm.fields_dict.error_preview.$wrapper.empty()
		frm.fields_dict.csv_preview.$wrapper.empty()
		frm.fields_dict.summary.$wrapper.empty()
		frm.trigger('show_csv_data')
		frm.trigger('show_summary')
		frm.add_custom_button(__('Print Summary'), function (){
			window.open(
				frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
					doctype=${encodeURIComponent("Shift Schedule")}
					&name=${encodeURIComponent(frm.doc.name)}
					&format=${encodeURIComponent('Shift Report')}`)
			);
		})
			if (frappe.user.has_role('HR')) {
				if (!frm.doc.__islocal){
			frm.add_custom_button(__('Re-Check'), function (){
				frappe.call({
					"method": "thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.enqueue_shift_assignment",
					"args":{
						"file" : frm.doc.upload,
						"from_date" : frm.doc.from_date,
						"to_date" : frm.doc.to_date,
						"name" : frm.doc.name
					},
					freeze: true,
					freeze_message: 'Submitting Shift Schedule....',
				})
				frm.call("on_submit")
			})
		}
		}
	},
	get_template: function (frm) {
		console.log(frappe.request.url)
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s', {
			cmd: "thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.get_template",
			from_date: frm.doc.from_date,
			to_date: frm.doc.to_date,
			department: (frm.doc.department).replace("&", "5")
		});
	},
	from_date(frm) {
		if (frm.doc.from_date) {
			if (frm.doc.from_date < frappe.datetime.now_date()) {
				frappe.msgprint("From Date should not be a Past Date")
				frm.set_value('from_date', '')
			}
			if (frm.doc.from_date > frappe.datetime.add_days(frappe.datetime.now_date(), 7)) {
				frappe.msgprint("From Date should be within 7 days from Today")
				frm.set_value('from_date', '')
			}
		}
	},
	to_date(frm) {
		if (frm.doc.to_date) {
			if (frm.doc.to_date < frappe.datetime.now_date()) {
				frappe.msgprint("To Date should not be a Past Date")
				frm.set_value('to_date', '')
			}
			else if (frm.doc.to_date < frm.doc.from_date) {
				frappe.msgprint("To Date should not be greater than From Date")
				frm.set_value('to_date', '')
			}
			else if (frm.doc.to_date > frappe.datetime.add_days(frm.doc.from_date, 7)) {
				frappe.msgprint("To Date should be within 8 days from From Date")
				frm.set_value('to_date', '')
			}
		}
	},
	upload(frm) {
		frappe.call({
			"method": "thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.get_count",
			"args":{
				"filename" : frm.doc.upload,
				"from_date" : frm.doc.from_date,
				"to_date" : frm.doc.to_date,
			},
			callback(r){
				console.log(r)
				if(r.message == "a"){
					frm.disable_save()
					// frm.set_value('upload','')
					console.log("HI")
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R1")
				}
				if(r.message == "b"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R2")
				}
				if(r.message == "c"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R3")
				}
				if(r.message == "d"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R4")
				}
				if(r.message == "e"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R5")
				}
				if(r.message == "f"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R6")
				}
				if(r.message == "g"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R7")
				}
				if(r.message == "h"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R8")
				}
				if(r.message == "i"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R9")
				}
				if(r.message == "j"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R9B")
				}
				if(r.message == "k"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R10")
				}
				if(r.message == "l"){
					frm.disable_save()
					// frm.set_value('upload','')
					frappe.throw("Employee's Count is more than Fixed Employee's Count through R12")
				}
			}
		})
		frm.trigger('show_csv_data')
		frm.trigger('show_summary')
		if (frm.doc.upload) {
			frm.fields_dict.error_preview.$wrapper.empty()
			frm.call('validate_employees').then(r => {
				if (r.message) {
					frm.fields_dict.error_preview.$wrapper.empty().append("<h2>Error Preview</h2><ul>" + r.message + "</ul>")
					frappe.msgprint(r.message)
					frm.disable_save()
					frm.set_value('upload','')
					frm.fields_dict.summary.$wrapper.empty()
					frm.fields_dict.error_preview.$wrapper.empty()
					frm.fields_dict.csv_preview.$wrapper.empty()

				}
			})
		}
	},
	validate(frm) {
		frm.trigger('show_csv_data')
		frm.trigger('upload')
		frm.trigger('show_summary')
	},
	after_save(frm){
		frappe.call({
			"method": "thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.enqueue_shift_assignment",
			"args":{
				"file" : frm.doc.upload,
				"from_date" : frm.doc.from_date,
				"to_date" : frm.doc.to_date,
				"name" : frm.doc.name
			},
			freeze: true,
			freeze_message: 'Submitting Shift Schedule....',
			// callback(r){
			// 	if(r.message == "ok"){
			// 		// frappe.msgprint("Attendance Marked Successfully")
			// 	}
			// }
		})
	},
	show_csv_data(frm) {
		if (frm.doc.upload) {
			frm.fields_dict.csv_preview.$wrapper.empty()
			frm.call('show_csv_data').then(r => {
				if (r.message) {
					frm.fields_dict.csv_preview.$wrapper.empty().append("<h2>Upload Preview</h2><table class='table table-bordered'>" + r.message + "</table>")
				}
			})
		}
	},
	show_summary(frm) {
		if (frm.doc.upload) {
			frm.fields_dict.summary.$wrapper.empty()
			frm.call('show_summary').then(r => {
				if (r.message) {
					frm.fields_dict.summary.$wrapper.empty().append("<h2>Summary</h2><table class='table table-bordered'>" + r.message + "</table>")
				}
			})
		}
	}
});
