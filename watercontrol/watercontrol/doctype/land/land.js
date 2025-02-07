// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Land", {
  refresh(frm) {
    frm.set_query('subscriber', function() {
        return {
            filters: {
                'docstatus': 1,
                'company':frm.doc.company
            }
        };
    });
  },
});
