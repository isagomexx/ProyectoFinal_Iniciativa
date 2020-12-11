from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpRequest
from django.views.generic import CreateView,ListView,TemplateView, FormView
from .Modelform import RegistroModelForm,Login, RegistroModelFormPro,DescripcionProyecto,grouped,RegistroCliente,Envio_oferta,Pagos,RegistroProfesional
from django.template.loader import get_template
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import Cliente,Proyecto,Profesional,Oferta,Pago
from django import forms
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from .forms import  UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F



def registro_cliente(request):
    return render(request,'inicio/registroCliente.html')

def index_cliente(request):
    return render(request,'cliente/index_cliente.html')
 
def index_profesional(request):
    cliente='hola'
    return render(request,'profesional/index_profesional.html',{'cliente':cliente})
def index(request):
    return render(request,'inicio/index.html')
def registroRol(request):
    return render(request,'inicio/registro_rol.html')
def escogerProyecto(request):
    return render(request,'profesional/escoger_proyecto.html')
# def ver_oferta(request):
#     return render(request,'cliente/ver_oferta.html')
def pagos(request):
    return render(request,'cliente/factura_pagos.html')
def asesoria(request):
    return render(request,'profesional/asesoria.html')
class Registros(CreateView):

    form_class = RegistroModelForm
    template_name = 'inicio/registro.html'
    def post(self,request):
        if request.method =='POST':
            form= RegistroModelForm(request.POST or None, request.FILES or None)
            
            if form.is_valid():
                user = form['userCliente'].save()
                cliente = form['cliente'].save(commit=False)
                proyecto = form['proyecto'].save(commit=False)
                cliente.user = user
                proyecto.cliente=cliente
                cliente.save()
                proyecto.save()
                msg=True
                if msg:
                    return render(request,'inicio/index.html',{'msg':msg,'form':form})
        return render(request,'inicio/registro.html',{'form':form})

        
        # return HttpResponseRedirect(reverse('login'))
        # except Exception:
        # for msg in form.error_messages:
        #  messages.error(request , f"{msg}:¨{form.error_messages[msg]}")
        
        

        
class RegistroPro(CreateView):
    
    form_class = RegistroModelFormPro
    template_name = 'inicio/registro_pro.html'
    def post(self,request):
        if request.method =='POST':
            form= RegistroModelFormPro(request.POST or None, request.FILES or None)
            
            if form.is_valid():
                user = form['userProfesional'].save()
                profesional= form['profesional'].save(commit=False)
                profesional.user = user
                profesional.save()
                msg=True
                if msg:
                    return render(request,'inicio/index.html',{'msg':msg,'form':form})
            return render(request,'inicio/registro_pro.html',{'form':form})
        
        
def Login_request(request):
    if request.method == "POST":
        form=Login(request,data=request.POST)
        if form.is_valid():
            usuario= form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')
            rol = form.cleaned_data.get('rol')
            # rol_tb=User.objects.filter(first_name=rol).only('first_name')
            user= authenticate(username=usuario,password=clave)
            if user is not None:
                if user.first_name == 'Cliente' and rol == 'Cliente':
                    login(request,user)
               
                    return redirect("inicio:plataforma_cliente")
                elif user.first_name == 'Profesional'  and rol == 'Profesional' :
                    login(request,user)
              
                    return redirect("inicio:plataforma_profesional")

                elif rol =='Seleccione':
                    messages.error(request,'Debe seleccionar un rol') 
                else:
                    messages.error(request,'Usted no tiene autorizacion para ingresar con el rol escogido')
            else:
                messages.error(request,'Usuario o contraseña incorrectos') 
        else:
            messages.error(request,'Usuario o contraseña incorrectos') 

    form= Login()
    return render(request,"inicio/login.html",{'form':form})

def Logout_request(request):
    logout(request)
    messages.info(request,"saliste exitosamente")
    return redirect("inicio:index.html")
    
        
