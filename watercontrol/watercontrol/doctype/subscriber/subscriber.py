# Copyright (c) 2025, Edwin Carrillo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Subscriber(Document):
	pass
	def validate(self):
		self.set_full_name()

	def set_full_name(self):
		self.full_name = " ".join(
			filter(lambda x: x, [self.first_name, self.middle_name, self.last_name])
		)
