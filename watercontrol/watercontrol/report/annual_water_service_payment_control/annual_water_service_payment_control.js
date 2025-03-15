// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.query_reports["Annual Water Service Payment Control"] = {
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
            fieldname: "year",
            label: __("Year"),
            fieldtype: "Int",
            reqd: 1, // Opcional: si el año debe ser obligatorio
            default: new Date().getFullYear() // Opción para establecer el año actual como predeterminado
        },
		{
            fieldname: "subscriber",
            label: __("Subscriber"),
            fieldtype: "Link",
			options:"Subscriber",
            reqd: 0, 
        },
		{
            fieldname: "block",
            label: __("Block"),
            fieldtype: "Int",
        },
		{
            fieldname: "house",
            label: __("House"),
            fieldtype: "Int",
        }
	]
};
