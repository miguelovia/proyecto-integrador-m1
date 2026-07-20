# Acceso remoto y VPN

## Configuración inicial

1. Descargar el cliente VPN corporativo desde el portal de IT (`Software Center` -> "Corporate VPN").
2. Iniciar sesión con tu correo corporativo y contraseña; se solicitará un código MFA.
3. Seleccionar el servidor más cercano a tu ubicación para minimizar latencia.

## Problemas comunes

- **"No puedo conectarme a la VPN" / error de autenticación**: normalmente es un problema de
  contraseña expirada o de MFA desincronizado. Sigue el proceso de restablecimiento de contraseña
  antes de abrir un ticket.
- **La VPN se conecta pero no tengo acceso a recursos internos**: verifica que estés conectado al
  servidor correcto para tu región; si persiste, abre un ticket categoría "Network Access".
- **Desconexiones frecuentes**: reportar como ticket categoría "VPN Stability" incluyendo hora,
  ubicación y proveedor de internet.

## SLA de soporte

Los tickets de acceso VPN marcados como urgentes se atienden dentro de 2 horas hábiles. Los no
urgentes, dentro de 1 día hábil.

## Perfiles de acceso por rol

- El acceso VPN estándar da visibilidad a recursos internos generales (intranet, herramientas de
  gestión de proyectos, impresoras de red). Acceso a entornos de producción o a bases de datos de
  clientes requiere un perfil VPN adicional, solicitado por el manager directo con categoría
  "Elevated Network Access".
- Los perfiles de acceso elevado se revisan cada 6 meses; si el rol del empleado ya no requiere ese
  nivel de acceso, IT lo revoca automáticamente y notifica al manager directo.
- Contratistas externos reciben un perfil VPN restringido con acceso únicamente a los sistemas
  explícitamente autorizados en su contrato, y su acceso expira automáticamente en la fecha de fin de
  contrato registrada en el sistema.

## Uso de VPN en redes no confiables

- Al conectarse desde redes wifi públicas o no confiables (aeropuertos, cafeterías, hoteles), la VPN
  debe activarse antes de acceder a cualquier sistema interno, no solo para recursos que parezcan
  sensibles.
- El cliente VPN corporativo incluye un "kill switch" que bloquea automáticamente el tráfico de
  internet si la conexión VPN se cae inesperadamente; no debe desactivarse manualmente salvo
  instrucción explícita de IT para depurar un problema de conectividad.

## Split tunneling

- Por defecto, la configuración de VPN de la empresa usa split tunneling: solo el tráfico dirigido a
  sistemas internos pasa por el túnel VPN, mientras que la navegación general de internet usa la
  conexión local directamente.
- Roles que manejan información especialmente sensible (por ejemplo, el equipo de seguridad de la
  información) pueden requerir un perfil de túnel completo (full tunneling), asignado individualmente
  por IT según el rol.

## Compatibilidad y dispositivos

El cliente VPN corporativo es compatible con macOS, Windows y las principales distribuciones de
Linux soportadas por IT. Dispositivos móviles personales no pueden conectarse a la VPN corporativa;
el acceso a correo y calendario desde móvil se gestiona a través de la app de gestión de dispositivos
móviles (MDM) en lugar de la VPN.

## Acceso VPN para contratistas y proveedores externos

- Un proveedor externo que necesite acceso temporal a sistemas internos (por ejemplo, un consultor de
  seguridad) recibe un perfil VPN de contratista, solicitado por el sponsor interno del proyecto con
  categoría "Contractor Network Access" y una fecha de expiración obligatoria no mayor a 90 días.
- Extensiones más allá de 90 días requieren una nueva solicitud con justificación actualizada; el
  sistema no permite renovaciones automáticas de accesos de contratistas por diseño.
- Todo acceso VPN de contratista queda registrado en un log separado que Legal y Seguridad de la
  Información revisan trimestralmente como parte de la auditoría de terceros con acceso a sistemas.

## Monitoreo y registro de conexiones

- El servicio de VPN registra hora de conexión, duración de la sesión y el sistema al que se accedió,
  con fines de seguridad y auditoría; estos registros no se usan para medir productividad o tiempo
  trabajado del empleado.
