from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
	message = "You must be the owner of this object"
	my_safe_method = ['GET', 'PUT']
	def has_permission(self, request, view): #basic custom permissions
		if request.method in self.my_safe_method:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		#member = Membership.objects.get(user=request.user)
		#member.is_active #more robust custom permission
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.user == request.user #user = owner in rest docs