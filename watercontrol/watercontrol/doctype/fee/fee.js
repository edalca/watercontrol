// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt
frappe.ui.form.on("Fee", {
  refresh(frm){
    calculate_totals(frm);
    frm.fields_dict['service_fee'].grid.get_field('service_name').get_query = function(doc, cdt, cdn) {
      return {
          filters: {
              'company': frm.doc.company
          }
      };
  };
  },
  before_save(frm) {
    calculate_totals(frm);
  },
  service_fee_add(frm) {
    calculate_totals(frm);
  },
  service_fee_remove(frm) {
    calculate_totals(frm);
  },
});

function calculate_totals(frm) {
  let total = 0;
  let total_discount = 0;

  frm.doc.service_fee.forEach(function (d) {
    total += d.fee; // Sumar el fee normal al total

    if (d.discount_applies) {
      total_discount += d.fee * 0.75; // Aplicar un descuento del 25%
    } else {
      total_discount += d.fee; // Usar el fee normal
    }
  });

  frm.set_value("total", total); // Actualizar el campo total
  frm.set_value("total_discount", Math.ceil(total_discount)); // Actualizar el campo total_discount
}
