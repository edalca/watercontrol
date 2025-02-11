// Copyright (c) 2025, Edwin Carrillo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Subscriber", {
  refresh(frm) {
    if(frm.is_new()){
        entityCheck(frm);
    }else{
        entityDisplay(frm);
    }
  },
  entity(frm) {
    entityCheck(frm);
  },
});

function entityCheck(frm) {
  entityDisplay(frm);
  entityClear(frm);
  entityReqd(frm);
  generateCode(frm)
}

function entityDisplay(frm) {
  if (frm.doc.entity == 1) {
    frm.toggle_enable("first_name", false);
    frm.toggle_enable("middle_name", false);
    frm.toggle_enable("last_name", false);
    frm.toggle_enable("full_name", true);
    frm.toggle_enable("identification", false);
    frm.toggle_enable("birthdate", false);
  } else {
    frm.toggle_enable("first_name", true);
    frm.toggle_enable("middle_name", true);
    frm.toggle_enable("last_name", true);
    frm.toggle_enable("full_name", false);
    frm.toggle_enable("identification", true);
    frm.toggle_enable("birthdate", true);
  }
}
function entityClear(frm) {
    if (frm.is_new()){
        frm.set_value("first_name");
        frm.set_value("middle_name");
        frm.set_value("last_name");
        frm.set_value("full_name");
        frm.set_value("identification")
        frm.set_value("birthdate")
    }

}
function entityReqd(frm) {
  if (frm.doc.entity === 0) {
    frm.toggle_reqd("first_name", true);
    frm.toggle_reqd("last_name", true);
    frm.toggle_reqd("full_name", false);
    frm.toggle_reqd("birthdate", true);
  } else {
    frm.toggle_reqd("first_name", false);
    frm.toggle_reqd("last_name", false);
    frm.toggle_reqd("full_name", true);
    frm.toggle_reqd("birthdate", false);
  }
}
function generateCode(frm) {
    // Verificar si el valor de doc.entity es 1
    if (frm.doc.entity == 1) {
        // Obtener la fecha y hora actual
        var now = new Date();

        // Formatear la fecha y hora
        var year = now.getFullYear().toString().slice(-2); // Últimos 2 dígitos del año
        var month = ('0' + (now.getMonth() + 1)).slice(-2); // Mes con 2 dígitos
        var day = ('0' + now.getDate()).slice(-2); // Día con 2 dígitos
        var hours = ('0' + now.getHours()).slice(-2); // Hora con 2 dígitos
        var minutes = ('0' + now.getMinutes()).slice(-2); // Minutos con 2 dígitos
        var seconds = ('0' + now.getSeconds()).slice(-2); // Segundos con 2 dígitos
        var milliseconds = ('00' + now.getMilliseconds()).slice(-3); // Milisegundos con 3 dígitos

        // Combinar para crear el código de 13 dígitos (usando los primeros 13 dígitos resultantes)
        var code = year + month + day + hours + minutes + seconds + milliseconds;

        // Asignar el código al campo 'identification'
        frm.set_value('identification', code.slice(0, 13)); // Asegurarse de que solo sean 13 dígitos
    }
}
