"""
expand_existing_pdfs.py
Expande los 7 PDFs existentes de Da&Da Solutions para que tengan minimo 15 paginas cada uno.
Ejecutar desde la raiz del proyecto:
    venv\\Scripts\\python scripts\\expand_existing_pdfs.py
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

# ──────────────────────────────────────────────────────────────
# ESTILOS (mismo que build_long_pdfs.py)
# ──────────────────────────────────────────────────────────────
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
}


def _story(title, subtitle, blocks):
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
    story.append(Paragraph("Documento Interno — Confidencial", STYLES["center"]))
    story.append(Paragraph(
        "Version 3.1  |  Ejercicio fiscal 2026  |  Departamento de Ingenieria",
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
        else:
            story.append(Paragraph(b, STYLES["body"]))
    return story


def make_pdf(out_path, title, subtitle, blocks):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2.3 * cm, rightMargin=2.3 * cm,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
    )
    doc.build(_story(title, subtitle, blocks))
    pages = _count_pages(out_path)
    kb = os.path.getsize(out_path) // 1024
    print(f"  [{pages:2d} pag | {kb:3d} KB]  {os.path.basename(out_path)}")


def _count_pages(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    return len(PdfReader(path).pages)


# ==============================================================
# Re-importamos los bloques originales del script existente
# y les agregamos secciones adicionales
# ==============================================================

# Para no duplicar todo el contenido original, importamos DOCS desde build_long_pdfs
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from build_long_pdfs import DOCS as ORIGINAL_DOCS


# ==============================================================
# BLOQUES EXTRA POR DOCUMENTO
# ==============================================================

ANNEXES = [
    ">>>BREAK",
    "---",
    "## Anexo A: Politicas de Calidad y Mejora Continua",
    "### A.1 Proposito y Alcance",
    "En Da&amp;Da Solutions, la calidad no es una opcion, es un pilar fundamental de nuestra entrega de valor. Este anexo establece las bases de nuestro Sistema de Gestion de Calidad (SGC) aplicable a todas las areas de ingenieria, desarrollo, operaciones y soporte de la organizacion. Nuestro compromiso es mantener estandares de excelencia en todos los productos y servicios que desarrollamos, asegurando la satisfaccion de nuestros clientes y el cumplimiento de los requisitos legales y regulatorios vigentes en todos los mercados donde operamos.",
    "El alcance de esta politica abarca desde la concepcion y diseno de los sistemas, pasando por el desarrollo, pruebas, despliegue, hasta el mantenimiento y soporte continuo. Todo el personal interno, asi como contratistas y proveedores de servicios de Da&amp;Da Solutions, estan obligados a conocer, comprender y aplicar estos principios en su labor diaria.",
    
    "### A.2 Principios de Calidad",
    "Nuestros principios de calidad se centran en:",
    "- <b>Enfoque al Cliente:</b> Entender las necesidades actuales y futuras de nuestros clientes para superar sus expectativas.",
    "- <b>Liderazgo:</b> Los lideres de todos los niveles deben establecer un proposito claro y crear un entorno interno que promueva la participacion activa del personal.",
    "- <b>Compromiso del Personal:</b> La competencia, empoderamiento y compromiso de las personas en todos los niveles son esenciales para crear y entregar valor.",
    "- <b>Enfoque Basado en Procesos:</b> Los resultados consistentes se logran de manera mas efectiva cuando las actividades se entienden y gestionan como procesos interrelacionados.",
    "- <b>Mejora Continua:</b> La mejora constante del desempeno general de la organizacion es un objetivo permanente.",
    "- <b>Toma de Decisiones Basada en Evidencia:</b> Las decisiones efectivas se basan en el analisis de datos y la informacion.",
    "- <b>Gestion de Relaciones:</b> Fomentar relaciones mutuamente beneficiosas con proveedores y socios estrategicos.",
    
    "### A.3 Metricas e Indicadores de Calidad",
    "Para asegurar el cumplimiento de nuestros objetivos de calidad, Da&amp;Da Solutions monitoriza de forma continua un conjunto de indicadores clave de rendimiento (KPIs). Estos incluyen:",
    "- <b>Defect Escape Rate (DER):</b> Porcentaje de defectos que se escapan a produccion frente al total de defectos encontrados.",
    "- <b>Time to Resolve (TTR):</b> Tiempo promedio necesario para resolver incidentes criticos reportados por clientes.",
    "- <b>Customer Satisfaction Score (CSAT):</b> Indice de satisfaccion del cliente recopilado mediante encuestas periodicas tras la resolucion de tickets y entrega de proyectos.",
    "- <b>Code Coverage:</b> Porcentaje de codigo cubierto por pruebas automatizadas (unitarias, integracion, e2e). El objetivo minimo es del 85% para todos los proyectos nuevos.",
    "- <b>Technical Debt Ratio:</b> Relacion entre el costo de solucionar problemas estructurales del codigo y el costo de desarrollar nuevo software.",
    
    "### A.4 Auditorias Internas y Externas",
    "Da&amp;Da Solutions realiza auditorias internas trimestrales para verificar el cumplimiento de los procesos documentados y detectar oportunidades de mejora. Estas auditorias son lideradas por el equipo de QA Corporativo, y sus resultados se presentan a la direccion ejecutiva para su revision. Ademas, nos sometemos a auditorias externas anuales para mantener nuestras certificaciones internacionales (como ISO 9001 e ISO 27001). Todo colaborador debe cooperar activamente y con total transparencia durante cualquier proceso de auditoria.",
    
    "---",
    "## Anexo B: Normativas de Compliance y Etica Corporativa",
    "### B.1 Codigo de Conducta y Etica",
    "El Codigo de Conducta de Da&amp;Da Solutions es la brujula que guia nuestras acciones y decisiones diarias. Esperamos que todos los empleados, contratistas y colaboradores actuen con la maxima integridad, honestidad y respeto en todas sus interacciones, ya sea con companeros de trabajo, clientes, socios o competidores.",
    "No toleramos ninguna forma de discriminacion, acoso (sexual, laboral o de cualquier otro tipo), ni represalias contra quienes reporten infracciones de buena fe. Promovemos un ambiente de trabajo inclusivo y diverso donde todas las voces son valoradas.",
    
    "### B.2 Prevencion del Fraude y Corrupcion",
    "Da&amp;Da Solutions se rige por politicas estrictas de tolerancia cero ante el soborno y la corrupcion. Esta terminantemente prohibido ofrecer, prometer, dar, aceptar o solicitar cualquier ventaja indebida (financiera o de otro tipo) para obtener un beneficio comercial o personal. Esto incluye regalos extravagantes, atenciones desproporcionadas y pagos de facilitacion.",
    "Cualquier colaborador que tenga conocimiento o sospecha de un acto de corrupcion debe reportarlo inmediatamente a traves del Canal de Denuncias Eticas, el cual garantiza el anonimato y la confidencialidad absoluta.",
    
    "### B.3 Conflictos de Interes",
    "Un conflicto de interes ocurre cuando los intereses personales de un colaborador interfieren, o parecen interferir, con los intereses de Da&amp;Da Solutions. Todos los empleados tienen la obligacion de evitar situaciones en las que su juicio objetivo pueda verse comprometido.",
    "Ejemplos comunes de conflictos de interes incluyen:",
    "- Tener una relacion financiera o comercial con un proveedor, cliente o competidor.",
    "- Usar informacion confidencial de la empresa para beneficio personal (Insider Trading).",
    "- Contratar o supervisar directamente a un familiar cercano o pareja sentimental.",
    "- Trabajar en proyectos paralelos o consultar para empresas de la misma industria sin autorizacion previa.",
    "Cualquier posible conflicto de interes debe ser revelado de inmediato al departamento de RRHH y al manager directo para su evaluacion y gestion adecuada.",
    
    "### B.4 Confidencialidad y Propiedad Intelectual",
    "Toda la informacion generada o procesada dentro de Da&amp;Da Solutions es propiedad exclusiva de la empresa o de sus clientes. Esto abarca codigo fuente, algoritmos, disenos, estrategias de negocio, bases de datos y cualquier documentacion tecnica o comercial.",
    "Los colaboradores tienen el deber de mantener la mas estricta confidencialidad sobre esta informacion, incluso despues de finalizada su relacion laboral con la empresa. Asimismo, todo desarrollo intelectual creado durante el horario laboral o utilizando recursos de la compania pertenece enteramente a Da&amp;Da Solutions. Se prohibe el uso de software sin licencia o material con derechos de autor sin la debida autorizacion.",
    
    ">>>BREAK",
    "---",
    "## Anexo C: Plan de Continuidad del Negocio (BCP)",
    "### C.1 Objetivos del BCP",
    "El Plan de Continuidad del Negocio de Da&amp;Da Solutions tiene como objetivo asegurar la operacion ininterrumpida de nuestros servicios criticos frente a eventos adversos (desastres naturales, pandemias, ciberataques a gran escala, fallas catastroficas de infraestructura). El BCP garantiza que podamos mantener nuestros compromisos contractuales, minimizar las perdidas financieras y proteger la reputacion de la compania.",
    
    "### C.2 Evaluacion de Riesgos y BIA (Business Impact Analysis)",
    "De forma anual, el Comite de Riesgos realiza un Analisis de Impacto al Negocio (BIA) para identificar los procesos criticos, evaluar las consecuencias de su interrupcion y determinar los Tiempos Objetivo de Recuperacion (RTO) y los Puntos Objetivo de Recuperacion (RPO) para cada sistema y servicio de la organizacion. Los resultados del BIA dictan las estrategias de recuperacion y la asignacion de recursos para el BCP.",
    
    "### C.3 Equipos de Respuesta y Roles",
    "El BCP define una estructura clara de respuesta ante crisis:",
    "- <b>Comite de Manejo de Crisis (CMC):</b> Formado por la alta direccion. Encargado de tomar decisiones estrategicas, aprobar comunicaciones corporativas y declarar formalmente el estado de emergencia.",
    "- <b>Equipo de Respuesta a Incidentes (IRT):</b> Formado por lideres tecnicos y de operaciones. Responsable de ejecutar las tareas tacticas para contener y mitigar el incidente en tiempo real.",
    "- <b>Coordinadores de Continuidad:</b> Designados en cada departamento para asegurar la ejecucion ordenada del plan a nivel operativo y gestionar al personal.",
    
    "### C.4 Procedimientos de Evacuacion y Trabajo Remoto",
    "En caso de que las instalaciones fisicas de Da&amp;Da Solutions queden inutilizables, se activara el protocolo de trabajo 100% remoto para todo el personal. La infraestructura en la nube esta disenada para soportar el acceso remoto seguro (via VPN corporativa y Zero Trust Network Access) del total de la plantilla sin degradacion del servicio.",
    "Se requiere que todos los empleados mantengan sus equipos portatiles actualizados y participen en los simulacros de evacuacion y pruebas de conectividad remota que se realizan semestralmente.",
    
    "---",
    "## Anexo D: Responsabilidad Social Corporativa y Sostenibilidad",
    "### D.1 Compromiso Ambiental",
    "En Da&amp;Da Solutions reconocemos nuestra responsabilidad con el medio ambiente. Estamos comprometidos a minimizar nuestra huella de carbono mediante la optimizacion de recursos y la implementacion de practicas sostenibles. Nuestros objetivos ambientales para los proximos cinco anos incluyen:",
    "- Reducir el consumo energetico en nuestras oficinas fisicas en un 25% mediante politicas de uso eficiente e iluminacion inteligente.",
    "- Migrar el 100% de nuestra carga de trabajo en la nube a regiones de proveedores (como AWS o GCP) que se alimenten exclusivamente de energias renovables.",
    "- Implementar un programa corporativo de reciclaje y gestion de residuos electronicos (e-waste), asegurando que los equipos obsoletos sean donados o reciclados correctamente.",
    
    "### D.2 Impacto Comunitario y Voluntariado",
    "Creemos firmemente en devolver valor a las comunidades en las que operamos. Da&amp;Da Solutions fomenta la participacion activa de sus colaboradores en programas de impacto social. Cada empleado dispone de 24 horas anuales remuneradas (3 dias habiles) para dedicarse a actividades de voluntariado en fundaciones u ONGs asociadas a la empresa.",
    "Nuestros programas se centran principalmente en la educacion tecnologica, ofreciendo mentoria y talleres de programacion gratuitos a jovenes de sectores vulnerables para reducir la brecha digital.",
    
    "### D.3 Diversidad e Inclusion en Tecnologia",
    "La diversidad de perspectivas es el motor de la innovacion. Da&amp;Da Solutions tiene un fuerte compromiso con la diversidad e inclusion (D&I). Nos esforzamos por crear equipos donde convivan diferentes generos, origenes etnicos, edades y trayectorias profesionales. Contamos con ERGs (Employee Resource Groups) activos para mujeres en tecnologia, comunidad LGBTQ+, y neurodiversidad. El equipo de adquisicion de talento tiene metas especificas para garantizar que los procesos de seleccion sean equitativos y libres de sesgos inconscientes.",
    
    ">>>BREAK",
    "---",
    "## Anexo E: Marco Metodologico y Adopcion Agile",
    "### E.1 Manifiesto Agile Interno",
    "Da&amp;Da Solutions abraza completamente los principios del desarrollo agil de software, adaptandolos a nuestra cultura y necesidades. Entendemos \"Agile\" no como un conjunto estricto de reuniones, sino como una mentalidad de adaptacion continua, entrega de valor temprano y colaboracion estrecha. Valoramos el software funcionando por encima de la documentacion exhaustiva (aunque, como se detalla en otros apartados, la documentacion justa y necesaria es vital).",
    
    "### E.2 Ciclos de Entrega (Sprints y Kanban)",
    "Los equipos de producto suelen operar en Sprints de dos semanas utilizando metodologias Scrum, con ceremonias de Planning, Daily Stand-up, Review y Retrospectiva. Sin embargo, los equipos de operaciones e infraestructura, asi como los squads que manejan alto volumen de incidencias y soporte no planificado, utilizan Kanban para gestionar su flujo de trabajo, priorizando la reduccion del Work In Progress (WIP) y el Lead Time.",
    "La eleccion del marco especifico se delega a la autonomia de cada equipo, siempre y cuando se cumplan los objetivos de visibilidad (a traves de Jira) y sincronizacion con el resto de la tribu.",
    
    "### E.3 Definition of Ready (DoR) y Definition of Done (DoD)",
    "Para mantener la calidad y predictibilidad, aplicamos de forma estricta los conceptos de DoR y DoD:",
    "- <b>Definition of Ready (DoR):</b> Una historia de usuario o tarea no puede entrar a un Sprint o a la columna \"In Progress\" si no tiene: Criterios de aceptacion claros, dependencias identificadas y resueltas, diseno UX/UI aprobado (si aplica), y ha sido refinada y estimada por el equipo.",
    "- <b>Definition of Done (DoD):</b> Un ticket no se considera terminado hasta que: El codigo compila y pasa todos los tests (unitarios y e2e), ha sido revisado (aprobado en PR por al menos 2 pares), ha sido desplegado en el entorno de Staging y validado funcionalmente, la documentacion tecnica esta actualizada, y no introduce nuevas vulnerabilidades (seguridad).",
    
    "### E.4 Ceremonias de Sincronizacion a Nivel Organizacional",
    "A nivel escalado, realizamos ceremonias para alinear a los distintos squads y tribes:",
    "- <b>Sprint Demo Tribe:</b> Sesion mensual donde cada equipo presenta el valor entregado y demos en vivo a los stakeholders.",
    "- <b>Tech Townhall:</b> Reunion trimestral liderada por el CTO para compartir la vision tecnologica, cambios de arquitectura globales y celebrar logros del equipo de ingenieria.",
    "- <b>Post-Mortems Transversales:</b> Cuando un incidente severo afecta a multiples equipos, se realiza un post-mortem conjunto para asegurar que los aprendizajes se distribuyan en toda la organizacion.",
    
    "---",
    "## Anexo F: Uso Aceptable de Tecnologias y Sistemas",
    "### F.1 Dispositivos Corporativos",
    "Los equipos proporcionados por Da&amp;Da Solutions (laptops, telefonos moviles, monitores) son propiedad de la empresa y se otorgan para uso exclusivamente profesional. Se permite un uso personal incidental siempre que no interfiera con las responsabilidades laborales, no infrinja las politicas de seguridad ni consuma recursos excesivos. Esta prohibida la instalacion de software pirata, herramientas de hacking (salvo autorizacion expresa para equipos de seguridad), mineros de criptomonedas, y clientes P2P para descarga de contenido protegido por derechos de autor.",
    
    "### F.2 Redes Sociales y Comunicacion Publica",
    "Alentamos a nuestros colaboradores a ser embajadores de la marca Da&amp;Da Solutions en redes sociales (como LinkedIn, Twitter, blogs tecnicos). Sin embargo, deben dejar claro que sus opiniones son personales y no representan posturas oficiales de la compania, salvo que sean portavoces autorizados. Esta estrictamente prohibido compartir informacion confidencial sobre clientes, vulnerabilidades de sistemas, estrategias financieras o conflictos internos en plataformas publicas.",
    
    "### F.3 Uso de Herramientas de Inteligencia Artificial (IA)",
    "El uso de herramientas de IA generativa (como ChatGPT, GitHub Copilot, Gemini) esta permitido y fomentado para aumentar la productividad, siempre y cuando se adhiera a las siguientes restricciones de seguridad: No se puede ingresar codigo fuente propietario, credenciales, secretos, datos de clientes o informacion confidencial de Da&amp;Da Solutions en versiones gratuitas o publicas de estas herramientas, ya que esos datos podrian ser utilizados para entrenar modelos externos. Se deben utilizar unicamente las licencias empresariales provistas por la compania que garantizan la privacidad de los datos."
]

EXTRA = {
    "onboarding.pdf": [
        "---",
        "## 11. Salud Mental y Bienestar en el Trabajo",

        "### 11.1 Politica de Desconexion Digital",
        "Da&amp;Da Solutions reconoce y protege activamente el derecho a la desconexion digital de todos sus colaboradores. Esto significa que fuera del horario laboral acordado no se espera que ningun colaborador este disponible para responder mensajes, correos, o revisar codigo, salvo que participe de una guardia de produccion remunerada. Los Engineering Managers tienen la responsabilidad explicita de modelar este comportamiento y de no enviar mensajes que generen expectativa de respuesta inmediata fuera del horario laboral.",
        "Para las guardias de produccion (on-call), existe una rotacion equitativa documentada en PagerDuty. Cada guardia tiene una duracion de 7 dias corridos y el colaborador que la realiza tiene el dia siguiente de trabajo con carga reducida como compensacion parcial. La guardia solo aplica a ingenieros Senior en adelante, y el numero de guardias por persona no puede superar las 4 rotaciones por trimestre.",

        "### 11.2 Licencias y Dias Adicionales",
        "Ademas de las licencias obligatorias por ley, Da&amp;Da Solutions ofrece los siguientes dias adicionales a todos sus colaboradores:",
        "- <b>Dias de salud mental:</b> 3 dias por ano calendario, no acumulables, que pueden tomarse sin justificacion medica ni aprobacion previa del manager. Solo se informa al manager el mismo dia con al menos 1 hora de anticipacion.",
        "- <b>Dia de mudanza:</b> 1 dia pago por evento de mudanza, hasta 2 veces por ano.",
        "- <b>Dia de cumpleanos:</b> 1 dia libre pago en la semana del cumpleanos del colaborador.",
        "- <b>Licencia extendida por duelo:</b> 10 dias habiles por fallecimiento de familiar directo (padres, hijxs, pareja), ademas de los 3 dias previstos por ley.",
        "- <b>Licencia de paternidad extendida:</b> 30 dias habiles para el rol no gestante, independientemente del genero y tipo de familia.",

        "### 11.3 Asistencia Psicologica Corporativa",
        "Da&amp;Da Solutions cubre hasta 12 sesiones anuales de psicologia o psiquiatria a traves de la red de profesionales asociados a la prepaga corporativa. Adicionalmente, disponemos de un servicio de asistencia psicologica de emergencia disponible las 24 horas del dia, los 7 dias de la semana, a traves de la linea de bienestar corporativo (numero en la intranet). Este servicio es completamente confidencial: ni RRHH ni ningun manager reciben informacion sobre su uso.",

        "---",
        "## 12. Carrera Profesional y Crecimiento",

        "### 12.1 El Framework de Evaluacion de Desempeno",
        "Da&amp;Da Solutions realiza evaluaciones formales de desempeno dos veces al ano: en junio y en diciembre. El proceso de evaluacion es un ciclo de 360 grados que incluye: autoevaluacion del colaborador, evaluacion del manager directo, evaluacion de pares (al menos 3 personas del equipo extendido) y feedback de los reports directos para roles de management.",
        "El resultado de la evaluacion alimenta las decisiones de ajuste de compensacion (que se aplican en enero y julio de cada ano), las decisiones de promocion, y el plan de desarrollo individual del siguiente semestre. El proceso completo esta documentado en Confluence bajo 'People - Evaluacion de Desempeno'.",

        "### 12.2 Promociones",
        "Las promociones en Da&amp;Da Solutions siguen el principio de 'promote for what you already do, not for what you promise to do'. Esto significa que no se promueve a alguien en anticipacion de que podra desempenar un rol mayor; se promueve cuando ya lleva al menos un trimestre operando de manera consistente en el nivel superior.",
        "El proceso de promocion requiere: una propuesta escrita del manager con evidencia de comportamientos del nivel superior, aprobacion del Engineering Manager del area y, en el caso de Staff Engineer y Principal Engineer, presentacion ante un comite de Staff Engineers.",

        "### 12.3 Programa de Mentoria Interna",
        "Da&amp;Da Solutions tiene un programa de mentoria interna voluntaria que conecta a ingenieros junior y mid con Staff Engineers o Senior Engineers de areas distintas a la propia. El programa dura 6 meses y consiste en sesiones quincenales de 45 minutos con agenda libre definida por el mentee.",
        "Para unirte como mentee o como mentor, escribe en el canal #mentoring de Slack. El programa no es gestionado por RRHH: es una iniciativa bottom-up coordinada por voluntarios.",

        "### 12.4 Presupuesto de Desarrollo Profesional",
        "Cada colaborador de Da&amp;Da Solutions dispone de un presupuesto anual de USD 1.200 para desarrollo profesional. Este presupuesto puede utilizarse en: cursos online (Platzi, Udemy for Business, Coursera, O'Reilly Learning), libros tecnicos (fisicos o digitales), certificaciones profesionales (AWS, GCP, CKAD, TOGAF, etc.), y conferencias y eventos del sector (requiere aprobacion del manager con 30 dias de anticipacion).",
        "El presupuesto no se acumula de un ano a otro. El proceso de solicitud es simple: completar el formulario en la intranet, adjuntar el comprobante de pago, y el reembolso se acredita en la siguiente liquidacion de haberes.",

        "---",
        "## 13. Seguridad de la Informacion para Nuevos Ingenieros",

        "### 13.1 Tus Responsabilidades de Seguridad desde el Dia 1",
        "La seguridad de la informacion es responsabilidad de cada persona en Da&amp;Da Solutions, no solo del equipo de seguridad. Como nuevo integrante del equipo, tus responsabilidades especificas son: nunca compartir tus credenciales con nadie, incluido el equipo de IT; no instalar software no autorizado en tu laptop corporativa; reportar cualquier correo, mensaje o llamada sospechosa al equipo de seguridad antes de interactuar con ellos; bloquear tu pantalla cada vez que te alejes de tu computadora; y no trabajar con datos de produccion en tu entorno local sin autorizacion expresa.",

        "### 13.2 Ingenieria Social y Phishing",
        "Los ataques de ingenieria social son la principal amenaza de seguridad para cualquier organizacion. El 90% de los incidentes de seguridad exitosos comienza con algun tipo de manipulacion de personas. Las senales de alerta de un ataque de phishing son: urgencia artificial, amenaza de consecuencias negativas, solicitud de credenciales por canales inusuales, URLs similares a dominios oficiales, y archivos adjuntos no esperados.",
        "Ante cualquier duda, la politica es clara: NO hagas clic, NO respondas, y reporta inmediatamente a security@dadacode.io o al canal #seguridad en Slack. Nunca seras penalizado por ser cauteloso.",

        "### 13.3 Manejo de Datos de Clientes",
        "Los datos de los clientes de Da&amp;Da Solutions son activos criticos. Las reglas fundamentales son: nunca accedas a datos de produccion de clientes para propositos de desarrollo (usa siempre staging con datos anonimizados); si necesitas acceso excepcional a produccion para resolver un incidente critico, usa el proceso de break-glass documentado en Confluence; nunca copies datos de clientes a tu entorno local, maquina personal, o herramientas de terceros no autorizadas.",

        "---",
        "## 14. Herramientas de Productividad Recomendadas",

        "### 14.1 Gestion del Tiempo y Foco",
        "El trabajo de ingenieria de software requiere periodos largos de concentracion profunda (deep work). En Da&amp;Da Solutions promovemos el bloqueo de tiempo en el calendario para tareas de alta concentracion y el uso del estado 'No molestar' en Slack durante esos bloques. La cultura de reuniones de Da&amp;Da Solutions prioriza la asincronicidad. Antes de agendar una reunion, preguntate si el tema puede resolverse por escrito en Slack o Confluence. Las reuniones sin agenda clara y sin un outcome definido estan explicitamente desalentadas.",

        "### 14.2 Documentar mientras Trabajas",
        "Una de las habilidades mas valiosas que podes desarrollar en Da&amp;Da Solutions es documentar de forma continua mientras realizas tu trabajo. Esto significa: actualizar el comentario del ticket de Jira con las decisiones tomadas y los bloqueantes encontrados, escribir el README del servicio antes de pedir la revision del PR, crear el ADR en Confluence cuando tomes una decision tecnica significativa, y compartir en el canal de Slack del squad los learnings importantes al final de cada tarea compleja.",
        "La documentacion no es una tarea separada: es parte de la definicion de 'done' en Da&amp;Da Solutions. Un ticket no esta completo hasta que la documentacion asociada este actualizada.",

        "---",
        "## 15. Glosario de Terminos Internos",

        "### 15.1 Terminos Organizacionales",
        "- <b>Squad:</b> equipo multidisciplinario autonomo dueno de un dominio de producto. La unidad basica de trabajo en Da&amp;Da Solutions.",
        "- <b>Tribe:</b> agrupacion de squads relacionados bajo un mismo objetivo de producto o de negocio.",
        "- <b>Chapter:</b> comunidad de practica horizontal que agrupa personas con el mismo rol tecnico de distintos squads (ej. el Chapter de Frontend agrupa a todos los ingenieros frontend de la empresa).",
        "- <b>Buddy:</b> el mentor asignado a cada nuevo ingresante durante los primeros 90 dias. Es un par del mismo nivel tecnico con al menos 6 meses de antiguedad.",
        "- <b>EM:</b> Engineering Manager. Lider de personas del equipo tecnico.",
        "- <b>IC:</b> Individual Contributor. Ingeniero que no gestiona personas.",

        "### 15.2 Terminos Tecnicos de Da&Da",
        "- <b>production-ready:</b> criterio que debe satisfacer un servicio para ser desplegado en produccion (tests, observabilidad, health checks, documentacion, runbook).",
        "- <b>ADR:</b> Architecture Decision Record. Documento corto que registra una decision de arquitectura relevante, su contexto, las alternativas consideradas y los fundamentos de la eleccion.",
        "- <b>good-first-issue:</b> ticket de Jira de complejidad baja, pensado para que un nuevo integrante pueda contribuir al codebase de forma significativa sin una curva de aprendizaje excesiva.",
        "- <b>break-glass:</b> proceso de acceso de emergencia a sistemas de produccion con alta auditoria, que requiere aprobacion explicita y genera alertas automaticas al equipo de seguridad.",
        "- <b>DORA metrics:</b> cuatro metricas de rendimiento de equipos de ingenieria: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery, y Change Failure Rate.",
        "[NOTE] Este glosario es un documento vivo. Si encontras un termino que se usa frecuentemente en la empresa y no esta aqui, abri un PR para agregarlo o envia un mensaje al canal #onboarding-feedback.",
    ],

    "backend_guide.pdf": [
        "---",
        "## 12. Migraciones de Base de Datos",

        "### 12.1 Principios de Migraciones Seguras",
        "Las migraciones de base de datos son una de las operaciones de mayor riesgo en produccion. En Da&amp;Da Solutions seguimos el patron de migraciones backward-compatible para poder hacer rollback en cualquier momento sin perdida de datos. Esto implica que nunca se hace un cambio destructivo (DROP TABLE, DROP COLUMN) en la misma migracion en que se despliega el nuevo codigo que deja de usar esa estructura.",
        "El proceso para un cambio destructivo seguro tiene tres fases: Fase 1: agregar la nueva estructura sin eliminar la vieja y deployar el codigo compatible con ambas. Fase 2: migrar los datos a la nueva estructura. Fase 3: una vez verificado que el codigo nuevo funciona correctamente en produccion por al menos 24 horas, eliminar la estructura vieja en una migracion separada.",

        "### 12.2 Herramientas de Migracion",
        "Para Python/FastAPI con SQLAlchemy usamos Alembic. Cada migracion es un archivo Python con funciones upgrade() y downgrade() que deben ser idempotentes cuando sea posible y ejecutarse en menos de 30 segundos en produccion. Para Node.js/NestJS con Prisma usamos Prisma Migrate. El SQL generado automaticamente debe revisarse siempre antes de commitear y se aplica en produccion via prisma migrate deploy en el pipeline de CD.",

        "### 12.3 Indices y Performance en Migraciones",
        "Agregar un indice a una tabla grande en produccion con PostgreSQL puede bloquear las escrituras durante varios minutos si no se hace correctamente. La regla es siempre usar CREATE INDEX CONCURRENTLY para agregar indices en produccion. Alembic no soporta esta opcion de forma nativa, por lo que se debe usar sql explicito en la migracion desactivando las transacciones en la funcion upgrade().",

        "---",
        "## 13. Mensajeria Asincrona con Kafka",

        "### 13.1 Cuando Usar Kafka vs REST Sincrono",
        "Kafka es la opcion correcta cuando: el productor y el consumidor no necesitan conocerse ni estar disponibles al mismo tiempo, la operacion puede fallar y se necesita reintento automatico, el mismo evento necesita ser consumido por multiples servicios (fan-out), o se necesita un registro inmutable y reproducible de todos los eventos del dominio. REST sincrono es preferible cuando el cliente necesita saber el resultado de la operacion inmediatamente para continuar, o cuando la latencia de extremo a extremo es critica.",

        "### 13.2 Convencion de Nombres de Topics",
        "Los nombres de topics de Kafka en Da&amp;Da Solutions siguen la convencion: {dominio}.{entidad}.{evento} en formato kebab-case. Ejemplos: billing.subscription.created, user.account.email-verified, payment.transaction.failed. Los nombres de topics son permanentes una vez creados en produccion; cambiarlos requiere un proceso de migracion complejo.",

        "### 13.3 Schema Registry y Contrato de Mensajes",
        "Todos los mensajes publicados a Kafka deben tener un schema registrado en Confluent Schema Registry. El formato es Avro para mensajes internos y JSON Schema para mensajes externos. Los schemas siguen reglas de compatibilidad BACKWARD: agregar campos opcionales es compatible, eliminar campos no lo es. Los cambios que rompen la compatibilidad requieren un proceso de doble publicacion durante el periodo de migracion.",

        "---",
        "## 14. Patrones de Diseno Aplicados",

        "### 14.1 Repository Pattern",
        "Da&amp;Da Solutions usa el Repository Pattern para aislar la logica de acceso a datos de la logica de negocio. Cada entidad de dominio tiene una interfaz de repositorio que define las operaciones de acceso a datos y una implementacion concreta que usa SQLAlchemy o Prisma. La capa de servicio siempre interactua con la interfaz, nunca con el ORM directamente.",

        "### 14.2 CQRS (Command Query Responsibility Segregation)",
        "Para servicios de alta carga con patrones de lectura muy diferentes a los de escritura, Da&amp;Da Solutions aplica CQRS de manera pragmatica: modelos de datos separados para Commands y Queries, optimizando cada uno para su caso de uso. El modelo de escritura puede usar un schema normalizado optimo para transacciones, mientras que el modelo de lectura puede usar vistas materializadas u otras bases de datos (Redis, Elasticsearch).",

        "### 14.3 Circuit Breaker para Resiliencia",
        "Los servicios que llaman a APIs externas o a otros microservicios deben implementar el patron Circuit Breaker para prevenir fallos en cascada. Usamos tenacity en Python y opossum en Node.js. El Circuit Breaker tiene tres estados: Closed (funcionando normalmente), Open (fallos detectados, todas las llamadas fallan rapido), y Half-Open (periodo de prueba para verificar recuperacion).",

        "### 14.4 Outbox Pattern para Consistencia Eventual",
        "Cuando una operacion debe actualizar la base de datos Y publicar un evento a Kafka de manera atomica, el patron Outbox garantiza la consistencia. Dentro de la misma transaccion de base de datos, se inserta el evento a publicar en una tabla auxiliar (outbox). Un proceso separado (outbox processor) lee periodicamente la tabla y publica los eventos pendientes a Kafka, marcandolos como procesados.",

        "---",
        "## 15. Estandares de Documentacion de Codigo",

        "### 15.1 Docstrings y Comentarios",
        "En Da&amp;Da Solutions el codigo debe ser autoexplicativo en la mayoria de los casos. Los comentarios deben explicar el 'por que', no el 'que'. Un comentario que dice 'incrementa el contador en 1' no agrega valor; un comentario que dice 'se incrementa aqui y no en el handler porque necesitamos contar intentos fallidos antes de la autenticacion' si lo hace.",
        "Los docstrings son obligatorios en: todas las funciones publicas de modulos de libreria, todos los metodos de clases de dominio y repositorios, todos los endpoints de API (el docstring se convierte en la descripcion del endpoint en la documentacion OpenAPI generada automaticamente), y todos los modulos que implementan logica de negocio no trivial.",

        "### 15.2 Generacion Automatica de Documentacion de API",
        "FastAPI genera automaticamente la documentacion OpenAPI 3.1 a partir de los type hints de Python y los docstrings de los endpoint handlers. Para que esta documentacion sea util, cada endpoint debe tener: un docstring con la descripcion funcional del endpoint, modelos Pydantic con Field() descriptivo para cada campo, response_model explicito para cada endpoint, y ejemplos representativos en los modelos.",
        "La documentacion Swagger generada automaticamente es accesible en /docs en todos los ambientes (excepto produccion donde esta restringida a IPs corporativas). La version Redoc esta disponible en /redoc.",

        "### 15.3 Architecture Decision Records (ADRs)",
        "Cuando el equipo toma una decision tecnica significativa (eleccion de una libreria, cambio de patron, adopcion de una nueva tecnologia), se debe escribir un ADR. El formato incluye: Titulo, Fecha, Estado (Propuesto / Aceptado / Deprecado), Contexto, Decision, Alternativas consideradas (con pros y contras), Consecuencias, y Notas.",
        "Los ADRs se almacenan en el directorio docs/adr/ del repositorio con nombres en el formato NNNN-titulo-en-kebab-case.md. Una vez aceptado, un ADR nunca se modifica; si la decision cambia, se crea un nuevo ADR que indica que reemplaza al anterior.",
    ],

    "frontend_guide.pdf": [
        "---",
        "## 12. Accesibilidad (a11y) en Da&Da Solutions",

        "### 12.1 Por Que la Accesibilidad es No-Negociable",
        "La accesibilidad no es una funcionalidad adicional ni un requisito de compliance: es un indicador de calidad de ingenieria. Una interfaz accesible es tambien una interfaz mas usable para todos los usuarios, incluidos aquellos con conexiones lentas, dispositivos antiguos, o que usan el teclado en lugar del mouse. Da&amp;Da Solutions se compromete con el nivel AA del estandar WCAG 2.1 en todas sus interfaces publicas.",

        "### 12.2 Principios WCAG Aplicados al Dia a Dia",
        "Los cuatro principios WCAG (POUR) en la practica:",
        "- <b>Perceptible:</b> todo contenido no textual tiene texto alternativo descriptivo. El contraste entre texto y fondo cumple los ratios minimos: 4.5:1 para texto normal y 3:1 para texto grande.",
        "- <b>Operable:</b> toda la interfaz es navegable completamente con teclado. El orden de tabulacion es logico y predecible. Los elementos interactivos tienen un indicador de foco visible.",
        "- <b>Comprensible:</b> el lenguaje de la interfaz es claro y simple. Los mensajes de error identifican el campo con el problema y describen como corregirlo.",
        "- <b>Robusto:</b> el HTML es semanticamente correcto. Los componentes interactivos usan los roles ARIA apropiados cuando el HTML semantico no es suficiente.",

        "### 12.3 Testing de Accesibilidad",
        "El testing opera en tres niveles: automatizado (axe-core en tests de Playwright, detecta el 30-40% de los problemas), manual (checklist de a11y en el proceso de revision de PRs que afecten la UI), y con usuarios reales (sesiones trimestrales de testing con usuarios con discapacidad visual o motriz).",

        "---",
        "## 13. Internacionalizacion (i18n) y Localizacion (l10n)",

        "### 13.1 La Estrategia de i18n de Da&Da Solutions",
        "Da&amp;Da Solutions tiene clientes en Argentina, Mexico, Colombia, Espana, Brasil y Estados Unidos. Todas las interfaces deben estar disenadas para soportar multiples idiomas desde el dia uno. Usamos react-i18next en todas las aplicaciones React. Los idiomas soportados son: es-AR (idioma base), es-MX, es-ES, en-US, y pt-BR.",

        "### 13.2 Reglas de i18n para Desarrolladores",
        "Reglas obligatorias: nunca escribir strings de texto visible al usuario directamente en el JSX; no asumir longitud de strings (en aleman o portugues los textos son tipicamente un 30-40% mas largos); las fechas y numeros siempre deben formatearse usando las APIs de internacionalizacion del navegador (Intl.DateTimeFormat, Intl.NumberFormat).",

        "---",
        "## 14. Formularios — La Guia Definitiva",

        "### 14.1 Libreria de Formularios: React Hook Form + Zod",
        "Da&amp;Da Solutions usa React Hook Form para gestion de formularios y Zod para la definicion del schema de validacion. Esta combinacion ofrece: performance optima (los inputs no re-renderizan el formulario completo en cada keystroke), type safety completo con TypeScript (el schema de Zod genera automaticamente los tipos), y una excelente experiencia de desarrollo con mensajes de error claros.",

        "### 14.2 Experiencia de Usuario en Formularios",
        "Principios de UX para formularios: validar en tiempo real (onBlur) pero solo mostrar errores despues de que el usuario haya interactuado con el campo; cuando hay un error de validacion del servidor (422), mapear los errores de campo especifico con setError de React Hook Form; nunca deshabilitar el boton de submit — en su lugar mostrar estado de carga visible.",

        "---",
        "## 15. Optimizacion de Performance para Front-end",

        "### 15.1 Metricas de Performance: Core Web Vitals",
        "Da&amp;Da Solutions usa las Core Web Vitals como metricas de performance objetivo:",
        "- <b>Largest Contentful Paint (LCP):</b> tiempo hasta que el elemento mas grande del viewport esta renderizado. Objetivo: menos de 2.5 segundos.",
        "- <b>Interaction to Next Paint (INP):</b> latencia de respuesta a interacciones del usuario. Objetivo: menos de 200 milisegundos.",
        "- <b>Cumulative Layout Shift (CLS):</b> cuanto se mueve el layout inesperadamente durante la carga. Objetivo: menos de 0.1.",

        "### 15.2 Estrategias de Optimizacion",
        "Las estrategias mas impactantes en el stack React de Da&amp;Da Solutions: code splitting por ruta con React.lazy y Suspense; optimizacion de imagenes con componentes que generan srcsets para formatos modernos (WebP, AVIF); prefetching de datos criticos con React Query; virtualizacion de listas largas con react-virtual para no renderizar miles de elementos en el DOM; y evitar renders innecesarios con React.memo y useCallback aplicados de forma estrategica.",

        "### 15.3 Bundle Analysis y Monitoreo Continuo",
        "Da&amp;Da Solutions ejecuta un analisis del bundle de JavaScript en cada PR que afecte el frontend. Una alerta en el pipeline de CI notifica al equipo cuando el tamano del bundle principal crece mas de un 10% respecto al baseline de la rama main. El monitoreo de Core Web Vitals en produccion se realiza usando el script web-vitals reportando a Google Analytics 4 y el Real User Monitoring (RUM) de Datadog.",

        "### 15.4 Estrategia de Caching en el Front-end",
        "React Query es la libreria estandar de Da&amp;Da Solutions para la gestion de estado del servidor en el cliente. La estrategia de caching sigue estas reglas: el staleTime de cada query debe configurarse en funcion de la frecuencia de actualizacion real del dato (datos de perfil de usuario: 5 minutos; precios de lista: 30 minutos); usar query keys como identificadores unicos y descriptivos; y usar el patron de optimistic updates para operaciones de escritura que deben sentirse instantaneas.",
    ],

    "ai_agents.pdf": [
        "---",
        "## 11. Evaluacion y Benchmarking de Agentes",

        "### 11.1 Por Que Evaluar es tan Importante como Construir",
        "Un agente de IA sin un conjunto de evaluaciones robustas es un agente en el que no se puede confiar para produccion. La evaluacion de agentes es significativamente mas compleja que la evaluacion de modelos de clasificacion tradicionales: las respuestas son abiertas, el espacio de inputs posibles es virtualmente infinito, y la calidad de una respuesta puede depender del contexto de la conversacion completa.",
        "En Da&amp;Da Solutions no deployamos ningun componente de agente a produccion sin un harness de evaluacion que corra en el pipeline de CI y que verifique que el agente cumple los criterios de calidad minimos definidos por el Product Manager.",

        "### 11.2 Tipos de Evaluaciones para Agentes",
        "Tres tipos principales de evaluaciones:",
        "- <b>Evaluaciones basadas en criterios deterministas:</b> para casos donde la respuesta correcta es unica y verificable. El agente llama a la herramienta correcta con los parametros correctos, o extrae correctamente un dato de un texto.",
        "- <b>Evaluaciones basadas en LLM como juez (LLM-as-Judge):</b> para casos donde la calidad es subjetiva. Un segundo modelo de lenguaje evalua la respuesta del agente en base a una rubrica definida: factualidad, concision, y tono apropiado.",
        "- <b>Evaluaciones con expertos humanos:</b> indispensables para validar que las evaluaciones automaticas se correlacionan con la satisfaccion de usuarios reales. Se realizan periodicamente con muestras del trafico de produccion.",

        "### 11.3 Conjunto de Datos de Evaluacion (Eval Sets)",
        "Cada agente deployado en produccion tiene un eval set asociado, version-controlado en el repositorio del agente. Contiene: ejemplos positivos (inputs con respuestas correctas), ejemplos negativos (inputs donde el agente NO debe realizar ciertas acciones), y ejemplos de casos extremos identificados durante el desarrollo o en produccion. Cada bug de produccion relacionado con el comportamiento del agente debe convertirse en un nuevo caso en el eval set para prevenir regresiones.",

        "---",
        "## 12. Seguridad en Agentes de IA",

        "### 12.1 Prompt Injection",
        "El prompt injection es el equivalente del SQL injection para los agentes de IA. Ocurre cuando datos no confiables (input del usuario, contenido de documentos, respuestas de APIs externas) contienen instrucciones que modifican el comportamiento del agente de maneras no previstas.",
        "Las mitigaciones que aplicamos: delimitar claramente con marcadores especiales los datos no confiables en los prompts; no incluir datos sensibles en el contexto si no son necesarios; implementar un filtro de salida (output guard) que detecta respuestas que contengan el system prompt; y usar modelos con instruction hierarchy donde las instrucciones del sistema tienen mayor prioridad que los mensajes del usuario.",

        "### 12.2 Privilegio Minimo para Agentes",
        "El principio de privilegio minimo aplica a los agentes igual que a los usuarios y sistemas. Un agente de soporte al cliente que responde preguntas de FAQs no debe tener acceso a la herramienta de procesamiento de reembolsos. En la arquitectura de Da&amp;Da Solutions, los tools disponibles para cada agente se definen en su configuracion (no en el system prompt) y son validados por el orchestrator antes de ejecutarse.",

        "### 12.3 Auditoria de Decisiones del Agente",
        "Toda accion ejecutada por un agente que involucre herramientas con efectos secundarios debe quedar registrada en un audit log inmutable con: el timestamp exacto, el agente que tomo la decision, el mensaje del usuario que desencadeno la accion, el razonamiento del agente (chain of thought), el tool call con sus parametros exactos, y el resultado de la ejecucion.",

        "---",
        "## 13. Agentes en Produccion — Operaciones",

        "### 13.1 Monitoreo Especifico para Agentes",
        "Ademas del monitoreo estandar, los agentes de IA requieren metricas especificas:",
        "- <b>Token usage per request:</b> para controlar costos y detectar runaway loops.",
        "- <b>Tool call success rate:</b> porcentaje de llamadas a herramientas que se completan exitosamente.",
        "- <b>Tasa de rechazo de guardrails:</b> cuantas respuestas son bloqueadas por los filtros de seguridad.",
        "- <b>User satisfaction score (CSAT):</b> obtenido via thumbs up/down en la interfaz.",
        "- <b>Escalacion a humano:</b> tasa de conversaciones que el agente derivo a un operador humano.",

        "### 13.2 Rollouts Graduales para Cambios de Agente",
        "Los cambios en los agentes se despliegan usando rollout gradual: 1% del trafico primero, monitoreo durante 24 horas, luego 10%, 50% y finalmente 100%. En cada etapa se comparan las metricas clave del nuevo agente vs el anterior usando un A/B test estadisticamente riguroso.",

        "---",
        "## 14. Glosario de Terminos de IA Generativa",

        "### 14.1 Conceptos Fundamentales",
        "- <b>Token:</b> la unidad basica de texto que procesa un LLM. Aproximadamente 4 caracteres en ingles o 3 en espanol. Los costos de los APIs de LLMs se miden en tokens.",
        "- <b>Context window:</b> la cantidad maxima de tokens que puede procesar un LLM en una sola llamada, incluyendo el system prompt, el historial de conversacion, y la respuesta generada.",
        "- <b>Temperature:</b> parametro que controla la aleatoriedad de las respuestas del modelo. Valores cercanos a 0 producen respuestas deterministas; valores cercanos a 1 producen respuestas mas variadas y creativas.",
        "- <b>RAG (Retrieval-Augmented Generation):</b> patron arquitectonico que combina un sistema de busqueda de documentos relevantes con un LLM. El LLM recibe los documentos recuperados como contexto adicional para responder con informacion especifica y actualizada.",
        "- <b>Embedding:</b> representacion vectorial de un texto en un espacio de alta dimension donde textos semanticamente similares tienen vectores cercanos. Base de los sistemas RAG y de busqueda semantica.",
        "- <b>Grounding:</b> tecnica para anclar las respuestas del modelo a fuentes de informacion verificables, reduciendo las alucinaciones.",
        "- <b>Hallucination:</b> cuando un LLM genera informacion factualmente incorrecta con aparente confianza. Es uno de los riesgos principales a mitigar en sistemas de produccion.",
        "- <b>Few-shot prompting:</b> tecnica de prompting que incluye ejemplos de inputs y outputs esperados en el prompt para guiar el comportamiento del modelo sin necesidad de fine-tuning.",
        "- <b>Fine-tuning:</b> proceso de ajuste de los pesos de un modelo pre-entrenado usando un dataset especifico para mejorar su performance en una tarea particular.",

        "### 14.2 Conceptos de Arquitectura de Agentes",
        "- <b>Tool / Function calling:</b> capacidad de los LLMs modernos de identificar cuando deben llamar a una funcion externa y con que argumentos, en lugar de responder directamente con texto.",
        "- <b>Orchestrator:</b> el componente que coordina la ejecucion de un agente multi-step, decidiendo cuando llamar al LLM, cuando ejecutar herramientas, y cuando terminar el ciclo.",
        "- <b>ReAct (Reason + Act):</b> patron de prompting para agentes que alterna ciclos de razonamiento (Thought) con ejecucion de acciones (Action) y observacion de resultados (Observation).",
        "- <b>Agent loop:</b> el ciclo iterativo del agente: recibir input, razonar, ejecutar herramienta (opcional), observar resultado, razonar nuevamente, hasta producir una respuesta final.",
        "- <b>Multi-agent system:</b> arquitectura donde multiples agentes especializados colaboran para resolver tareas complejas, comunicandose entre si y coordinando su trabajo.",
    ],

    "data_persistence.pdf": [
        "---",
        "## 9. Estrategias de Backup y Recuperacion",

        "### 9.1 La Regla 3-2-1 de Backups",
        "Da&amp;Da Solutions aplica la regla 3-2-1 para todos los datos criticos de produccion: al menos 3 copias del dato, en al menos 2 tipos de almacenamiento distintos, con al menos 1 copia fuera del datacenter principal (offsite). En la practica: la base de datos primaria en produccion cuenta como copia 1; la replica de lectura sincrona en la misma region como copia 2; y el backup diario a S3 en una region diferente como copia 3.",

        "### 9.2 Backups de PostgreSQL con pgBackRest",
        "Para los clusters de PostgreSQL usamos pgBackRest con: backups completos semanales, backups incrementales diarios, y continuous WAL archiving a S3 que permite point-in-time recovery (PITR) con granularidad de hasta 1 segundo. Todos los backups se cifran con AES-256 usando claves del KMS antes de ser enviados a S3. Semanalmente, el sistema realiza un test de restore automatico en un cluster efimero aislado para validar la integridad del backup.",

        "### 9.3 Recuperacion ante Desastres — RTO y RPO",
        "Los objetivos de recuperacion para los sistemas de persistencia de Da&amp;Da Solutions:",
        "- <b>PostgreSQL primario (Aurora):</b> RPO: 0 (replica sincrona). RTO: menos de 30 segundos en failover automatico.",
        "- <b>PostgreSQL con replica inter-region:</b> RPO: menos de 1 segundo. RTO: 2-5 minutos para promover la replica.",
        "- <b>Recuperacion desde backup S3:</b> RPO: hasta 24 horas o PITR a cualquier punto de los ultimos 7 dias. RTO: 2-6 horas segun el tamano de la base de datos.",
        "- <b>DynamoDB:</b> RPO: 0 con Point-in-Time Recovery activo. RTO: menos de 1 minuto con tablas globales.",

        "---",
        "## 10. Cifrado y Seguridad en la Capa de Persistencia",

        "### 10.1 Cifrado en Reposo",
        "Todos los sistemas de persistencia de Da&amp;Da Solutions tienen cifrado en reposo habilitado de forma obligatoria. Para Amazon RDS Aurora y DynamoDB, el cifrado es con AWS KMS usando Customer Managed Keys (CMK) para tener control total sobre la rotacion y la auditoria de uso. Para datos que requieren el maximo nivel de proteccion (numeros de documentos de identidad, informacion de salud), adicionalmente al cifrado de disco aplicamos cifrado a nivel de campo usando claves derivadas especificas por tenant.",

        "### 10.2 Gestion de Credenciales de Base de Datos",
        "Las credenciales de base de datos en Da&amp;Da Solutions nunca son estaticas. Usamos HashiCorp Vault con el Database Secrets Engine para generar credenciales dinamicas con TTL corto para cada servicio. El flujo es: el servicio se autentica con Vault usando su identidad de Kubernetes, Vault genera un usuario y contrasena temporales con los permisos minimos, y el servicio usa esas credenciales hasta que expiran (tipicamente 1 hora para credenciales de lectura/escritura).",

        "---",
        "## 11. Multi-Tenancy en la Capa de Datos",

        "### 11.1 Modelos de Aislamiento de Datos por Tenant",
        "Da&amp;Da Solutions sirve a multiples clientes desde la misma infraestructura. Los tres modelos de aislamiento:",
        "- <b>Database per tenant:</b> cada cliente tiene su propia base de datos independiente. Mayor aislamiento, mayor costo operacional. Usado para clientes Enterprise con requisitos regulatorios estrictos.",
        "- <b>Schema per tenant (PostgreSQL):</b> todos los tenants en el mismo servidor pero en schemas separados. Buen balance entre aislamiento y eficiencia.",
        "- <b>Row-level security (RLS):</b> todos los tenants comparten las mismas tablas pero cada fila tiene una columna tenant_id y PostgreSQL aplica politicas de seguridad a nivel de fila automaticamente.",

        "### 11.2 Row-Level Security en PostgreSQL",
        "La implementacion de RLS en Da&amp;Da Solutions: todas las tablas multi-tenant tienen columna tenant_id NOT NULL. Se activa RLS con ALTER TABLE nombre ENABLE ROW LEVEL SECURITY. Las politicas usan current_setting('app.current_tenant_id'). La aplicacion establece el tenant_id al inicio de cada transaccion con SET LOCAL app.current_tenant_id = 'tenant-uuid'. Esto garantiza que incluso ante un bug en el codigo, PostgreSQL automaticamente filtra los resultados al tenant activo.",

        "---",
        "## 12. Bases de Datos NoSQL — Casos de Uso Especificos",

        "### 12.1 DynamoDB para Acceso de Baja Latencia y Alta Escala",
        "Da&amp;Da Solutions usa DynamoDB para casos de uso donde se requiere latencia de un solo digito de milisegundos a cualquier escala y donde los patrones de acceso son conocidos y bien definidos. Casos de uso tipicos: almacenamiento de sesiones de usuario, cache de resultados de computaciones costosas con TTL automatico, almacenamiento de configuraciones por tenant con acceso frecuente, y tablas de lookup de alta frecuencia de lectura.",
        "El diseno del partition key es la decision mas critica en DynamoDB. Un partition key con baja cardinalidad crea hot partitions que degradan la performance. El patron de single-table design, donde multiples tipos de entidades coexisten en la misma tabla con atributos PK y SK que incluyen el tipo de entidad, es la aproximacion que Da&amp;Da Solutions adopta para la mayoria de sus tablas DynamoDB.",

        "### 12.2 Redis para Cache y Estructuras de Datos Especializadas",
        "Da&amp;Da Solutions usa Amazon ElastiCache para Redis en los siguientes casos de uso: cache de respuestas de API de alta frecuencia (rate de hit esperado mayor al 70%), implementacion de rate limiting distribuido usando el algoritmo sliding window log con sorted sets, colas de mensajes simples para jobs en background, pub/sub para notificaciones en tiempo real, y Leaderboards y rankings usando sorted sets con operaciones ZADD/ZRANGE en O(log N).",
        "Redis se usa como cache, no como base de datos primaria. Los datos almacenados deben poder regenerarse desde la fuente de verdad (PostgreSQL, DynamoDB) en caso de perdida. Toda clave en Redis debe tener un TTL explicitamente configurado para evitar que la memoria crezca indefinidamente.",

        "---",
        "## 13. Monitoreo de la Capa de Datos",

        "### 13.1 Metricas Criticas de PostgreSQL",
        "Las metricas de PostgreSQL que Da&amp;Da Solutions monitorea en Grafana incluyen: tasa de hit del shared_buffers cache (objetivo mayor al 99%), numero de conexiones activas vs el maximo configurado (alerta cuando supera el 80%), duracion de las queries mas lentas (P99 en pg_stat_statements), tamano del replication lag en replicas (alerta cuando supera los 10 segundos), numero de deadlocks por hora, y tasa de uso del autovacuum.",

        "### 13.2 Alertas de Performance de Base de Datos",
        "Da&amp;Da Solutions tiene las siguientes alertas criticas configuradas en PagerDuty para la capa de datos: conexiones de base de datos al 90% del maximo configurado (alerta P2), replication lag superior a 60 segundos (alerta P1), query con duracion mayor a 5 minutos en ejecucion (alerta P2), tabla o indice con tamano creciendo mas de un 10% por hora (alerta informativa), y disponibilidad del cluster inferior al 99.9% en la ventana de 5 minutos (alerta P1).",
    ],

    "devops_cicd.pdf": [
        "---",
        "## 10. Seguridad en el Pipeline (DevSecOps)",

        "### 10.1 Shift-Left Security",
        "El concepto de 'shift-left security' significa integrar las practicas de seguridad lo mas temprano posible en el ciclo de desarrollo. En Da&amp;Da Solutions, la seguridad es parte del dia a dia del desarrollo: los desarrolladores tienen extensiones de analisis de seguridad en sus IDEs, el pipeline de CI ejecuta multiples capas de analisis antes de que el codigo llegue a staging, y los ingenieros reciben capacitacion anual en desarrollo seguro basada en el OWASP Top 10.",

        "### 10.2 Software Composition Analysis (SCA)",
        "El 80% del codigo en cualquier aplicacion moderna es codigo de terceros. Cada dependencia puede tener vulnerabilidades conocidas (CVEs). Da&amp;Da Solutions ejecuta SCA en cada PR y diariamente en la rama main:",
        "- <b>Python:</b> pip-audit y Safety escanean todas las dependencias en pyproject.toml y poetry.lock.",
        "- <b>Node.js:</b> npm audit y Snyk escanean package.json y package-lock.json.",
        "- <b>Contenedores:</b> Trivy escanea las imagenes Docker en busca de vulnerabilidades en paquetes del sistema operativo.",
        "Los hallazgos CRITICAL bloquean el merge inmediatamente. Los HIGH deben remediarse dentro de las 48 horas. Los MEDIUM se agregan al backlog de seguridad.",

        "### 10.3 Secretos en el Pipeline",
        "Ninguna credencial debe aparecer jamas en el codigo fuente ni en la historia de git. Medidas preventivas: GitGuardian monitorea todos los pushes a GitHub en tiempo real y bloquea cualquier push que contenga patrones de secretos conocidos; detect-secrets corre en el pipeline de CI como verificacion adicional; y GitHub Advanced Security escanea la historia completa del repositorio. Si un secreto es accidentalmente commiteado: rotarlo inmediatamente es la primera accion, luego informar al equipo de seguridad, y finalmente limpiar la historia con git-filter-repo.",

        "---",
        "## 11. Kubernetes — Configuracion y Buenas Practicas",

        "### 11.1 Estructura de los Manifiestos de Kubernetes",
        "Todos los manifiestos de Kubernetes en Da&amp;Da Solutions estan organizados usando Kustomize con la siguiente estructura: base/ (recursos comunes a todos los ambientes), overlays/development/, overlays/staging/, y overlays/production/. Esto permite mantener una fuente de verdad unica para la configuracion base y solo especificar las diferencias por ambiente.",

        "### 11.2 Resource Requests y Limits",
        "Todos los contenedores en Kubernetes deben tener definidos resource requests y limits. Sin requests, el scheduler no puede tomar decisiones de placement informadas. Sin limits, un contenedor puede consumir todos los recursos del nodo y degradar pods vecinos. Los valores de requests y limits se determinan midiendo el consumo real del servicio en staging bajo carga representativa. La regla general: requests = consumo promedio, limits = consumo maximo tolerable (tipicamente 2-3x los requests).",

        "### 11.3 Pod Disruption Budgets",
        "Para servicios criticos, Da&amp;Da Solutions define Pod Disruption Budgets (PDB) que garantizan que siempre haya un minimo de pods disponibles durante operaciones de mantenimiento (drenaje de nodos, upgrades de cluster). El PDB tipico para un servicio con 3 replicas especifica que nunca se puede tener menos de 2 pods disponibles simultaneamente.",

        "---",
        "## 12. Gestion de Incidentes desde el Punto de Vista de DevOps",

        "### 12.1 El Rol de DevOps en un Incidente de Produccion",
        "Cuando ocurre un incidente de produccion, el equipo de DevOps/SRE asume el rol de soporte de infraestructura: verificar que los dashboards muestran el estado correcto, acceder a logs y traces para ayudar en el diagnostico, ejecutar acciones de infraestructura necesarias (escalar recursos, hacer rollback, deshabilitar un componente), y mantener el status page actualizado.",

        "### 12.2 Runbooks Operacionales",
        "Cada servicio critico de Da&amp;Da Solutions tiene un runbook operacional en Confluence que documenta los procedimientos para los escenarios de falla mas comunes. Un runbook efectivo incluye: el sintoma observable (que se ve en los dashboards o logs), la causa mas probable, los pasos de verificacion para confirmar la causa, y los pasos de remediacion ordenados por probabilidad de exito. Los runbooks se vinculan directamente desde las alertas de Grafana/PagerDuty.",

        "### 12.3 Post-Mortems sin Culpa",
        "La cultura de Post-Mortem sin culpa (blameless) es un pilar de la ingenieria de confiabilidad en Da&amp;Da Solutions. El objetivo no es identificar al 'culpable' sino entender como el sistema permitio que el incidente ocurriera. El Post-Mortem incluye: timeline del incidente con timestamps exactos, impacto en clientes y negocio, causa raiz identificada con los '5 Porques', factores contribuyentes, items de accion con responsables y fechas, y reconocimiento de las cosas que funcionaron bien durante la respuesta.",

        "---",
        "## 13. Disaster Recovery y Business Continuity",

        "### 13.1 Niveles de Criticidad de los Sistemas",
        "Da&amp;Da Solutions clasifica sus sistemas en cuatro niveles de criticidad que determinan los objetivos de recuperacion (RTO y RPO):",
        "- <b>Nivel 1 - Critico:</b> sistemas cuya indisponibilidad impacta directamente la capacidad de generar ingresos o cumplir obligaciones contractuales. RTO: 15 minutos. RPO: 0. Ejemplos: API Gateway, servicio de autenticacion, motor de pagos.",
        "- <b>Nivel 2 - Importante:</b> sistemas cuya indisponibilidad afecta la experiencia del usuario de forma significativa. RTO: 1 hora. RPO: 1 hora. Ejemplos: servicio de notificaciones, generador de reportes.",
        "- <b>Nivel 3 - Normal:</b> sistemas cuya indisponibilidad es tolerable por periodos cortos. RTO: 4 horas. RPO: 24 horas.",
        "- <b>Nivel 4 - Bajo impacto:</b> sistemas internos o de soporte. RTO: 8 horas. RPO: 24 horas.",

        "### 13.2 Multi-Region para Sistemas de Nivel 1",
        "Los sistemas de Nivel 1 se despliegan en configuracion activo-activo o activo-pasivo en dos regiones de AWS: sa-east-1 (Sao Paulo, primaria) y us-east-1 (N. Virginia, secundaria). El enrutamiento de trafico entre regiones se gestiona con Amazon Route 53 con health checks y failover automatico configurado con TTL de 30 segundos. Las bases de datos de Nivel 1 usan Aurora Global Database para replicacion cross-region con lag tipico de menos de 1 segundo.",

        "### 13.3 Drill de Disaster Recovery",
        "Da&amp;Da Solutions realiza un drill de disaster recovery completo semestralmente (en enero y en julio). El drill simula la perdida total de la region primaria y verifica que todos los sistemas de Nivel 1 y Nivel 2 pueden recuperarse dentro de sus RTO y RPO objetivos. El resultado del drill se documenta en un informe que incluye los tiempos de recuperacion reales vs los objetivos, los incidentes encontrados durante el drill, y los items de accion para cerrar las brechas identificadas.",
    ],

    "microservices_architecture.pdf": [
        "---",
        "## 11. Service Mesh con Istio",

        "### 11.1 Que es un Service Mesh y Por Que lo Usamos",
        "Un service mesh es una capa de infraestructura dedicada para gestionar la comunicacion servicio-a-servicio en una arquitectura de microservicios. Da&amp;Da Solutions usa Istio en todos sus clusters de produccion. Istio opera inyectando un proxy sidecar (Envoy) en cada pod, que intercepta todo el trafico sin que la aplicacion tenga que modificarse.",
        "Los beneficios obtenidos: mTLS automatico para toda la comunicacion interna, traffic management granular para canary deployments, observabilidad de red completa, y politicas de autorizacion a nivel de servicio.",

        "### 11.2 Traffic Management con Istio",
        "Los recursos principales de Istio para traffic management:",
        "- <b>VirtualService:</b> define como enrutar el trafico hacia un servicio. Permite split de trafico por porcentaje, enrutamiento basado en headers HTTP, y retries con backoff exponencial configurados de forma centralizada.",
        "- <b>DestinationRule:</b> define las politicas para el trafico hacia un destino: configuracion del circuit breaker (outlier detection), configuracion del pool de conexiones, y definicion de subsets (v1, v2, canary) que el VirtualService puede referenciar.",

        "### 11.3 Seguridad con Istio: AuthorizationPolicy",
        "Istio permite definir politicas de autorizacion que restringen que servicios pueden comunicarse entre si. Las politicas se definen como AuthorizationPolicy en YAML y se aplican en tiempo de ejecucion sin reiniciar pods. El modo de auditoria permite activar las politicas en modo 'log only' antes de aplicarlas en modo blocking, para verificar que no rompan comunicaciones legitimas.",

        "---",
        "## 12. Patrones de Comunicacion Avanzados",

        "### 12.1 Saga Pattern para Transacciones Distribuidas",
        "Las transacciones ACID que abarcan multiples microservicios son el problema mas dificil de la arquitectura de microservicios. Da&amp;Da Solutions usa el patron Saga con coreografia (choreography-based): cada servicio escucha eventos de Kafka y publica sus propios eventos de exito o fallo. No hay un orquestador central.",
        "Ejemplo de Saga de creacion de orden: el servicio de Ordenes publica order.created, el servicio de Inventario reserva stock, el servicio de Pagos procesa el pago, y el servicio de Envios inicia la logistica. Si cualquier paso falla, cada servicio ejecuta su transaccion compensatoria (liberar stock, reembolsar el pago).",

        "### 12.2 API Gateway Pattern",
        "Da&amp;Da Solutions usa un API Gateway como punto de entrada unico para todos los clientes externos. El API Gateway centraliza: autenticacion (validacion del JWT), rate limiting por cliente y plan de suscripcion, request routing, response aggregation (BFF pattern para clientes moviles), y observabilidad (logging de todas las requests con trace_id).",

        "### 12.3 Event-Driven Architecture — Principios",
        "La arquitectura orientada a eventos sigue estos principios: los eventos representan hechos del pasado (inmutables), los productores no conocen a sus consumidores (loose coupling), cada evento debe ser auto-contenido (incluir toda la informacion necesaria), y los consumidores deben ser idempotentes (procesar el mismo evento multiples veces produce el mismo resultado).",

        "---",
        "## 13. Observabilidad Distribuida",

        "### 13.1 El Problema del Diagnostico en Microservicios",
        "En un monolito, cuando algo falla, el stack trace te dice exactamente donde. En una arquitectura de microservicios donde una request puede pasar por 10 o 15 servicios diferentes, el diagnostico es radicalmente diferente. La observabilidad distribuida hace posible el diagnostico en este contexto a traves de los tres pilares: logs (que paso), metricas (cuanto tarda y cuanto falla), y traces (en que parte del flujo ocurre el problema).",

        "### 13.2 Tracing Distribuido con Tempo y Grafana",
        "Da&amp;Da Solutions usa Grafana Tempo como backend de almacenamiento de traces. El flujo: cada request que llega al API Gateway recibe un trace_id unico (W3C Trace Context). Los SDKs de OpenTelemetry en cada servicio propagan automaticamente el trace_id en los headers HTTP salientes y en los mensajes de Kafka. En Grafana es posible navegar de una metrica anormal directamente a los traces que contribuyeron a ella, y desde un trace a los logs del intervalo de tiempo correspondiente.",

        "### 13.3 Service Level Objectives (SLOs) y Error Budgets",
        "Un SLO es un objetivo interno de calidad de servicio. Ejemplo de SLO para el servicio de autenticacion: 'El 99.9% de las requests de login deben completarse en menos de 500ms en un periodo de 30 dias'. El error budget es el margen de incumplimiento permitido (0.1% = 43.8 minutos al mes). Cuando se consume el error budget, el equipo detiene el desarrollo de nuevas features y se enfoca exclusivamente en mejorar la confiabilidad.",

        "---",
        "## 14. Gobernanza y Estandares para Microservicios",

        "### 14.1 El Registro de Servicios (Service Catalog)",
        "Da&amp;Da Solutions mantiene un Service Catalog centralizado en Backstage (backstage.dadacode.io) donde cada microservicio tiene una ficha que incluye: nombre y descripcion del servicio, equipo responsable (con contacto de guardia), repositorio de GitHub, documentacion tecnica, estado actual (saludable, degradado, en mantenimiento), dependencias del servicio, y consumidores del servicio.",
        "El Service Catalog se actualiza automaticamente desde los repositorios de GitHub usando el backstage-github-discovery plugin. Cada servicio debe tener un archivo catalog-info.yaml en la raiz del repositorio para ser registrado automaticamente.",

        "### 14.2 Estandares de API para Microservicios Internos",
        "Ademas de los estandares de API REST documentados en la Guia de Back-end, los microservicios internos de Da&amp;Da Solutions deben cumplir los siguientes requisitos adicionales:",
        "- <b>Contrato de API versionado:</b> el esquema de la API (OpenAPI o Protobuf para gRPC) debe estar en el repositorio y versionarse con el codigo.",
        "- <b>Contract testing con Pact:</b> todos los consumer-provider pairs deben tener contratos en el Pact Broker.",
        "- <b>Documentacion de SLOs:</b> cada servicio debe publicar sus SLOs en el Service Catalog.",
        "- <b>Runbook operacional:</b> enlazado desde el Service Catalog y desde las alertas de PagerDuty.",

        "### 14.3 Proceso de Introduccion de un Nuevo Microservicio",
        "Introducir un nuevo microservicio en la plataforma de Da&amp;Da Solutions no es una decision que se toma de forma unilateral. El proceso requerido es: escribir un RFC (Request for Comments) describiendo el nuevo servicio, su caso de uso, sus dependencias, y por que no puede implementarse dentro de un servicio existente. El RFC es revisado por al menos dos Staff Engineers y el Engineering Manager del area en una sesion de arquitectura.",
        "Si el RFC es aprobado, se instancia el repositorio desde el template corporativo (dada-solutions/service-template), se registra el servicio en el Service Catalog, y se crea el proyecto correspondiente en Jira. Este proceso existe porque el costo de operar cada nuevo microservicio adicional (despliegue, monitoreo, seguridad, actualizaciones) es significativo. La fragmentacion excesiva de la logica de negocio en microservicios demasiado pequenos (nanoservicios) es un antipatron conocido que genera mas complejidad de la que resuelve.",
    ],
}


if __name__ == "__main__":
    script_dir_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir_path)
    docs_dir = os.path.join(project_root, "docs")

    print(f"\nExpandiendo PDFs en: {docs_dir}\n")

    for orig in ORIGINAL_DOCS:
        fname = orig["filename"]
        if fname not in EXTRA:
            print(f"  [SKIP]  {fname}  (sin bloques extra definidos)")
            continue

        combined_blocks = list(orig["blocks"]) + EXTRA[fname] + ANNEXES
        out_path = os.path.join(docs_dir, fname)
        make_pdf(
            out_path,
            orig["title"],
            orig["subtitle"],
            combined_blocks,
        )

    print("\nListo.")
