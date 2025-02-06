// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Water Bill Payment", {
  onload: function (frm) {
    set_current_date(frm);
  },
  refresh: function (frm) {
    frm.fields_dict.receipts_pay.grid.wrapper.find(".grid-buttons").hide();
    frm.fields_dict.receipts_pay.grid.wrapper.find('.grid-row-check').hide();
    if (frm.is_new()) {
      set_current_date(frm);
    }
  },
});

frappe.ui.form.on("Water Bill Paid",{
    paid: function(frm){
        calculate_total(frm)
    }
})
function calculate_total(frm) {
  let total = 0;
  frm.doc.receipts_pay.forEach(function (row) {
    if (row.paid) {
      total += row.total; // Reemplaza 'amount_field' con el nombre real del campo que quieres sumar
    }
  });
  frm.set_value("total_to_pay", total); // Reemplaza 'total_field' con el nombre real de tu campo de total
}
function set_current_date(frm) {
  let today = frappe.datetime.get_today();
  frm.set_value("date", today); // Reemplaza 'your_date_field' con el nombre real de tu campo de fecha
}