class Nuevo_proyecto(CreateView):
    model=Proyecto
    form_class = DescripcionProyecto
    template_name = 'cliente/Nuevo_proyecto.html'
    
    def post(self,request):

        if request.method =='POST':
            form= DescripcionProyecto (request.POST or None, request.FILES or None)
           
            if form.is_valid():
                client = Cliente()
                client.id_cliente = Cliente.objects.get(user = request.user )
                instance = form.save(commit=False)
                instance.cliente = client.id_cliente
                instance.save()
               
                return redirect('/publicar_proyecto')
        return render(request,'cliente/Nuevo_proyecto.html',{'form':form})
        
class listar_proyecto(ListView):
    model=Proyecto
    form_class = DescripcionProyecto
    template_name = 'cliente/publicar_proyecto.html'
    
   
    def get_context_data(self,**kwargs):
        cliente=Cliente.objects.get(user=self.request.user.id)
        proyecto=Proyecto.objects.filter(cliente=cliente.id_cliente)
        pago=Pago.objects.values_list('proyecto',flat=True)
        # usu=Proyecto.objects.values_list('user')
        context=super().get_context_data(**kwargs)
        context['title']='Publicar Proyecto'
        context['object_list'] = grouped(Proyecto.objects.all(), 2)
        context['form']=DescripcionProyecto()
        context['proyecto']=proyecto
        context['pago']=list(pago)


        return context

        
class listar_proyecto_Prof(ListView):
    model=Proyecto
    form_class = DescripcionProyecto
    template_name = 'profesional/escoger_proyecto.html'
    
   
    def get_context_data(self,**kwargs):
        profesional=Profesional.objects.get(user=self.request.user.id)
        oferta=Oferta.objects.all()
        oferta1=Oferta.objects.filter(profesional=profesional.id_profesional).values_list('proyecto', flat=True).distinct()
        oferta_e=Oferta.objects.filter(profesional=profesional.id_profesional,estado=1).values_list('proyecto', flat=True).distinct()
        oferta_r=Oferta.objects.filter(profesional=profesional.id_profesional,estado=2).values_list('proyecto', flat=True).distinct()
        pago=Pago.objects.values_list('proyecto',flat=True)
        context=super().get_context_data(**kwargs)
        context['object_list'] = grouped(Proyecto.objects.all().prefetch_related('cliente'), 2)
        context['list_pro']=Profesional.objects.filter(user=self.request.user.id)
        context['form']=DescripcionProyecto()
        context['oferta']=oferta
        context['oferta1']=list(oferta1)
        context['oferta_estado']=list(oferta_e)
        context['oferta_rechazada']=list(oferta_r)
        context['pago']=list(pago)
      
  
        return context
class listar_asesoria(ListView):
    model=Proyecto
    form_class = DescripcionProyecto
    template_name = 'profesional/asesoria.html'
    
   
    def get_context_data(self,**kwargs):
        profesional=Profesional.objects.get(user=self.request.user.id)
        oferta=Oferta.objects.filter(profesional=profesional.id_profesional).values_list('proyecto', flat=True).distinct()
        oferta_e=Oferta.objects.filter(profesional=profesional.id_profesional,estado=1).values_list('proyecto', flat=True).distinct()
        oferta_r=Oferta.objects.filter(profesional=profesional.id_profesional,estado=2).values_list('proyecto', flat=True).distinct()
        pago=Pago.objects.values_list('proyecto',flat=True)
        context=super().get_context_data(**kwargs)
        context['object_list'] = grouped(Proyecto.objects.all().prefetch_related('cliente'), 2)
        context['list_pro']=Profesional.objects.filter(user=self.request.user.id)
        context['form']=DescripcionProyecto()
        context['oferta']=list(oferta)
        context['oferta_estado']=list(oferta_e)
        context['oferta_rechazada']=list(oferta_r)
        context['pago']=list(pago)
        

        return context
    
    
class listar_oferta(ListView):
    model=Oferta
    form_class = Envio_oferta
    template_name = 'cliente/ver_oferta.html'
    
   
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cliente= Cliente.objects.get(user=self.request.user.id)
        context['object_list'] = grouped(Oferta.objects.all(), 2)
        context['list_pro']=Proyecto.objects.filter(cliente=cliente)
        context['form']=Pagos()
        
        return context
