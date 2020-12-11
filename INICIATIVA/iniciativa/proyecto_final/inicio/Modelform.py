from django import forms
from betterforms.multiform import MultiModelForm
from django.forms import ModelForm
from .models import Cliente,Proyecto,Profesional,Oferta,Pago
from .forms import RegistroUsuario,RegistroUsuarioPro
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin import widgets  
from django.forms import DateTimeField
from datetime import datetime ,date
from django_select2.forms import Select2MultipleWidget




class RegistroCliente(ModelForm):
    nro_doc_cliente =forms.CharField(label='Numero de Documento',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Numero de Documento','autofocus':'True'}))
    nombre_cliente =forms.CharField(label='Nombre',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres'}))
    apellido_paterno =forms.CharField(label='Primer apellido',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Primer Apellido'}))
    apellido_materno =forms.CharField(label='Segundo Apellido',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo Apellido'}))
    telefono =forms.CharField(label='Telefono',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono'}))
    ocupacion =forms.CharField(label='Ocupacion',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ocupacion'}))
    sexo =forms.ChoiceField(choices=(('seleccione',("Sexo")),('Masculino', ("Masculino")),('Femenino', ("Femenino"))),label='sexo',widget=forms.Select(attrs={'class':'form-control'}))
    fecha_nacimiento=forms.CharField(
        widget=forms.TextInput(attrs={
         'class':"form-control",'id':'date','name':'date','placeholder':'Fecha de Nacimiento    YY/MM/DD'
        })
    )
    correo_electronico=forms.EmailField(label='Correo electronico',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo Electronico'}))
 
    
   
    
    class Meta:
        model = Cliente
        fields = ['nro_doc_cliente','nombre_cliente',
        'apellido_paterno','apellido_materno','sexo',
        'telefono' ,'ocupacion','fecha_nacimiento','correo_electronico']
        

class DescripcionProyecto(ModelForm):
    
    nombre_proyecto =forms.CharField(label='Nombre del proyecto',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Proyecto','autofocus':'autofocus'}))
    descripcion =forms.CharField(label='descripcion del proyecto',widget=forms.Textarea(attrs={"rows":5, "cols":50 ,'placeholder': 'Describenos brevemente tu proyecto','class':'form-control'}))
    CHOICES1=[('Seleccione','Servicio'),('Asesoria','Asesoria'),
         ('Desarrollo del proyecto','Desarrollo del proyecto')]       
    CHOICES2=[('Seleccione','Tipo de proyecto'),
         ('Desarrollo web','Desarrollo web'),
         ('Desarrollo movil','Desarrollo movil'),
         ('Diseño grafico','Diseño grafico')]
    CHOICES3=[('Seleccione','Tipo de Ayuda'),('Una persona','Necesito una persona'),
         ('Un Equipo','Necesito un equipo completo')]
    tipo_servicio=forms.ChoiceField(choices=CHOICES1,label='tipo de servicio',initial ='Seleccione',widget=forms.Select(attrs={'class':'custom-select'}))
    # tipo_proyecto =forms.MultipleChoiceField(label='Tipo de proyecto',choices=CHOICES2,widget=forms.CheckboxSelectMultiple(attrs={}))
    precio_propuesto=forms.IntegerField(label='Precio ',help_text='¿Cuanto dinero estas dispuesto ofrecer?',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'$ Establece tu presupuesto '}))
    persona_solicitada=forms.ChoiceField(choices=CHOICES3,label='TIPO DE AYUDA',widget=forms.Select(attrs={'class':'custom-select'}))
    tipo_proyecto =forms.ChoiceField(choices=CHOICES2,label='tipo de proyecto',initial ='Seleccione',widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto','tipo_servicio',
        'descripcion','precio_propuesto','persona_solicitada','tipo_proyecto']
        
class RegistroModelForm(MultiModelForm):
    form_classes = {
        'userCliente': RegistroUsuario,
        'cliente': RegistroCliente,
        'proyecto':DescripcionProyecto
    }

class Login(AuthenticationForm):
    rol=forms.ChoiceField(choices=(('Seleccione',("Seleccione")),('Cliente', ("Cliente")),('Profesional', ("Profesional"))),initial ='Seleccione',widget=forms.Select(attrs={'class':'custom-select'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario','id':'usuario'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña','id':'contraseña'}))

    class Meta:
        model = User
        fields = ["username", "password","rol"]

class RegistroProfesional(ModelForm):
    nro_doc_profesional = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Numero de Documento','autofocus':'True'}))
    nombre_profesional = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres'}))
    apellido_paterno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Primer Apellido'}))
    apellido_materno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo Apellido'}))
    tiempo_experiencia = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Años de Experiencia'}))
    sexo =forms.ChoiceField(choices=(('seleccione',("Sexo")),('Masculino', ("Masculino")),('Femenino', ("Femenino"))),label='sexo',widget=forms.Select(attrs={'class':'form-control'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Direccion'}))
    titulo_profesional = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo Profesional'}))
    fecha_nacimiento=forms.CharField(
        widget=forms.TextInput(attrs={
         'class':"form-control",'id':'date','name':'date','placeholder':'Fecha de Nacimiento    YY/MM/DD'
        })
    )
    numero_cuenta=forms.IntegerField(label='Precio ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Numero de cuenta '}))
    CHOICES2=[
        ('Desarrollo web','Desarrollo web'),
        ('Desarrollo movil','Desarrollo movil'),
        ('Diseño grafico','Diseño grafico')]
    servicio_a_brindar=forms.MultipleChoiceField(label='Servicio a Ofrecer',choices=CHOICES2,widget=forms.CheckboxSelectMultiple(attrs={}))
    correo_electronico=forms.EmailField(label='Correo electronico',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo Electronico'}))
   
    
    class Meta:
        model = Profesional
        fields = ['nro_doc_profesional','nombre_profesional',
        'apellido_paterno','apellido_materno','sexo',
        'telefono' ,'tiempo_experiencia','fecha_nacimiento','direccion', 'titulo_profesional','servicio_a_brindar','correo_electronico','numero_cuenta']
        
class RegistroModelFormPro(MultiModelForm):
    form_classes = {
        'userProfesional': RegistroUsuarioPro,
        'profesional': RegistroProfesional
    }
    
def grouped(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
        
        
class Envio_oferta(ModelForm):
    
    fecha_entrega=forms.CharField(
            widget=forms.TextInput(attrs={
            'class':"form-control",'id':'date','name':'date','placeholder':'Fecha de entrega    YY/MM/DD'
            }))
    precio_final=forms.IntegerField(label='Precio ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'$ Establece el precio final '}))
    argumento=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50 ,'placeholder': 'Define tu oferta..','class':'form-control'}))
    
    
    class Meta:
        model = Oferta
        fields = ["fecha_entrega", "precio_final","argumento"]
        
class Pagos(ModelForm):
    fecha_hora=datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    fecha=forms.DateTimeField(widget=forms.TextInput(attrs={'class':'form-control','value':str(fecha_hora) ,'readonly':'True'}))
    precio=forms.IntegerField(label='Precio ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Precio a pagar'}))
   
    class Meta:
        model = Pago
        fields = ["precio","fecha"]