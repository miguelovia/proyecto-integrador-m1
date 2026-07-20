# Política de contraseñas y acceso

## Requisitos de contraseña

- Mínimo 12 caracteres, con mayúsculas, minúsculas, números y un símbolo.
- Las contraseñas expiran cada 180 días para cuentas con acceso a sistemas de producción; cada 365
  días para el resto de las cuentas.
- No se permite reutilizar ninguna de las últimas 8 contraseñas.

## Restablecer contraseña

1. Ir al portal de autoservicio: `https://sso.empresa.com/reset`.
2. Verificar identidad con el segundo factor (MFA) configurado (app autenticadora o SMS de respaldo).
3. Si no tienes acceso al MFA configurado, abre un ticket en el portal de IT con la categoría
   "Account Access" y un miembro del equipo verificará tu identidad manualmente (puede tardar hasta
   4 horas hábiles).

## Autenticación multifactor (MFA)

MFA es obligatorio para todas las cuentas desde el primer día. Se recomienda usar una app autenticadora
(Authy, Google Authenticator) en lugar de SMS, que se mantiene solo como respaldo.

## Cambio o pérdida del segundo factor

- Si cambias de teléfono, registra el nuevo dispositivo en la app autenticadora antes de dar de baja el
  anterior; el portal de autoservicio permite tener hasta 2 dispositivos MFA activos simultáneamente
  durante la transición.
- Si pierdes o te roban el dispositivo con el segundo factor configurado, notifica a IT de inmediato
  (categoría "Account Access - Urgent") para que se revoque el MFA anterior y se emitan códigos de
  respaldo de un solo uso mientras configuras un nuevo dispositivo.
- Los códigos de respaldo de un solo uso se generan desde el portal de autoservicio y deben
  almacenarse en un lugar seguro (gestor de contraseñas corporativo), nunca en texto plano en el
  correo o en notas compartidas.

## Gestor de contraseñas corporativo

- La empresa provee una licencia de gestor de contraseñas corporativo a todos los empleados; su uso es
  obligatorio para almacenar credenciales de cuentas de trabajo que no estén integradas con el inicio
  de sesión único (SSO).
- Compartir credenciales de cuentas compartidas del equipo (por ejemplo, cuentas de redes sociales
  corporativas) debe hacerse únicamente a través de las carpetas compartidas del gestor de
  contraseñas, nunca por chat o correo.

## Cuentas de servicio y credenciales de aplicaciones

- Las cuentas de servicio (usadas por aplicaciones, no por personas) siguen una política de rotación
  de credenciales cada 90 días, gestionada por el equipo de IT/Seguridad, no por los equipos de
  producto individualmente.
- Cualquier credencial de servicio expuesta accidentalmente (por ejemplo, subida por error a un
  repositorio de código) debe reportarse de inmediato a IT como incidente de seguridad, incluso si el
  repositorio es privado, para rotar la credencial cuanto antes.

## Auditoría de accesos

IT realiza una auditoría trimestral de accesos activos por sistema, cotejando contra la lista de
empleados activos en RH. Cuentas de exempleados o de contratistas cuyo contrato ya terminó que
sigan apareciendo con acceso activo se desactivan de inmediato y se reporta el hallazgo a IT y a RH
para revisar por qué el proceso de offboarding no las revocó a tiempo.

## Inicio de sesión único (SSO)

- La mayoría de las herramientas internas se integran con el proveedor de identidad corporativo vía
  SSO, de forma que una sola contraseña y un solo MFA cubren el acceso a todas las aplicaciones
  integradas, en lugar de credenciales independientes por herramienta.
- Al solicitar acceso a una nueva herramienta SaaS para el equipo, IT evalúa primero si el proveedor
  soporta integración SSO antes de aprobar una cuenta con contraseña independiente; herramientas sin
  soporte SSO requieren una excepción documentada y quedan sujetas a la misma política de rotación de
  contraseñas de 180/365 días descrita arriba.
- Si el proveedor de identidad presenta una interrupción, IT activa un procedimiento de acceso de
  emergencia documentado internamente para sistemas críticos, comunicado únicamente a los equipos que
  lo necesiten durante el incidente.

## Preguntas frecuentes sobre contraseñas

