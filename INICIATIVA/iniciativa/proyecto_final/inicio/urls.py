from django.contrib import admin
from django.urls import path,include
from .views import *
# Registros,index_cliente,Login_request,index_profesional,principal,registroRol,RegistroPro,listar_proyecto,Actualizar_pro
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

app_name='inicio'
urlpatterns = [
    path('plataforma_cliente/',login_required(index_cliente, login_url='/login'), name='plataforma_cliente'),
    path('plataforma_profesional/', login_required(index_profesional, login_url='/login'), name='plataforma_profesional'),
    path('', index, name='principal'),
    path('registro/', Registros.as_view(), name='registro'),
    path('registro_profesional/', RegistroPro.as_view(), name='registro_profesional'),
    path('login/', Login_request,name='login'),
    path('logout/', LogoutView.as_view(template_name='inicio/login.html'),name='logout'),
    path('registro_rol/', registroRol,name='registro_rol'),
    path('publicar_proyecto/',login_required(listar_proyecto.as_view(), login_url='/login')),
    path('Nuevo_proyecto/', login_required( Nuevo_proyecto.as_view(), login_url='/login')),
    path('editar_proyecto/<int:proyecto_id>',login_required( Funciones_info.edit, login_url='/login')),
    path('eliminar_proyecto/<int:proyecto_id>', login_required(Funciones_info.eliminar, login_url='/login')),
    path('eliminar_oferta/<int:oferta_id>/<int:profesional_id>/<int:proyecto_id>',login_required( Funciones_info.rechazar_oferta, login_url='/login')),
    path('escoger_proyecto' , login_required(listar_proyecto_Prof.as_view(), login_url='/login')),
    path('ver_oferta' ,login_required(listar_oferta.as_view(), login_url='/login')),
    path('asesoria' ,login_required(listar_asesoria.as_view(), login_url='/login')),
    path('factura_pago' ,login_required(listar_pagos.as_view(), login_url='/login')),
    path('realizar_pago/<int:proyecto_id>/<int:profesional_id>/<int:oferta_id>' ,login_required(Funciones_info.realizar_pago, login_url='/login')),
    path('enviar_oferta/<int:proyecto_id>' ,login_required(Funciones_info.enviar_info, login_url='/login'),name='enviar_oferta'),
    path('enviar_oferta_asesoria/<int:proyecto_id>' ,login_required(Funciones_info.enviar_info_oferta, login_url='/login'),name='enviar_oferta_asesoria'),
    path('enviar_correo/<str:mail>/<int:proyecto_id>/<int:profesional_id>/<int:oferta_id>', login_required( Funciones_info.send_email, login_url='/login')),
    path('eliminar_pago/<int:pago_id>', login_required( Funciones_info.eliminar_pago, login_url='/login')),
    path('config_cliente', login_required(Funciones_info.config_cliente ,login_url='/login')),
    path('config_profesional', login_required(Funciones_info.config_profesional ,login_url='/login')),
    path('c_p', login_required(CambiarPasswordView.as_view() ,login_url='/login')),
    
   
 
]
