# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class Cliente(models.Model):
    def validation(value):
        if value == 'seleccione':
            raise ValidationError('Debe elegir una opcion del selector')
            
    nro_doc_cliente= models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    sexo = models.CharField(max_length=20,validators=[validation])
    telefono = models.CharField(max_length=20)
    ocupacion = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    user= models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="user")
    id_cliente = models.AutoField(primary_key=True)
    correo_electronico =models.CharField(max_length=150)
    
    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Cliente(user=user)
            user_profile.save()
        post_save.connect(create_profile, sender=User)

    class Meta:
        managed = False
        db_table = 'cliente'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'





class Proyecto(models.Model):
    
    def validation(value):
        if value == '$':
            raise ValidationError('Debe diligenciar un presupuesto')
        elif value =='Seleccione':
            raise ValidationError('Debe elegir una opcion del selector')
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=150)
    tipo_proyecto = models.CharField(max_length=40,validators=[validation])
    descripcion = models.CharField(max_length=400)
    persona_solicitada= models.CharField(max_length=50,validators=[validation])
    cliente = models.ForeignKey(Cliente, on_delete =models.CASCADE)
    precio_propuesto= models.CharField(max_length=50,validators=[validation])
    tipo_servicio = models.CharField(max_length=50,validators=[validation])
    
    
    def create_profile(sender, **kwargs):
        id_cliente = kwargs["instance"]
        if kwargs["created"]:
            Id_cliente =Proyecto(user=user)
            Id_cliente.save()
        post_save.connect(create_profile, sender=Cliente)

    class Meta:
        managed = False
        db_table = 'proyecto'



class Profesional(models.Model):
    def validation(value):
        if value == 'seleccione':
            raise ValidationError('Debe elegir una opcion del selector')
    id_profesional = models.AutoField(primary_key=True)
    nro_doc_profesional = models.CharField(max_length=20)
    nombre_profesional = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    tiempo_experiencia = models.IntegerField()
    sexo = models.CharField(max_length=20,validators=[validation])
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=40)
    titulo_profesional = models.CharField(max_length=60)
    fecha_nacimiento = models.DateField()
    user= models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="user")
    servicio_a_brindar=models.CharField(max_length=150)
    correo_electronico =models.CharField(max_length=150)
    numero_cuenta =models.CharField(max_length=50,unique=True)
    
       
    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Profesional(user=user)
            user_profile.save()
        post_save.connect(create_profile, sender=User)

    class Meta:
        managed = False
        db_table = 'profesional'

class Oferta(models.Model):
    id_oferta =  models.AutoField(primary_key=True)
    profesional = models.ForeignKey(Profesional, on_delete =models.CASCADE)
    fecha_entrega = models.DateField()
    precio_final =models.CharField(max_length=50)
    argumento = models.CharField(max_length=400)
    proyecto= models.ForeignKey(Proyecto, on_delete =models.CASCADE)
    estado=models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'oferta'

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    proyecto=models.ForeignKey(Proyecto, on_delete =models.CASCADE)
    precio=models.CharField(max_length=50)
    fecha= models.DateTimeField()
    destinatario=models.CharField(max_length=150)
    
    
    class Meta:
        managed = False
        db_table = 'pago'
    

