from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Comentario, Estado, Prioridad
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.

def registro_view(request):
    if request.method == 'GET':
        return render(request, 'formularioRegistro.html')

    else:
        # recibir los datos
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username= request.POST['username']
        email = request.POST['user_email']
        password = request.POST['user_password1']

        # Validar campos obligatorios
        if not first_name or not last_name or not username or not email or not password:
            messages.error(request, 'Debe completar todos los campos obligatorios.')
            return redirect('registro') 
        
        """
            TODO:
            enviar un correo electrónico de confirmación después de que los usuarios se registren y 
            pedirles verificar que tengan acceso a la dirección de correo electrónico y son capacez de hacer 
            click a un enlace en el correo electrónico.
        """
        # validar correo
        # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Ingrese un correo electrónico válido.')
            return redirect('registro')

        # validar que la contraseña
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('registro')
        if not any(char.isdigit() for char in password):
            messages.error(request,'La contraseña debe contener al menos un número.')
            return redirect('registro')
        if not any(char.isupper() for char in password):
            messages.error(request,'La contraseña debe contener al menos una letra mayúscula.')
            return redirect('registro')
        if not any(char.islower() for char in password):
            messages.error(request,'La contraseña debe contener al menos una letra minúscula.')
            return redirect('registro')
        if not any(char in ['$', '#', '@'] for char in password):
            messages.error(request,'La contraseña debe contener al menos uno de los siguientes caracteres especiales: $ # @.')
            return redirect('registro')

        if request.POST['user_password1'] == request.POST['user_password2']:
            # register user
            try:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                user.save()
                login(request, user)
                return redirect('principal_miticket')
            except IntegrityError:
                messages.error(request, 'Este usuario ya existe.')
                return redirect('registro')
        else:
            messages.error(request, 'las contraseñas no coinciden.')
            return redirect('registro') 

@login_required
def principal_miticket_view(request):
    return render(request, 'principal_miticket.html')

@login_required
def generar_reportes_view(request):
    # Incluir la información de Estado y Prioridad de cada ticket, 
    # usando la función prefetch_related para hacer una consulta en lotes de las relaciones:
    if request.method == 'POST':
        # Obtenga el rango de fechas seleccionado por el usuario en el Date Range Picker
        fecha_inicio, fecha_fin = request.POST.get('dates').split(' - ')
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y')
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y')
        # Filtre los tickets que se encuentran dentro del rango de fechas seleccionado
        tickets = Ticket.objects.filter(
            Q(fecha_creacion__date__gte=fecha_inicio) &
            Q(fecha_creacion__date__lte=fecha_fin)
        ).prefetch_related('estados', 'prioridades').all()
    else:
        tickets = Ticket.objects.prefetch_related('estados', 'prioridades').all()

    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'generar_reportes.html', {
            'tickets': tickets,
        })
    return redirect('principal_miticket')

@login_required
def consultar_usuarios_view(request):
    if request.user.is_superuser or request.user.is_staff:
        todos_los_usuarios = User.objects.all()
        numero_maximo_usuarios = User.objects.count()
        return render(request, 'consultar_usuarios.html', {
            'todos_los_usuarios': todos_los_usuarios,
            'numero_maximo_usuarios': numero_maximo_usuarios
        })
    return redirect('principal_miticket')

