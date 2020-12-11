from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm,AuthenticationForm
from django import forms
from betterforms.multiform import MultiModelForm
from django.forms import ModelForm
from django.forms import Select

class RegistroUsuario(UserCreationForm):
    username =forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}))
    password1=forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2=forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Contraseña'}))
    first_name=forms.CharField(label='Rol de usuario',widget=forms.TextInput(attrs={'value':'Cliente','readonly':'true','class':'form-control',}))
 

    class Meta:
         
        model= User
        fields = ['id','username','password1','password2','first_name']
        help_texts = {k:"" for k in fields }
        # widgets={'groups':forms.TextInput(attrs={'value':'Cliente','readonly':True})}

class RegistroUsuarioPro(UserCreationForm):
    username =forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}))
    password1=forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2=forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Contraseña'}))
    first_name=forms.CharField(label='Rol de usuario',widget=forms.TextInput(attrs={'value':'Profesional','readonly':'true','class':'form-control',}))
 

    class Meta:
         
        model= User
        fields = ['id','username','password1','password2','first_name']
        help_texts = {k:"" for k in fields }
        # widgets={'groups':forms.TextInput(attrs={'value':'Cliente','readonly':True})}
        

class UserChangeForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control form-control-sm'}))

    class Meta:
        model = User
        fields = ['username']
      
        
        

  
        
        # widgets={'fecha_nacimiento':forms.DateInput(attrs={'type':'date'})}
