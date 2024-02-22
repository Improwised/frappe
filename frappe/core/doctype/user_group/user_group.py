# Copyright (c) 2021, Frappe Technologies and contributors
# License: MIT. See LICENSE

import frappe
from frappe.core.doctype.user_group_permission.user_group_permission import (
	get_user_permissions_from_user_group,
)
from frappe.model.document import Document


class UserGroup(Document):
	def on_update(self):
		old_doc = self.get_doc_before_save()
		if not old_doc:
			for user in self.user_group_members:
				frappe.cache().hdel("user_group_permission", user)
				frappe.publish_realtime("update_user_group", user=user, after_commit=True)
				get_user_permissions_from_user_group(user)
		else:
			old_users = []
			for user in old_doc.user_group_members:
				old_users.append(user.user)

			new_users = []
			for user in self.user_group_members:
				new_users.append(user.user)

			deleted_users, added_users = self.find_modified_users(old_users, new_users)

			for user in deleted_users:
				frappe.cache().hdel("user_group_permission", user)
				frappe.publish_realtime("update_user_group", user=user, after_commit=True)

			for user in added_users:
				frappe.cache().hdel("user_group_permission", user)
				frappe.publish_realtime("update_user_group", user=user, after_commit=True)
				get_user_permissions_from_user_group(user)

	def find_modified_users(self, old_list, new_list):
		deleted_users = [user for user in old_list if user not in new_list]
		added_users = [user for user in new_list if user not in old_list]
		return deleted_users, added_users
