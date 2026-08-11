from rest_framework.permissions import BasePermission


class IsCaseOwnerOrCollaborator(BasePermission):
    """
    Faqat case egasi yoki unga qo'shilgan hamkorlar ushbu case'ni
    tahrirlashi mumkin. Boshqalar uchun ruxsat berilmaydi.
    """

    def has_object_permission(self, request, view, obj):
        # obj — bu yerda Case obyekti bo'ladi
        if obj.created_by_id == request.user.id:
            return True
        return obj.collaborators.filter(user=request.user).exists()