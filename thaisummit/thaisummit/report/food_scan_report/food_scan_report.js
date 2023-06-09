// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Food Scan Report"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1,
            // "default": frappe.datetime.nowdate()
    
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1,
            // "default": frappe.datetime.nowdate()
            
        },
        {
			"fieldname": "menu",
			"label": __("Menu"),
			"fieldtype": "Link",
			"options": "Food Menu"
		},
        // {
		// 	"fieldname": "employee",
		// 	"label": __("Employee"),
		// 	"fieldtype": "Link",
        //     "options": "Employee"

		// },
    ]
};

