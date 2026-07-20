# Privacidad de datos y cumplimiento

## Principios generales

- Solo se recopilan datos personales de clientes que sean estrictamente necesarios para prestar el
  servicio contratado.
- Los datos de clientes en regiones con regulación de protección de datos (por ejemplo, esquemas
  tipo GDPR) deben almacenarse y procesarse conforme a los acuerdos de procesamiento de datos (DPA)
  firmados con cada cliente.

## Manejo de incidentes de datos

- Cualquier sospecha de acceso no autorizado, fuga o exposición de datos de clientes o empleados
  debe reportarse de inmediato a Legal a través del canal de incidentes ("Data Incident"), incluso
  si no se ha confirmado que ocurrió una fuga real.
- Legal, junto con Seguridad de la Información, determina si el incidente requiere notificación a
  clientes o autoridades regulatorias y en qué plazo, según la jurisdicción aplicable.
- Los problemas de acceso técnico (por ejemplo, cuentas bloqueadas, permisos mal configurados) se
  atienden primero como ticket de IT; solo se escalan a Legal cuando existe evidencia o sospecha de
  que datos protegidos fueron efectivamente expuestos o accedidos indebidamente.

## Solicitudes de titulares de datos

Las solicitudes de acceso, corrección o eliminación de datos personales por parte de un titular
(cliente o empleado) deben canalizarse a Legal, que coordina la respuesta dentro de los plazos
regulatorios aplicables.

## Subprocesadores y proveedores externos

- Cualquier proveedor externo que procese datos de clientes en nombre de la empresa (un
  subprocesador) requiere un acuerdo de procesamiento de datos (DPA) firmado antes de recibir acceso a
  esos datos, revisado y aprobado por Legal.
- La lista de subprocesadores activos se mantiene actualizada en el portal de Legal y debe reflejar
  la lista pública de subprocesadores que la empresa comparte con sus clientes según los contratos
  vigentes; agregar un nuevo subprocesador que procese datos de clientes existentes puede requerir
  notificación previa a esos clientes según el DPA firmado con ellos.
- Antes de contratar un nuevo subprocesador, el área solicitante debe completar un cuestionario de
  seguridad y privacidad coordinado entre Legal y Seguridad de la Información.

## Minimización y retención de datos

- Los datos personales de clientes se conservan únicamente durante el tiempo necesario para prestar
  el servicio y cumplir obligaciones legales o contractuales; los periodos de retención específicos
  por tipo de dato están documentados en el registro interno de tratamiento de datos que mantiene
  Legal.
- Al finalizar la relación con un cliente, los datos personales asociados se eliminan o anonimizan
  conforme al periodo de retención acordado en el contrato, salvo obligación legal de conservarlos por
  más tiempo (por ejemplo, registros fiscales).
- Solicitudes internas para conservar datos más allá del periodo estándar (por ejemplo, para análisis
  de producto) requieren justificación documentada y aprobación de Legal.

## Transferencias internacionales de datos

Cuando el procesamiento de datos de un cliente implica transferirlos a un país distinto al de origen
del cliente, Legal evalúa si existe un mecanismo de transferencia válido (por ejemplo, cláusulas
contractuales estándar) antes de autorizar la transferencia. Los equipos de Ingeniería no deben
habilitar replicación de datos de clientes hacia una nueva región sin confirmar primero con Legal que
el mecanismo de transferencia correspondiente está vigente.

## Capacitación en privacidad

Todos los empleados con acceso a datos de clientes completan una capacitación anual obligatoria de
privacidad y manejo de datos, coordinada por Legal en conjunto con RH. El incumplimiento de esta
capacitación puede resultar en la suspensión temporal de accesos a sistemas que contengan datos de
clientes hasta que se complete.

## Clasificación de datos

- La empresa clasifica la información en cuatro niveles: pública, interna, confidencial y
  restringida. Los datos personales de clientes y empleados se clasifican por default como
  confidenciales, y ciertas categorías especialmente sensibles (datos de salud, información
  financiera detallada) como restringidas.
- El nivel de clasificación determina los controles aplicables: la información restringida requiere
  cifrado tanto en tránsito como en reposo, acceso limitado a un grupo explícito de personas
  autorizadas, y registro de auditoría de cada acceso.
- Cualquier duda sobre cómo clasificar un nuevo tipo de dato que el equipo de producto planea
  recolectar debe consultarse con Legal antes de implementarlo, no después.

## Privacidad desde el diseño

