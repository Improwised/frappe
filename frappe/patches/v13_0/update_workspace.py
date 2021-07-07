import frappe
import json
from frappe import _

def execute():
	frappe.reload_doc('desk', 'doctype', 'workspace', force=True)
	order_by = "is_standard asc, pin_to_top desc, pin_to_bottom asc, name asc"
	for seq, wspace in enumerate(frappe.get_all('Workspace', order_by=order_by)):
		doc = frappe.get_doc('Workspace', wspace.name)
		content = create_content(doc)
		update_wspace(doc, seq, content)
	frappe.db.commit()

def create_content(doc):
	content = []
	if doc.charts:
		for c in doc.charts:
			content.append({"type":"chart","data":{"chart_name":c.label,"col":12,"pt":0,"pr":0,"pb":0,"pl":0}})
	if doc.shortcuts:
		content.append({"type":"spacer","data":{"col":12,"pt":0,"pr":0,"pb":0,"pl":0}})
		content.append({"type":"header","data":{"text":doc.shortcuts_label or _("Your Shortcuts"),"level":4,"col":12,"pt":0,"pr":0,"pb":0,"pl":0}})
		for s in doc.shortcuts:
			content.append({"type":"shortcut","data":{"shortcut_name":s.label,"col":4,"pt":0,"pr":0,"pb":0,"pl":0}})
	if doc.links:
		content.append({"type":"spacer","data":{"col":12,"pt":0,"pr":0,"pb":0,"pl":0}})
		content.append({"type":"header","data":{"text":doc.cards_label or _("Reports & Masters"),"level":4,"col":12,"pt":0,"pr":0,"pb":0,"pl":0}})
		for l in doc.links:
			if l.type == 'Card Break':
				content.append({"type":"card","data":{"card_name":l.label,"col":4,"pt":0,"pr":0,"pb":0,"pl":0}})
	return content

def update_wspace(doc, seq, content):
	doc.sequence_id = seq + 1
	doc.content = json.dumps(content)
	if doc.is_standard:
		doc.public = 1
		doc.for_user = ''
		doc.title = doc.label
	else:
		doc.public = 0
		doc.for_user = doc.for_user
		doc.title = doc.extends
	doc.extends = ''
	doc.module = ''
	doc.category = ''
	doc.restrict_to_domain = ''
	doc.onboarding = ''
	doc.extends_another_page = 0
	doc.is_default = 0
	doc.is_standard = 0
	doc.developer_mode_only = 0
	doc.disable_user_customization = 0
	doc.pin_to_top = 0
	doc.pin_to_bottom = 0
	doc.hide_custom = 0
	doc.save()