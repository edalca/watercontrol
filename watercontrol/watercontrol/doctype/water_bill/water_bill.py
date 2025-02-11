# Copyright (c) 2025, Edwin Carrillo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date  # Importar date
from calendar import monthrange

class WaterBill(Document):
    def validate(self):
        self.monthly_receipts_insert()

    def monthly_receipts_insert(self):
        self.set('monthly_receipts', [])
        fee = frappe.get_doc('Fee', self.fee)  
        for month in range(1, 13):
            item = self.append('monthly_receipts', {})
            item.month = month  # Asignar el valor de la columna 'month'
            item.service_amount = fee.total  # Asignar el valor del campo de enlace
            item.discount = self.calculate_discount(fee.total, fee.total_discount)  # Calcular el descuento
            item.total = fee.total - item.discount  # Asignar el valor del campo de enlace - item.discount
            
            # Obtener el último día del mes correspondiente
            year = datetime.now().year  # Año en curso
            last_day_of_month = monthrange(year, month)[1]
            item.payment_due_date = date(year, month, last_day_of_month)  # Asignar la fecha límite de pago

        # Realizar alguna acción adicional si es necesario
        self.total = sum(item.total for item in self.get('monthly_receipts')) 

    def calculate_discount(self, total, total_discount):
        # Calcular el descuento si la edad es mayor o igual a 60
        if self.age is not None and self.age != '':
            if self.age >= 60:
                return total - total_discount
            else:
                return 0
        else:
            return 0