- **¿Por qué mi contraseña expiró si la cambié hace poco?** El contador de expiración se reinicia
  cada vez que cambias la contraseña exitosamente; si expiró antes de lo esperado, verifica que el
  cambio se haya guardado correctamente y no haya quedado revertido por una sincronización pendiente.
- **¿Puedo usar la misma contraseña en varias cuentas de trabajo?** No; cada sistema que no esté
  integrado con SSO debe tener una contraseña única, generada y almacenada en el gestor de
  contraseñas corporativo.
- **¿Qué hago si sospecho que mi cuenta fue comprometida?** Cambia la contraseña de inmediato desde
  el portal de autoservicio y abre un ticket a IT categoría "Security Incident" sin esperar
  confirmación de que hubo acceso no autorizado; es preferible reportar de más que de menos.

## Cuentas privilegiadas y acceso administrativo

- Cuentas con privilegios administrativos (acceso root, administración de infraestructura en la nube,
  administración del proveedor de identidad) requieren MFA con una app autenticadora obligatoriamente;
  SMS no se acepta como segundo factor para este tipo de cuentas bajo ninguna circunstancia.
- El acceso administrativo se otorga de forma nominal, nunca a través de una cuenta compartida
  genérica; cada acción administrativa queda asociada a la persona que la realizó en los registros de
  auditoría del sistema correspondiente.
- Empleados con acceso administrativo pasan por una recertificación de acceso cada 90 días, en la que
  su manager directo confirma explícitamente que el acceso sigue siendo necesario para el rol.

## Bloqueo de cuenta por intentos fallidos

- Después de 5 intentos fallidos de inicio de sesión consecutivos, el sistema bloquea la cuenta
  temporalmente por 15 minutos como medida de protección contra ataques de fuerza bruta.
- Si el bloqueo persiste después de ese periodo o el empleado necesita acceso inmediato, puede abrir
  un ticket de IT categoría "Account Access" para un desbloqueo manual, previa verificación de
  identidad.
- Bloqueos repetidos en un corto periodo de tiempo (por ejemplo, 3 bloqueos en una semana) generan una
  alerta automática al equipo de Seguridad de la Información para descartar un intento de acceso no
  autorizado en curso.

## Requisitos de contraseña para sistemas de terceros

- Herramientas SaaS de terceros que no soportan SSO pero manejan información confidencial de clientes
  deben configurarse con los mismos requisitos mínimos de contraseña y MFA que los sistemas internos,
  verificado por IT antes de aprobar el uso de la herramienta para el equipo solicitante.
- Si una herramienta de terceros no soporta MFA en absoluto, IT documenta la excepción como riesgo
  aceptado y la reporta a Seguridad de la Información para su seguimiento, en lugar de bloquear
  automáticamente el uso de la herramienta si ya es crítica para la operación del equipo.

## Política de contraseñas para cuentas de invitados y temporales

- Cuentas de acceso temporal para visitantes, candidatos en proceso de entrevista técnica o auditores
  externos se crean con una expiración automática no mayor a 5 días hábiles, sin excepción, y con
  acceso limitado únicamente a los sistemas explícitamente necesarios para el propósito de la visita.
- Estas cuentas nunca heredan permisos de una cuenta de empleado existente; se crean desde cero con el
  conjunto mínimo de permisos requerido.

## Rotación forzada tras un incidente de seguridad

Si ocurre un incidente de seguridad que involucre o pueda haber involucrado credenciales de acceso
(por ejemplo, una fuga de datos de un proveedor externo usado por varios empleados), IT puede forzar
una rotación de contraseña inmediata para todos los usuarios afectados, sin esperar al ciclo normal de
expiración de 180 o 365 días. La notificación de este tipo de rotación forzada incluye siempre el
motivo general del incidente, salvo que la investigación en curso requiera confidencialidad temporal
sobre los detalles.

## Capacitación de seguridad relacionada con contraseñas y phishing

Todo empleado completa una capacitación de seguridad de la información al ingresar a la empresa (ver
documentación de RH sobre onboarding) y una capacitación de actualización anual, que incluye
simulacros periódicos de phishing. Empleados que interactúen con un simulacro de phishing de forma
insegura (por ejemplo, ingresando su contraseña en una página simulada) reciben una capacitación
adicional obligatoria, sin que esto se registre como una falta disciplinaria la primera vez que
ocurre.
