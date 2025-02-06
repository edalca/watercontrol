// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Water Bill", {

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
