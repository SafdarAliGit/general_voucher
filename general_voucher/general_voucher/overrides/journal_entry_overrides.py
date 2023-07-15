import frappe
from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry
from frappe.model.naming import make_autoname


class JournalEntryOverrides(JournalEntry):
    def autoname(self):
        self.name = self.bill_no



