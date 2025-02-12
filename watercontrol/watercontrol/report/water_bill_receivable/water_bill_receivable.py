# Copyright (c) 2025, Edwin Carrillo and contributors
# For license information, please see license.txt

import frappe
from frappe import _, qb, query_builder, scrub
from frappe.query_builder import Criterion
from frappe.query_builder.functions import Date, Substring, Sum
from frappe.utils import cint, cstr, flt, getdate, nowdate
from calendar import monthrange
from datetime import datetime, date  

def execute(filters=None):
	return WaterBillreceivableReport(filters).run()

class WaterBillreceivableReport:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.qb_selection_filter = []
		self.filters.cutoff_date = getdate(self.filters.cutoff_date or nowdate())  # Asegurar que cutoff_date es datetime.date
		self.wb = qb.DocType("Water Bill")
		if not self.filters.range:
			self.filters.range = "30, 60, 90, 120"
		self.ranges = [num.strip() for num in self.filters.range.split(",") if num.strip().isdigit()]
		self.range_numbers = [num for num in range(1, len(self.ranges) + 2)]

	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data
	
	def get_columns(self):
		self.columns=[]
		self.add_column(	
			label=_("Subscriber"),
			fieldname="subscriber",
			fieldtype="Data",
			width=240)
		self.add_column(_("Block"),"block","Int")
		self.add_column(_("House"),"house","Int")
		self.add_column(_("Paid Amount"), "paid")
		self.add_column(_("Outstanding Amount"),"outstanding")
		self.setup_ageing_columns()

	def add_column(self, label, fieldname=None, fieldtype="Currency", options=None, width=120):
		if not fieldname:
			fieldname = scrub(label)
		if fieldtype == "Currency":
			options = "currency"
		if fieldtype == "Date":
			width = 90

		self.columns.append(
			dict(label=label, fieldname=fieldname, fieldtype=fieldtype, options=options, width=width)
		)
	def setup_ageing_columns(self):
			# for charts
			self.ageing_column_labels = []
			ranges = [*self.ranges, _("Above")]

			prev_range_value = 0
			for idx, curr_range_value in enumerate(ranges):
				label = f"{prev_range_value}-{curr_range_value}"
				self.add_column(label=label, fieldname="range" + str(idx + 1))

				self.ageing_column_labels.append(label)

				if curr_range_value.isdigit():
					prev_range_value = cint(curr_range_value) + 1

	def get_data(self):
		self.qb_selection_filter = []  # Inicializar la lista de filtros

		# Agregar filtros a la lista
		self.qb_selection_filter.append(self.wb.company.eq(self.filters.company))
		self.qb_selection_filter.append(self.wb.docstatus.eq(1))

		# Filtrar por suscriptor si se proporciona
		if self.filters.get("subscriber"):
			self.qb_selection_filter.append(self.wb.subscriber.eq(self.filters.subscriber))

		# Definir el DocType "Water Bill"
		wb = qb.DocType("Water Bill")

		# Construir la consulta con los filtros agregados
		query = (
			qb.from_(wb)
			.select(
				wb.name,
				wb.fee,
				wb.land,
				wb.subscriber,
				wb.block,
				wb.house,
			)
			.where(Criterion.all(self.qb_selection_filter))
		)

		# Ejecutar la consulta y almacenar los resultados
		self.wb_entries = query.run(as_dict=True)

		# Obtener y procesar los datos del DocType secundario
		for entry in self.wb_entries:
			bill_payment_scheduling = frappe.get_all(
				'Bill Payment Scheduling', 
				filters={'parent': entry['name']}, 
				fields=['month', 'service_amount', 'discount', 'total', 'payment_date', 'payment_due_date']
			)

			# Inicializar montos pagados y pendientes
			paid_amount = 0
			outstanding_amount = 0
			range_totals = {f"range{idx + 1}": 0 for idx in range(len(self.ranges) + 1)}

			# Calcular montos pagados y pendientes
			for bps in bill_payment_scheduling:
				if bps['payment_date'] is None and getdate(self.payment_due_date(entry,bps))> getdate(self.filters.cutoff_date):
					outstanding_amount += bps['total']
					# Determinar el rango de atraso
					days_past_due = (getdate(self.filters.cutoff_date) - getdate(self.payment_due_date(entry,bps))).days
					for idx, range_end in enumerate(self.ranges):
						if days_past_due <= int(range_end):
							range_totals[f"range{idx + 1}"] += bps['total']
							break
					else:
						range_totals[f"range{len(self.ranges) + 1}"] += bps['total']
				elif bps['payment_date'] is not None:
					paid_amount += bps['total']

			entry['Paid Amount'] = paid_amount
			entry['Outstanding Amount'] = outstanding_amount
			for range_label, total in range_totals.items():
				entry[range_label] = total

		self.data = self.wb_entries

	def payment_due_date(self,entry, bps):
		fee = frappe.get_doc("Fee",entry.fee)
		year = int(fee.bill_year)
		month = bps['month']
		last_day_of_month = monthrange(year, month)[1]
		payment_due_date = datetime(year, month, last_day_of_month).date()
		if bps["payment_due_date"] is None:
			return payment_due_date
		else:
			return bps["payment_due_date"]