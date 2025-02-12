// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.query_reports["Water Bill Receivable"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "cutoff_date",
			label: __("Cutoff Date"),
			fieldtype: "Date",
			reqd:1,
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "subscriber",
			label: __("Subscriber"),
			fieldtype: "Link",
			options: "Subscriber",
			get_query: () => {
				var company = frappe.query_report.get_filter_value("company");
				return {
					filters: {
						company: company,
						docstatus: 1,
					},
				};
			},
		},
		{
			fieldname: "range",
			label: __("Ageing Range"),
			fieldtype: "Data",
			default: "30, 60, 90, 120",
		},
	]
};