@login_required
def crear_usuario_view(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':

            # Obtener los datos del formulario
            username = request.POST['username']
            nombre = request.POST['first_name']
            apellido = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Verificar que los campos obligatorios estén completos
            if not username or not nombre or not apellido or not email or not password1 or not password2:
                messages.error(request, 'Por favor, complete todos los campos obligatorios.')
                return redirect('crear_usuario')
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return redirect('crear_usuario')

            if request.user.check_password(request.POST['passwordModal']):
                if request.POST['password1'] == request.POST['password2']:
                    try:

                        rol_de_usuario = request.POST.get('flexRadioRol')

                        # Crear el nuevo usuario
                        user_args = {
                            'username': username,
                            'first_name': nombre,
                            'last_name': apellido,
                            'email': email,
                            'password': password1,
                        }

                        if rol_de_usuario == 'Staff':
                            user_args['is_staff'] = True
                        elif rol_de_usuario == 'SuperUser':
                            user_args['is_superuser'] = True

                        # Se pasa el diccionario al método create_user() utilizando la sintaxis de desempaquetado **
                        user = User.objects.create_user(**user_args)
                        user.save()
                        
                        messages.success(request, f'Usuario ``{user.id} - {user.username}`` creado exitosamente')
                        return redirect('consultar_usuarios')
                    except IntegrityError:
                        messages.error(request, 'Error al crear el usuario.')
                        return redirect('consultar_usuarios')
            else:
                messages.error(request, 'Contraseña incorrecta.')
                # return redirect('crear_usuario')

        # Mostrar el formulario para crear un nuevo usuario
        return render(request, 'crear_usuario.html')
    return redirect('consultar_usuarios')

@login_required
def editar_usuario_view(request, id):
    if request.user.is_superuser or request.user.is_staff:
        usuario = get_object_or_404(User, id=id)

        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre_usuario = request.POST['username']
            nombre = request.POST['first_name']
            apellido = request.POST['last_name']
            email = request.POST['email']
            rol_de_usuario = request.POST.get('flexRadioRol')

            # Validar campos obligatorios estan llenos
            if not nombre_usuario or not nombre or not apellido or not email:
                messages.error(request, 'Debe completar todos los campos obligatorios.')
                return redirect('editar_usuario', id=id)
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return redirect('editar_usuario', id=id)

            if request.user.check_password(request.POST['passwordModal']):
                try:
                    # actualizar los datos
                    staff = False
                    superuser = False

                    if rol_de_usuario == 'Staff':
                        staff = True
                    elif rol_de_usuario == 'SuperUser':
                        staff = True
                        superuser = True

                    usuario.username = nombre_usuario
                    usuario.first_name = nombre
                    usuario.last_name = apellido
                    usuario.email = email
                    usuario.is_staff = staff
                    usuario.is_superuser = superuser
                    usuario.save()

                    messages.success(request, f'¡Usuario ``{usuario.id} - {usuario.username}`` actualizado exitosamente!')
                    return redirect('consultar_usuarios')
                except IntegrityError:
                    messages.error(request, 'Error al actualizr el usuario.')
                    return redirect('consultar_usuarios')
            else:
                messages.error(request, 'Contraseña incorrecta.')
                return redirect('editar_usuario', id)

        return render(request, 'editar_usuario.html', {
            'usuario': usuario
        })
    else:
        raise Http404('No tiene permisos para acceder a esta pagina')

@login_required
def perfil_de_usuario_view(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'GET':
        # Verificar si el usuario esta entrando a su propio perfil
        if request.user.id == usuario.id:
            return render(request, 'perfil_de_usuario.html', {
                'usuario': usuario
            })
        else:
            raise Http404('No tiene permisos para acceder a este perfil')
    else:
        if 'editar_perfil' in request.POST:
            # procesar el formulario de editar perfil
            # recibir los datos
            username = request.POST['username']
            nombre = request.POST['first_name']
            apellido = request.POST['last_name']
            email = request.POST['email']

            # Validar campos obligatorios
            if not username or not nombre or not apellido or not email:
                messages.error(request, 'Debe completar todos los campos obligatorios.')
                return redirect('perfil_de_usuario', id=id)
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return redirect('perfil_de_usuario', id=id)

            # actualizar los datos
            usuario.username = username
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = email
            usuario.save()
            messages.success(request, f'¡Datos editados exitosamente!')
            return redirect('perfil_de_usuario', id=id)

        elif 'cambiar_contraseña' in request.POST:
            # procesar el formulario de cambiar contraseña
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            password3 = request.POST['password3']

            # Validar campos obligatorios
            if not password1 or not password2 or not password3:
                messages.error(request, 'Debe completar todos los campos obligatorios.')
                return redirect('perfil_de_usuario', id=id)
            
            # validar que la contraseña actual sea correcta
            if request.user.check_password(password1):
                # validar contraseñas nuevas
                if password2 != password3:
                    messages.error(request, 'Las contraseñas nuevas no coinciden.')
                    return redirect('perfil_de_usuario', id=id)
                
                # actualizar contraseña del usuario
                usuario.set_password(password2)
                usuario.save()
                # volver a autenticar al usuario con la nueva contraseña
                user = authenticate(username=usuario.username, password=password2)
                if user is not None:
                    login(request, user)
                messages.success(request, f'¡Contraseña cambiada exitosamente!')
                return redirect('perfil_de_usuario', id=id)
            else:
                messages.error(request, f'La contraseña es incorrecta.')
                return redirect('perfil_de_usuario', id=id)
        else:
            messages.error(request, f'No se pudiron editar los datos o cambiar la contraseña.')
            return redirect('perfil_de_usuario', id=id)

@login_required
def eliminar_usuario(request, id):
    # Aquí se procesa la solicitud para eliminar el usuario
    usuario = get_object_or_404(User, id=id)
    # usuario.delete()
    messages.success(request, f'¡Usuario ``{usuario.id} - {usuario.username}`` eliminado exitosamente!')
    return redirect('consultar_usuarios')

@login_required # Eliminar
def cuenta_usuario(request):
    return render(request, 'cuenta_usuario.html')

@login_required # Eliminar
def estado_de_ticket(request):
    return render(request, 'estado_de_ticket.html')

@login_required
def crear_ticket_view(request):
    departamentos = Ticket.DEPARTAMENTO_CHOICES

    if request.method == 'POST':

        # Verificar que los campos obligatorios estén completos
        # Con y sin comprensión de listas.
        # if not all(field in request.POST and request.POST[field] for field in ['txtAsunto', 'formControlDepartamento', 'formControlDescripcion']):
        if not request.POST.get('txtAsunto') or not request.POST.get('formControlDepartamento') or not request.POST.get('formControlDescripcion'):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return redirect('crear_ticket')

        try:
            asunto = request.POST['txtAsunto']
            departamento = request.POST['formControlDepartamento']
            descripcion = request.POST['formControlDescripcion']
            # Usuario logeado
            usuario = request.user

            ticket = Ticket.objects.create(
                asunto=asunto,
                departamento=departamento,
                descripcion=descripcion,
                usuario=usuario
            )
            ticket.save()

            estados = Estado.ESTADO_CHOICES
            estado = Estado.objects.create(
                FK_id_ticket=ticket,
                usuario_creacion=usuario,
                usuario_modificacion=usuario,
                estado=estados[0][0]
            )
            estado.save()

            prioridades = Prioridad.PRIORIDAD_CHOICES
            prioridad = Prioridad.objects.create(
                FK_id_ticket=ticket,
                usuario_creacion=usuario,
                usuario_modificacion=usuario,
                prioridad=prioridades[0][0]
            )
            prioridad.save()

            messages.success(request, '¡Ticket creado exitosamente!')
            return redirect('consultar_ticket')
        except IntegrityError:
            messages.error(request, 'Error al crear el ticket.')
            return redirect('crear_ticket')

    return render(request, 'crear_ticket.html', {
        'departamentos': departamentos
    })

@login_required
def consultar_ticket_view(request):
    try:
        todos_los_tickets = Ticket.objects.all()
        tickets_usuario_especifico = Ticket.objects.filter(usuario_id = request.user)
    except Ticket.DoesNotExist:
        raise Http404("El ticket no existe.")

    return render(request, 'consultar_ticket.html', {
        'todos_los_tickets': todos_los_tickets,
        'tickets_usuario_especifico': tickets_usuario_especifico,
    })

# En este código, primero se realiza la validación de campos obligatorios y se verifica que departamento sea un valor válido. 
# Si se encuentran errores, se envía un mensaje de error y se redirige de vuelta a la página de edición con el mismo id. 
# Si todo está bien, se actualizan los datos del ticket y se envía un mensaje de éxito.
@login_required
def editar_ticket_view(request, id):
    # definir la variable fuera del condicional para que este definida y accesible en ambos bloques de código.
    departamentos = Ticket.DEPARTAMENTO_CHOICES

    # listar los datos por id
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'GET':
        # Verificar si el usuario es el creador del ticket o si es un administrador
        if request.user == ticket.usuario:
            return render(request, 'editar_ticket.html', {
                'ticket': ticket,
                'departamentos': departamentos
            })
        else:
            # Si el usuario no es el creador del ticket ni es un administrador, 
            # redirigir a una página de error o a una página que informe que no tiene permisos para acceder a ese ticket
            raise Http404('No tiene permisos para acceder a este ticket')
    else:
        # recibir los datos
        asunto = request.POST['txtAsunto']
        departamento = request.POST.get('formControlDepartamento')
        descripcion = request.POST['formControlDescripcion']

        # Validar campos obligatorios
        if not asunto or not descripcion:
            messages.error(request, 'Debe completar todos los campos obligatorios.')
            return redirect('editar_ticket', id=id)

        # actualizar los datos
        ticket.asunto = asunto
        ticket.departamento = departamento
        ticket.descripcion = descripcion
        ticket.save()
        messages.success(request, '¡Ticket editado exitosamente!')
        return redirect('consultar_ticket')

@login_required
def eliminar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # ticket.delete()
    messages.success(request, f'¡Ticket #{ticket.id} eliminado exitosamente!')
    return redirect('consultar_ticket')

@login_required
def estado_prioridad_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    estado = Estado.objects.get(FK_id_ticket=ticket)
    prioridad = Prioridad.objects.get(FK_id_ticket=ticket)

    if request.method == 'POST':
        try:
            usuario = request.user

            estado_update = request.POST['estado']
            estado.estado = estado_update
            estado.usuario_modificacion = usuario
            estado.save()

            prioridad_update = request.POST['prioridad']
            prioridad.prioridad = prioridad_update
            prioridad.usuario_modificacion = usuario
            prioridad.save()

            messages.success(request, '¡Estado y prioridad cambiados satisfactoriamente!')  
            return redirect('comentar_ticket', id=id)
        except:
            messages.error(request, 'Error al cambiar el estado y la prioridad.')  
            return redirect('comentar_ticket', id=id)
    return redirect('comentar_ticket', id=id)

@login_required
def comentar_ticket_view(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    comentarios = Comentario.objects.filter(FK_id_ticket=ticket)
    estados = Estado.ESTADO_CHOICES
    prioridades = Prioridad.PRIORIDAD_CHOICES

    # Obtener el estado y prioridad actual para mostrarlo en el HTML
    try:
        estado_actual = Estado.objects.filter(FK_id_ticket=ticket).order_by('-fecha_modificacion').first()
        prioridad_actual = Prioridad.objects.filter(FK_id_ticket=ticket).order_by('-fecha_modificacion').first()

        # Para cambiar estado a 'En progreso' cuando se comenta
        estado_actual_update = Estado.objects.get(FK_id_ticket=ticket)

    except Estado.DoesNotExist or Prioridad.DoesNotExist:
        estado_actual = None
        prioridad_actual = None

    # Verificar si el usuario es el creador del ticket o si es un administrador
    if request.user == ticket.usuario or request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            # Verificar que los campos obligatorios estén completos
            if not request.POST.get('textAreacomentario'):
                messages.error(request, 'Por favor, complete todos los campos obligatorios.')  
                return redirect('comentar_ticket', id=id)
            try:
                comentario_texto = request.POST['textAreacomentario']
                usuario = request.user
                comentario = Comentario.objects.create(
                    comentario=comentario_texto,
                    usuario=usuario,
                    FK_id_ticket=ticket 
                )
                comentario.save()
                ticket.asignado_a = usuario
                ticket.save()
                # Pasar estado del ticket a 'En progreso' al añadir un comentario
                if estado_actual_update.estado == 'Abierto':
                    estado_actual = estados[1][0]
                    estado_actual_update.estado = estado_actual
                    estado_actual_update.save()

                messages.success(request, '¡Comentario agregado correctamente!')

                # messages.success(request, f'¡El estado del ticket a pasado a {estado_actual}!')
                return redirect('comentar_ticket', id=id)
            except IntegrityError:
                messages.error(request, 'Error al comentar el ticket.')
                # messages.error(request, 'Error al cambiar el estado y la prioridad.') 
                return redirect('comentar_ticket', id=id)

        return render(request, 'comentar_ticket.html', {
            'ticket': ticket,
            'comentarios': comentarios,
            'estados': estados,
            'estado_actual': estado_actual,
            'prioridades': prioridades,
            'prioridad_actual': prioridad_actual
        })
    else:
        # Si el usuario no es el creador del ticket ni es un administrador, 
        # redirigir a una página de error o a una página que informe que no tiene permisos para acceder a ese ticket
        raise Http404('No tiene permisos para acceder a este ticket')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')

def cambio_clave(request):
    return render(request, 'cambio_clave.html')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'loginticket.html')
    else:
        user = authenticate(request, 
            username=request.POST['user_nombre'],
            password=request.POST['user_clave1']
        )
        # Comprobando si el usuario es normal o admin
        if user is None:
            messages.error(request, 'El usuario o la contraseña son incorrectos.')
            return redirect('iniciar_sesion') 
        else:
            login(request, user)
            if request.user.is_superuser or request.user.is_staff:
                return redirect('principal_miticket')
            else:
                return redirect('principal_miticket') 