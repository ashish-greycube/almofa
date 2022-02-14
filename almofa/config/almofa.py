from __future__ import unicode_literals
from frappe import _


def get_data():
    config = [
        {'label': _('Tender'), 
        'items': [
                {
                    "type": "doctype",
                    "name": "Tender Info",
                    "label": _("Tender Info")
                },
                {
                    "type": "doctype",
                    "name": "Quotation",
                    "label": _("Quotation")
                },
                {
                    "type": "doctype",
                    "name": "Sales Order",
                    "label": _("Sales Order")
                }                                   
            ]
        }
    ]
    return config    