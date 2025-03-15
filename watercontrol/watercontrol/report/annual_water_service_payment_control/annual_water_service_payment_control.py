import frappe
from frappe import _

def execute(filters=None):
    # Crear las columnas y los datos del reporte
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    # Definir las columnas del reporte
    return [
        {"label": "Nombre del Abonado", "fieldname": "subscriber", "fieldtype": "Data", "width": 200},
        {"label": "EXT", "fieldname": "rate_type", "fieldtype": "Data", "width": 150},
        {"label": "Edad", "fieldname": "age", "fieldtype": "Int", "width": 80},
        {"label": "B", "fieldname": "block", "fieldtype": "Data", "width": 80},
        {"label": "C", "fieldname": "house", "fieldtype": "Data", "width": 80},
        {"label": "January", "fieldname": "jan", "fieldtype": "Data", "width": 80},
        {"label": "February", "fieldname": "feb", "fieldtype": "Data", "width": 80},
        {"label": "March", "fieldname": "mar", "fieldtype": "Data", "width": 80},
        {"label": "April", "fieldname": "apr", "fieldtype": "Data", "width": 80},
        {"label": "May", "fieldname": "may", "fieldtype": "Data", "width": 80},
        {"label": "June", "fieldname": "jun", "fieldtype": "Data", "width": 80},
        {"label": "July", "fieldname": "jul", "fieldtype": "Data", "width": 80},
        {"label": "August", "fieldname": "aug", "fieldtype": "Data", "width": 80},
        {"label": "September", "fieldname": "sep", "fieldtype": "Data", "width": 80},
        {"label": "October", "fieldname": "oct", "fieldtype": "Data", "width": 80},
        {"label": "November", "fieldname": "nov", "fieldtype": "Data", "width": 80},
        {"label": "December", "fieldname": "dec", "fieldtype": "Data", "width": 80},
    ]

def get_data(filters):
    if not filters or not filters.get("company"):
        frappe.throw(_("Please select a Company"))

    company = filters.get("company")
    fiscal_year = "2025"  # Año fiscal específico para el filtro

    # Paso 1: Obtener los Fee relacionados con el año fiscal
    fee_names = frappe.get_all(
        "Fee",
        filters={"bill_year": fiscal_year},
        fields=["name"]
    )
    fee_names = [fee["name"] for fee in fee_names]  # Convertir a lista de nombres

    # Paso 2: Obtener los Water Bills relacionados con los Fee anteriores
    water_bills = frappe.get_all(
        "Water Bill",
        filters={
            "company": company,
            "docstatus": 1,
            "fee": ["in", fee_names]  # Filtrar por Fee
        },
        fields=["name", "subscriber", "age", "fee", "block", "house"]
    )

    # Paso 3: Construir los datos del reporte
    data = []
    for bill in water_bills:
        # Obtener la tarifa relacionada (Fee)
        fee_doc = frappe.get_doc("Fee", bill.fee) if bill.fee else None
        fee_name = fee_doc.fee_name if fee_doc else "N/A"

        # Obtener los registros de Bill Payment Scheduling
        bill_scheduling = frappe.get_all(
            "Bill Payment Scheduling",
            filters={"parent": bill.name},
            fields=["month", "payment_date"]
        )

        # Inicializar estado de los meses
        months_status = {month: "" for month in range(1, 13)}
        for schedule in bill_scheduling:
            if schedule.payment_date:  # Si tiene una fecha de pago, significa que fue pagado
                months_status[schedule.month] = '<div style="text-align: center; vertical-align: middle;"><span class="badge badge-success">{}</span></div>'.format(_("Pagado"))

        # Agregar fila al reporte
        data.append({
            "subscriber": bill.subscriber or "Sin Abonado",  # Nombre del abonado
            "rate_type": fee_name,                          # Tipo de tarifa
            "age": bill.age or "",                       # Edad del abonado
            "block": bill.block or "",                   # Bloque
            "house": bill.house or "",                   # Casa
            "jan": months_status.get(1, ""),               # Pagos para enero
            "feb": months_status.get(2, ""),               # Pagos para febrero
            "mar": months_status.get(3, ""),               # Pagos para marzo
            "apr": months_status.get(4, ""),               # Pagos para abril
            "may": months_status.get(5, ""),               # Pagos para mayo
            "jun": months_status.get(6, ""),               # Pagos para junio
            "jul": months_status.get(7, ""),               # Pagos para julio
            "aug": months_status.get(8, ""),               # Pagos para agosto
            "sep": months_status.get(9, ""),               # Pagos para septiembre
            "oct": months_status.get(10, ""),              # Pagos para octubre
            "nov": months_status.get(11, ""),              # Pagos para noviembre
            "dec": months_status.get(12, ""),              # Pagos para diciembre
        })

    return data
