// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Water Bill", {
  refresh(frm) {
    frm.set_query("fee", function () {
      return {
        filters: {
          docstatus: 1,
          company: frm.doc.company,
        },
      };
    });
    frm.set_query("land", function () {
      return {
        filters: {
          docstatus: 1,
          company: frm.doc.company,
        },
      };
    });
  },
  after_save: function (frm) {
    frm.trigger("birthdate");
    const expected_name = `${frm.doc.fee}-${frm.doc.land}`;
    // Verificar si el name actual coincide con la combinación de fee y land
    if (frm.doc.name !== expected_name) {
      // Redirigir al nuevo URL
      frappe.set_route("Form", "Water Bill", expected_name);
    }
  },
  birthdate(frm) {
    calculate_age(frm);
  },
});

function calculate_age(frm) {
  if (frm.doc.birthdate) {
    const birthdate = new Date(frm.doc.birthdate);
    const today = new Date();
    let age = today.getFullYear() - birthdate.getFullYear();
    const monthDifference = today.getMonth() - birthdate.getMonth();
    if (
      monthDifference < 0 ||
      (monthDifference === 0 && today.getDate() < birthdate.getDate())
    ) {
      age--;
    }
    frm.set_value("age", age);
  }
}
