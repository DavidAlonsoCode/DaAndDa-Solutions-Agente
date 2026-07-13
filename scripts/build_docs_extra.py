"""
build_docs_extra.py
Genera 4 PDFs de minimo 15 paginas para Da&Da Solutions:
  - faq_soporte.pdf
  - politica_privacidad.pdf
  - planes_precios.pdf
  - terminos_uso.pdf

Ejecutar desde la raiz del proyecto:
    venv\\Scripts\\python scripts\\build_docs_extra.py
Los PDFs se generan en la carpeta docs/.
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

_base = getSampleStyleSheet()

STYLES = {
    "body": ParagraphStyle("body", parent=_base["Normal"],
                           alignment=TA_JUSTIFY, fontSize=10.5, leading=16,
                           spaceAfter=8),
    "h2":   ParagraphStyle("h2", parent=_base["Normal"],
                           alignment=TA_LEFT, fontSize=13, leading=17,
                           spaceAfter=6, spaceBefore=16,
                           fontName="Helvetica-Bold",
                           textColor=colors.HexColor("#1A1A2E")),
    "h3":   ParagraphStyle("h3", parent=_base["Normal"],
                           alignment=TA_LEFT, fontSize=11, leading=15,
                           spaceAfter=4, spaceBefore=12,
                           fontName="Helvetica-Bold",
                           textColor=colors.HexColor("#2D2D60")),
    "bullet": ParagraphStyle("bullet", parent=_base["Normal"],
                              alignment=TA_LEFT, fontSize=10.5, leading=15,
                              spaceAfter=4, leftIndent=20),
    "center": ParagraphStyle("center", parent=_base["Normal"],
                              alignment=TA_CENTER, fontSize=10, leading=14,
                              spaceAfter=4,
                              textColor=colors.HexColor("#555555")),
    "note":   ParagraphStyle("note", parent=_base["Normal"],
                              alignment=TA_JUSTIFY, fontSize=9.5, leading=14,
                              spaceAfter=6, leftIndent=16, rightIndent=16,
                              textColor=colors.HexColor("#444444")),
    "legal":  ParagraphStyle("legal", parent=_base["Normal"],
                              alignment=TA_JUSTIFY, fontSize=9.5, leading=14,
                              spaceAfter=6,
                              textColor=colors.HexColor("#333333")),
}


def _story(title, subtitle, doc_type, blocks):
    story = []
    story.append(Spacer(1, 2.5 * cm))
    cover_co = ParagraphStyle("cov", fontSize=24, leading=30,
                               alignment=TA_CENTER, fontName="Helvetica-Bold",
                               textColor=colors.HexColor("#0D0D14"))
    story.append(Paragraph("Da&amp;Da Solutions", cover_co))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="85%", thickness=3,
                             color=colors.HexColor("#7C3AED"), hAlign="CENTER"))
    story.append(Spacer(1, 0.5 * cm))
    cover_tit = ParagraphStyle("covt", fontSize=19, leading=25,
                                alignment=TA_CENTER, fontName="Helvetica-Bold",
                                textColor=colors.HexColor("#2D2D2D"))
    story.append(Paragraph(title, cover_tit))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(subtitle, STYLES["center"]))
    story.append(Spacer(1, 2 * cm))
    story.append(HRFlowable(width="55%", thickness=1,
                             color=colors.HexColor("#AAAAAA"), hAlign="CENTER"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(doc_type, STYLES["center"]))
    story.append(Paragraph(
        "Version 1.0  |  Ejercicio fiscal 2026  |  Departamento Legal y Comercial",
        STYLES["center"]))
    story.append(PageBreak())

    for raw in blocks:
        b = raw.strip()
        if not b:
            continue
        if b == ">>>BREAK":
            story.append(PageBreak())
        elif b == "---":
            story.append(Spacer(1, 8))
            story.append(HRFlowable(width="100%", thickness=0.6,
                                     color=colors.HexColor("#DDDDDD")))
            story.append(Spacer(1, 8))
        elif b.startswith("### "):
            story.append(Paragraph(b[4:], STYLES["h3"]))
        elif b.startswith("## "):
            story.append(Paragraph(b[3:], STYLES["h2"]))
        elif b.startswith("- "):
            story.append(Paragraph("\u2022 " + b[2:], STYLES["bullet"]))
        elif b.startswith("[NOTE] "):
            story.append(Paragraph(b[7:], STYLES["note"]))
        elif b.startswith("[LEGAL] "):
            story.append(Paragraph(b[8:], STYLES["legal"]))
        else:
            story.append(Paragraph(b, STYLES["body"]))
    return story


def make_pdf(out_path, title, subtitle, doc_type, blocks):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2.3 * cm, rightMargin=2.3 * cm,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
    )
    doc.build(_story(title, subtitle, doc_type, blocks))
    pages = _count_pages(out_path)
    kb = os.path.getsize(out_path) // 1024
    print(f"  [{pages:2d} pag | {kb:3d} KB]  {os.path.basename(out_path)}")


def _count_pages(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return "?"
    return len(PdfReader(path).pages)


DOCS = []

# ==============================================================
# 1. FAQ DE SOPORTE
# ==============================================================
DOCS.append(dict(
    filename="faq_soporte.pdf",
    title="Preguntas Frecuentes de Soporte",
    subtitle="Centro de ayuda oficial para usuarios de Da&amp;Da Solutions",
    doc_type="Documento de Soporte — Uso Publico",
    blocks=[
        "## 1. Acerca de Da&Da Solutions",

        "### 1.1 ¿Que es Da&Da Solutions?",
        "Da&amp;Da Solutions es una empresa de desarrollo de software y consultoria tecnologica fundada en 2014 con sede principal en Buenos Aires, Argentina. Ofrecemos plataformas SaaS, integraciones de sistemas, soluciones de inteligencia artificial aplicada y servicios de desarrollo a medida para empresas de mediana y gran escala en America Latina, Espana y Estados Unidos.",
        "Nuestra propuesta de valor se centra en tres pilares: velocidad de entrega sin sacrificar calidad, tecnologia de vanguardia con enfoque practico, y acompanamiento continuo post-implementacion. Mas del 91% de nuestros clientes renueva su contrato ano a ano, lo que refleja el compromiso que asumimos con cada proyecto.",
        "Contamos con mas de 350 colaboradores distribuidos en cuatro paises: Argentina, Colombia, Mexico y Espana. Hemos completado mas de 600 proyectos de software desde nuestra fundacion, en verticales que van desde fintech y salud digital hasta e-commerce, logistica y educacion.",
        "El nombre Da&amp;Da Solutions nace de los apellidos de sus dos cofundadores, Diego Aramburu y Dario Aguilar, quienes se conocieron en la Facultad de Ingenieria de la Universidad de Buenos Aires en 2010 y fundaron la empresa cuatro anos despues con una mision clara: hacer tecnologia de impacto sin perder el foco humano.",

        "### 1.2 ¿En que industrias trabaja Da&Da Solutions?",
        "Tenemos experiencia solida y equipos especializados en las siguientes verticales de negocio:",
        "- <b>Fintech:</b> plataformas de pagos, billeteras digitales, sistemas de core bancario, analisis de riesgo crediticio, cumplimiento regulatorio (KYC/AML), plataformas de prestamos digitales.",
        "- <b>Salud Digital:</b> historias clinicas electronicas (HCE), telemedicina, integracion con HL7 FHIR, gestion de turnos y agendas medicas, plataformas de diagnostico asistido por IA.",
        "- <b>E-commerce y Retail:</b> plataformas de marketplace B2B y B2C, gestion de inventario multialmacen, motores de recomendacion personalizados, sistemas de loyalty y gamificacion.",
        "- <b>Logistica y Supply Chain:</b> sistemas de tracking en tiempo real con GPS e IoT, ruteo inteligente con optimizacion de ultima milla, gestion de almacenes (WMS), integracion con operadores logisticos.",
        "- <b>Educacion:</b> plataformas LMS con gamificacion, sistemas de evaluacion adaptativa con IA, reportes de aprendizaje para docentes e instituciones, plataformas de educacion corporativa.",
        "- <b>Energia y Utilities:</b> monitoreo de infraestructura critica, medicion inteligente (smart metering), optimizacion de redes de distribucion, plataformas de gestion de energia renovable.",
        "- <b>Sector Publico:</b> sistemas de gestion de tramites digitales, plataformas de transparencia y datos abiertos, sistemas de recaudacion tributaria, portales ciudadanos.",
        "Cada vertical cuenta con al menos un equipo con experiencia de dominio profunda, lo que nos permite no solo construir software sino tambien asesorar en las mejores practicas del sector y anticipar requisitos regulatorios especificos.",

        "### 1.3 ¿Da&Da Solutions trabaja con startups o solo con grandes empresas?",
        "Trabajamos con organizaciones de todos los tamanos, aunque nuestro modelo de servicios esta optimizado para empresas que tienen entre 50 y 5.000 empleados. Para startups en etapa temprana, ofrecemos nuestro programa <b>Da&amp;Da Launchpad</b>, que incluye condiciones comerciales especiales, mentoria tecnica y acceso a nuestra red de inversores asociados.",
        "Para startups seleccionadas en etapa pre-seed o seed, podemos explorar modelos de compensacion hibrida que incluyan equity a cambio de servicios, sujeto a evaluacion caso por caso por parte de nuestro comite de partnerships estrategicos. Actualmente participamos como socios tecnologicos en 14 startups en distintas etapas de crecimiento.",
        "Para grandes corporaciones y multinacionales, ofrecemos el Plan Enterprise con infraestructura dedicada, SLAs personalizados y un equipo asignado exclusivamente al cliente. Entre nuestros clientes Enterprise se encuentran organizaciones del sector financiero, asegurador, de salud y de consumo masivo.",

        "### 1.4 ¿Donde tienen oficinas y en que zonas horarias operan?",
        "Da&amp;Da Solutions opera de manera distribuida con presencia fisica en cuatro ciudades y equipos remotos en mas de 15 paises:",
        "- <b>Buenos Aires, Argentina (sede central):</b> Av. Corrientes 3456, Piso 12. Horario: GMT-3.",
        "- <b>Ciudad de Mexico, Mexico:</b> Insurgentes Sur 1898, Piso 4. Horario: GMT-6.",
        "- <b>Bogota, Colombia:</b> Cra. 11 N° 93-53, Piso 8. Horario: GMT-5.",
        "- <b>Madrid, Espana:</b> Calle Serrano 41, Piso 3. Horario: GMT+1 / GMT+2 en verano.",
        "El equipo de soporte opera en horario extendido para cubrir las zonas horarias de todos nuestros clientes. El soporte 24/7 para incidentes criticos esta disponible para planes Professional en adelante.",

        "---",
        "## 2. Soporte Tecnico General",

        "### 2.1 ¿Como puedo contactar al soporte tecnico?",
        "Da&amp;Da Solutions ofrece multiples canales de soporte segun el plan contratado. Es importante elegir el canal correcto para garantizar los tiempos de respuesta comprometidos:",
        "- <b>Portal de Soporte Web:</b> support.dadacode.io — disponible 24/7 para apertura de tickets, seguimiento del estado, consulta de historial y acceso a la base de conocimiento con mas de 800 articulos.",
        "- <b>Correo electronico:</b> soporte@dadacode.io — tiempo de primera respuesta maximo 4 horas habiles para planes Starter, 2 horas para planes Professional, 30 minutos para planes Enterprise.",
        "- <b>Chat en vivo:</b> disponible dentro de la plataforma para planes Professional y Enterprise, de lunes a viernes de 8:00 a 20:00 hs (GMT-3). Tiempo de espera promedio: menos de 2 minutos.",
        "- <b>Telefono:</b> +54 11 4800-9200 — solo para planes Enterprise, disponible 24/7 para incidencias criticas. Para incidencias no criticas: lunes a viernes de 9:00 a 18:00 hs GMT-3.",
        "- <b>Slack Connect:</b> canal privado de Slack conectado directamente con el equipo de soporte, disponible para planes Enterprise Plus y contratos de servicios gestionados.",
        "- <b>Microsoft Teams:</b> para clientes que usan el ecosistema Microsoft, ofrecemos integracion directa via Teams para el reporte y seguimiento de incidentes.",
        "Al abrir un ticket, incluye siempre: el nombre del proyecto o producto afectado, una descripcion detallada del problema, los pasos exactos para reproducirlo, capturas de pantalla o videos si aplica, el ambiente afectado (produccion, staging, testing) y el impacto estimado en el negocio.",

        "### 2.2 ¿Cuales son los tiempos de respuesta garantizados (SLAs)?",
        "Los SLAs de tiempo de respuesta y resolucion varian segun la severidad del incidente y el plan contratado. La clasificacion oficial de severidad es la siguiente:",
        "- <b>Severity 1 — Critica:</b> el sistema de produccion esta completamente inaccesible o hay perdida de datos activa. Respuesta inicial: 15 min (Enterprise), 1 hora (Professional), 4 horas (Starter). Resolucion objetivo: 4 horas.",
        "- <b>Severity 2 — Alta:</b> funcionalidad critica degradada con impacto en usuarios finales, existe workaround parcial. Respuesta: 1 hora (Enterprise), 4 horas (Professional), 8 horas (Starter). Resolucion: 8 horas habiles.",
        "- <b>Severity 3 — Media:</b> funcionalidad no critica afectada, el negocio puede continuar operando normalmente. Respuesta: 4 horas habiles para todos los planes. Resolucion: 3 dias habiles.",
        "- <b>Severity 4 — Baja:</b> consultas, mejoras menores, solicitudes de documentacion o acceso. Respuesta: 1 dia habil. Resolucion: segun backlog prioritario (tipicamente 5-10 dias habiles).",
        "[NOTE] Los SLAs aplican solo durante el horario de cobertura acordado en el contrato. Los incidentes Severity 1 siempre tienen cobertura 24/7 independientemente del plan, dado su impacto en el negocio. Si un incidente escala de severidad durante su gestion, los nuevos SLAs aplican desde el momento de la escalada.",

        "### 2.3 ¿Como se mide y reporta el cumplimiento de SLAs?",
        "Cada cliente con plan Professional o superior tiene acceso a un dashboard de SLA en tiempo real dentro del portal de soporte. Este dashboard muestra: el numero de tickets abiertos y cerrados en el mes, el tiempo promedio de primera respuesta por categoria, el tiempo promedio de resolucion, el porcentaje de cumplimiento de SLA por severidad, y el historico mensual de los ultimos 12 meses.",
        "Al cierre de cada mes se genera automaticamente un reporte PDF que se envia al contacto tecnico y al contacto comercial registrados. Si en algun mes el cumplimiento de SLA cae por debajo del umbral contratado, se activa automaticamente el proceso de acreditacion de creditos de servicio segun lo estipulado en los Terminos y Condiciones de Uso.",
        "Los clientes Enterprise reciben adicionalmente un reporte trimestral de calidad de servicio (QBR — Quarterly Business Review) presentado por su Technical Account Manager, que incluye analisis de tendencias, recomendaciones de optimizacion y planificacion del proximo trimestre.",

        "### 2.4 ¿Que informacion debo incluir al reportar un problema?",
        "Para agilizar la resolucion de cualquier incidente, te pedimos que incluyas la siguiente informacion al abrir un ticket:",
        "- <b>Descripcion del problema:</b> que ocurre, cuando ocurrio por primera vez, con que frecuencia se reproduce.",
        "- <b>Pasos para reproducir:</b> una secuencia numerada de acciones que lleva al error, partiendo de un estado conocido (por ejemplo, 'ya logueado como usuario admin').",
        "- <b>Comportamiento esperado vs. comportamiento observado:</b> que deberia ocurrir vs. que ocurre realmente.",
        "- <b>Ambiente afectado:</b> produccion, staging, sandbox. Region geografica si corresponde.",
        "- <b>Impacto:</b> cuantos usuarios estan afectados, que procesos de negocio estan bloqueados, hay perdida de datos.",
        "- <b>Evidencia:</b> capturas de pantalla, videos, logs de consola del navegador (F12), mensajes de error exactos (incluyendo codigos de error y stack traces si los hay).",
        "- <b>Contexto de cambios recientes:</b> hubo algun deploy reciente, cambio de configuracion, actualizacion de integraciones o migracion de datos cerca del momento en que empezo el problema.",
        "Cuanto mas completa sea la informacion inicial, mas rapida sera la resolucion. Los tickets con informacion incompleta pueden requerir rondas adicionales de preguntas que alargan el tiempo de resolucion.",

        "---",
        "## 3. Gestion de Incidentes",

        "### 3.1 ¿Que sucede cuando reporto un incidente critico?",
        "Cuando se clasifica un incidente como Severity 1, se activa automaticamente el protocolo de gestion de incidentes criticos (P1 Protocol). El proceso es el siguiente:",
        "- El sistema asigna automaticamente un Incident Commander del equipo de guardia, quien toma la responsabilidad de la coordinacion general del incidente.",
        "- Se crea un canal de comunicacion exclusivo en Slack o Teams (segun preferencia registrada del cliente) donde participan: el Incident Commander, ingenieros de guardia con expertise en el area afectada, y los contactos tecnicos del cliente.",
        "- El Incident Commander actualiza el estado del incidente cada 30 minutos como maximo hasta la resolucion, independientemente del progreso.",
        "- Se notifica automaticamente al status page publico (status.dadacode.io) con el impacto correspondiente.",
        "- Una vez resuelto el incidente, se realiza un Post-Mortem dentro de las 48 horas siguientes. El documento de Post-Mortem incluye: cronologia completa del incidente (con timestamps exactos), causa raiz identificada, acciones correctivas implementadas, y acciones preventivas planificadas con fechas de compromiso.",
        "- El Post-Mortem se comparte con el cliente sin censuras. Creemos en la transparencia total como base de una relacion de confianza duradera.",

        "### 3.2 ¿Tienen un status page publico?",
        "Si. Podes monitorear el estado de todos los servicios de Da&amp;Da Solutions en <b>status.dadacode.io</b>. La pagina muestra en tiempo real:",
        "- Estado actual de cada servicio y componente (Operational, Degraded Performance, Partial Outage, Major Outage, Under Maintenance).",
        "- Historico de incidentes de los ultimos 90 dias con Post-Mortems publicos cuando aplica.",
        "- Incidentes activos con actualizaciones cronologicas en tiempo real.",
        "- Metricas de uptime de los ultimos 30, 60 y 90 dias por servicio.",
        "- Proximas ventanas de mantenimiento programado.",
        "Podes suscribirte a notificaciones automaticas via email, SMS, Slack, PagerDuty, OpsGenie, o webhook personalizado para recibir alertas en el momento en que el estado de cualquier servicio cambie.",

        "### 3.3 ¿Que garantia de uptime ofrecen?",
        "Da&amp;Da Solutions garantiza los siguientes niveles de disponibilidad mensual segun el plan contratado:",
        "- <b>Starter:</b> 99.5% de uptime mensual (equivalente a hasta 3.6 horas de downtime por mes).",
        "- <b>Professional:</b> 99.9% de uptime mensual (equivalente a hasta 43.8 minutos de downtime por mes).",
        "- <b>Business:</b> 99.95% de uptime mensual (equivalente a hasta 21.9 minutos de downtime por mes).",
        "- <b>Enterprise:</b> 99.99% de uptime mensual (equivalente a hasta 4.38 minutos de downtime por mes), con arquitectura multi-region activo-activo.",
        "El downtime planificado por mantenimiento programado (comunicado con al menos 72 horas de anticipacion) no se computa dentro del calculo de SLA de uptime. El cumplimiento del SLA se mide mensualmente con datos tomados de nuestro sistema de monitoreo interno y de herramientas de monitoreo de terceros independientes.",

        "### 3.4 ¿Como funciona el proceso de escalada de incidentes?",
        "Cuando un incidente no se resuelve dentro de los tiempos esperados o su impacto crece, se activa el proceso de escalada automatica:",
        "- <b>Nivel 1:</b> el agente de soporte que recibio el ticket busca resolucion con los recursos disponibles.",
        "- <b>Nivel 2:</b> si no hay resolucion en el 70% del tiempo SLA, el ticket escala automaticamente al equipo de ingenieria de guardia.",
        "- <b>Nivel 3:</b> si tampoco hay resolucion, escala al Staff Engineer de guardia y se activa el P1 Protocol.",
        "- <b>Nivel 4:</b> incidentes que persisten o tienen impacto catastrofico escalan directamente al CTO o al VP de Ingenieria.",
        "Los clientes Enterprise tienen acceso directo al Nivel 3 para incidentes Severity 1, sin necesidad de pasar por los niveles anteriores.",

        "---",
        "## 4. Facturacion y Pagos",

        "### 4.1 ¿Que metodos de pago aceptan?",
        "Aceptamos los siguientes metodos de pago segun la modalidad del contrato:",
        "- <b>Transferencia bancaria:</b> disponible para todos los planes, emitimos factura al confirmar el credito en cuenta.",
        "- <b>Tarjeta de credito:</b> disponible para planes Starter y Professional con pago mensual o anual, a traves de nuestra pasarela de pagos segura (Stripe). Aceptamos Visa, Mastercard y American Express.",
        "- <b>PayPal:</b> disponible para clientes fuera de Argentina y Colombia.",
        "- <b>Crypto (USDT/USDC en red Polygon o Ethereum):</b> disponible para contratos anuales superiores a USD 10.000, previa coordinacion con el equipo comercial.",
        "Para contratos Enterprise el pago se coordina directamente con el equipo de finanzas y generalmente se realiza mediante transferencia bancaria con condiciones a 30, 60 o 90 dias segun lo acordado en el contrato.",

        "### 4.2 ¿Como puedo acceder a mis facturas?",
        "Todas las facturas se envian automaticamente al correo de facturacion registrado en tu cuenta dentro de las 24 horas de procesado el pago. Adicionalmente, podes acceder al historial completo de facturas desde el portal de cliente en <b>billing.dadacode.io</b>, donde podes: descargar facturas en formato PDF y XML, ver el estado de cada factura (pendiente, pagada, vencida), actualizar los datos de facturacion y el correo de recepcion, y descargar el resumen anual de facturacion para uso contable.",
        "Para clientes con contratos anuales, emitimos la factura completa del ano al inicio del periodo contratado (o en cuotas semestrales si asi se acordo). Para suscripciones mensuales, la factura se genera el primer dia habil de cada mes por el periodo siguiente.",

        "### 4.3 ¿Que pasa si hay un retraso en el pago?",
        "En caso de retraso en el pago, el proceso es el siguiente:",
        "- <b>Dias 1-7 de atraso:</b> recordatorio automatico por email (dias 1, 3 y 7).",
        "- <b>Dias 8-15 de atraso:</b> el equipo de finanzas contacta al cliente directamente para coordinar el pago o acordar un plan de cuotas sin interes.",
        "- <b>Dias 16-30 de atraso:</b> se puede aplicar una suspension temporal del servicio, previa notificacion con 48 horas de anticipacion. El servicio se reactiva automaticamente al confirmar el pago.",
        "- <b>Mas de 30 dias de atraso:</b> se puede proceder a la baja del servicio y remision a proceso de gestion de cobranza. Se aplican intereses punitorios segun lo estipulado en los Terminos y Condiciones.",
        "Entendemos que pueden surgir situaciones imprevistas. Si anticipas un problema de pago, contacta al equipo comercial antes del vencimiento: buscaremos soluciones flexibles sin afectar la continuidad del servicio.",

        "---",
        "## 5. Cuenta y Gestion de Usuarios",

        "### 5.1 ¿Como agrego nuevos usuarios a mi cuenta?",
        "Para agregar nuevos usuarios, el administrador de la cuenta debe ingresar al panel de administracion en <b>app.dadacode.io/admin</b> y seleccionar 'Gestion de Usuarios'. Desde alli podes: invitar usuarios por correo electronico, asignarles un rol predefinido (Viewer, Editor, Developer, Admin, Billing Admin), configurar permisos granulares a nivel de proyecto o modulo, organizar usuarios en equipos y asignar equipos a proyectos especificos, y establecer restricciones de acceso por horario o por IP.",
        "El usuario invitado recibira un correo con un enlace de activacion valido por 7 dias. Si el enlace vence, el administrador puede reenviar la invitacion desde el panel de gestion de usuarios. El numero de usuarios incluidos varia segun el plan contratado; los usuarios adicionales por encima del limite del plan tienen un costo adicional por usuario segun la guia de Planes y Precios.",

        "### 5.2 ¿Como restablezco mi contrasena?",
        "Si olvidaste tu contrasena, podes restablecerla desde la pantalla de login en <b>app.dadacode.io</b> haciendo clic en '¿Olvidaste tu contrasena?'. Recibiras un enlace de restablecimiento en tu correo registrado, valido por 15 minutos. Al hacer clic en el enlace se te pedira ingresar una nueva contrasena que cumpla con la politica de seguridad: minimo 12 caracteres, al menos una mayuscula, una minuscula, un numero y un simbolo especial.",
        "Si no tenes acceso al correo registrado o tu cuenta esta bloqueada por multiples intentos fallidos, contacta al soporte en soporte@dadacode.io desde otro correo verificado con informacion que permita verificar tu identidad. Por razones de seguridad, el restablecimiento de acceso por canal telefonico o chat no esta disponible; todas las solicitudes se procesan unicamente por via escrita con verificacion de identidad.",

        "### 5.3 ¿Puedo configurar el inicio de sesion unico (SSO)?",
        "Si. Da&amp;Da Solutions soporta SSO (Single Sign-On) mediante los siguientes protocolos y proveedores:",
        "- <b>SAML 2.0:</b> compatible con Okta, OneLogin, Azure AD, PingIdentity, ADFS.",
        "- <b>OpenID Connect (OIDC):</b> compatible con Google Workspace, Azure AD, Auth0, Keycloak.",
        "- <b>LDAP / Active Directory:</b> disponible para planes Business y Enterprise.",
        "La configuracion de SSO requiere que el administrador de la cuenta ingrese al panel en app.dadacode.io/admin/sso y siga el wizard de configuracion guiado. Para configuraciones complejas con SAML, el equipo de soporte puede agendar una sesion de asistencia tecnica. Una vez configurado el SSO, el administrador puede hacer obligatorio el uso de SSO para todos los usuarios de la organizacion, bloqueando el login con usuario y contrasena.",

        "### 5.4 ¿Que roles y permisos estan disponibles?",
        "Da&amp;Da Solutions implementa un sistema de control de acceso basado en roles (RBAC) con los siguientes roles predefinidos:",
        "- <b>Viewer:</b> puede ver proyectos y reportes, pero no puede crear, editar ni eliminar nada.",
        "- <b>Editor:</b> puede crear y editar contenido dentro de los proyectos a los que tiene acceso.",
        "- <b>Developer:</b> acceso completo a las funcionalidades tecnicas, incluyendo API, integraciones y configuracion tecnica de proyectos.",
        "- <b>Admin:</b> control total sobre la plataforma excepto las configuraciones de facturacion.",
        "- <b>Billing Admin:</b> acceso exclusivo al modulo de facturacion y suscripcion.",
        "- <b>Super Admin:</b> acceso total sin restricciones, tipicamente asignado solo al dueno de la cuenta.",
        "Adicionalmente, en planes Business y Enterprise es posible crear roles personalizados con permisos granulares a nivel de modulo, proyecto y accion especifica (leer, crear, editar, eliminar, exportar, compartir).",

        "---",
        "## 6. Seguridad y Privacidad",

        "### 6.1 ¿Da&Da Solutions esta certificada en alguna norma de seguridad?",
        "Si. Da&amp;Da Solutions mantiene las siguientes certificaciones y cumplimientos auditados externamente:",
        "- <b>ISO/IEC 27001:2022</b> — Gestion de Seguridad de la Informacion. Certificado N° ISO27001-2024-ARG-0047, emitido por Bureau Veritas. Renovacion anual.",
        "- <b>SOC 2 Type II</b> — Controles de seguridad, disponibilidad, integridad de procesamiento, confidencialidad y privacidad. Auditado anualmente por Deloitte Argentina.",
        "- <b>PCI DSS Level 2</b> — Para los modulos que involucran procesamiento de pagos con tarjeta de credito o debito.",
        "- <b>Cumplimiento GDPR</b> — Para el procesamiento de datos de ciudadanos europeos, con DPO designado.",
        "- <b>Cumplimiento LGPD</b> — Para el procesamiento de datos de ciudadanos brasileneos.",
        "- <b>Cumplimiento Ley 25.326 Argentina</b> — Inscripcion ante la AAIP con numero de registro RNBD-2024-0158.",
        "Los reportes de auditoria SOC 2 estan disponibles bajo NDA para clientes con planes Enterprise. Podes solicitarlos a traves de tu Account Manager o a security@dadacode.io.",

        "### 6.2 ¿Como protegen mis datos?",
        "Los datos de los clientes estan protegidos mediante una arquitectura de seguridad en capas (defense-in-depth):",
        "- <b>Cifrado en transito:</b> TLS 1.3 en todas las comunicaciones externas e internas entre microservicios.",
        "- <b>Cifrado en reposo:</b> AES-256 para todos los datos almacenados en bases de datos, sistemas de archivos y backups.",
        "- <b>Gestion de claves:</b> AWS KMS con rotacion automatica de claves cada 90 dias y auditoria de cada uso.",
        "- <b>Aislamiento por tenant:</b> arquitectura multi-tenant con namespacing estricto a nivel de base de datos. Los datos de un cliente nunca son accesibles por otro cliente.",
        "- <b>Acceso con privilegio minimo:</b> ningun empleado de Da&amp;Da Solutions tiene acceso a datos de produccion sin proceso formal de break-glass con logging auditado.",
        "- <b>Monitoreo continuo:</b> SIEM con correlacion de eventos y alertas en tiempo real, respaldado por un equipo de seguridad disponible 24/7.",
        "- <b>Pen testing:</b> pruebas de penetracion externas realizadas anualmente por una firma independiente, con retest de vulnerabilidades encontradas.",

        "### 6.3 ¿Puedo solicitar la eliminacion de mis datos?",
        "Si, tenes derecho a solicitar la eliminacion de tus datos personales y de los datos de tu organizacion. Para hacerlo: envia una solicitud formal a privacidad@dadacode.io con el asunto 'Solicitud de Eliminacion de Datos'. El proceso de eliminacion se completa en un maximo de 30 dias calendario. Recibiras un certificado de eliminacion que acredita que los datos fueron borrados de todos nuestros sistemas, incluyendo backups.",
        "[NOTE] La eliminacion de datos de produccion se inicia automaticamente a los 90 dias del vencimiento o cancelacion del contrato, a menos que el cliente solicite una retencion extendida por razones regulatorias o de auditoria interna.",

        "---",
        "## 7. Integraciones, API y Herramientas para Desarrolladores",

        "### 7.1 ¿Da&Da Solutions tiene una API publica?",
        "Si. Da&amp;Da Solutions expone una API REST y una API GraphQL para todos los planes Professional en adelante. La documentacion completa esta disponible en <b>docs.dadacode.io/api</b>. La API esta versionada semanticamente (actualmente en version v3) y toda version mayor se mantiene activa durante al menos 24 meses tras el lanzamiento de una nueva version, con un periodo de depreciacion claramente comunicado.",
        "La API incluye: autenticacion mediante OAuth 2.0 y API Keys, rate limiting configurable por plan, webhooks para eventos en tiempo real con reintentos automaticos y firma HMAC-SHA256, SDKs oficiales en Python, JavaScript/TypeScript, Java y Go, y una coleccion de Postman actualizada disponible en docs.dadacode.io/postman.",

        "### 7.2 ¿Con que herramientas externas se integran nativamente?",
        "Da&amp;Da Solutions cuenta con integraciones nativas listas para usar con las siguientes plataformas y herramientas:",
        "- <b>CRM:</b> Salesforce, HubSpot, Pipedrive, Zoho CRM, Microsoft Dynamics 365.",
        "- <b>ERP:</b> SAP Business One, Oracle NetSuite, Microsoft Dynamics 365 Finance.",
        "- <b>Comunicaciones:</b> Slack, Microsoft Teams, Google Workspace, Zoom, WhatsApp Business API.",
        "- <b>BI y Analytics:</b> Power BI, Tableau, Looker, Google Looker Studio, Metabase.",
        "- <b>DevOps y gestion de proyectos:</b> GitHub, GitLab, Jira, Confluence, Asana, Monday.com, Linear.",
        "- <b>Pagos:</b> Stripe, MercadoPago, PayPal, Adyen, Kushki, Openpay.",
        "- <b>Almacenamiento y documentos:</b> Google Drive, OneDrive, Dropbox, SharePoint.",
        "- <b>Marketing:</b> Mailchimp, HubSpot Marketing, Braze, Customer.io.",
        "Todas las integraciones nativas se configuran desde el panel de administracion sin necesidad de escribir codigo. Para integraciones con sistemas no listados, el equipo de ingenieria puede desarrollar conectores personalizados.",

        "### 7.3 ¿Tienen sandbox o ambiente de pruebas para desarrolladores?",
        "Si. Todo cliente con plan Professional o superior tiene acceso a un ambiente de sandbox completamente aislado de produccion. El sandbox incluye: credenciales separadas de API con un prefijo 'sk_test_' para distinguirlas, datos de prueba pre-cargados para todos los modulos y escenarios comunes, simuladores de servicios externos (pagos, notificaciones, geolocalización, servicios de terceros), reset diario automatico a las 3:00 AM GMT-3, y acceso a la interfaz de monitoreo de requests de API en tiempo real para depuracion.",

        "### 7.4 ¿Como reporto un bug en la API o solicito una nueva funcionalidad?",
        "Para reportar bugs en la API: abri un ticket en support.dadacode.io clasificandolo como 'API Bug Report'. Incluye el endpoint afectado, el request completo (metodo, headers, body) con datos de prueba anonimizados, la respuesta obtenida vs. la esperada, y el request ID que aparece en el header X-Request-ID de cada respuesta de la API.",
        "Para solicitar nuevas funcionalidades o cambios en la API: usa la seccion 'Feature Requests' del portal de soporte. Las solicitudes con mas votos de la comunidad de clientes tienen mayor prioridad en el roadmap de producto, que se revisa trimestralmente.",

        "---",
        "## 8. Cancelacion y Portabilidad de Datos",

        "### 8.1 ¿Como cancelo mi suscripcion?",
        "La cancelacion de una suscripcion mensual puede realizarse en cualquier momento desde el panel de administracion en <b>app.dadacode.io/billing</b>, seccion 'Gestion de Suscripcion', haciendo clic en 'Cancelar suscripcion'. La cancelacion surte efecto al final del periodo facturado en curso; no se realizan reembolsos proporcionales por el periodo no utilizado.",
        "Para cancelar contratos anuales o contratos Enterprise, el proceso debe seguir los terminos estipulados en el contrato firmado. Generalmente se requiere un aviso con 30 o 60 dias de anticipacion segun el tipo de contrato. Contacta a tu Account Manager para iniciar el proceso formal.",

        "### 8.2 ¿Puedo exportar mis datos antes de cancelar?",
        "Absolutamente. Da&amp;Da Solutions garantiza la portabilidad total de tus datos. Podes exportar todos tus datos en formatos estandar (JSON, CSV, SQL dump) desde el panel de administracion en cualquier momento, sin costo adicional. Para datos de gran volumen (mas de 10 GB), el proceso de exportacion se coordina con el equipo tecnico y los datos se entregan via enlace seguro de descarga con vigencia de 7 dias.",
        "Recomendamos realizar la exportacion antes de cancelar el servicio. Una vez cancelado, tenes 90 dias de gracia para acceder a los datos en modo solo lectura antes de que se proceda a su eliminacion definitiva e irreversible.",

        "### 8.3 ¿Que pasa con mis datos luego de la cancelacion?",
        "Luego de la cancelacion, tus datos permanecen almacenados en modo solo lectura por 90 dias. Durante este periodo podes solicitar exportaciones adicionales sin costo. Transcurridos los 90 dias, todos los datos son eliminados de manera permanente e irreversible de nuestros sistemas activos y backups, y se emite un certificado de eliminacion.",
        "[NOTE] Si necesitas un periodo de retencion de datos extendido por razones regulatorias o de auditoria interna, podes solicitar una extension de hasta 5 anos adicionales. Este servicio tiene un costo mensual de almacenamiento segun el volumen de datos retenidos.",

        "---",
        "## 9. Preguntas Frecuentes sobre la Plataforma",

        "### 9.1 ¿La plataforma funciona en todos los navegadores?",
        "Da&amp;Da Solutions soporta oficialmente las ultimas dos versiones de los siguientes navegadores: Google Chrome, Mozilla Firefox, Microsoft Edge, y Safari. Internet Explorer no esta soportado. Para obtener la mejor experiencia, recomendamos usar Google Chrome o Microsoft Edge en sus versiones mas recientes.",
        "La plataforma tambien esta disponible como aplicacion movil nativa para iOS (version 15 o superior) y Android (version 10 o superior), descargable desde la App Store y Google Play respectivamente. La aplicacion movil incluye soporte para biometria (Face ID, huella digital) como metodo de autenticacion adicional.",

        "### 9.2 ¿Tienen documentacion tecnica completa?",
        "Toda la documentacion tecnica de Da&amp;Da Solutions esta centralizada en <b>docs.dadacode.io</b>. La documentacion incluye: guias de inicio rapido por caso de uso, referencias completas de API (REST y GraphQL), tutoriales paso a paso con ejemplos de codigo ejecutables, guias de arquitectura y patrones de integracion recomendados, changelog detallado por version con descripcion del impacto de cada cambio, y guias de migracion entre versiones con herramientas de compatibilidad.",
        "La documentacion esta disponible en espanol e ingles. Para cada endpoint de la API se incluyen ejemplos de codigo en los cuatro lenguajes del SDK oficial. Aceptamos contribuciones de la comunidad via pull requests en nuestro repositorio publico de documentacion en GitHub.",

        "### 9.3 ¿Como puedo capacitar a mi equipo en el uso de la plataforma?",
        "Da&amp;Da Solutions ofrece multiples recursos de capacitacion:",
        "- <b>Da&amp;Da Academy:</b> plataforma de e-learning gratuita en academy.dadacode.io con cursos estructurados por rol (administradores, desarrolladores, usuarios finales) y nivel (basico, intermedio, avanzado). Incluye evaluaciones y certificaciones.",
        "- <b>Webinars mensuales:</b> sesiones online gratuitas de 60-90 minutos sobre nuevas funcionalidades, casos de uso y buenas practicas. Grabaciones disponibles para suscriptores.",
        "- <b>Capacitacion a medida:</b> para planes Business y Enterprise, ofrecemos sesiones de capacitacion personalizadas (onsite o virtual) dictadas por instructores certificados de Da&amp;Da Solutions.",
        "- <b>Comunidad de usuarios:</b> foro en community.dadacode.io donde usuarios comparten experiencias, consultas y soluciones. Moderado por el equipo de Da&amp;Da Solutions.",
    ]
))

# ==============================================================
# 2. POLITICA DE PRIVACIDAD
# ==============================================================
DOCS.append(dict(
    filename="politica_privacidad.pdf",
    title="Politica de Privacidad y Proteccion de Datos",
    subtitle="Documento legal vigente para todos los usuarios de Da&amp;Da Solutions — Version 4.2 — 1 de enero de 2026",
    doc_type="Documento Legal — Uso Publico",
    blocks=[
        "## 1. Introduccion y Compromiso con la Privacidad",
        "Da&amp;Da Solutions S.A. (en adelante, 'Da&amp;Da Solutions', 'la Empresa', 'nosotros' o 'nuestro') se compromete de manera firme e irrestricta con la proteccion de la privacidad y la seguridad de los datos personales de todas las personas que interactuan con nuestros servicios, plataformas, sitios web y aplicaciones.",
        "Esta Politica de Privacidad describe de manera detallada y transparente que datos personales recopilamos, con que finalidades los tratamos, bajo que bases juridicas los procesamos, con quienes los compartimos, cuanto tiempo los conservamos, y cuales son los derechos que asisten a las personas titulares de dichos datos.",
        "Esta politica esta redactada en cumplimiento de la legislacion aplicable en materia de proteccion de datos personales, incluyendo: la Ley N° 25.326 de Proteccion de Datos Personales de la Republica Argentina y sus decretos reglamentarios, el Reglamento General de Proteccion de Datos de la Union Europea (RGPD/GDPR, Reglamento UE 2016/679), la Lei Geral de Protecao de Dados Pessoais de Brasil (LGPD, Lei N° 13.709/2018), la Ley Federal de Proteccion de Datos Personales en Posesion de los Particulares de Mexico (LFPDPPP), y la California Consumer Privacy Act de los Estados Unidos (CCPA/CPRA).",
        "Al utilizar los servicios de Da&amp;Da Solutions, el usuario declara haber leido, comprendido y aceptado las condiciones establecidas en la presente Politica de Privacidad. Si el usuario no esta de acuerdo con alguna disposicion, debera abstenerse de utilizar nuestros servicios e informarnos para procesar la solicitud de eliminacion de cualquier dato que ya hubiera sido recopilado. Le recomendamos revisar esta politica periodicamente, ya que puede ser actualizada para reflejar cambios en nuestras practicas de tratamiento de datos, cambios legales o mejoras en nuestros servicios.",

        "---",
        "## 2. Responsable del Tratamiento de Datos",
        "El responsable del tratamiento de los datos personales recopilados a traves de los servicios de Da&amp;Da Solutions es:",
        "- <b>Razon Social:</b> Da&amp;Da Solutions S.A.",
        "- <b>CUIT:</b> 30-71234567-8",
        "- <b>Domicilio legal:</b> Av. Corrientes 3456, Piso 12, Ciudad Autonoma de Buenos Aires, Argentina (C1193AAQ).",
        "- <b>Correo de contacto para privacidad:</b> privacidad@dadacode.io",
        "- <b>Delegado de Proteccion de Datos (DPO):</b> Dra. Valentina Moreno, DPO certificada CIPP/E. Contacto: dpo@dadacode.io",
        "- <b>Registro ante la AAIP:</b> Inscripta ante la Agencia de Acceso a la Informacion Publica de Argentina con numero de registro RNBD-2024-0158.",
        "Para cualquier consulta, ejercicio de derechos o reclamo relacionado con el tratamiento de datos personales, podes contactar a nuestro equipo de privacidad en privacidad@dadacode.io o mediante carta documento dirigida al domicilio legal indicado.",

        "---",
        "## 3. Categorias de Datos Personales que Recopilamos",

        "### 3.1 Datos Proporcionados Directamente por el Usuario",
        "Recopilamos los datos personales que el usuario nos proporciona de forma activa al interactuar con nuestros servicios. Estas son las categorias principales:",
        "- <b>Datos de identificacion:</b> nombre completo, apellido, numero de documento de identidad (DNI, pasaporte u equivalente segun pais), fecha de nacimiento, nacionalidad.",
        "- <b>Datos de contacto:</b> direccion de correo electronico principal y secundario, numero de telefono movil y fijo, direccion postal completa (calle, numero, ciudad, pais, codigo postal).",
        "- <b>Datos de cuenta:</b> nombre de usuario, contrasena (almacenada unicamente en formato hash con algoritmo Argon2id, nunca en texto plano), foto de perfil (opcional), preferencias de notificaciones y comunicacion.",
        "- <b>Datos profesionales:</b> cargo, departamento, empresa u organizacion, industria, tamano de la empresa, pais de operacion.",
        "- <b>Datos de pago:</b> solo los ultimos 4 digitos del numero de tarjeta de credito/debito (el numero completo nunca es almacenado por Da&amp;Da Solutions; el procesamiento integro es realizado por nuestros procesadores de pago certificados PCI DSS), titular de la tarjeta, informacion de facturacion (razon social, CUIT/RFC/NIF, domicilio fiscal), historial de transacciones.",
        "- <b>Datos de comunicacion:</b> mensajes enviados a traves de nuestros canales de soporte, formularios de contacto, encuestas de satisfaccion y cualquier comunicacion escrita con nuestro equipo.",
        "- <b>Datos de candidatos a empleo:</b> cuando el usuario aplica a una posicion en Da&amp;Da Solutions, recopilamos el curriculum vitae, carta de presentacion, historial laboral, formacion academica y cualquier informacion voluntariamente proporcionada durante el proceso de seleccion.",

        "### 3.2 Datos Recopilados Automaticamente",
        "Cuando el usuario accede y utiliza nuestros servicios, recopilamos automaticamente ciertos datos tecnicos necesarios para el correcto funcionamiento de la plataforma y para mejorar la experiencia de usuario:",
        "- <b>Datos de acceso y logs:</b> direccion IP de origen, fecha y hora exacta de acceso, paginas y recursos visitados, tiempo de permanencia en cada seccion, acciones realizadas dentro de la plataforma, codigos de respuesta HTTP.",
        "- <b>Datos del dispositivo:</b> tipo de dispositivo (PC, tablet, smartphone), sistema operativo y version, version del navegador, idioma del navegador, resolucion de pantalla, modelo del dispositivo para aplicaciones moviles.",
        "- <b>Datos de uso de la plataforma:</b> funcionalidades utilizadas, frecuencia de uso, patrones de navegacion dentro de la plataforma, features activadas y desactivadas, errores encontrados (con stack trace anonimizado), consultas de busqueda dentro de la aplicacion.",
        "- <b>Datos de ubicacion aproximada:</b> pais y ciudad inferidos a partir de la direccion IP (no recopilamos ubicacion GPS precisa sin consentimiento explicito del usuario).",
        "- <b>Datos de comunicaciones de marketing:</b> si el usuario abre o hace clic en nuestros correos electronicos de marketing (usando pixels de seguimiento estandar de la industria, con posibilidad de desactivacion).",
        "- <b>Cookies y tecnologias de seguimiento:</b> segun lo detallado en la seccion de Cookies de este documento.",

        "### 3.3 Datos Obtenidos de Terceros",
        "En determinadas circunstancias podemos recibir datos personales de terceras fuentes, siempre con base juridica legitima:",
        "- <b>Redes sociales y proveedores de identidad:</b> cuando el usuario elige registrarse o iniciar sesion con su cuenta de Google, LinkedIn o GitHub, recibimos los datos basicos de perfil autorizados por el usuario en esa plataforma (tipicamente: nombre, apellido, correo electronico y foto de perfil).",
        "- <b>Partners comerciales:</b> cuando un partner de Da&amp;Da Solutions nos refiere a un potencial cliente, puede compartir datos de contacto basicos sujetos a su propia politica de privacidad y a un acuerdo de confidencialidad firmado con Da&amp;Da Solutions.",
        "- <b>Fuentes publicas verificadas:</b> podemos complementar datos de empresas cliente con informacion disponible en registros oficiales publicos, directorios profesionales legalmente accesibles o bases de datos corporativas de uso comun.",
        "- <b>Proveedores de datos de enriquecimiento:</b> en el contexto comercial B2B, podemos usar servicios de enriquecimiento de datos para completar informacion de contactos profesionales, siempre dentro de los limites legales aplicables.",

        "### 3.4 Categorias Especiales de Datos (Datos Sensibles)",
        "Da&amp;Da Solutions <b>no recopila deliberadamente</b> categorias especiales de datos personales (datos sensibles) tales como: origen etnico o racial, opiniones politicas, convicciones religiosas o filosoficas, afiliacion sindical, datos de salud o biometricos, datos sobre vida u orientacion sexual, datos sobre condenas penales o infracciones administrativas.",
        "En el improbable caso de que el usuario comparta datos de estas categorias de manera voluntaria (por ejemplo, al describir un caso de soporte), los trataremos con el nivel maximo de confidencialidad, no los incorporaremos a ninguna base de datos estructurada, y los eliminaremos tan pronto como ya no sean necesarios para resolver la consulta especifica.",

        "---",
        "## 4. Finalidades y Bases Juridicas del Tratamiento",

        "### 4.1 Prestacion y Mejora del Servicio",
        "<b>Finalidad:</b> proporcionar los servicios contratados, gestionar la cuenta del usuario, procesar pagos, brindar soporte tecnico, diagnosticar y resolver problemas tecnicos, y mejorar continuamente la calidad y funcionalidades de nuestras plataformas mediante el analisis de datos de uso agregados y anonimizados.",
        "<b>Base juridica:</b> ejecucion de un contrato en el que el interesado es parte (Art. 6(1)(b) GDPR); interes legitimo del responsable en la mejora continua del servicio (Art. 6(1)(f) GDPR).",

        "### 4.2 Cumplimiento de Obligaciones Legales",
        "<b>Finalidad:</b> cumplir con obligaciones fiscales, contables, regulatorias y legales aplicables a nuestra actividad en cada jurisdiccion: emision de facturas y documentos comerciales, retencion de registros contables segun plazos legales, respuesta a requerimientos de autoridades competentes (judiciales, fiscales, regulatorias), cumplimiento de normativas de prevencion de lavado de activos y financiamiento del terrorismo (PLDAFT) cuando aplique.",
        "<b>Base juridica:</b> cumplimiento de una obligacion legal aplicable al responsable (Art. 6(1)(c) GDPR).",

        "### 4.3 Comunicaciones Comerciales y Marketing",
        "<b>Finalidad:</b> enviar comunicaciones sobre nuevos productos y funcionalidades, invitaciones a webinars y eventos, articulos de blog y contenido educativo, casos de exito y materiales de referencia, y ofertas comerciales personalizadas que puedan ser de interes del usuario.",
        "<b>Base juridica:</b> consentimiento explicito del usuario (Art. 6(1)(a) GDPR), que puede ser retirado en cualquier momento haciendo clic en el enlace 'Desuscribirse' de cualquier comunicacion de marketing, o contactando a marketing@dadacode.io. Para clientes existentes en el contexto de la relacion comercial, puede aplicar el interes legitimo (Art. 6(1)(f) GDPR) respecto de comunicaciones sobre productos similares a los ya contratados.",

        "### 4.4 Seguridad, Prevencion del Fraude y Proteccion de Sistemas",
        "<b>Finalidad:</b> detectar, prevenir e investigar actividades fraudulentas, accesos no autorizados, usos abusivos de la plataforma, ataques informaticos y cualquier actividad que pueda suponer un riesgo para la seguridad de nuestros sistemas, de los datos almacenados o de otros usuarios.",
        "<b>Base juridica:</b> interes legitimo del responsable en la proteccion de sus sistemas e infraestructura (Art. 6(1)(f) GDPR); en ciertos casos, cumplimiento de obligaciones legales de seguridad informatica.",

        "### 4.5 Analisis, Estadisticas e Investigacion",
        "<b>Finalidad:</b> realizar analisis estadisticos sobre el uso de la plataforma con datos anonimizados o seudonimizados para entender patrones de comportamiento, medir la efectividad de funcionalidades, identificar areas de mejora, y tomar decisiones de producto y negocio basadas en datos.",
        "<b>Base juridica:</b> interes legitimo del responsable en la mejora de sus productos y servicios (Art. 6(1)(f) GDPR). Los datos utilizados para este proposito se anonomizan previamente en la medida de lo posible, eliminando cualquier identificador directo.",

        "### 4.6 Recursos Humanos y Gestion de Candidatos",
        "<b>Finalidad:</b> gestionar procesos de seleccion de personal, evaluar candidaturas, realizar onboarding de nuevos empleados, gestionar la relacion laboral y cumplir con obligaciones de empleador.",
        "<b>Base juridica:</b> ejecucion de medidas precontractuales a peticion del interesado (Art. 6(1)(b) GDPR) para candidatos; ejecucion del contrato de trabajo para empleados; cumplimiento de obligaciones legales laborales y previsionales.",

        "---",
        "## 5. Comparticion de Datos con Terceros",

        "### 5.1 Principio General",
        "Da&amp;Da Solutions no vende, alquila, ni cede datos personales de sus usuarios a terceros con fines comerciales propios. La privacidad de los datos de nuestros clientes es un activo de confianza que protegemos activamente. Unicamente compartimos datos en las circunstancias especificas y limitadas que se describen en esta seccion, siempre bajo acuerdos contractuales que garantizan niveles de proteccion equivalentes a los establecidos en esta politica.",

        "### 5.2 Proveedores de Servicios (Encargados del Tratamiento)",
        "Trabajamos con proveedores de servicios que actuan como encargados del tratamiento. Estos proveedores acceden a datos personales exclusivamente para prestar servicios en nuestro nombre, bajo nuestras instrucciones escritas, con acceso restringido al minimo necesario, y con obligaciones contractuales de proteccion de datos (Data Processing Agreements, DPAs):",
        "- <b>Infraestructura cloud:</b> Amazon Web Services, Inc. (AWS). Region principal: us-east-1 (Virginia del Norte). Region LATAM: sa-east-1 (Sao Paulo, Brasil). DPA firmado con clausulas contractuales estandar.",
        "- <b>Procesamiento de pagos:</b> Stripe, Inc. PCI DSS Level 1 certificado. No acceden al numero completo de tarjeta.",
        "- <b>Correo electronico transaccional:</b> Twilio SendGrid para notificaciones de sistema y transaccionales.",
        "- <b>Herramienta de soporte:</b> Zendesk, Inc. para gestion de tickets de soporte al cliente.",
        "- <b>Analiticas de producto:</b> Mixpanel, Inc. con datos seudonimizados y sin identificadores de usuarios finales.",
        "- <b>Monitoreo de aplicaciones:</b> Datadog, Inc. para monitoreo de rendimiento e infraestructura.",
        "- <b>Seguridad de endpoints:</b> CrowdStrike Holdings, Inc. para deteccion y respuesta a amenazas en dispositivos corporativos.",
        "- <b>Gestion de identidades:</b> Auth0 (Okta) para autenticacion y autorizacion.",

        "### 5.3 Transferencias Internacionales de Datos",
        "Algunos de nuestros proveedores de servicios procesan datos en paises fuera del Espacio Economico Europeo (EEE) o de Argentina que pueden no ofrecer un nivel de proteccion equivalente al europeo o argentino. En estos casos, garantizamos el nivel adecuado de proteccion mediante alguna de las siguientes salvaguardas:",
        "- Clausulas Contractuales Estandar (CCE) adoptadas por la Comision Europea (decision de ejecucion UE 2021/914), aplicadas mediante DPAs firmados con cada proveedor.",
        "- Adhesion del proveedor al marco EU-US Data Privacy Framework, cuando sea aplicable.",
        "- Evaluacion de Impacto de Transferencias Internacionales (Transfer Impact Assessment, TIA) documentada para cada proveedor que opere fuera del EEE, evaluando el marco juridico del pais de destino.",
        "El listado actualizado de todos nuestros subencargados del tratamiento, incluyendo su pais de operacion y la medida de salvaguarda aplicada, esta disponible bajo solicitud dirigida a privacidad@dadacode.io.",

        "### 5.4 Operaciones Corporativas",
        "En el contexto de una fusion, adquisicion, escision, reorganizacion societaria, o venta de activos de Da&amp;Da Solutions, los datos personales podrian ser transferidos a la entidad resultante o adquirente. En ese caso, notificaremos a los usuarios afectados con al menos 30 dias de anticipacion y, de ser necesario, solicitaremos un nuevo consentimiento si el tratamiento propuesto no es compatible con los fines originales.",

        "### 5.5 Divulgacion por Obligacion Legal",
        "Podemos divulgar datos personales a autoridades gubernamentales, judiciales o regulatorias cuando estemos obligados a hacerlo por ley o en respuesta a una orden judicial valida emitida por tribunal competente. En la medida en que la ley lo permita, notificaremos al usuario antes de proceder a dicha divulgacion.",

        "---",
        "## 6. Conservacion de los Datos Personales",

        "### 6.1 Criterios Generales de Conservacion",
        "Conservamos los datos personales solo durante el tiempo estrictamente necesario para cumplir las finalidades para las que fueron recopilados, respetando los periodos minimos obligatorios establecidos por la legislacion aplicable. Al determinar los plazos de conservacion, consideramos: la duracion de la relacion contractual, los periodos de conservacion exigidos por legislacion fiscal y contable, los plazos de prescripcion de acciones legales y reclamaciones, la necesidad de los datos para fines de seguridad, y las instrucciones de los usuarios sobre la gestion de sus datos.",

        "### 6.2 Plazos Especificos por Categoria de Datos",
        "- <b>Datos de cuenta activa:</b> durante toda la vigencia de la cuenta, mas 90 dias de periodo de gracia tras la cancelacion.",
        "- <b>Datos de facturacion y transacciones:</b> 10 anos desde la fecha de la transaccion (obligacion fiscal en la mayoria de las jurisdicciones).",
        "- <b>Registros de comunicaciones de soporte:</b> 3 anos desde el cierre del ticket.",
        "- <b>Logs de seguridad y acceso:</b> 12 meses, salvo que exista una investigacion activa que requiera mayor retencion.",
        "- <b>Datos de marketing:</b> mientras el consentimiento este vigente, mas 90 dias tras la desuscripcion.",
        "- <b>Datos de candidatos no seleccionados:</b> 6 meses desde el cierre del proceso de seleccion (con consentimiento explicito del candidato, podemos conservarlos hasta 2 anos para futuras posiciones).",
        "- <b>Registros de contratos y acuerdos:</b> 10 anos desde la finalizacion del contrato.",
        "- <b>Datos de cookies analiticas:</b> 13 meses desde su creacion.",

        "### 6.3 Eliminacion Segura",
        "Una vez transcurridos los plazos de conservacion, los datos personales son eliminados de manera segura mediante procesos que garantizan su irrecuperabilidad. Para datos en soporte digital, aplicamos estandares de borrado seguro (sobreescritura multiple o destruccion criptografica de las claves de cifrado). Para datos en soporte fisico (impresiones, documentos en papel), se procede a su destruccion mediante destructoras de papel certificadas.",

        "---",
        "## 7. Derechos de los Titulares de Datos",

        "### 7.1 Catalogo de Derechos",
        "Conforme a la legislacion de proteccion de datos aplicable, los titulares de datos personales tienen los siguientes derechos que Da&amp;Da Solutions garantiza y facilita:",
        "- <b>Derecho de Acceso (Art. 15 GDPR / Art. 14 Ley 25.326):</b> obtener confirmacion sobre si tratamos datos personales del interesado y, en caso afirmativo, acceder a una copia completa de dichos datos junto con informacion detallada sobre el tratamiento (finalidades, categorias, destinatarios, plazos de conservacion).",
        "- <b>Derecho de Rectificacion (Art. 16 GDPR / Art. 16 Ley 25.326):</b> solicitar la correccion de datos inexactos o la completitud de datos incompletos sin demora injustificada.",
        "- <b>Derecho de Supresion / 'Derecho al Olvido' (Art. 17 GDPR / Art. 16 Ley 25.326):</b> solicitar la eliminacion de datos personales cuando ya no sean necesarios para la finalidad para la que fueron recopilados, el interesado retire su consentimiento, los datos hayan sido tratados ilicitamente, o deban suprimirse para cumplir con una obligacion legal.",
        "- <b>Derecho de Oposicion (Art. 21 GDPR):</b> oponerse en cualquier momento al tratamiento de datos con fines de marketing directo o cuando el tratamiento se base en el interes legitimo del responsable y el interesado tenga motivos particulares para ello.",
        "- <b>Derecho a la Limitacion del Tratamiento (Art. 18 GDPR):</b> solicitar la suspension temporal del tratamiento de sus datos mientras verificamos una inexactitud, evaluamos una oposicion, o determinamos si existen motivos legitimos que prevalezcan sobre los del interesado.",
        "- <b>Derecho a la Portabilidad de Datos (Art. 20 GDPR):</b> recibir los datos personales que hubiera proporcionado a Da&amp;Da Solutions en formato estructurado, de uso comun y lectura mecanica (JSON, CSV), y transmitirlos directamente a otro responsable del tratamiento.",
        "- <b>Derecho a no ser objeto de decisiones automatizadas (Art. 22 GDPR):</b> no ser objeto de decisiones basadas unicamente en tratamiento automatizado, incluida la elaboracion de perfiles, que produzcan efectos juridicos significativos o le afecten de modo igualmente significativo.",
        "- <b>Derecho a retirar el consentimiento:</b> en cualquier momento y sin perjuicio de la licitud del tratamiento basado en el consentimiento previo a su retirada.",

        "### 7.2 Como Ejercer tus Derechos",
        "Para ejercer cualquiera de los derechos mencionados, el interesado puede:",
        "- Enviar una solicitud a privacidad@dadacode.io con el asunto que indique claramente el derecho que desea ejercer.",
        "- Completar el formulario en linea disponible en dadacode.io/privacidad/derechos.",
        "El interesado debera acreditar su identidad adjuntando una copia de su documento de identidad o mediante verificacion electronica. Responderemos a todas las solicitudes en un plazo maximo de 30 dias calendario desde su recepcion. En casos de especial complejidad, este plazo puede extenderse por 60 dias adicionales, de lo que se informara al interesado por correo electronico.",
        "[NOTE] El ejercicio de estos derechos es gratuito. Solo en caso de solicitudes manifiestamente infundadas, excesivas o repetitivas podemos cobrar un cargo razonable administrativo o negarnos a tramitar la solicitud, informando los motivos por escrito.",

        "### 7.3 Derecho a Presentar una Queja ante la Autoridad de Control",
        "Sin perjuicio de cualquier otro recurso administrativo o judicial, el interesado tiene derecho a presentar una reclamacion ante la autoridad supervisora competente en materia de proteccion de datos:",
        "- <b>Argentina:</b> Agencia de Acceso a la Informacion Publica (AAIP) — datospersonales.aaip.gob.ar",
        "- <b>Union Europea:</b> autoridad de control del Estado miembro donde el interesado tenga su residencia habitual o lugar de trabajo.",
        "- <b>Brasil:</b> Autoridade Nacional de Protecao de Dados (ANPD) — gov.br/anpd",
        "- <b>Mexico:</b> Instituto Nacional de Transparencia, Acceso a la Informacion y Proteccion de Datos Personales (INAI) — inai.org.mx",

        "---",
        "## 8. Cookies y Tecnologias de Seguimiento",

        "### 8.1 Que son las Cookies y Tecnologias Similares",
        "Las cookies son pequenos archivos de texto que un sitio web almacena en el dispositivo del usuario cuando este lo visita. Ademas de cookies, utilizamos tecnologias similares como: web beacons (pixeles de seguimiento, pequenas imagenes transparentes de 1x1 px), localStorage y sessionStorage del navegador, IndexedDB para almacenamiento local de mayor capacidad, y fingerprinting de dispositivos de manera limitada para deteccion de fraude.",

        "### 8.2 Tipos de Cookies que Utilizamos",
        "- <b>Cookies estrictamente necesarias (siempre activas):</b> esenciales para el funcionamiento de la plataforma: gestion de sesion autenticada, seguridad CSRF, preferencias de idioma seleccionadas, consentimiento de cookies registrado. No requieren consentimiento del usuario y no pueden desactivarse.",
        "- <b>Cookies de rendimiento y analiticas (requieren consentimiento):</b> recopilan informacion anonima o seudonimizada sobre como los usuarios interactuan con el sitio: paginas mas visitadas, tiempo de carga, errores, flujos de navegacion. Usamos Google Analytics 4 y Mixpanel con IP anonimizada.",
        "- <b>Cookies de funcionalidad (requieren consentimiento):</b> recuerdan las preferencias del usuario para personalizar la experiencia: tema visual claro/oscuro, disposicion del panel, columnas visibles en tablas, idioma preferido.",
        "- <b>Cookies de marketing y seguimiento (requieren consentimiento):</b> rastrean la actividad del usuario a traves de diferentes sitios para mostrar publicidad relevante y medir la efectividad de campanas de marketing. Usamos Google Ads y LinkedIn Insight Tag.",

        "### 8.3 Duracion de las Cookies",
        "- <b>Cookies de sesion:</b> se eliminan automaticamente al cerrar el navegador.",
        "- <b>Cookies persistentes de corto plazo:</b> duracion de 30 dias (preferencias de usuario, estado de consentimiento de cookies).",
        "- <b>Cookies persistentes de largo plazo:</b> duracion de 12-13 meses (analiticas, identificadores de usuario para marketing).",

        "### 8.4 Gestion y Control de Cookies",
        "Al ingresar por primera vez a nuestro sitio web, se muestra un banner de gestion de consentimiento de cookies (Cookiebot) donde podes: aceptar todas las cookies con un clic, rechazar todas excepto las estrictamente necesarias, o personalizar las categorias de cookies que deseas permitir.",
        "Podes modificar tus preferencias en cualquier momento accediendo al enlace 'Preferencias de Privacidad' en el pie de pagina del sitio. Tambien podes gestionar o eliminar cookies directamente desde la configuracion de tu navegador; ten en cuenta que desactivar ciertas cookies puede afectar la funcionalidad de la plataforma.",

        "---",
        "## 9. Seguridad de los Datos",

        "### 9.1 Medidas Tecnicas de Seguridad",
        "Da&amp;Da Solutions implementa medidas tecnicas actualizadas y apropiadas para proteger los datos personales contra el acceso no autorizado, la perdida accidental, la destruccion, la alteracion o la divulgacion no autorizada:",
        "- <b>Cifrado en transito:</b> TLS 1.3 obligatorio en todas las comunicaciones externas. Comunicaciones internas entre microservicios cifradas con mTLS.",
        "- <b>Cifrado en reposo:</b> AES-256-GCM para todos los datos almacenados en bases de datos relacionales, NoSQL y almacenamiento de objetos.",
        "- <b>Gestion de secretos:</b> AWS KMS y HashiCorp Vault para gestion centralizada de claves de cifrado, tokens y credenciales. Rotacion automatica de claves cada 90 dias.",
        "- <b>Autenticacion robusta:</b> 2FA obligatorio para todos los accesos. Politica de contrasenas con minimo 12 caracteres y complejidad. Bloqueo automatico tras 5 intentos fallidos.",
        "- <b>Gestion de accesos:</b> principio de minimo privilegio aplicado a todos los sistemas. Acceso a datos de produccion solo via proceso break-glass con aprobacion y registro auditado.",
        "- <b>Monitoreo continuo:</b> SIEM (Security Information and Event Management) con correlacion de eventos en tiempo real y alertas automatizadas ante patrones anomalos.",

        "### 9.2 Medidas Organizativas de Seguridad",
        "- Capacitacion anual obligatoria en seguridad de la informacion y privacidad para todos los colaboradores.",
        "- Acuerdos de confidencialidad (NDA) firmados por todos los empleados, contratistas y proveedores con acceso a datos.",
        "- Politica de escritorios limpios y pantallas bloqueadas en las oficinas fisicas.",
        "- Proceso formal de gestion de accesos: alta, modificacion y baja de accesos vinculada al ciclo de vida del empleado.",
        "- Auditorias de seguridad internas trimestrales y externas anuales por firma independiente.",
        "- Programa de Bug Bounty privado para reporte responsable de vulnerabilidades por investigadores de seguridad.",

        "---",
        "## 10. Notificacion de Brechas de Seguridad",
        "En caso de una brecha de seguridad que involucre datos personales, Da&amp;Da Solutions actuara de conformidad con el siguiente procedimiento:",
        "- <b>Deteccion y contencion:</b> activacion inmediata del equipo de respuesta a incidentes (CSIRT) para contener el incidente y preservar evidencia.",
        "- <b>Evaluacion:</b> determinacion del alcance, tipo y volumen de datos afectados, e impacto potencial para los titulares.",
        "- <b>Notificacion a la autoridad:</b> dentro de las 72 horas de haber tomado conocimiento de la brecha (cuando aplique segun legislacion GDPR, LGPD, Ley 25.326).",
        "- <b>Notificacion a usuarios afectados:</b> cuando la brecha represente un alto riesgo para los derechos y libertades de los titulares, se notificara sin demora indebida con la mayor brevedad posible.",
        "La notificacion a usuarios afectados incluira: descripcion de la naturaleza de la brecha, categorias y volumen aproximado de datos afectados, datos de contacto del DPO, posibles consecuencias de la brecha, y medidas adoptadas o propuestas para remediar y mitigar los posibles efectos adversos.",

        "---",
        "## 11. Privacidad de Menores de Edad",
        "Los servicios de Da&amp;Da Solutions estan dirigidos exclusivamente a personas mayores de 18 anos. No recopilamos deliberadamente datos personales de menores de edad. Si tomamos conocimiento de que un menor de 18 anos nos ha proporcionado datos personales sin el consentimiento verificable de sus padres o tutores legales, procederemos a eliminar dichos datos de manera inmediata.",
        "Si eres padre, madre o tutor legal y crees que tu hijo o pupilo nos ha proporcionado datos personales, contactanos a privacidad@dadacode.io para que podamos proceder a su eliminacion.",

        "---",
        "## 12. Cambios en esta Politica",
        "Da&amp;Da Solutions se reserva el derecho de modificar esta Politica de Privacidad en cualquier momento para adaptarla a novedades legislativas, cambios en nuestras practicas de tratamiento de datos, nuevos servicios incorporados, o cualquier otro motivo justificado. Toda modificacion sustancial sera notificada a los usuarios con al menos 30 dias de antelacion mediante correo electronico al correo registrado y aviso destacado en la plataforma.",
        "Si el usuario continua utilizando nuestros servicios despues de la entrada en vigor de la nueva version de la politica, se considerara que ha aceptado los cambios. La version actualizada siempre estara disponible en dadacode.io/privacidad. Conservamos un archivo historico de todas las versiones anteriores, disponible bajo solicitud a privacidad@dadacode.io.",

        "---",
        "## 13. Contacto y Consultas de Privacidad",
        "Para cualquier consulta, ejercicio de derechos o reclamacion relacionada con el tratamiento de datos personales, podes ponerte en contacto con nosotros a traves de:",
        "- <b>Correo electronico del equipo de Privacidad:</b> privacidad@dadacode.io (tiempo de respuesta: 5 dias habiles).",
        "- <b>Correo electronico del DPO:</b> dpo@dadacode.io (para escaladas y consultas complejas).",
        "- <b>Formulario en linea:</b> dadacode.io/privacidad/contacto",
        "- <b>Correo postal:</b> Da&amp;Da Solutions S.A. — Atencion: Delegado de Proteccion de Datos — Av. Corrientes 3456, Piso 12, CABA, Argentina (C1193AAQ).",
        "Nos comprometemos a responder a todas las consultas de privacidad en un plazo maximo de 5 dias habiles desde su recepcion, salvo que la complejidad de la consulta requiera mayor tiempo, en cuyo caso te informaremos de los plazos estimados.",
    ]
))

# ==============================================================
# 3. PLANES Y PRECIOS
# ==============================================================
DOCS.append(dict(
    filename="planes_precios.pdf",
    title="Planes y Precios",
    subtitle="Guia completa de suscripciones, capacidades y condiciones comerciales — 2026",
    doc_type="Documento Publico — Comercial",
    blocks=[
        "## 1. Introduccion a los Planes de Da&Da Solutions",
        "Da&amp;Da Solutions disena sus planes de suscripcion para adaptarse a la realidad de cada organizacion, desde equipos de cinco personas que estan digitalizando su primer proceso hasta corporaciones con miles de usuarios concurrentes que necesitan garantias de disponibilidad de nivel bancario. No creemos en el modelo 'talla unica': cada empresa tiene su propio ritmo de crecimiento, sus propias necesidades de seguridad y su propio presupuesto.",
        "En 2026 relanzamos nuestra estructura de planes con un enfoque renovado en transparencia de precios, modularidad y escalabilidad sin fricciones. Esta guia describe en detalle las caracteristicas, limites, precios y condiciones de cada plan disponible a partir del 1 de enero de 2026.",
        "Todos los planes incluyen un periodo de prueba gratuito de 14 dias sin necesidad de ingresar datos de tarjeta de credito. Al finalizar el periodo de prueba, el cliente elige el plan que mejor se adapta a sus necesidades y el sistema migra automaticamente todos los datos y configuraciones sin interrupcion del servicio.",
        "Los precios se expresan en dolares estadounidenses (USD). Para clientes en Argentina, los precios se facturan al tipo de cambio oficial vendedor del Banco Nacion del dia de emision de la factura, con IVA del 21% incluido. Para clientes en otras jurisdicciones, los impuestos locales se calculan al momento de facturacion segun la normativa vigente.",

        "---",
        "## 2. Plan Starter — USD 99/mes (facturacion anual)",

        "### 2.1 Descripcion General",
        "El Plan Starter esta disenado para equipos pequenos, microempresas, estudios profesionales, y organizaciones que estan comenzando su proceso de transformacion digital. Incluye todo lo necesario para digitalizar procesos esenciales, gestionar proyectos basicos y acceder a nuestra plataforma de manera profesional, con la tranquilidad de saber que pueden escalar al plan siguiente en cualquier momento sin interrupcion del servicio ni perdida de datos.",

        "### 2.2 Caracteristicas Incluidas en el Plan Starter",
        "- <b>Usuarios:</b> hasta 5 usuarios activos incluidos.",
        "- <b>Usuarios adicionales:</b> USD 18/usuario/mes.",
        "- <b>Proyectos:</b> hasta 10 proyectos activos simultaneos.",
        "- <b>Almacenamiento:</b> 25 GB de almacenamiento en la nube para archivos, documentos, imagenes y assets.",
        "- <b>API REST:</b> acceso con limite de 10.000 llamadas/mes y rate limit de 10 requests/segundo.",
        "- <b>Soporte:</b> soporte por email con SLA de 4 horas habiles, acceso completo a la base de conocimiento en docs.dadacode.io, y acceso al foro de la comunidad.",
        "- <b>Uptime SLA:</b> 99.5% mensual.",
        "- <b>Seguridad:</b> autenticacion con usuario y contrasena, 2FA obligatorio via TOTP (Google Authenticator, Authy), cifrado TLS en transito y AES-256 en reposo.",
        "- <b>Integraciones nativas:</b> hasta 5 integraciones activas simultaneamente del marketplace de integraciones.",
        "- <b>Reportes:</b> acceso a los 15 reportes predefinidos del catalogo basico, exportacion en formato CSV.",
        "- <b>Backups:</b> backup diario automatico con retencion de 7 dias.",
        "- <b>Entornos:</b> 1 entorno de produccion incluido.",
        "- <b>Notificaciones:</b> notificaciones por email y dentro de la aplicacion.",

        "### 2.3 Limitaciones del Plan Starter",
        "Las siguientes caracteristicas no estan disponibles en el Plan Starter y requieren actualizar a un plan superior:",
        "- Acceso a la API GraphQL.",
        "- Funciones de inteligencia artificial y machine learning.",
        "- Single Sign-On (SSO) empresarial con SAML 2.0 u OIDC.",
        "- Audit logs y registros de actividad extendidos.",
        "- Soporte en tiempo real (chat en vivo o telefono).",
        "- Ambiente de staging o sandbox separado.",
        "- Constructor de reportes personalizado.",
        "- Webhooks salientes configurables.",
        "- Acceso a la API de administracion.",

        "### 2.4 Para quien es el Plan Starter",
        "Ideal para: estudios contables, juridicos y de diseno con hasta 5 profesionales; agencias de marketing o publicidad pequenas; startups en etapa pre-seed; equipos de innovacion dentro de empresas que necesitan un espacio de trabajo separado; organizaciones sin fines de lucro (aplica descuento adicional, ver seccion 9).",

        "---",
        "## 3. Plan Professional — USD 349/mes (facturacion anual)",

        "### 3.1 Descripcion General",
        "El Plan Professional es nuestro plan mas popular y el punto de entrada recomendado para empresas en crecimiento. Esta disenado para equipos de entre 5 y 25 personas que necesitan mayor capacidad, funcionalidades avanzadas y niveles de soporte superiores. Incluye acceso a la totalidad de las funcionalidades de la plataforma base, con la excepcion de las capacidades de infraestructura dedicada reservadas para planes superiores.",

        "### 3.2 Caracteristicas Incluidas en el Plan Professional",
        "- <b>Usuarios:</b> hasta 25 usuarios activos incluidos.",
        "- <b>Usuarios adicionales:</b> USD 13/usuario/mes (o USD 60/bloque de 5 usuarios/mes).",
        "- <b>Proyectos:</b> ilimitados.",
        "- <b>Almacenamiento:</b> 200 GB incluidos, ampliable a USD 0.08/GB adicional/mes.",
        "- <b>API:</b> acceso completo a la API REST v3 y GraphQL v2. Limite de 500.000 llamadas/mes. Rate limit de 100 req/seg. Sin limite de webhooks configurables.",
        "- <b>Soporte:</b> email con SLA de 2 horas habiles, chat en vivo de lunes a viernes de 8:00 a 20:00 hs GMT-3 (tiempo de espera promedio: menos de 2 minutos).",
        "- <b>Uptime SLA:</b> 99.9% mensual.",
        "- <b>Seguridad:</b> todo lo del Starter mas SSO con SAML 2.0 y OIDC, RBAC con roles predefinidos y personalizados, politica de contrasenas configurable.",
        "- <b>Integraciones:</b> integraciones nativas ilimitadas. Acceso completo al marketplace con mas de 150 conectores disponibles.",
        "- <b>Reportes:</b> constructor de reportes personalizado drag-and-drop, mas de 50 visualizaciones distintas, exportacion en CSV, Excel, PDF y PNG. Programacion de reportes automaticos.",
        "- <b>Backups:</b> backup diario con retencion de 30 dias, backup semanal con retencion de 6 meses, backup mensual con retencion de 1 ano.",
        "- <b>Entornos:</b> 1 entorno de produccion + 1 entorno de staging incluido.",
        "- <b>Sandbox de desarrollo:</b> incluido con reset diario automatico.",
        "- <b>Inteligencia Artificial:</b> acceso al modulo de IA basico: busqueda semantica en documentos, generacion de reportes en lenguaje natural (en espanol e ingles), clasificacion automatica de datos con modelos preentrenados, deteccion de anomalias en series de tiempo.",
        "- <b>Audit Logs:</b> registro de actividad de usuarios con retencion de 90 dias. Filtros por usuario, accion, recurso y rango de fechas.",
        "- <b>Notificaciones:</b> email, in-app, Slack, Microsoft Teams, y webhooks personalizados.",
        "- <b>Feature Requests:</b> acceso al portal de roadmap publico con capacidad de votar y agregar solicitudes.",

        "### 3.3 Add-ons Disponibles para el Plan Professional",
        "Podes extender las capacidades del Plan Professional con los siguientes complementos:",
        "- <b>Modulo de IA Avanzada:</b> USD 180/mes. Incluye analisis predictivo, NLP avanzado con modelos propios, computer vision basico, y entrenamiento de modelos sobre datos del cliente.",
        "- <b>Soporte 24/7:</b> USD 300/mes. Extiende la cobertura de soporte por email y chat a los 7 dias, las 24 horas.",
        "- <b>Ambiente de produccion adicional:</b> USD 250/mes por ambiente adicional.",
        "- <b>Retencion extendida de Audit Logs:</b> USD 60/mes por 6 meses adicionales de retencion.",
        "- <b>Capacitacion a medida (sesion de 2 horas):</b> USD 350 por sesion, dictada por un instructor certificado de Da&amp;Da Solutions.",

        "---",
        "## 4. Plan Business — USD 999/mes (facturacion anual)",

        "### 4.1 Descripcion General",
        "El Plan Business esta disenado para organizaciones medianas a grandes con equipos de entre 25 y 100 personas, que necesitan capacidad extendida, herramientas de administracion corporativa, funcionalidades avanzadas de seguridad y compliance, y un nivel de acompanamiento proactivo. Ofrece un salto cualitativo en capacidades de inteligencia artificial, gobernanza de datos y controles de seguridad.",

        "### 4.2 Caracteristicas Incluidas en el Plan Business",
        "- <b>Usuarios:</b> hasta 100 usuarios activos incluidos.",
        "- <b>Usuarios adicionales:</b> USD 9/usuario/mes.",
        "- <b>Proyectos y almacenamiento:</b> ilimitados.",
        "- <b>API:</b> llamadas ilimitadas sin costo adicional. Rate limit de 500 req/seg. Prioridad en colas de procesamiento asincronico.",
        "- <b>Soporte:</b> email 24/7, chat en vivo 24/5, telefono en horario habil (9:00-18:00 GMT-3, lunes a viernes). Technical Account Manager (TAM) dedicado con reunion mensual de revision.",
        "- <b>Uptime SLA:</b> 99.95% mensual.",
        "- <b>Seguridad:</b> todo lo del Professional mas: gestion centralizada de politicas de seguridad para toda la organizacion, integracion con SIEM externo (Splunk, Datadog, IBM QRadar), escaneo de vulnerabilidades en pipelines CI/CD, gestion de dispositivos para aplicacion movil (MDM integration), y restricciones de acceso por IP y por horario.",
        "- <b>Entornos:</b> produccion + staging + testing + 1 ambiente adicional a eleccion (QA, pre-produccion, demos).",
        "- <b>Inteligencia Artificial:</b> acceso completo a todos los modulos de IA de Da&amp;Da Solutions, incluyendo modelos personalizados entrenados sobre datos propios del cliente, pipelines de NLP con soporte multilingue (espanol, ingles, portugues, frances), analisis de sentimientos, extraccion de entidades, y API de prediccion de demanda.",
        "- <b>Audit Logs:</b> retencion de 12 meses. Exportacion en tiempo real a sistemas externos via webhook o streaming a S3/BigQuery/Datadog. Alertas configurables por patron de actividad sospechosa.",
        "- <b>Administracion avanzada:</b> gestion de politicas de contrasenas granulares, configuracion de sesiones (duracion, timeout, sesiones concurrentes), restriccion de dispositivos autorizados, flujos de aprobacion para acciones criticas.",
        "- <b>Compliance:</b> reportes de cumplimiento preconfigurados para SOC 2, ISO 27001, GDPR y LGPD. Evidencia exportable para auditorias externas.",
        "- <b>Data Governance:</b> modulo de clasificacion y etiquetado de datos segun sensibilidad, lineage de datos para trazabilidad, gestion de periodos de retencion por tipo de dato, y control de acceso a nivel de campo en registros.",

        "### 4.3 Add-ons Disponibles para el Plan Business",
        "- <b>Infraestructura en region dedicada:</b> USD 900/mes. Tu instancia en una region AWS a eleccion sin compartir recursos de computo ni red con otros clientes.",
        "- <b>Integracion con Active Directory / LDAP:</b> USD 250/mes. Sincronizacion bidireccional de usuarios y grupos.",
        "- <b>Modulo de Disaster Recovery activo-activo:</b> USD 1.400/mes. Replicacion en tiempo real en dos regiones con failover automatico.",
        "- <b>Revision de seguridad anual:</b> USD 3.500 por revision. Incluye pen testing de caja gris y entrega de reporte ejecutivo con plan de remediacion.",

        "---",
        "## 5. Plan Enterprise — Precio a convenir",

        "### 5.1 Descripcion General",
        "El Plan Enterprise es nuestra oferta premium para grandes corporaciones, instituciones financieras, organismos de salud, entidades gubernamentales, y cualquier organizacion que requiera: infraestructura completamente dedicada, SLAs de disponibilidad de hasta 99.99%, personalizacion profunda de la plataforma, y un nivel de acompanamiento que va mucho mas alla del soporte estandar.",
        "No existe un precio fijo para el Plan Enterprise: cada contrato es el resultado de un proceso de descubrimiento con el equipo tecnico y comercial de Da&amp;Da Solutions para disenar la solucion exacta que necesita cada cliente. Los contratos Enterprise tipicamente tienen una duracion de 1 a 3 anos con condiciones comerciales mejoradas por volumen y compromiso.",

        "### 5.2 Capacidades Exclusivas del Plan Enterprise",
        "- <b>Usuarios:</b> ilimitados sin costo por usuario.",
        "- <b>Infraestructura dedicada:</b> instancia exclusiva con recursos de computo, memoria, red y almacenamiento no compartidos con ningun otro cliente. Opcion de cloud privada en las instalaciones del cliente (on-premise) o cloud privada gestionada por Da&amp;Da Solutions en AWS/Azure/GCP.",
        "- <b>Multi-region activo-activo:</b> arquitectura de alta disponibilidad con failover automatico entre multiples regiones geograficas. RTO (Recovery Time Objective) menor a 1 minuto. RPO (Recovery Point Objective) menor a 30 segundos.",
        "- <b>SLA personalizado:</b> hasta 99.99% de uptime mensual garantizado contractualmente. Creditos de servicio automaticos en caso de incumplimiento. Penalidades adicionales por incumplimientos graves segun contrato.",
        "- <b>Soporte 24/7/365:</b> linea telefonica directa exclusiva, Slack Connect con tiempo de respuesta garantizado de 15 minutos para incidentes criticos, Microsoft Teams integrado, y canal de escalada directo al VP de Ingenieria.",
        "- <b>Customer Success Manager (CSM) dedicado:</b> punto de contacto unico para todo lo relacionado con la relacion comercial, satisfaccion, renovacion, y expansion. Reunion semanal o quincenal segun necesidad.",
        "- <b>Technical Account Manager (TAM) dedicado:</b> ingeniero senior de Da&amp;Da asignado exclusivamente al cliente para revisiones de arquitectura, optimizacion de rendimiento, revision de roadmaps de upgrade, y planificacion tecnica de largo plazo.",
        "- <b>Revisiones de seguridad trimestrales:</b> pen testing, revision de arquitectura de seguridad, simulacros de DR, y entrega de reporte ejecutivo con plan de remediacion.",
        "- <b>Desarrollo personalizado incluido:</b> hasta 40 horas/mes de desarrollo de funcionalidades o integraciones a medida, ejecutadas por el equipo de Da&amp;Da Solutions bajo los procesos de desarrollo del cliente.",
        "- <b>Acceso a codigo fuente:</b> disponible bajo contrato de escrow de codigo fuente con un tercero de confianza para garantizar la continuidad operativa del cliente ante cualquier eventualidad.",
        "- <b>Onboarding ejecutivo:</b> programa de onboarding de 3 meses con un equipo dedicado, incluyendo migracion de datos de sistemas legacy, integracion con todos los sistemas existentes, y capacitacion certificada del equipo tecnico del cliente.",
        "- <b>SLAs de seguridad:</b> tiempo maximo de respuesta ante vulnerabilidades criticas (CVSS >= 9.0): 24 horas. Tiempo maximo de respuesta ante vulnerabilidades altas (CVSS 7.0-8.9): 7 dias.",

        "### 5.3 Proceso de Contratacion Enterprise",
        "El proceso tipico de contratacion Enterprise sigue estos pasos:",
        "- <b>Paso 1 — Discovery Call (60 min):</b> reunion inicial con el equipo de soluciones para entender necesidades, casos de uso, volumen de datos, requisitos de seguridad, compliance, y restricciones de infraestructura.",
        "- <b>Paso 2 — Propuesta Tecnica (5-7 dias habiles):</b> elaboracion de una propuesta de arquitectura personalizada que cubre: topologia de infraestructura, plan de migracion, matriz de integraciones, plan de seguridad, y hoja de ruta de implementacion.",
        "- <b>Paso 3 — Propuesta Comercial:</b> presentacion de la propuesta economica con todas las opciones de configuracion, condiciones de pago y descuentos aplicables por volumen y compromiso.",
        "- <b>Paso 4 — Prueba de Concepto (POC, opcional, 30 dias):</b> implementacion de un piloto en un entorno controlado para validar la arquitectura y las integraciones clave antes de la firma del contrato.",
        "- <b>Paso 5 — Revision Legal y Firma:</b> revision del contrato por los equipos legales de ambas partes, negociacion de clausulas especificas, firma y kick-off del proyecto.",
        "Para iniciar el proceso, contacta al equipo de ventas Enterprise en enterprise@dadacode.io o completa el formulario en dadacode.io/enterprise.",

        "---",
        "## 6. Managed Services — desde USD 2.500/mes",

        "### 6.1 Que son los Managed Services",
        "El modelo de Managed Services (Servicios Gestionados) es diferente a la suscripcion de plataforma: en lugar de solo proveer el software, Da&amp;Da Solutions asume la operacion, el mantenimiento y la evolucion continua de los sistemas del cliente. Da&amp;Da actua como el departamento de tecnologia externo o como extension dedicada del equipo tecnico interno.",
        "Este modelo es ideal para empresas que quieren aprovechar tecnologia de punta sin necesidad de construir y mantener un equipo tecnico propio, o para empresas que tienen un equipo pero necesitan escalar capacidad en areas especificas como seguridad, DevOps, o desarrollo de funcionalidades.",

        "### 6.2 Modalidades de Managed Services",
        "- <b>MSP-OPS — Operaciones Gestionadas (desde USD 2.500/mes):</b> monitoreo 24/7 de infraestructura y aplicaciones, gestion de incidentes con SLA garantizado, aplicacion proactiva de parches de seguridad, gestion de backups y validacion de recuperacion, optimizacion continua de rendimiento y costos de infraestructura.",
        "- <b>MSP-DEV — Evolucion Continua (desde USD 5.000/mes):</b> todo lo de MSP-OPS mas un squad de desarrollo asignado (tipicamente 2 backend, 1 frontend, 1 QA) para evolucion funcional del sistema. Sprints quincenales con demos al cliente. Entrega continua (CI/CD). Hasta 80 story points de trabajo de desarrollo por mes segun estimacion.",
        "- <b>MSP-AI — Inteligencia Artificial Gestionada (desde USD 3.500/mes):</b> desarrollo, entrenamiento y operacion de modelos de IA/ML sobre los datos del cliente. Incluye: ingenieria de datos, feature engineering, entrenamiento y evaluacion de modelos, deployment a produccion con monitoreo de drift, y reentrenamiento periodico.",
        "- <b>MSP-TRANSFORM — Transformacion Digital (precio a convenir):</b> proyecto integral de transformacion tecnologica: auditoria del estado actual, diseno de arquitectura objetivo, roadmap de transformacion, migracion de sistemas legacy, modernizacion de procesos, y transferencia de conocimiento al equipo interno.",

        "---",
        "## 7. Comparativa Rapida de Planes",

        "### 7.1 Limites por Plan",
        "La siguiente tabla resume los limites principales de cada plan:",
        "- <b>Usuarios incluidos:</b> Starter: 5 | Professional: 25 | Business: 100 | Enterprise: Ilimitados.",
        "- <b>Almacenamiento:</b> Starter: 25 GB | Professional: 200 GB | Business: Ilimitado | Enterprise: Ilimitado.",
        "- <b>Proyectos:</b> Starter: 10 | Professional: Ilimitados | Business: Ilimitados | Enterprise: Ilimitados.",
        "- <b>Llamadas API/mes:</b> Starter: 10.000 | Professional: 500.000 | Business: Ilimitadas | Enterprise: Ilimitadas.",
        "- <b>Rate limit API (req/seg):</b> Starter: 10 | Professional: 100 | Business: 500 | Enterprise: personalizado.",
        "- <b>Entornos:</b> Starter: 1 prod | Professional: prod + staging | Business: prod + staging + testing + 1 extra | Enterprise: personalizado.",
        "- <b>Uptime SLA:</b> Starter: 99.5% | Professional: 99.9% | Business: 99.95% | Enterprise: hasta 99.99%.",
        "- <b>Soporte:</b> Starter: email | Professional: email + chat | Business: email + chat + telefono + TAM | Enterprise: 24/7 con linea directa.",
        "- <b>Retencion de backups:</b> Starter: 7 dias | Professional: 1 ano | Business: 3 anos | Enterprise: segun contrato.",

        "---",
        "## 8. Condiciones Comerciales",

        "### 8.1 Ciclos de Facturacion",
        "- <b>Mensual:</b> disponible para Starter y Professional. Precio con recargo del 20% sobre el precio anual equivalente.",
        "- <b>Anual:</b> precio base sin recargo. Facturacion al inicio del periodo anual por el total del ano.",
        "- <b>Anual con pago en cuotas:</b> disponible para planes Business y Enterprise. Posibilidad de fraccionar el pago anual en 12 cuotas mensuales sin recargo adicional (requiere domiciliacion bancaria o autorizacion de debito automatico).",
        "- <b>Multi-ano:</b> 5% de descuento adicional por contrato de 2 anos, 10% por contrato de 3 anos. Disponible para todos los planes.",

        "### 8.2 Politica de Periodo de Prueba Gratuita",
        "El periodo de prueba gratuita de 14 dias aplica a los planes Starter, Professional y Business. Durante este periodo: no se requiere tarjeta de credito, hay acceso completo a todas las funcionalidades del plan elegido, hay hasta 5 usuarios de prueba sin importar el plan seleccionado, 5 GB de almacenamiento de prueba, y soporte por email incluido sin SLA garantizado.",
        "Al finalizar los 14 dias, si no se ingresa informacion de pago, la cuenta entra en modo 'solo lectura' por 7 dias adicionales. Transcurridos esos 7 dias, la cuenta se suspende. Los datos se conservan por 30 dias adicionales despues de la suspension antes de ser eliminados permanentemente.",

        "### 8.3 Politica de Upgrades y Downgrades",
        "- <b>Upgrade (de plan inferior a superior):</b> efectivo inmediatamente. Se cobra la diferencia proporcional al tiempo restante del periodo de facturacion actual.",
        "- <b>Downgrade (de plan superior a inferior):</b> efectivo al inicio del siguiente periodo de facturacion. No se realizan reembolsos por el periodo en curso. Los datos que excedan los limites del nuevo plan deben ser gestionados antes del inicio del nuevo periodo.",
        "- <b>Cancelacion de plan mensual:</b> efectiva al final del mes en curso. Sin reembolso proporcional.",
        "- <b>Cancelacion de plan anual:</b> segun condiciones del contrato firmado. Generalmente se aplica una penalidad equivalente al 20% del valor restante del contrato.",

        "### 8.4 Descuentos y Condiciones Especiales",
        "Da&amp;Da Solutions ofrece condiciones preferenciales para las siguientes categorias:",
        "- <b>Organizaciones sin fines de lucro:</b> 30% de descuento en planes Starter y Professional, previa presentacion de documentacion que acredite la personeria juridica sin fines de lucro.",
        "- <b>Instituciones educativas:</b> 40% de descuento en todos los planes, con condicion de uso exclusivo para fines academicos y de investigacion no comercial.",
        "- <b>Startups con menos de 2 anos de constitucion:</b> programa Da&amp;Da Launchpad con 50% de descuento el primer ano y 25% el segundo, sujeto a verificacion de antiguedad y facturacion.",
        "- <b>Pago anual adelantado en un solo pago:</b> 2 meses bonificados (equivalente al 16.7% de descuento respecto al precio mensual).",
        "- <b>Programa de referidos:</b> por cada nuevo cliente que contrate cualquier plan pagado a partir de tu referencia, recibis un credito de USD 250 en tu proxima factura, sin limite de referidos.",
        "- <b>Contratos multi-ano:</b> 5% adicional por contrato de 2 anos, 10% adicional por contrato de 3 anos.",
        "[NOTE] Los descuentos de categoria (ONG, educacion, startup) no son acumulables entre si ni con el descuento de pago anual. El descuento de pago anual si puede combinarse con el descuento de contrato multi-ano.",

        "---",
        "## 9. Infraestructura y Tecnologia",

        "### 9.1 Arquitectura de la Plataforma",
        "Da&amp;Da Solutions opera sobre una arquitectura de microservicios desplegada en Amazon Web Services (AWS), disenada para alta disponibilidad, escalabilidad horizontal automatica, y recuperacion ante desastres:",
        "- <b>Region principal:</b> us-east-1 (Virginia del Norte, EE. UU.).",
        "- <b>Region secundaria LATAM:</b> sa-east-1 (Sao Paulo, Brasil), disponible como region principal para clientes con requisitos de residencia de datos en America Latina.",
        "- <b>CDN global:</b> Amazon CloudFront con mas de 450 puntos de presencia en 90 paises, garantizando latencia baja para usuarios en cualquier parte del mundo.",
        "- <b>Bases de datos:</b> Amazon RDS Aurora PostgreSQL para datos transaccionales, Amazon DynamoDB para datos de alta velocidad, Amazon ElastiCache (Redis 7) para cache distribuido.",
        "- <b>Mensajeria y eventos:</b> Amazon SQS para colas de mensajes, Amazon Kinesis para streaming de eventos en tiempo real.",
        "- <b>Contenedores y orquestacion:</b> Amazon EKS (Kubernetes 1.29) con auto-scaling horizontal (HPA) y vertical (VPA) configurados.",
        "- <b>Observabilidad:</b> Datadog para metricas, logs y traces. PagerDuty para alertas y on-call. Incident.io para gestion de incidentes.",

        "### 9.2 Ventanas de Mantenimiento Programado",
        "Da&amp;Da Solutions realiza mantenimientos programados para aplicar actualizaciones de seguridad, mejoras de rendimiento y nuevas versiones de la plataforma. La politica de ventanas de mantenimiento es:",
        "- <b>Mantenimiento rutinario (zero-downtime):</b> domingos de 2:00 a 4:00 hs GMT-3. Implementado mediante despliegues blue/green o canary sin interrupcion del servicio.",
        "- <b>Mantenimiento mayor (posible downtime < 30 min):</b> se comunica con al menos 7 dias habiles de anticipacion por email y en status.dadacode.io. El downtime de mantenimiento mayor programado no se computa en el SLA.",
        "Toda ventana de mantenimiento (rutinaria o mayor) se publica previamente en status.dadacode.io y se notifica por email a los contactos tecnicos registrados. Los clientes Enterprise pueden negociar ventanas de mantenimiento alternativas que no afecten sus horarios de mayor actividad.",

        "### 9.3 Disaster Recovery y Continuidad del Negocio",
        "Da&amp;Da Solutions cuenta con un plan de recuperacion ante desastres (DRP) documentado y probado semestralmente:",
        "- <b>RTO (Recovery Time Objective):</b> 4 horas para planes Starter y Professional, 1 hora para Business, menos de 15 minutos para Enterprise con multi-region.",
        "- <b>RPO (Recovery Point Objective):</b> 24 horas para Starter, 4 horas para Professional, 1 hora para Business, menos de 30 segundos para Enterprise con replicacion en tiempo real.",
        "- <b>Simulacros de DR:</b> realizados semestralmente con participacion del equipo de operaciones y documentacion de resultados. Los clientes Enterprise pueden solicitar participar como observadores en los simulacros.",
        "- <b>Certificacion de continuidad:</b> Da&amp;Da Solutions mantiene un Business Continuity Plan (BCP) alineado con los requisitos de ISO/IEC 22301.",

        "---",
        "## 10. Onboarding y Soporte Post-Venta",
        "Todos los planes de Da&amp;Da Solutions incluyen soporte de migracion e incorporacion. El alcance varia segun el plan:",
        "- <b>Starter:</b> guia de migracion en la documentacion oficial, herramientas de importacion estandar (CSV, JSON, XML), y soporte por email para consultas durante las primeras 2 semanas.",
        "- <b>Professional:</b> sesion de onboarding guiado de hasta 4 horas con un especialista de Da&amp;Da Solutions, asistencia en la configuracion inicial de la plataforma, SSO y primeras integraciones.",
        "- <b>Business:</b> proyecto de onboarding de hasta 20 horas con un equipo tecnico dedicado: diseno de arquitectura de uso, configuracion de entornos, migracion de datos, integraciones principales, y capacitacion del equipo administrador.",
        "- <b>Enterprise:</b> programa de onboarding ejecutivo de 3 meses con equipo dedicado: migracion de datos de sistemas legacy, integracion con todos los sistemas existentes, configuracion de seguridad y compliance, y capacitacion certificada del equipo tecnico del cliente.",
        "Para clientes que migran desde plataformas competidoras, Da&amp;Da Solutions ofrece el servicio 'Competitive Migration' con herramientas especificas para las 15 plataformas mas comunes del mercado y asistencia dedicada sin costo adicional en planes Business y Enterprise.",
    ]
))

# ==============================================================
# 4. TERMINOS DE USO
# ==============================================================
DOCS.append(dict(
    filename="terminos_uso.pdf",
    title="Terminos y Condiciones de Uso",
    subtitle="Acuerdo legal que rige el acceso y uso de los servicios de Da&amp;Da Solutions — Version 5.0 — 1 de enero de 2026",
    doc_type="Documento Legal — Uso Publico",
    blocks=[
        "## 1. Aceptacion de los Terminos",
        "Los presentes Terminos y Condiciones de Uso (en adelante, 'Terminos', 'TyC' o 'el Acuerdo') constituyen un contrato legalmente vinculante entre usted (en adelante, 'el Usuario', 'usted' o 'su organizacion') y Da&amp;Da Solutions S.A. (en adelante, 'Da&amp;Da Solutions', 'la Empresa', 'nosotros' o 'nuestro'), con domicilio legal en Av. Corrientes 3456, Piso 12, Ciudad Autonoma de Buenos Aires, Argentina, CUIT 30-71234567-8.",
        "Al acceder, registrarse, instalar o utilizar cualquiera de los servicios, aplicaciones, plataformas, APIs, SDKs o sitios web operados por Da&amp;Da Solutions (colectivamente, 'los Servicios'), el Usuario declara haber leido integra y comprensivamente los presentes Terminos y haberlos aceptado de forma expresa e incondicional.",
        "Si el Usuario actua en representacion de una persona juridica (empresa, organizacion, entidad publica o privada), declara y garantiza tener las facultades y autorizaciones legalmente necesarias para vincular a dicha entidad a los presentes Terminos y Condiciones. La persona que acepta los Terminos en nombre de una organizacion asume responsabilidad personal solidaria por el cumplimiento de dichos terminos.",
        "La utilizacion de los Servicios por parte de menores de 18 anos no esta permitida bajo ninguna circunstancia. Al aceptar estos Terminos, el Usuario declara ser mayor de 18 anos y tener plena capacidad juridica para contratar.",
        "Si el Usuario no acepta alguno de los terminos establecidos en este documento, debera abstenerse de acceder o utilizar los Servicios, y contactar a Da&amp;Da Solutions para que proceda a la eliminacion de cualquier cuenta, datos o informacion que pudiera haber sido creada.",

        "---",
        "## 2. Definiciones",
        "Para los efectos de los presentes Terminos, los siguientes terminos tendran el significado que se indica a continuacion:",
        "- <b>Cuenta:</b> el perfil de acceso unico creado por el Usuario al registrarse en la plataforma de Da&amp;Da Solutions, compuesto por credenciales de autenticacion y configuracion personalizada.",
        "- <b>Contenido del Usuario:</b> cualquier dato, informacion, archivo, documento, codigo, imagen, video, audio, o material de cualquier tipo que el Usuario cargue, transmita, publique, procese o almacene a traves de los Servicios.",
        "- <b>Datos de la Cuenta:</b> la informacion de identificacion, configuracion y contacto del Usuario y su organizacion.",
        "- <b>Servicios:</b> la totalidad de las plataformas, aplicaciones web y moviles, APIs, SDKs, documentacion, herramientas, integraciones y funcionalidades ofrecidas por Da&amp;Da Solutions.",
        "- <b>Plan de Suscripcion:</b> el nivel de servicio contratado por el Usuario segun las condiciones descritas en la guia de Planes y Precios vigente.",
        "- <b>Datos Personales:</b> cualquier informacion que permita identificar directa o indirectamente a una persona fisica, segun lo definido en la Politica de Privacidad.",
        "- <b>Incidente de Seguridad:</b> cualquier acceso no autorizado, perdida, destruccion, alteracion o divulgacion no autorizada de datos almacenados o procesados en los Servicios.",
        "- <b>Tercero:</b> cualquier persona fisica o juridica que no sea Da&amp;Da Solutions ni el Usuario.",
        "- <b>SLA:</b> Service Level Agreement, el acuerdo de nivel de servicio que establece los compromisos de disponibilidad y tiempo de respuesta de Da&amp;Da Solutions.",
        "- <b>Fuerza Mayor:</b> todo evento extraordinario, imprevisible e irresistible ajeno a la voluntad de las partes, incluyendo pero no limitado a: catastrofes naturales, pandemia declarada por la OMS, conflictos armados o actos de terrorismo, fallos masivos de infraestructura de Internet a nivel regional o global, cortes de electricidad masivos, o actos de autoridad gubernamental que afecten directamente la prestacion del servicio.",
        "- <b>Propiedad Intelectual:</b> todos los derechos de propiedad intelectual e industrial, incluyendo derechos de autor, marcas comerciales, patentes, know-how, secretos comerciales, y cualesquiera otros derechos de naturaleza analoga reconocidos por la legislacion aplicable.",

        "---",
        "## 3. Registro de Cuenta y Responsabilidades del Usuario",

        "### 3.1 Creacion y Veracidad de la Cuenta",
        "Para acceder a los Servicios de Da&amp;Da Solutions, el Usuario debe crear una Cuenta proporcionando informacion veraz, completa y actualizada en el formulario de registro. El Usuario es responsable de la exactitud y completitud de la informacion proporcionada y de mantenerla actualizada en todo momento. Da&amp;Da Solutions no asume responsabilidad alguna por los perjuicios derivados de informacion incorrecta, desactualizada o fraudulenta en la Cuenta.",
        "Da&amp;Da Solutions se reserva el derecho de verificar la identidad del Usuario y rechazar o cancelar el registro de cualquier cuenta que: proporcione informacion falsa o fraudulenta, viole los presentes Terminos o la normativa aplicable, represente un riesgo de seguridad para la plataforma o para otros usuarios, o sea creada con fines ilegitimos o contrarios a las buenas costumbres comerciales.",

        "### 3.2 Seguridad de las Credenciales de Acceso",
        "El Usuario es el unico y exclusivo responsable de mantener la confidencialidad y seguridad de todas sus credenciales de acceso, incluyendo: nombre de usuario o correo electronico, contrasena, tokens de API, tokens de acceso OAuth, claves privadas de certificados, y cualquier otro mecanismo de autenticacion.",
        "El Usuario se compromete expresamente a:",
        "- No compartir ni divulgar sus credenciales a ningun tercero, incluyendo otros empleados de la misma organizacion que no sean usuarios autorizados.",
        "- Utilizar contrasenas robustas que cumplan con la politica de seguridad de la plataforma.",
        "- Activar y mantener activa la autenticacion de dos factores (2FA), que es obligatoria para todos los planes.",
        "- Notificar inmediatamente a Da&amp;Da Solutions enviando un correo a security@dadacode.io ante cualquier sospecha de acceso no autorizado, compromiso de credenciales, o actividad sospechosa en la cuenta.",
        "- Cerrar sesion al finalizar el uso de la plataforma, especialmente en dispositivos compartidos.",
        "Da&amp;Da Solutions no sera responsable de ninguna perdida o dano resultante del incumplimiento de estas obligaciones por parte del Usuario. Toda actividad realizada con las credenciales del Usuario se presumira realizada por el propio Usuario.",

        "### 3.3 Gestion de Usuarios de la Organizacion",
        "El titular de la Cuenta (Administrador) puede invitar a otros usuarios a formar parte de su organizacion. El Administrador asume plena responsabilidad por:",
        "- Asignar roles y permisos apropiados a cada usuario segun el principio de minimo privilegio.",
        "- Revocar el acceso de usuarios que ya no deban tenerlo (ex-empleados, contratistas que finalizaron su engagement, etc.) sin demora.",
        "- Garantizar que todos los usuarios de su organizacion conozcan, comprendan y cumplan los presentes Terminos y Condiciones.",
        "- Las acciones de todos los usuarios de su organizacion dentro de la plataforma, como si fueran acciones propias.",
        "Da&amp;Da Solutions puede suspender cuentas de usuarios individuales si detecta actividad que viola los presentes Terminos, sin necesidad de suspender la cuenta de la organizacion completa.",

        "---",
        "## 4. Uso Aceptable de los Servicios",

        "### 4.1 Usos Permitidos",
        "El Usuario tiene derecho a utilizar los Servicios de Da&amp;Da Solutions exclusivamente para los fines legitimos del negocio para los cuales fueron contratados, de acuerdo con el Plan de Suscripcion vigente y en conformidad con la normativa aplicable en la jurisdiccion del Usuario. El uso de los Servicios para cualquier actividad no contemplada en los presentes Terminos requiere autorizacion previa y por escrito de Da&amp;Da Solutions.",

        "### 4.2 Usos Expresamente Prohibidos",
        "Queda expresamente prohibido al Usuario, y a cualquier persona que acceda a los Servicios a traves de la Cuenta del Usuario:",
        "- Utilizar los Servicios para actividades ilegales, fraudulentas, o que violen derechos de terceros en cualquier jurisdiccion.",
        "- Distribuir, alojar o transmitir malware, spyware, ransomware, adware, keyloggers, o cualquier tipo de codigo malicioso a traves de los Servicios.",
        "- Realizar ataques de denegacion de servicio (DoS/DDoS), intentos de explotacion de vulnerabilidades (salvo dentro del programa de Bug Bounty formalmente autorizado), o cualquier tipo de ataque informatico.",
        "- Acceder, intentar acceder, o extraer datos de otros clientes o usuarios sin su autorizacion expresa.",
        "- Utilizar los Servicios para el envio masivo de comunicaciones no solicitadas (spam) o para practicas de marketing engananoso.",
        "- Realizar ingenieria inversa, desensamblar, descompilar, o intentar extraer el codigo fuente de los Servicios o cualquiera de sus componentes.",
        "- Revender, sublicenciar, redistribuir, prestar o alquilar los Servicios a terceros sin autorizacion expresa y por escrito de Da&amp;Da Solutions.",
        "- Utilizar los Servicios para procesar, almacenar o transmitir contenido ilegal, obsceno, difamatorio, que incite al odio, a la discriminacion o a la violencia, o que viole derechos de propiedad intelectual de terceros.",
        "- Sobrecargar intencionalmente la infraestructura de Da&amp;Da Solutions mas alla de los limites del Plan contratado mediante requests artificiales, bucles de carga, o cualquier otra tecnica de estres no autorizada.",
        "- Usar sistemas automatizados, bots o scrapers para acceder a la interfaz web de la plataforma de una manera que impacte negativamente el rendimiento del servicio para otros usuarios.",
        "- Eludir o intentar eludir cualquier mecanismo de seguridad, autenticacion, autorizacion, o limite de uso de los Servicios.",
        "- Falsificar la identidad de otra persona o entidad al utilizar los Servicios.",
        "[NOTE] Da&amp;Da Solutions se reserva el derecho de suspender o cancelar unilateralmente el acceso de cualquier Usuario que incurra en usos prohibidos, con o sin notificacion previa segun la gravedad del caso, y sin obligacion de reembolso de importes ya pagados.",

        "### 4.3 Cumplimiento Legal",
        "El Usuario es responsable de garantizar que su uso de los Servicios cumple con toda la normativa aplicable en su jurisdiccion, incluyendo: leyes de proteccion de datos personales, normativas sectoriales de su industria (regulacion financiera, normativa de salud, etc.), leyes de propiedad intelectual, normativas de exportacion y control de tecnologia, y leyes de competencia y comercio electronico.",
        "Da&amp;Da Solutions no asume responsabilidad por el incumplimiento por parte del Usuario de la normativa aplicable a su actividad especifica.",

        "---",
        "## 5. Propiedad Intelectual",

        "### 5.1 Propiedad de Da&Da Solutions",
        "Da&amp;Da Solutions es y permanecera siendo la unica y exclusiva titular de todos los derechos de Propiedad Intelectual relacionados con los Servicios, incluyendo sin limitacion: el codigo fuente y compilado de las plataformas, APIs, SDKs y herramientas; el diseno visual, la interfaz de usuario y la experiencia de usuario; la arquitectura del sistema, los algoritmos y modelos de inteligencia artificial; la documentacion tecnica y comercial; las bases de datos y su estructura; las marcas comerciales 'Da&amp;Da Solutions', 'Da&amp;Da Code', 'DaDaCode.io' y los logotipos asociados.",
        "Nada en los presentes Terminos se interpretara como una transferencia o cesion de derechos de Propiedad Intelectual de Da&amp;Da Solutions al Usuario. El acceso a los Servicios unicamente otorga al Usuario una licencia de uso limitada segun lo establecido en este documento.",

        "### 5.2 Licencia de Uso Otorgada al Usuario",
        "Sujeto al cumplimiento continuo de los presentes Terminos y al pago puntual de los importes correspondientes al Plan de Suscripcion vigente, Da&amp;Da Solutions otorga al Usuario una licencia de uso limitada, no exclusiva, intransferible, no sublicenciable y revocable para: acceder y utilizar los Servicios durante el periodo de suscripcion, integrar los Servicios con los sistemas del Usuario a traves de la API oficial de Da&amp;Da Solutions, utilizar los SDKs oficiales de Da&amp;Da Solutions unicamente en las aplicaciones del propio Usuario.",
        "Esta licencia NO incluye el derecho a: modificar, adaptar, traducir o crear obras derivadas de los Servicios o cualquiera de sus componentes; distribuir, hacer accesibles o prestar los Servicios a terceros no autorizados; usar las marcas comerciales o el nombre comercial de Da&amp;Da Solutions sin autorizacion escrita previa; o extraer o copiar sistematicamente datos o contenido de los Servicios fuera del uso normal contemplado en el Plan contratado.",

        "### 5.3 Contenido del Usuario y Licencia Limitada",
        "El Usuario conserva la plena titularidad sobre todo el Contenido del Usuario que cargue, transmita o procese a traves de los Servicios. Da&amp;Da Solutions no reivindica ninguna titularidad sobre el Contenido del Usuario.",
        "Al utilizar los Servicios, el Usuario otorga a Da&amp;Da Solutions una licencia de uso limitada, no exclusiva, mundial, royalty-free y sublicenciable unicamente a proveedores de servicios tecnicos, para: almacenar, reproducir, procesar, transmitir y mostrar el Contenido del Usuario exclusivamente en la medida necesaria para prestar los Servicios contratados, y para mantener, mejorar y proteger los Servicios.",
        "Esta licencia finaliza automaticamente cuando el Usuario elimina el Contenido especifico o cancela su suscripcion, sujeto a los plazos de conservacion legal aplicables.",

        "### 5.4 Retroalimentacion y Sugerencias",
        "Si el Usuario proporciona sugerencias, ideas, comentarios, propuestas de mejora, informes de error o cualquier otra retroalimentacion sobre los Servicios ('Feedback'), Da&amp;Da Solutions puede usar, reproducir, modificar y comercializar dicho Feedback sin restriccion y sin obligacion de pago o atribucion al Usuario. El Usuario renuncia a cualquier derecho de propiedad intelectual que pudiera tener sobre el Feedback.",

        "---",
        "## 6. Disponibilidad del Servicio y SLAs",

        "### 6.1 Compromiso de Disponibilidad",
        "Da&amp;Da Solutions se compromete a mantener los Servicios disponibles segun los niveles de servicio (SLAs) establecidos para cada Plan de Suscripcion, tal como se describe en la guia de Planes y Precios vigente. El porcentaje de disponibilidad se calcula mensualmente con la siguiente formula: Disponibilidad (%) = [(Minutos totales del mes - Minutos de downtime no planificado) / Minutos totales del mes] x 100.",
        "El calculo de disponibilidad excluye: periodos de mantenimiento programado comunicados con al menos 72 horas de anticipacion; interrupciones causadas por factores de Fuerza Mayor; interrupciones causadas por acciones u omisiones del propio Usuario o de terceros bajo su control; interrupciones por uso de los Servicios en exceso de los limites del Plan contratado; periodos de prueba gratuita y entornos de sandbox (sujetos a SLA reducido del 95%); y cualquier periodo en que el Usuario no hubiera reportado la interrupcion a traves de los canales oficiales de soporte.",

        "### 6.2 Creditos de Servicio por Incumplimiento de SLA",
        "Si en algun mes calendario el porcentaje de disponibilidad efectivo resulta inferior al comprometido en el Plan, el Usuario tendra derecho a creditos de servicio segun la siguiente escala:",
        "- <b>Disponibilidad entre el SLA comprometido y el 99%:</b> credito equivalente al 10% del valor proporcional mensual del plan.",
        "- <b>Disponibilidad entre el 95% y el 99%:</b> credito equivalente al 25% del valor proporcional mensual del plan.",
        "- <b>Disponibilidad por debajo del 95%:</b> credito equivalente al 50% del valor proporcional mensual del plan.",
        "Los creditos de SLA se aplican automaticamente en la siguiente factura del mes en que se produce el incumplimiento. Para reclamar creditos, el Usuario debe presentar una solicitud a soporte@dadacode.io dentro de los 30 dias siguientes al mes del incumplimiento, adjuntando evidencia del impacto. Los creditos no son acumulables mas alla del valor de la mensualidad del plan ni convertibles en dinero en efectivo.",

        "---",
        "## 7. Facturacion, Precios y Pagos",

        "### 7.1 Precios y Modificaciones",
        "Los precios de los Servicios son los que figuran en la guia de Planes y Precios vigente en el momento de la contratacion. Da&amp;Da Solutions se reserva el derecho de modificar los precios en cualquier momento, debiendo notificar al Usuario con al menos 60 dias de anticipacion por correo electronico y aviso en la plataforma. Las modificaciones de precios solo seran aplicables al inicio del siguiente periodo de facturacion posterior a la notificacion.",
        "Si el Usuario no acepta los nuevos precios, tiene derecho a cancelar su suscripcion antes del inicio del periodo en que los nuevos precios entren en vigor, sin penalidad adicional. La continuacion del uso de los Servicios despues de esa fecha implica la aceptacion tacita de los nuevos precios.",

        "### 7.2 Obligaciones Tributarias",
        "Los precios base indicados en la guia de Planes y Precios no incluyen impuestos, tasas o contribuciones, los cuales son adicionales segun la legislacion vigente en cada jurisdiccion. El Usuario es responsable de determinar y cumplir con sus obligaciones tributarias locales derivadas del uso de los Servicios.",
        "Para clientes con domicilio en Argentina: los precios expresados en USD se facturaran al tipo de cambio oficial vendedor del Banco Nacion Argentina del dia de emision de la factura. Se adicionara IVA del 21%, percepcion de IIBB si corresponde segun jurisdiccion, y cualquier otro tributo aplicable segun la actividad del cliente.",

        "### 7.3 Mora, Intereses y Consecuencias del Impago",
        "El incumplimiento en el pago de cualquier importe adeudado en la fecha de vencimiento da derecho a Da&amp;Da Solutions a aplicar automaticamente un interes punitorio del 2% mensual (no acumulativo) sobre el capital adeudado desde la fecha de vencimiento hasta la fecha de efectivo pago. Adicionalmente, Da&amp;Da Solutions podra: suspender el acceso a los Servicios tras 15 dias de atraso, previa notificacion con 48 horas de anticipacion; cancelar definitivamente el contrato y eliminar la cuenta tras 30 dias de atraso; y remitir la deuda a proceso de gestion de cobro extrajudicial o judicial, con todos los costos y costas a cargo del deudor.",

        "---",
        "## 8. Confidencialidad",

        "### 8.1 Definicion de Informacion Confidencial",
        "A los efectos de los presentes Terminos, se considera Informacion Confidencial toda informacion que una parte (parte divulgadora) proporcione a la otra (parte receptora) en el contexto de la relacion comercial y que: sea marcada o identificada expresamente como 'Confidencial', 'Propiedad Exclusiva', 'Secreto Comercial' o denominaciones analogas; o que por su naturaleza, el contexto de su divulgacion o su contenido sea razonablemente considerada confidencial por una persona razonable en el sector.",
        "Sin perjuicio de lo anterior, se considera siempre Informacion Confidencial de Da&amp;Da Solutions: el codigo fuente de los Servicios, la arquitectura tecnica, los algoritmos, los modelos de IA, la informacion financiera, los datos de clientes, y las estrategias de negocio y hoja de ruta de producto. Se considera siempre Informacion Confidencial del Usuario: el Contenido del Usuario, sus datos de negocio, sus datos de clientes, y su informacion financiera.",

        "### 8.2 Obligaciones de Confidencialidad",
        "Cada parte se compromete a: mantener en estricta confidencialidad la Informacion Confidencial de la otra parte durante la vigencia del Acuerdo y por un periodo de 3 anos adicionales tras su extincion; no divulgar la Informacion Confidencial a ningun tercero sin el consentimiento previo y por escrito de la parte divulgadora; utilizar la Informacion Confidencial unicamente para los fines previstos en el presente Acuerdo; restringir el acceso a la Informacion Confidencial unicamente al personal que necesite conocerla para el cumplimiento de sus funciones y que este sujeto a obligaciones de confidencialidad equivalentes; y adoptar medidas de proteccion equivalentes a las que aplica a su propia informacion confidencial y en ningun caso inferiores a las que un profesional diligente del sector aplicaria.",

        "### 8.3 Excepciones a las Obligaciones de Confidencialidad",
        "Las obligaciones de confidencialidad establecidas en esta seccion no aplican a informacion que: sea o pase a ser de dominio publico sin accion u omision de la parte receptora; sea ya conocida por la parte receptora con anterioridad a su divulgacion por la parte divulgadora, segun evidencia documentada preexistente; sea desarrollada de manera independiente por la parte receptora sin uso ni referencia de la Informacion Confidencial divulgada; o deba divulgarse por exigencia legal o de autoridad judicial o regulatoria competente, en cuyo caso la parte receptora notificara a la parte divulgadora con la maxima antelacion posible para que esta pueda ejercer sus derechos.",

        "---",
        "## 9. Limitacion de Responsabilidad",

        "### 9.1 Exclusion de Garantias Implicitas",
        "En la maxima medida permitida por la ley aplicable, Da&amp;Da Solutions excluye toda garantia implicita de comerciabilidad, idoneidad para un fin particular, no infraccion de derechos de terceros, y disponibilidad continua e ininterrumpida del servicio, distintas de las garantias expresamente establecidas en los presentes Terminos.",
        "Da&amp;Da Solutions no garantiza que los Servicios satisfagan todos los requisitos especificos del Usuario, que esten libres de errores en todo momento (mas alla de los SLAs comprometidos), o que los resultados obtenidos sean precisos, completos o confiables en todos los casos de uso posibles.",

        "### 9.2 Limitacion de Responsabilidad por Danos Indirectos",
        "En ningun caso y bajo ninguna teoria legal (contractual, extracontractual, estricta responsabilidad, u otra), Da&amp;Da Solutions sera responsable ante el Usuario por: danos indirectos, incidentales, especiales, ejemplares, punitivos o consecuentes; lucro cesante o perdida de ingresos esperados; perdida o corrupcion de datos del Usuario (mas alla de lo cubierto por los SLAs); interrupcion del negocio del Usuario; danos a la reputacion o imagen del Usuario; o perdida de oportunidades de negocio; aunque Da&amp;Da Solutions haya sido informada de la posibilidad de dichos danos y aunque los remedios previstos resulten insuficientes.",

        "### 9.3 Limite Maximo de Responsabilidad",
        "La responsabilidad total y acumulada de Da&amp;Da Solutions ante el Usuario por cualquier causa, independientemente de la forma o fundamentacion de la accion, estara limitada al importe total efectivamente pagado por el Usuario a Da&amp;Da Solutions en los 12 meses inmediatamente anteriores al evento que dio lugar al reclamo.",

        "### 9.4 Excepciones Irrenunciables",
        "Las limitaciones de responsabilidad establecidas en esta seccion no aplican en los siguientes casos: (a) dano causado por dolo o culpa grave comprobada de Da&amp;Da Solutions; (b) fallecimiento o lesiones corporales causadas por negligencia; (c) fraude o representacion dolosa; o (d) en cualquier caso en que la legislacion aplicable no permita tales limitaciones de responsabilidad.",

        "---",
        "## 10. Indemnizacion",
        "El Usuario se compromete a indemnizar, defender y mantener indemne a Da&amp;Da Solutions, sus accionistas, directivos, empleados, agentes, representantes y proveedores, de y frente a cualquier reclamo, demanda, procedimiento, dano, perdida, responsabilidad, costo y gasto (incluyendo honorarios razonables de abogados y costas judiciales) que surja de, este relacionado con, o resulte de: el incumplimiento por parte del Usuario de cualquier clausula de los presentes Terminos; el uso ilicito, abusivo o no autorizado de los Servicios por parte del Usuario o de los usuarios de su organizacion; la violacion de derechos de terceros (incluyendo derechos de propiedad intelectual, derechos al honor, a la imagen, o a la privacidad) a traves del Contenido del Usuario; el incumplimiento de la normativa aplicable por parte del Usuario; o cualquier reclamacion de terceros derivada de los productos o servicios que el Usuario desarrolle o preste usando los Servicios de Da&amp;Da Solutions.",

        "---",
        "## 11. Plazo, Suspension y Terminacion",

        "### 11.1 Vigencia del Acuerdo",
        "Los presentes Terminos entran en vigor en el momento en que el Usuario los acepta (mediante el proceso de registro o uso de los Servicios) y permanecen vigentes mientras el Usuario mantenga una cuenta activa o utilice los Servicios de Da&amp;Da Solutions en cualquier modalidad.",

        "### 11.2 Suspension Preventiva por Da&Da Solutions",
        "Da&amp;Da Solutions puede suspender el acceso del Usuario a los Servicios de manera preventiva, sin necesidad de notificacion previa, en los siguientes casos de urgencia: (a) deteccion de actividad que representa un riesgo inmediato para la seguridad de la plataforma o de otros clientes; (b) uso de los Servicios para actividades claramente ilegales; (c) compromiso confirmado de las credenciales de la cuenta que pone en riesgo datos del usuario u otros clientes. Da&amp;Da Solutions informara al Usuario sobre la suspension y sus motivos tan pronto como sea posible.",

        "### 11.3 Terminacion por el Usuario",
        "El Usuario puede dar por terminada su relacion con Da&amp;Da Solutions en cualquier momento cancelando su suscripcion a traves del panel de administracion o notificando por escrito. Para planes mensuales, la terminacion surte efecto al final del periodo facturado en curso. Para planes anuales y contratos Enterprise, aplican los terminos de terminacion anticipada del contrato firmado.",

        "### 11.4 Terminacion por Da&Da Solutions por Incumplimiento",
        "Da&amp;Da Solutions puede terminar el Acuerdo con el Usuario, con previo aviso razonable (salvo en casos de urgencia), ante los siguientes incumplimientos: violation reiterada o grave de los presentes Terminos; falta de pago de importes adeudados por mas de 30 dias tras la notificacion de mora; uso de los Servicios para actividades ilegales o fraudulentas debidamente documentadas; o actos del Usuario que danien la reputacion o los intereses de Da&amp;Da Solutions o de otros clientes.",

        "### 11.5 Efectos de la Terminacion",
        "Independientemente de la causa de terminacion: el acceso a los Servicios cesa en la fecha acordada o en la fecha de terminacion; el Usuario tiene un periodo de gracia de 90 dias para exportar todos sus datos; transcurridos los 90 dias, Da&amp;Da Solutions procede a la eliminacion definitiva e irreversible de todos los datos segun la Politica de Privacidad; los importes adeudados por el Usuario hasta la fecha de terminacion son exigibles inmediatamente; y las clausulas de confidencialidad, propiedad intelectual, limitacion de responsabilidad, indemnizacion, ley aplicable y resolucion de disputas sobreviven a la terminacion del Acuerdo.",

        "---",
        "## 12. Fuerza Mayor",
        "Ninguna de las partes sera responsable ante la otra por el incumplimiento o retraso en el cumplimiento de sus obligaciones cuando dicho incumplimiento sea causado directamente por un evento de Fuerza Mayor segun la definicion establecida en este documento. La parte afectada debe: notificar a la otra parte dentro de las 48 horas de tomado conocimiento del evento, indicando su naturaleza, duracion estimada e impacto previsto; adoptar todas las medidas razonablemente posibles para mitigar los efectos del evento; y reanudar el cumplimiento de sus obligaciones tan pronto como el evento de Fuerza Mayor cese.",
        "Si el evento de Fuerza Mayor se prolonga por mas de 30 dias calendario, cualquiera de las partes puede dar por terminado el Acuerdo mediante notificacion escrita, sin responsabilidad adicional. En ese caso, Da&amp;Da Solutions reembolsara al Usuario los importes proporcionales al periodo de servicio no prestado, deduciendo los costos directos en que hubiera incurrido para restablecer el servicio.",

        "---",
        "## 13. Modificaciones a los Terminos",
        "Da&amp;Da Solutions se reserva el derecho de modificar los presentes Terminos en cualquier momento para adaptarlos a cambios legales, regulatorios, tecnologicos, o de modelo de negocio. El procedimiento de notificacion de cambios es el siguiente:",
        "- <b>Modificaciones sustanciales:</b> las que afecten derechos o responsabilidades de las partes. Se notificaran con al menos 30 dias de anticipacion por email al correo registrado y mediante aviso destacado en la plataforma.",
        "- <b>Modificaciones menores:</b> correcciones tipograficas, aclaraciones de redaccion sin cambio de contenido, actualizaciones de datos de contacto. Pueden realizarse sin notificacion previa y son efectivas de inmediato.",
        "Si el Usuario no acepta los nuevos Terminos, debe discontinuar el uso de los Servicios antes de la fecha en que los nuevos Terminos entran en vigor. La continuacion en el uso de los Servicios despues de dicha fecha implica la aceptacion irrevocable de los nuevos Terminos.",
        "La version vigente siempre estara disponible en dadacode.io/terminos. Mantenemos un archivo historico de versiones anteriores disponible bajo solicitud a legal@dadacode.io.",

        "---",
        "## 14. Resolucion de Disputas",

        "### 14.1 Procedimiento de Resolucion Amigable",
        "Ante cualquier disputa o controversia derivada de o relacionada con los presentes Terminos, las partes se comprometen a intentar resolver la diferencia de manera amigable dentro de los 30 dias siguientes a la notificacion escrita de la disputa por parte de la parte afectada. Durante este periodo, las partes designaran representantes con poder de decision para entablar negociaciones de buena fe.",

        "### 14.2 Mediacion",
        "Si la negociacion directa entre las partes no resultara exitosa dentro del plazo de 30 dias, cualquiera de las partes puede someter la disputa a mediacion ante el Centro de Mediacion de la Camara Comercial de Buenos Aires, cuyas reglas de procedimiento se aplicaran supletoriamente. Los costos de la mediacion seran compartidos en partes iguales, salvo acuerdo en contrario.",

        "### 14.3 Ley Aplicable y Jurisdiccion",
        "Los presentes Terminos se rigen e interpretan de conformidad con las leyes de la Republica Argentina, con exclusion de sus normas de conflicto de leyes. Para la resolucion final de cualquier controversia que no se hubiera resuelto amigablemente o por mediacion, las partes se someten a la jurisdiccion exclusiva de los Tribunales Ordinarios en lo Comercial de la Ciudad Autonoma de Buenos Aires, con renuncia expresa a cualquier otro fuero que pudiera corresponderles, incluyendo el fuero federal.",

        "---",
        "## 15. Disposiciones Generales",

        "### 15.1 Divisibilidad",
        "Si alguna disposicion de los presentes Terminos fuera declarada nula, invalida, ilegal o inaplicable por cualquier tribunal o autoridad competente, dicha declaracion no afectara la validez, legalidad y vigencia del resto de las disposiciones, que permanecen plenamente vigentes y exigibles. Las partes negociaran de buena fe una disposicion valida y equivalente que reemplace a la declarada invalida.",

        "### 15.2 No Renuncia",
        "El hecho de que Da&amp;Da Solutions no ejercite o haga valer alguno de sus derechos o disposiciones en una ocasion determinada, o que conceda una extension de plazo, no se interpretara como renuncia definitiva a dichos derechos o disposiciones, ni impedira su ejercicio en el futuro.",

        "### 15.3 Cesion del Contrato",
        "El Usuario no puede ceder, transferir ni sublicenciar sus derechos u obligaciones bajo los presentes Terminos sin el consentimiento previo y escrito de Da&amp;Da Solutions. Da&amp;Da Solutions puede ceder libremente sus derechos y obligaciones a cualquier empresa del grupo economico, filial o subsidiaria, o en el contexto de una fusion, adquisicion, reorganizacion societaria o venta total o parcial de activos, notificando al Usuario con al menos 30 dias de anticipacion.",

        "### 15.4 Integralidad del Acuerdo",
        "Los presentes Terminos, junto con la Politica de Privacidad, la guia de Planes y Precios, las ordenes de compra, addenda y acuerdos complementarios formalmente firmados entre las partes, constituyen el acuerdo integral y completo entre el Usuario y Da&amp;Da Solutions respecto al objeto del mismo, y reemplazan y sustituyen todos los acuerdos, propuestas, negociaciones, representaciones o entendimientos anteriores, orales o escritos, relacionados con dicho objeto.",

        "### 15.5 Idioma del Acuerdo",
        "Los presentes Terminos han sido redactados en idioma espanol, que es el idioma oficial de la relacion contractual. En caso de que Da&amp;Da Solutions ponga a disposicion una traduccion de estos Terminos a otro idioma, dicha traduccion tiene caracter meramente informativo. En caso de discrepancia entre la version en espanol y cualquier traduccion, la version en espanol prevalecera en todos los casos.",

        "### 15.6 Contacto Legal",
        "Para consultas de indole legal relacionadas con los presentes Terminos, podes contactar al departamento legal de Da&amp;Da Solutions a traves de:",
        "- <b>Correo electronico:</b> legal@dadacode.io (tiempo de respuesta: 5 dias habiles).",
        "- <b>Correo postal:</b> Da&amp;Da Solutions S.A. — Departamento Legal — Av. Corrientes 3456, Piso 12, CABA, Argentina (C1193AAQ).",
        "- <b>Telefono:</b> +54 11 4800-9210 (lunes a viernes, 9:00 a 18:00 hs GMT-3).",
        "Da&amp;Da Solutions se compromete a responder todas las consultas legales dentro de los 5 dias habiles siguientes a su recepcion.",
    ]
))


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

# ==============================================================
# BLOQUES ADICIONALES PARA ALCANZAR MINIMO 15 PAGINAS
# ==============================================================

FAQ_EXTRA = [
    "---",
    "## 10. Gestion del Conocimiento y Documentacion",

    "### 10.1 ¿Donde encuentro la documentacion tecnica de la plataforma?",
    "Toda la documentacion tecnica de Da&amp;Da Solutions esta centralizada en <b>docs.dadacode.io</b>. La plataforma de documentacion esta construida con Docusaurus y se actualiza automaticamente con cada release de produccion mediante pipelines de CI/CD que extraen la documentacion directamente del codigo fuente (docstrings, OpenAPI specs, GraphQL schemas).",
    "La documentacion esta organizada en las siguientes secciones principales: Primeros Pasos (getting started y tutoriales guiados), Guias de Usuario (documentacion funcional por modulo), Referencia de API (REST y GraphQL con ejemplos ejecutables via Try It), Guias de Integracion (conectores, webhooks y patrones de integracion), Arquitectura y Seguridad (whitepapers y guias tecnicas avanzadas), y Changelog (historial de cambios por version con impacto y guia de migracion).",
    "Si encontras que un articulo de documentacion esta desactualizado o tiene errores, podes reportarlo haciendo clic en el boton 'Sugerir una mejora' presente en cada pagina. Tu feedback ayuda a mantener la calidad de la documentacion para toda la comunidad.",

    "### 10.2 ¿Tienen una base de conocimiento o wiki para usuarios?",
    "Si. Da&amp;Da Solutions mantiene una base de conocimiento publica con mas de 800 articulos en <b>help.dadacode.io</b>, organizada por tema, modulo y nivel de experiencia. Los articulos incluyen: guias paso a paso con capturas de pantalla, videos tutoriales de entre 2 y 10 minutos, FAQ por funcionalidad, articulos de troubleshooting para los problemas mas comunes, y mejores practicas recomendadas por el equipo de Da&amp;Da.",
    "La base de conocimiento es buscable por palabras clave y tiene un sistema de valoracion ('¿Te fue util este articulo?') que alimenta el proceso de mejora continua. Los 20 articulos mas consultados se revisan y actualizan mensualmente.",

    "### 10.3 ¿Tienen videos tutoriales o demos?",
    "Si. Contamos con una biblioteca de contenido audiovisual accesible en <b>academy.dadacode.io</b> y en nuestro canal oficial de YouTube (youtube.com/DaDaSolutionsOficial). El contenido disponible incluye: video-tutoriales por funcionalidad (duracion promedio: 5 minutos), demos de producto por industria y caso de uso, grabaciones de webinars anteriores, demos de integraciones con plataformas populares, y testimonios y casos de exito de clientes.",
    "Los suscriptores de cualquier plan tienen acceso sin costo a todo el contenido de la Da&amp;Da Academy. Los planes Business y Enterprise incluyen ademas acceso a contenido avanzado exclusivo: workshops de arquitectura, laboratorios practicos (hands-on labs) con entornos virtuales preconfigados, y sesiones grabadas de training corporativo.",

    "---",
    "## 11. Actualizaciones y Versionado de la Plataforma",

    "### 11.1 ¿Con que frecuencia actualizan la plataforma?",
    "Da&amp;Da Solutions sigue un ciclo de releases continuo con las siguientes cadencias:",
    "- <b>Patch releases (hotfixes):</b> segun necesidad, tipicamente 1-3 veces por semana. Incluyen correcciones de bugs criticos y parches de seguridad. No requieren intervencion del cliente.",
    "- <b>Minor releases:</b> cada dos semanas, alineados con nuestros sprints de desarrollo. Incluyen nuevas funcionalidades menores, mejoras de rendimiento y correcciones de bugs no criticos.",
    "- <b>Major releases:</b> trimestralmente. Incluyen nuevas funcionalidades mayores, cambios de arquitectura, y a veces cambios que requieren accion por parte del cliente (configuraciones, integraciones).",
    "Todos los releases se anuncian con anticipacion en el Changelog en docs.dadacode.io/changelog y se notifican por email a los contactos tecnicos registrados. Los major releases se comunican con al menos 30 dias de anticipacion.",

    "### 11.2 ¿Como me entero de las nuevas funcionalidades?",
    "Da&amp;Da Solutions comunica las novedades de producto a traves de multiples canales:",
    "- <b>Changelog en la plataforma:</b> al ingresar a la aplicacion, el icono de novedad (campana) en la barra superior muestra las ultimas funcionalidades disponibles en tu plan.",
    "- <b>Email de 'Release Notes':</b> boletin mensual con todas las novedades del mes enviado al correo registrado (suscripcion activa por defecto, se puede desactivar).",
    "- <b>Roadmap publico:</b> en roadmap.dadacode.io podes ver que se viene en los proximos 3-6 meses, votar por funcionalidades y agregar sugerencias.",
    "- <b>Webinar mensual de producto:</b> el primer martes de cada mes, el equipo de Product realiza una sesion de 45 minutos con las principales novedades del mes y una sesion de preguntas y respuestas en vivo.",

    "### 11.3 ¿Pueden romperse mis integraciones con las actualizaciones?",
    "Da&amp;Da Solutions sigue una politica estricta de compatibilidad hacia atras (backward compatibility) en su API. Ninguna actualizacion de version menor o patch puede introducir cambios que rompan integraciones existentes. Los cambios que afectan la compatibilidad (breaking changes) solo pueden introducirse en major releases, con un periodo de depreciacion de al menos 6 meses durante el cual ambas versiones (vieja y nueva) coexisten.",
    "Para cada breaking change, la documentacion incluye: que cambio exactamente, como migrarlo (migration guide paso a paso), herramientas automaticas de migracion cuando sea posible, y un periodo de soporte extendido para la version anterior.",

    "---",
    "## 12. Accesibilidad y Cumplimiento",

    "### 12.1 ¿La plataforma cumple con estandares de accesibilidad?",
    "Si. Da&amp;Da Solutions esta comprometida con la accesibilidad digital. La interfaz web de la plataforma cumple con el nivel AA del estandar WCAG 2.1 (Web Content Accessibility Guidelines). Esto incluye: compatibilidad con lectores de pantalla (NVDA, JAWS, VoiceOver), navegacion completa por teclado sin necesidad de mouse, contraste de colores suficiente para personas con baja vision, textos alternativos en todas las imagenes y elementos visuales, y mensajes de error descriptivos para personas con discapacidad cognitiva.",
    "Realizamos auditorias de accesibilidad semestrales con usuarios con discapacidad visual y motriz, y mantenemos un backlog dedicado a mejoras de accesibilidad. Si encontras alguna barrera de accesibilidad, reportala en support.dadacode.io clasificandola como 'Accesibilidad'.",

    "### 12.2 ¿La plataforma tiene version en multiple idiomas?",
    "La interfaz de la plataforma esta disponible en los siguientes idiomas: espanol (variantes: Argentina, Mexico, Espana), ingles (variante: Estados Unidos), y portugues (variante: Brasil). El cambio de idioma se realiza desde las preferencias de cuenta en app.dadacode.io/configuracion. La documentacion tecnica esta disponible en espanol e ingles. Los webinars y trainings se realizan en espanol e ingles segun la demanda.",
]

PRIVACIDAD_EXTRA = [
    "---",
    "## 14. Privacidad en el Contexto de la Inteligencia Artificial",

    "### 14.1 ¿Como usa Da&Da Solutions la IA con mis datos?",
    "Cuando el Usuario activa los modulos de inteligencia artificial de la plataforma (disponibles en planes Professional en adelante), el procesamiento de datos para entrenar o ejecutar modelos de IA se realiza exclusivamente con los datos del propio Usuario, dentro de su ambiente aislado. Da&amp;Da Solutions no usa los datos de un cliente para entrenar modelos compartidos que beneficien a otros clientes.",
    "Los modelos de IA pre-entrenados que Da&amp;Da Solutions provee como parte del servicio fueron entrenados usando datasets publicos y datos sinteticos generados internamente, sin usar datos de clientes. La base juridica para el procesamiento de datos del Usuario en el contexto de la IA es la ejecucion del contrato de servicios (Art. 6(1)(b) GDPR).",

    "### 14.2 ¿Que pasa con las consultas que hago al asistente de IA?",
    "Da&amp;Da Solutions ofrece en su plataforma un asistente de IA conversacional (Da&amp;Da Copilot) que permite realizar consultas en lenguaje natural sobre datos del cliente, generar reportes, y obtener recomendaciones. Las consultas realizadas al Da&amp;Da Copilot: se procesan en tiempo real sin ser almacenadas permanentemente como datos de entrenamiento, se registran en el audit log del cliente por 90 dias a efectos de trazabilidad y seguridad, no se comparten con proveedores de IA de terceros para propositos de entrenamiento, y pueden ser eliminadas bajo solicitud expresa del Usuario.",

    "### 14.3 ¿Usan modelos de IA de terceros para procesar mis datos?",
    "Para algunas funcionalidades del modulo de IA (particularmente procesamiento de lenguaje natural complejo), Da&amp;Da Solutions puede usar modelos de IA de proveedores de terceros. En todos estos casos: los datos se transmiten de manera cifrada, los proveedores estan sujetos a DPAs firmados, no se permite al proveedor usar los datos del cliente para entrenar sus modelos, y se utilizan tecnicas de minimizacion de datos (enviamos solo la informacion estrictamente necesaria para la consulta especifica).",
    "La lista actualizada de proveedores de IA utilizados, junto con las salvaguardas aplicadas, esta disponible bajo solicitud a privacidad@dadacode.io.",

    "---",
    "## 15. Privacidad para Empleados y Candidatos",

    "### 15.1 Datos de empleados de Da&Da Solutions",
    "Da&amp;Da Solutions trata datos personales de sus empleados en el contexto de la relacion laboral. Los datos tratados incluyen: datos de identificacion y contacto, informacion de remuneracion y beneficios, datos de rendimiento y evaluaciones, registros de asistencia y horarios, datos de capacitacion y desarrollo profesional, y comunicaciones internas en la medida necesaria para la gestion empresarial.",
    "El tratamiento de datos de empleados se basa en la ejecucion del contrato de trabajo, en el cumplimiento de obligaciones legales del empleador, y en el interes legitimo de Da&amp;Da Solutions en la gestion eficiente de su organizacion. Los empleados tienen acceso a sus propios datos laborales a traves del portal de Recursos Humanos en hr.dadacode.io.",

    "### 15.2 Datos de candidatos a posiciones en Da&Da Solutions",
    "Cuando una persona aplica a una posicion en Da&amp;Da Solutions, recopilamos los datos proporcionados voluntariamente en el curriculum vitae y durante el proceso de seleccion. Estos datos se utilizan exclusivamente para: evaluar la idoneidad del candidato para la posicion, comunicar el estado del proceso de seleccion, y (con consentimiento expreso del candidato) conservar el perfil para futuras oportunidades durante un maximo de 2 anos.",
    "Los datos de candidatos no seleccionados se conservan durante 6 meses desde el cierre del proceso de seleccion, tras lo cual son eliminados automaticamente, salvo que el candidato haya dado consentimiento expreso para una conservacion mayor.",

    "---",
    "## 16. Glosario de Terminos de Privacidad",
    "Con el objetivo de facilitar la comprension de esta politica, se presenta a continuacion un glosario de los terminos tecnicos mas frecuentemente utilizados en materia de proteccion de datos personales:",
    "- <b>Responsable del Tratamiento:</b> la persona fisica o juridica que determina los fines y los medios del tratamiento de datos personales. En el contexto de esta politica, Da&amp;Da Solutions actua como responsable del tratamiento respecto de los datos de sus clientes y usuarios.",
    "- <b>Encargado del Tratamiento:</b> la persona fisica o juridica que trata datos personales por cuenta del responsable. Los proveedores de servicios tecnicos de Da&amp;Da Solutions actuan como encargados del tratamiento.",
    "- <b>Tratamiento:</b> cualquier operacion o conjunto de operaciones realizadas sobre datos personales, ya sea por procedimientos automatizados o no: recopilacion, registro, organizacion, estructuracion, conservacion, adaptacion, modificacion, extraccion, consulta, utilizacion, comunicacion por transmision, difusion o cualquier otra forma de habilitacion de acceso, cotejo o interconexion, limitacion, supresion o destruccion.",
    "- <b>Seudonimizacion:</b> el tratamiento de datos personales de manera tal que los datos no puedan atribuirse a un interesado especifico sin utilizar informacion adicional que se mantiene separada y sujeta a medidas tecnicas y organizativas que garantizan su no atribucion.",
    "- <b>Anonimizacion:</b> proceso mediante el cual los datos personales se transforman de manera irreversible en datos que no pueden asociarse a ninguna persona identificada o identificable. Los datos verdaderamente anonimizados no estan sujetos a las normativas de proteccion de datos.",
    "- <b>Base juridica:</b> el fundamento legal que legitima el tratamiento de datos personales. Las bases juridicas del GDPR incluyen: consentimiento, ejecucion de un contrato, cumplimiento de una obligacion legal, proteccion de intereses vitales, mision de interes publico, e interes legitimo.",
    "- <b>Interesado / Titular de los datos:</b> la persona fisica cuyos datos personales son objeto de tratamiento.",
    "- <b>Transferencia internacional:</b> cualquier envio de datos personales a un destinatario ubicado fuera del Espacio Economico Europeo (EEE) o de Argentina, segun la legislacion aplicable.",
    "- <b>DPA (Data Processing Agreement):</b> contrato mediante el cual el responsable del tratamiento regula las condiciones en que el encargado puede tratar los datos personales.",
    "- <b>DPO (Data Protection Officer / Delegado de Proteccion de Datos):</b> persona designada por el responsable del tratamiento para supervisar el cumplimiento de la normativa de proteccion de datos y actuar como punto de contacto con las autoridades de control y los interesados.",
]

PRECIOS_EXTRA = [
    "---",
    "## 11. Garantia de Satisfaccion y Politica de Reembolsos",

    "### 11.1 Garantia de satisfaccion de 30 dias",
    "Da&amp;Da Solutions ofrece una garantia de satisfaccion de 30 dias para todos los clientes nuevos que contraten un plan de pago por primera vez (excluye renovaciones y upgrades). Si dentro de los primeros 30 dias de tu primer pago no estas satisfecho con la plataforma por cualquier motivo, podes solicitar un reembolso completo del importe pagado sin necesidad de justificacion.",
    "Para solicitar el reembolso bajo la garantia de 30 dias: envia un correo a finanzas@dadacode.io con el asunto 'Solicitud de reembolso - Garantia 30 dias', incluyendo tu nombre, el nombre de la organizacion, y el numero de factura. El reembolso se procesa dentro de los 5 dias habiles siguientes a la recepcion de la solicitud, usando el mismo metodo de pago original.",

    "### 11.2 Reembolsos fuera del periodo de garantia",
    "Fuera del periodo de garantia de 30 dias, Da&amp;Da Solutions no realiza reembolsos proporcionales por periodos no utilizados en los siguientes casos: cancelacion de plan mensual antes del vencimiento del mes, cancelacion de plan anual antes del vencimiento del ano (se aplican las condiciones de terminacion anticipada del contrato), y downgrade de plan durante el periodo de facturacion.",
    "Excepcionalmente, Da&amp;Da Solutions puede evaluar solicitudes de reembolso parcial en casos de: falla sistematica grave imputable a Da&amp;Da Solutions no cubierta por los creditos de SLA, error de facturacion documentado, o cambios sustanciales en el alcance del servicio no aceptados por el cliente. Estas solicitudes se evaluan caso por caso por el equipo comercial.",

    "---",
    "## 12. Seguridad Adicional y Cumplimiento para Sectores Regulados",

    "### 12.1 Soluciones para el Sector Financiero",
    "Da&amp;Da Solutions ofrece configuraciones especificas para clientes del sector financiero que deben cumplir con regulaciones tales como: Comunicaciones del Banco Central de la Republica Argentina (BCRA) en materia de ciberseguridad (Com. A 7724 y complementarias), normas de la Superintendencia Financiera de Colombia, regulaciones de la CNBV en Mexico, y directivas de servicios de pago (PSD2) en la Union Europea.",
    "Las capacidades especificas para fintech incluyen: trazabilidad completa de todas las operaciones con timestamps inmutables, segregacion de ambientes de produccion y testing con controles independientes, logs de acceso a datos sensibles en tiempo real exportables a sistemas regulatorios, y reportes de cumplimiento en los formatos requeridos por cada regulador.",

    "### 12.2 Soluciones para el Sector Salud",
    "Para clientes del sector de salud que manejan informacion clinica, Da&amp;Da Solutions ofrece: cifrado de campo a campo para datos clinicos sensibles, control de acceso por rol medico con firma electronica, auditoria de acceso a historias clinicas conforme a normativas de proteccion de datos de salud, integracion con sistemas de gestion hospitalaria via HL7 FHIR R4, y configuraciones de retencion de datos alineadas con los plazos de conservacion de documentacion clinica segun cada jurisdiccion.",

    "### 12.3 Programas de Cumplimiento para Organismos Publicos",
    "Da&amp;Da Solutions trabaja con organismos del sector publico y ofrece configuraciones que cumplen con los requisitos de seguridad y contratacion publica. Contamos con: experiencia en licitaciones publicas en Argentina, Colombia y Mexico, capacidad de firma de contratos con el Estado bajo modalidad de servicios en la nube, cumplimiento con estandares de seguridad para la administracion publica, y posibilidad de despliegue en nubes soberanas o en las instalaciones del organismo cuando la normativa lo exige.",

    "---",
    "## 13. Programa de Partners y Revendedores",

    "### 13.1 ¿Da&Da Solutions tiene un programa de partners?",
    "Si. El Programa de Partners de Da&amp;Da Solutions (Da&amp;Da Partner Network) esta disenado para integradores de sistemas, consultoras tecnologicas, agencias digitales y revendedores que quieran incorporar los servicios de Da&amp;Da Solutions a su portfolio de oferta. Los beneficios del programa incluyen: descuentos de entre el 15% y el 30% sobre los precios de lista segun el nivel de partnership (Silver, Gold, Platinum), comisiones por ventas nuevas generadas, acceso anticipado a nuevas funcionalidades, material de marketing co-branded, listing en el directorio oficial de partners en dadacode.io/partners, capacitacion y certificacion gratuita para el equipo tecnico y comercial del partner, y soporte tecnico preferencial para demo environments y proyectos de implementacion.",

    "### 13.2 ¿Como me uno al programa de partners?",
    "Para unirte al Programa de Partners de Da&amp;Da Solutions: completa el formulario de aplicacion en dadacode.io/partners/aplicar. El equipo de Channel Partnerships revisara tu solicitud en un plazo maximo de 5 dias habiles y te contactara para agendar una reunion de evaluacion. Los criterios de seleccion incluyen: experiencia en implementacion de software empresarial, capacidad tecnica del equipo, presencia geografica, y alineacion de propuesta de valor con los segmentos objetivo de Da&amp;Da Solutions.",

    "---",
    "## 14. Preguntas Frecuentes sobre Facturacion",

    "### 14.1 ¿Puedo cambiar de plan en cualquier momento?",
    "Si. Podes cambiar de plan en cualquier momento desde el panel de administracion en app.dadacode.io/billing. Los upgrades (paso a un plan superior) son efectivos de inmediato; los downgrades (paso a un plan inferior) se aplican al inicio del proximo periodo de facturacion. Da&amp;Da Solutions no cobra ninguna comision ni tarifa administrativa por cambio de plan.",
    "Al hacer un upgrade durante el periodo de facturacion, se cobra la diferencia proporcional al tiempo restante del periodo en curso. Por ejemplo, si tenes el Plan Starter (USD 99/mes) y haces upgrade al Plan Professional (USD 349/mes) a mitad del mes, se cobra USD 125 adicionales por los 15 dias restantes del mes, y desde el siguiente mes se factura el importe completo del Plan Professional.",

    "### 14.2 ¿Como funciona la facturacion para equipos que crecen?",
    "Da&amp;Da Solutions no penaliza el crecimiento. Si tu equipo supera el limite de usuarios de tu plan, el sistema te notificara automaticamente y te propondra las siguientes opciones: agregar usuarios individuales al precio adicional por usuario del plan actual, hacer upgrade al plan siguiente que incluye mas usuarios, o comprar bloques de usuarios adicionales a precio preferencial (disponible desde el Plan Professional).",
    "Los usuarios adicionales se facturan en forma proporcional al tiempo restante del periodo de facturacion y se consolidan en la siguiente factura mensual. No hay periodo de gracia: el acceso del usuario adicional esta disponible en el momento en que se confirma el pago del usuario extra.",

    "### 14.3 ¿Que pasa con el almacenamiento si supero el limite de mi plan?",
    "Si el almacenamiento utilizado supera el limite incluido en tu plan, el sistema te enviara una notificacion automatica cuando alcances el 80% del limite. Al llegar al 95%, recibiras una segunda notificacion. Al alcanzar el 100%, el sistema no eliminara tus datos, pero si bloqueara la carga de nuevos archivos hasta que liberes espacio o amplies tu almacenamiento.",
    "Podes ampliar el almacenamiento en cualquier momento desde el panel de administracion a USD 0.08/GB adicional/mes (mismo precio en todos los planes). El almacenamiento adicional se factura mensualmente por los GB efectivamente utilizados por encima del limite del plan, medido al cierre de cada periodo.",

    "---",
    "## 15. Recursos Adicionales para Clientes",

    "### 15.1 Comunidad de usuarios Da&Da",
    "Da&amp;Da Solutions cuenta con una comunidad activa de usuarios en <b>community.dadacode.io</b>. La comunidad es un espacio donde los usuarios pueden: hacer preguntas y obtener respuestas de otros usuarios y del equipo de Da&amp;Da, compartir casos de uso, templates, integraciones y soluciones, participar en encuestas de producto y dar feedback directo al equipo de Product, acceder a beta de nuevas funcionalidades antes que el publico general, y conectar con otros profesionales del sector que usan Da&amp;Da Solutions.",
    "La comunidad es moderada por el equipo de Da&amp;Da Solutions y tiene un codigo de conducta que promueve el respeto, la colaboracion y la inclusion. Los usuarios que realizan contribuciones de alto valor (respuestas utiles, templates compartidos, feedback de calidad) pueden obtener el status de 'Da&amp;Da Champion', con beneficios como reconocimiento publico, acceso anticipado a features y descuentos en la renovacion de su plan.",

    "### 15.2 Newsletter y blog tecnico",
    "Da&amp;Da Solutions publica contenido de valor para su comunidad a traves de los siguientes canales:",
    "- <b>Blog tecnico (blog.dadacode.io):</b> publicaciones semanales sobre tecnologia, arquitectura, buenas practicas de desarrollo, casos de exito de clientes, y novedades del sector.",
    "- <b>Newsletter quincenal:</b> resumen de los articulos del blog, novedades de la plataforma, proximos webinars, y oportunidades exclusivas para suscriptores.",
    "- <b>LinkedIn y Twitter/X:</b> actualizaciones diarias, participacion en conversaciones del sector, y convocatorias a eventos.",
    "El blog y el newsletter son de acceso publico y gratuito. La suscripcion al newsletter puede gestionarse en dadacode.io/newsletter.",
]

TERMINOS_EXTRA = [
    "---",
    "## 16. Condiciones Especificas para Servicios de Inteligencia Artificial",

    "### 16.1 Alcance de los Servicios de IA",
    "Los modulos de inteligencia artificial de Da&amp;Da Solutions (colectivamente, 'Servicios de IA') incluyen: modelos de clasificacion y prediccion entrenados sobre datos del cliente, funcionalidades de procesamiento de lenguaje natural (NLP), el asistente conversacional Da&amp;Da Copilot, la busqueda semantica en documentos, y la deteccion automatica de anomalias en series temporales.",

    "### 16.2 Limitaciones y Advertencias sobre los Servicios de IA",
    "El Usuario reconoce y acepta expresamente que: (a) Los Servicios de IA producen resultados probabilisticos y no garantizan precision absoluta en sus predicciones, clasificaciones o recomendaciones. (b) Los resultados de los Servicios de IA deben ser revisados por personas calificadas antes de ser utilizados para tomar decisiones de negocio o que afecten a terceros. (c) Da&amp;Da Solutions no sera responsable de las decisiones tomadas por el Usuario o por terceros basadas exclusivamente en los resultados de los Servicios de IA sin revision humana. (d) El rendimiento de los modelos de IA puede degradarse con el tiempo a medida que los datos del cliente evolucionan (model drift), y el Usuario es responsable de monitorear y solicitar reentrenamiento cuando sea necesario.",

    "### 16.3 Propiedad de los Modelos Entrenados",
    "Cuando Da&amp;Da Solutions entrena modelos de IA personalizados sobre datos del cliente, la propiedad de dichos modelos y de los datos de entrenamiento pertenece al Cliente. Da&amp;Da Solutions retiene los derechos sobre la arquitectura base del modelo, el codigo de entrenamiento, y los algoritmos subyacentes. Al terminar el contrato, el Cliente puede solicitar la exportacion del modelo entrenado en formato estandar (ONNX, TensorFlow SavedModel, o equivalente) sin costo adicional.",

    "---",
    "## 17. Condiciones para el Uso de la API y SDKs",

    "### 17.1 Uso Aceptable de la API",
    "El acceso a la API de Da&amp;Da Solutions esta sujeto a las siguientes condiciones adicionales especificas: (a) El Usuario debe mantener confidencial su API Key y no incluirla en codigo fuente publico (repositorios publicos, foros, etc.). Si una API Key es comprometida, el Usuario debe rotarla inmediatamente desde el panel de administracion. (b) El Usuario es responsable de implementar mecanismos de retry con backoff exponencial para manejar errores transitorios, sin saturar la API con solicitudes repetidas. (c) El Usuario debe respetar los headers de rate limiting devueltos por la API (X-RateLimit-Remaining, X-RateLimit-Reset) para anticipar y gestionar los limites sin generar errores. (d) El uso de la API para scraping sistematico de datos o para replicar la plataforma en otro sistema esta expresamente prohibido.",

    "### 17.2 Condiciones de los SDKs",
    "Los SDKs oficiales de Da&amp;Da Solutions se distribuyen bajo licencia MIT para facilitar su integracion en proyectos del cliente. Esta licencia permite: usar, copiar, modificar y distribuir el SDK dentro de las aplicaciones del cliente. Sin embargo, los SDKs son herramientas para conectarse a los Servicios de Da&amp;Da Solutions y no pueden usarse de manera desconectada de dichos Servicios. Da&amp;Da Solutions puede publicar nuevas versiones de los SDKs; el Usuario es responsable de mantener sus integraciones actualizadas dentro de los plazos de soporte de cada version.",

    "---",
    "## 18. Acuerdos de Nivel de Servicio Extendidos",

    "### 18.1 SLA para Integraciones y Webhooks",
    "Ademas del SLA de disponibilidad de la plataforma, Da&amp;Da Solutions se compromete a los siguientes niveles de servicio para componentes especificos:",
    "- <b>API REST:</b> latencia de respuesta p99 (percentil 99) menor a 500ms para endpoints estandar.",
    "- <b>API GraphQL:</b> latencia de respuesta p99 menor a 1.000ms para consultas no agregadas.",
    "- <b>Entrega de Webhooks:</b> entrega del primer intento dentro de los 30 segundos del evento. En caso de falla, reintento automatico con backoff exponencial durante 24 horas.",
    "- <b>Procesamiento de colas asincronicas:</b> procesamiento del 99% de los mensajes dentro de los 5 minutos de su ingreso a la cola bajo condiciones normales de carga.",

    "### 18.2 SLA para el Soporte por Chat en Vivo",
    "Para los planes que incluyen soporte por chat en vivo, Da&amp;Da Solutions se compromete a los siguientes tiempos de espera:",
    "- <b>Horario pico (lunes a viernes, 10:00-14:00 hs GMT-3):</b> tiempo de espera maximo de 5 minutos.",
    "- <b>Horario normal (lunes a viernes, 8:00-10:00 y 14:00-20:00 hs GMT-3):</b> tiempo de espera maximo de 2 minutos.",
    "- <b>Fuera de horario (con add-on 24/7):</b> tiempo de espera maximo de 10 minutos.",
    "En caso de que el tiempo de espera supere el compromiso establecido, el sistema ofrece automaticamente la opcion de dejar un mensaje y ser contactado por email dentro del SLA de respuesta del plan correspondiente.",
]

# Agregar bloques extra a cada documento
DOCS[0]["blocks"].extend(FAQ_EXTRA)
DOCS[1]["blocks"].extend(PRIVACIDAD_EXTRA)
DOCS[2]["blocks"].extend(PRECIOS_EXTRA)
DOCS[3]["blocks"].extend(TERMINOS_EXTRA)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    docs_dir = os.path.join(project_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    print(f"\nGenerando PDFs en: {docs_dir}\n")
    for d in DOCS:
        out_path = os.path.join(docs_dir, d["filename"])
        make_pdf(
            out_path,
            d["title"],
            d["subtitle"],
            d["doc_type"],
            d["blocks"],
        )
    print("\nListo. Todos los PDFs generados correctamente.")
