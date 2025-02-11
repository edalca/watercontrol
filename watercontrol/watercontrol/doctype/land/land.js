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

function checkReadOnly(frm){
  if (frm.doc.party==1 && frm.doc.subscriber){
    frm.toggle_enable("full_name",true)
  }else{
    frm.toggle_enable("full_name",false)
  }
}