import frappe
from frappe.model.document import Document
from datetime import datetime, date  # Importar date
from calendar import monthrange

class WaterBill(Document):
     
    def before_save(self):
        # Generar el nuevo nombre basado en fee y land
        new_name = f"{self.fee}-{self.land}"
        # Si el name actual no coincide con el nuevo nombre, proceder
        if self.name and self.name != new_name:
            try:
                # Eliminar el registro existente con el nuevo nombre si hay un conflicto
                if frappe.db.exists("Water Bill", new_name):
                    frappe.delete_doc("Water Bill", new_name, force=True)
                
                # Renombrar el documento principal
                frappe.rename_doc("Water Bill", self.name, new_name, force=True)
                self.name = new_name  # Actualizar el valor del `name` en la instancia
            except frappe.ValidationError as e:
                frappe.throw(f"No se pudo renombrar el documento: {e}")
        self.monthly_receipts_insert()

    def monthly_receipts_insert(self):
        # Limpiar los recibos mensuales existentes
        self.set('monthly_receipts', [])
        fee = frappe.get_doc('Fee', self.fee)  

        # Crear registros para cada mes
        for month in range(1, 13):
            item = self.append('monthly_receipts', {})
            item.month = month  # Asignar el mes
            item.service_amount = fee.total  # Obtener el total del servicio desde la tarifa (fee)
            item.discount = self.calculate_discount(fee.total, fee.total_discount)  # Calcular descuento
            item.total = fee.total - item.discount  # Calcular el total después del descuento

            # Obtener el último día del mes correspondiente
            year = datetime.now().year  # Año actual
            last_day_of_month = monthrange(year, month)[1]
            item.payment_due_date = date(year, month, last_day_of_month)  # Asignar fecha límite de pago

        # Calcular el total acumulado
        self.total = sum(item.total for item in self.get('monthly_receipts'))

    def calculate_discount(self, total, total_discount):
        # Calcular el descuento basado en la edad (mayores o iguales a 60)
        if self.age is not None and self.age != '':
            if self.age >= 60:
                return total - total_discount
            else:
                return 0
        else:
            return 0