- Todo proyecto nuevo que involucre recolectar, almacenar o procesar datos personales de clientes
  debe pasar por una evaluación de impacto de privacidad antes de su lanzamiento, coordinada entre
  Legal, Seguridad de la Información y el equipo de producto responsable.
- La evaluación de impacto revisa qué datos se recolectan, por qué son necesarios, cuánto tiempo se
  conservan y qué salvaguardas técnicas y organizativas se aplican; proyectos que no puedan
  justificar la necesidad de un dato personal específico deben ajustar su diseño para no recolectarlo.
- Cambios significativos a un producto existente que amplíen el tipo o volumen de datos personales
  recolectados requieren una nueva evaluación de impacto, no solo el lanzamiento inicial.

## Cookies y rastreo web

- El sitio web y la aplicación de la empresa usan un banner de consentimiento de cookies conforme a
  la regulación aplicable en cada región, gestionado por el equipo de marketing en coordinación con
  Legal.
- Cookies estrictamente necesarias para el funcionamiento del servicio no requieren consentimiento
  explícito; cookies de analítica y de marketing sí lo requieren, y el usuario puede retirar su
  consentimiento en cualquier momento desde la configuración de privacidad del sitio.
- Cualquier nueva herramienta de analítica o de marketing que involucre rastreo de usuarios debe
  revisarse con Legal antes de integrarse al sitio o la aplicación.

## Menores de edad

La empresa no dirige sus servicios a menores de edad y no recolecta intencionalmente datos
personales de menores. Si se detecta que se recolectaron datos de un menor sin el consentimiento
parental requerido por la jurisdicción aplicable, el equipo debe notificar a Legal de inmediato para
coordinar la eliminación de esos datos y evaluar si se requiere alguna notificación regulatoria.

## Solicitudes de autoridades regulatorias

- Cualquier requerimiento de información recibido de una autoridad regulatoria o de protección de
  datos (por ejemplo, una auditoría o una solicitud de información sobre el tratamiento de datos de un
  cliente específico) debe canalizarse de inmediato a Legal, sin que ningún otro equipo responda
  directamente a la autoridad sin la coordinación de Legal.
- Legal mantiene un registro de todas las comunicaciones con autoridades regulatorias relacionadas con
  privacidad de datos, incluyendo plazos de respuesta comprometidos y su cumplimiento.

## Privacidad en integraciones con inteligencia artificial

- Cualquier funcionalidad de producto que utilice modelos de inteligencia artificial procesando datos
  personales de clientes (por ejemplo, para generar recomendaciones o respuestas automatizadas) debe
  pasar por la misma evaluación de impacto de privacidad que cualquier otro proyecto nuevo, prestando
  atención específica a si el proveedor del modelo retiene o utiliza los datos enviados para entrenar
  otros modelos.
- Legal revisa los términos contractuales de cualquier proveedor de inteligencia artificial de
  terceros para confirmar que los datos de clientes no se usan para entrenar modelos de uso general sin
  consentimiento explícito, y que existe un DPA vigente si el proveedor califica como subprocesador.
- Decisiones automatizadas que tengan un efecto significativo sobre un cliente o usuario (por ejemplo,
  aprobación o rechazo automático de una solicitud) deben ofrecer un mecanismo de revisión humana
  cuando la regulación aplicable lo requiera.

## Gestión de brechas de seguridad: línea de tiempo de respuesta

- **0-24 horas**: contención inicial del incidente por Seguridad de la Información, notificación a
  Legal y evaluación preliminar del alcance.
- **24-72 horas**: determinación de si el incidente califica como una brecha reportable según la
  regulación aplicable en cada jurisdicción afectada, y preparación de la notificación si corresponde.
- **Según plazo regulatorio**: notificación formal a las autoridades y, si aplica, a los clientes o
  titulares de datos afectados, dentro del plazo específico que exija la regulación de cada
  jurisdicción (que puede variar considerablemente entre regiones).
- Después de resuelto el incidente, Legal y Seguridad de la Información documentan un análisis
  post-mortem con las causas raíz y las medidas correctivas implementadas, disponible para consulta
  interna del equipo de liderazgo.

## Derechos de portabilidad de datos

Cuando un cliente solicita la portabilidad de sus datos (recibir sus datos en un formato estructurado
para transferirlos a otro proveedor), Legal coordina con el equipo técnico responsable para generar la
exportación en un formato de uso común, dentro del plazo regulatorio aplicable. Esta solicitud es
distinta de una solicitud de eliminación y no implica que la relación contractual con el cliente
termine.
