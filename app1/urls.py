from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.registro_view, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('principal_miticket/', views.principal_miticket_view, name='principal_miticket'),

    # Vistas de Django de recuperar contraseña
    path('reset/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html'), name="password_reset"),
    path('reset/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('reset/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Consultar tickets
    path('consultar_ticket/', views.consultar_ticket_view, name='consultar_ticket'),
    path('crear_ticket/', views.crear_ticket_view, name='crear_ticket'),
    path('editar_ticket/<int:id>/', views.editar_ticket_view, name='editar_ticket'),
    path('eliminar_ticket/<int:id>/', views.eliminar_ticket, name='eliminar_ticket'),
    path('estado_prioridad_update/<int:id>', views.estado_prioridad_update, name='estado_prioridad_update'),
    path('comentar_ticket/<int:id>/', views.comentar_ticket_view, name='comentar_ticket'),

    # Vista de general reportes
    path('generar_reportes/', views.generar_reportes_view, name='generar_reportes'),

    # Crear usuarios / consultar usuarios
    path('consultar_usuarios/', views.consultar_usuarios_view, name='consultar_usuarios'),
    path('perfil_de_usuario/<int:id>/', views.perfil_de_usuario_view, name='perfil_de_usuario'),
    path('crear_usuario/', views.crear_usuario_view, name='crear_usuario'),
    path('editar_usuario/<int:id>/', views.editar_usuario_view, name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # -----
    # path('update_usuario_view/<int:id>/', views.update_usuario_view, name='update_usuario_view'),
    path('cambio_clave/', views.cambio_clave, name='cambio_clave'),
    path('cuenta_usuario/', views.cuenta_usuario, name='cuenta_usuario'),
    path('estado_de_ticket/', views.estado_de_ticket, name='estado_de_ticket') # <- Eliminar...

]