frappe.listview_settings["Subscriber"] = {
    get_indicator: function(doc) {
        // Si el abonado está desactivado
        if (doc.disabled) {
            return [__("Disabled"), "grey", "disabled,=,1"];
        }
        // Si el abonado está activo
        return [__("Enabled"), "green", "disabled,=,0"];
    }
};