class Funciones_info(HttpRequest):
    
    def edit(request, proyecto_id):
        instancia = Proyecto.objects.get(pk=proyecto_id)
        form = DescripcionProyecto(instance=instancia)
        if request.method == "POST":
            form = DescripcionProyecto(request.POST, instance=instancia)
            if form.is_valid():
                instancia = form.save(commit=False)
                instancia.save()
                return redirect('/publicar_proyecto')
        return render(request,'cliente/editar_proyecto.html',{'form':form})
    def eliminar(request, proyecto_id):
        instancia = Proyecto.objects.get(pk=proyecto_id)
        instancia.delete()
        return redirect('/publicar_proyecto')
    def rechazar_oferta(request,oferta_id,profesional_id,proyecto_id):
        instancia = Oferta.objects.get(pk=oferta_id)
        profesional=Profesional.objects.get(id_profesional=profesional_id)
        proyecto= Proyecto.objects.get(id_proyecto=proyecto_id)
        instancia.estado=2
        instancia.save()
        context={'mail':profesional.correo_electronico,'proyecto':proyecto,'profesional':profesional}
        template = get_template('profesional/correo_oferta_rechazada.html')
        content= template.render(context)
        email= EmailMultiAlternatives('INICIATIVA','Iniciativa',settings.EMAIL_HOST_USER,[profesional.correo_electronico])
        email.attach_alternative(content,'text/html')
        email.send()
        return redirect('/ver_oferta')
    
    def enviar_info(request, proyecto_id):
        instancia1 = Proyecto.objects.get(pk=proyecto_id)
        instancia2= Profesional.objects.get(user=request.user)
        form = Envio_oferta()
        if request.method == "POST":
            form = Envio_oferta(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.profesional = instancia2
                instance.proyecto = instancia1
                instance.save()
                msg=True
                if msg:
                    return render(request,'profesional/escoger_proyecto.html',{'msg':msg}) 
    
        return render(request,'profesional/enviar_oferta.html',{'form':form})   
    
    def send_email(request,mail,proyecto_id,profesional_id,oferta_id):
        cliente =Cliente.objects.get(user=request.user.id)
        proyecto= Proyecto.objects.get(id_proyecto=proyecto_id)
        profesional=Profesional.objects.get(id_profesional=profesional_id)
        context={'mail':mail,'cliente':cliente,'proyecto':proyecto,'profesional':profesional}
        template = get_template('profesional/correo.html')
        content= template.render(context)
        email= EmailMultiAlternatives('INICIATIVA','Iniciativa',settings.EMAIL_HOST_USER,[mail])
        email.attach_alternative(content,'text/html')
        email.send()
        oferta=Oferta.objects.get(id_oferta=oferta_id)
        oferta.estado=1
        oferta.save()
        msg=True
        return render(request,'cliente/ver_oferta.html',{'msg':msg})
        
    
 
   
        
    def enviar_info_oferta(request, proyecto_id):
        instancia1 = Proyecto.objects.get(pk=proyecto_id)
        instancia2= Profesional.objects.get(user=request.user)
        form = Envio_oferta()
        if request.method == "POST":
            form = Envio_oferta(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.profesional = instancia2
                instance.proyecto = instancia1
                instance.save()
                msg=True
                return render(request,'profesional/asesoria.html',{'msg':msg}) 
                
        return render(request,'profesional/enviar_oferta_asesoria.html',{'form':form})  
    def config_cliente(request):
        usuario=User.objects.get(id=request.user.id)
        instancia =Cliente.objects.get(user=request.user.id)
        instancia2 =User.objects.get(id=request.user.id)
        form = RegistroCliente(instance=instancia)
        form2 = UserChangeForm(instance=instancia2)
        if request.method == "POST":
            form =RegistroCliente(request.POST, instance=instancia)
            form2 =UserChangeForm(request.POST, instance=instancia2)
            if form.is_valid():
                if form2.is_valid():
                    instancia = form.save(commit=False)
                    instancia2 = form2.save(commit=False)
                    instancia.save()
                    instancia2.save()
                    msg=False
                    return render(request,'cliente/index_cliente.html',{'msg':msg})   
        return render(request,'cliente/confi_cliente.html',{'form':form,'form2':form2,'usuario':usuario})  
    def config_profesional(request):
        usuario=User.objects.get(id=request.user.id)
        instancia =Profesional.objects.get(user=request.user.id)
        S=instancia.servicio_a_brindar
        instancia2 =User.objects.get(id=request.user.id)
        form2 = UserChangeForm(instance=instancia2)
        form = RegistroProfesional(instance=instancia)
        if request.method == "POST":
            form =RegistroProfesional(request.POST, instance=instancia)
            form2 =UserChangeForm(request.POST, instance=instancia2)
            if form.is_valid():
                instancia = form.save(commit=False)
                instancia2 = form2.save(commit=False)
                instancia.save()
                instancia2.save()
                msg=False
                return render(request,'profesional/index_profesional.html',{'msg':msg})   
        return render(request,'profesional/config_profesional.html',{'form':form,'form2':form2,'s':S,'usuario':usuario}) 
    
    def realizar_pago(request, proyecto_id,profesional_id,oferta_id):
        profesional=Profesional.objects.get(id_profesional=profesional_id)
        oferta=Oferta.objects.get(id_oferta=oferta_id)
        cliente =Cliente.objects.get(user=request.user.id)
        proyecto= Proyecto.objects.get(id_proyecto=proyecto_id)
        form = Pagos()
        if request.method == "POST":
            form = Pagos(request.POST or None, request.FILES or None)
            
            if form.is_valid():
                precio = form.cleaned_data.get('precio')
                if precio >= int(oferta.precio_final):
                    instance = form.save(commit=False)
                    instance.proyecto = oferta.proyecto
                    instance.destinatario=profesional.numero_cuenta
                    instance.save()
                    context={'mail':profesional.correo_electronico,'cliente':cliente,'proyecto':proyecto,'profesional':profesional}
                    template = get_template('cliente/correo_pago.html')
                    content= template.render(context)
                    email= EmailMultiAlternatives('INICIATIVA','Iniciativa',settings.EMAIL_HOST_USER,[profesional.correo_electronico])
                    email.attach_alternative(content,'text/html')
                    email.send()
                    oferta.delete()
                    return redirect('/factura_pago')
            
                    # raise fields.errors('La cantidad a pagar no es valida.')
                    
        return render(request,'cliente/realizar_pago.html',{'form':form})
       
    def eliminar_pago(request, pago_id):
        instancia = Pago.objects.get(pk=pago_id)
        proyecto=Proyecto.objects.get(pk=instancia.proyecto.id_proyecto)
        proyecto.delete()
        instancia.delete()
        return redirect('/factura_pago')
    
class listar_pagos(ListView):
    model=Pago
    form_class = Pagos()
    template_name = 'cliente/factura_pagos.html'
    
   
    def get_context_data(self,**kwargs):
        pago=Pago.objects.all()
        profesional=Profesional.objects.filter()
        cliente=Cliente.objects.get(user=self.request.user.id)
        proyecto=Proyecto.objects.filter(cliente=cliente.id_cliente)
        context=super().get_context_data(**kwargs)
        context['title']='Publicar Proyecto'
        context['object_list'] = Pago.objects.all()
        context['form']=DescripcionProyecto()
        context['proyecto']=proyecto
        context['profesional']=profesional
        context['cliente']=cliente
  
        


        return context


class CambiarPasswordView(FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'inicio/cambiar_contraseña.html'

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/logout')
            
        return render(request,'inicio/cambiar_contraseña.html',{'form':form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario=User.objects.get(id=self.request.user.id)
        context['form'] = PasswordChangeForm(user=self.request.user)
        context['usuario'] = usuario
        return context
