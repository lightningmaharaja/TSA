// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["First Aid"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
	
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
			
		},
		{
			"fieldname": "id_no",
			"label": __("ID NO"),
			"fieldtype": "Link",
			"options": "Employee"
		}

	]
};