- Actividad inusual (por ejemplo, conexión simultánea desde dos países distintos) genera una alerta
  automática al equipo de Seguridad de la Información, que puede contactar directamente al empleado
  para confirmar que la conexión es legítima antes de bloquear la cuenta preventivamente.

## Rendimiento y elección de servidor

Si notas latencia alta o velocidad reducida al usar la VPN, prueba primero conectarte al servidor de
la región más cercana desde el selector del cliente; si el problema persiste con el servidor correcto
seleccionado, repórtalo como ticket categoría "VPN Stability" incluyendo un resultado de prueba de
velocidad con y sin la VPN activa, para que IT pueda descartar un problema del lado del proveedor de
internet del empleado.

## Acceso condicional por dispositivo

- La VPN corporativa verifica que el dispositivo que intenta conectarse esté enrolado en la
  plataforma de gestión de dispositivos (MDM) y cumpla con las políticas mínimas de seguridad (cifrado
  de disco activo, sistema operativo actualizado) antes de permitir la conexión.
- Un dispositivo que no cumpla con estas condiciones recibe un mensaje indicando qué requisito falta
  y un enlace para remediarlo; IT no otorga excepciones manuales a este control salvo un caso de
  emergencia documentado y aprobado por Seguridad de la Información.

## VPN de sitio a sitio para oficinas

Las oficinas físicas de la empresa se conectan a los sistemas internos a través de un túnel VPN de
sitio a sitio administrado directamente por IT, independiente del cliente VPN individual que usan los
empleados; los empleados conectados a la red de oficina no necesitan activar manualmente su cliente
VPN personal para acceder a recursos internos, salvo que estén accediendo a un sistema con controles
de acceso adicionales que lo requieran explícitamente.

## Desconexión automática por inactividad

Las sesiones VPN se desconectan automáticamente después de 12 horas continuas de conexión o después
de 2 horas de inactividad de red, lo que ocurra primero, como medida de seguridad. Esto es
independiente del bloqueo de pantalla local del equipo, que ocurre a los 5 minutos de inactividad
según la política de contraseñas y acceso.

## Acceso VPN desde múltiples dispositivos

- Un mismo empleado puede tener el cliente VPN instalado en más de un dispositivo asignado por la
  empresa (por ejemplo, laptop principal y una laptop de respaldo), pero solo se permite una sesión
  VPN activa simultánea por usuario; iniciar sesión en un segundo dispositivo cierra automáticamente
  la sesión activa en el primero.
- Si necesitas trabajar simultáneamente desde dos dispositivos por una razón operativa específica,
  contacta a IT para evaluar un perfil de excepción, en lugar de intentar sortear la restricción
  reutilizando credenciales de otra forma.

## Actualizaciones del cliente VPN

- El cliente VPN corporativo se actualiza automáticamente a través del sistema de gestión de
  dispositivos; no se debe descargar el cliente VPN desde ninguna fuente distinta al portal interno de
  IT, ni siquiera desde el sitio oficial del proveedor, para garantizar que la configuración
  correcta específica de la empresa se aplique correctamente.
- Si el cliente VPN muestra una notificación de actualización pendiente, se recomienda aplicarla
  dentro de las 48 horas siguientes; versiones desactualizadas del cliente pueden perder
  compatibilidad con los servidores y generar fallas de conexión.

## Documentación de arquitectura de red interna

Para roles de Ingeniería que necesiten entender la topología de red interna (rangos de IP,
segmentación de entornos), IT mantiene documentación técnica detallada en el wiki interno de
Infraestructura, accesible únicamente a través de VPN con perfil de acceso elevado, dado que describe
la arquitectura de seguridad de la red corporativa.

## Solicitud de excepciones a la política de VPN

Cualquier excepción a esta política (por ejemplo, un caso de negocio que requiera desactivar
temporalmente el kill switch, o permitir un dispositivo no enrolado en el MDM) requiere aprobación
conjunta de IT y de Seguridad de la Información, documentada con fecha de expiración de la excepción;
no existen excepciones permanentes a los controles de seguridad de la VPN.
