from django.urls import path
from .views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, edit_group, create_group,group_list

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:id>/edit-group',edit_group, name='edit-group' ),
    path('admin/create-group', create_group, name = 'create-group'),
    path('admin/group-list', group_list, name='group-list')
]
