# Copyright (c) 2025, Edwin Carrillo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WaterBillPayment(Document):
	def validate(self):
		self.receipts_pay_insert()

	def before_submit(self):
		self.remove_unmarked_payments()
		self.update_payment_scheduling_dates()

	def on_cancel(self):
		self.reset_payment_scheduling_dates()

	def receipts_pay_insert(self):
		if not self.receipts_pay:
			self.set('receipts_pay', [])
			waterBill = frappe.get_doc('Water Bill', self.water_bill)  
			for billPayment in waterBill.monthly_receipts:
				if  not billPayment.payment_date:
					item = self.append('receipts_pay', {})
					item.month =billPayment.month
					item.service_amount=billPayment.service_amount
					item.discount =billPayment.discount
					item.total = billPayment.total

	def remove_unmarked_payments(self):
		keep_items = [d for d in self.receipts_pay if d.paid]
		self.receipts_pay = keep_items
	
	def update_payment_scheduling_dates(self):
		for receipt in self.receipts_pay:
			if receipt.paid:
				frappe.db.sql("""
                    UPDATE `tabBill Payment Scheduling`
                    SET payment_date = %s, water_bill_payment = %s
                    WHERE parent = %s AND month = %s
                """, (self.date, self.name, self.water_bill, receipt.month))
	
	def reset_payment_scheduling_dates(self):
		frappe.db.sql("""
            UPDATE `tabBill Payment Scheduling`
            SET payment_date = NULL, water_bill_payment = NULL
            WHERE parent = %s
        """, (self.water_bill,))