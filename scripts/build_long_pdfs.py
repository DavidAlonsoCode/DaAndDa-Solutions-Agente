"""
build_long_pdfs.py
Genera 7 PDFs de ~25 paginas para Da&Da Solutions.
Ejecutar desde la raiz del proyecto: venv\\Scripts\\python scripts\\build_long_pdfs.py
Los PDFs se generan en la carpeta docs_new/ (no toca docs/).
"""
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak,
    KeepTogether
)
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

# ───────────────────────────────────────────────────────────────
# ESTILOS
# ───────────────────────────────────────────────────────────────
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
                              textColor=colors.HexColor("#444444"),
                              borderPadding=6),
}


# ───────────────────────────────────────────────────────────────
# BUILDER
# ───────────────────────────────────────────────────────────────

def _story(title, subtitle, blocks):
    """Convierte titulo + lista de bloques en una lista de Flowables."""
    story = []

    # --- Portada ---
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

    # --- Contenido ---
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
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return "?"
    return len(PdfReader(path).pages)


# ═══════════════════════════════════════════════════════════════
# CONTENIDOS  (7 documentos, ~25 paginas cada uno)
# ═══════════════════════════════════════════════════════════════

DOCS = []

# ─────────────────────────────────────────────────────────────
# 1. ONBOARDING  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="onboarding.pdf",
    title="Manual de Onboarding para Nuevos Desarrolladores",
    subtitle="Tu guia completa para los primeros 90 dias en Da&amp;Da Solutions",
    blocks=[
        "## 1. Bienvenida de la Direccion de Ingenieria",
        "Bienvenido a Da&amp;Da Solutions. Somos una empresa tecnologica fundada en 2014 con sede principal en Buenos Aires, Argentina, y oficinas regionales en Ciudad de Mexico, Bogota y Madrid. En 12 anios de historia hemos crecido de un equipo de 4 personas a mas de 350 colaboradores distribuidos en cuatro continentes, manteniendo siempre el mismo ADN: tecnologia de impacto, hecha con cuidado.",
        "Nuestra mision es transformar los negocios de nuestros clientes a traves de soluciones de software de alto impacto, combinando excelencia tecnica con una cultura de innovacion continua. En la actualidad prestamos servicios a mas de 80 empresas de mediana y gran escala en verticales tan diversas como fintech, salud digital, e-commerce y logistica.",
        "Este manual ha sido escrito con cariño por el equipo de People &amp; Engineering para guiarte en tus primeros 90 dias. Guardalo como referencia permanente y no dudes en consultar a tu Buddy o a tu Team Lead ante cualquier duda.",
        "---",
        "## 2. Nuestros Valores Fundacionales",
        "Creemos firmemente en tres valores que guian todo lo que hacemos en Da&amp;Da Solutions:",
        "### 2.1 Colaboracion Radical",
        "El conocimiento que no se comparte muere. En Da&amp;Da el trabajo individual brillante es siempre superado por el trabajo colaborativo ordinario. Fomentamos la cultura de preguntar, ensenar y documentar. Nadie es 'dueno' de una pieza de conocimiento: todos somos custodios del conocimiento colectivo.",
        "Esto se manifiesta en practicas concretas: pair programming cuando hay bloqueos complejos, revisiones de codigo como espacios de aprendizaje mutuo, documentacion como ciudadana de primera clase en cada tarea, y sesiones de 'show &amp; tell' mensuales donde cualquier persona puede compartir algo que aprendio.",
        "### 2.2 Excelencia Tecnica Sostenible",
        "Construimos software para que dure. No tomamos atajos tecnicos que aceleren el presente a expensas del futuro. La deuda tecnica no es un pecado — es una decision consciente con fecha de vencimiento conocida. Cuando la tomamos, la documentamos, la medimos y la pagamos con interes.",
        "La excelencia no significa perfeccionismo paralizante. Significa entregar codigo que funciona, que esta testeado, que es legible para el siguiente desarrollador, y que puede ser modificado con confianza seis meses despues por alguien que nunca lo vio.",
        "### 2.3 Responsabilidad con el Impacto",
        "Nuestro software es usado por personas reales para tomar decisiones reales. Un bug en produccion puede afectar el salario de alguien, la atencion medica de un paciente, o la cadena de suministro de una empresa. Esta responsabilidad es enorme y la tomamos en serio. Cada line de codigo que mergeamos a main es nuestra firma.",
        "---",
        "## 3. Estructura Organizacional",
        "Da&amp;Da Solutions opera bajo un modelo de organizacion matricial con equipos funcionales y squads de producto. La compania se divide en cuatro grandes areas:",
        "- <b>Engineering:</b> Backend, Frontend, Infraestructura/DevOps e Inteligencia Artificial.",
        "- <b>Product:</b> Product Managers, UX Researchers y Disenadores de Experiencia.",
        "- <b>Data:</b> Data Engineers, Data Scientists y Analytics Engineers.",
        "- <b>People &amp; Operations:</b> Recursos Humanos, Finanzas, Legal y Administracion.",
        "Cada Squad de producto es un equipo autonomo y multidisciplinario compuesto generalmente por 1 Product Manager, 1 UX Designer, 2-4 ingenieros Backend, 2-3 ingenieros Frontend y 1 QA Engineer. Los squads son los duenos de sus propios servicios y sus propios ciclos de releases, lo que significa que no necesitan pedir permiso a otro equipo para deployar.",
        "El organigrama completo y actualizado siempre esta disponible en la intranet corporativa en la seccion 'Empresa - Organigrama'. La intranet esta disponible en <b>intranet.dadacode.io</b> una vez que tengas tus credenciales activas.",
        "### 3.1 Niveles de Seniority en Engineering",
        "En Da&amp;Da Solutions los ingenieros de software siguen la siguiente escala de seniority: Junior Engineer (0-2 anios de experiencia), Engineer (2-5 anios), Senior Engineer (5-8 anios), Staff Engineer (8+ anios, enfoque en impacto cross-team), Principal Engineer (impacto a nivel de compania). Los criterios exactos de cada nivel, las responsabilidades y las expectativas estan documentados en la Career Ladder que puedes encontrar en Confluence en la seccion 'Engineering - Career Development'.",
        "### 3.2 El Rol del Engineering Manager",
        "El Engineering Manager (EM) es el lider del equipo en el eje de personas, no en el eje tecnico. El EM se ocupa de: facilitar el crecimiento profesional de cada integrante del equipo, remover bloqueantes organizacionales, asegurar que el equipo tenga la claridad de prioridades necesaria para trabajar, y cuidar el bienestar y la motivacion del equipo. El liderazgo tecnico del squad recae en el Staff o Senior Engineer mas experimentado.",
        "---",
        "## 4. Los Primeros 7 Dias: Semana Cero",
        "### 4.1 Dia 1: Bienvenida y Accesos",
        "El primer dia esta disenado sin presion productiva. Tu unico objetivo es configurar tu entorno y conocer al equipo. Tu Buddy te esperara a las 9:00 AM hora local en la sala 'Turing' (o en el canal de Slack de tu squad si eres remoto) y te acompanara durante todo el dia.",
        "Checklist del Dia 1: Activar tu cuenta corporativa de Google Workspace (correo @dadacode.io). Configurar la autenticacion de dos factores (obligatorio) en Google, GitHub y Slack. Instalar y configurar el cliente VPN corporativo (usamos Tailscale). Unirte a los canales de Slack de tu squad y a los canales generales. Solicitar acceso a los repositorios de GitHub de tu squad. Completar el formulario de preferencias de trabajo (horario, zona horaria, preferencias de comunicacion).",
        "### 4.2 Dias 2 y 3: Configuracion del Entorno Local",
        "El entorno de desarrollo es tu herramienta mas importante. Durante los dias 2 y 3 te concentraras en tener todo funcionando localmente. El proceso estandar es: clonar el repositorio principal de tu squad (disponible en GitHub bajo la org dada-solutions), seguir las instrucciones del DEVELOPMENT.md en la raiz del repositorio, instalar las dependencias con el gestor de paquetes del proyecto (Poetry para Python, pnpm para JavaScript/TypeScript) y levantar todos los servicios con docker compose up -d --build.",
        "Si el DEVELOPMENT.md tiene instrucciones incompletas o desactualizadas, uno de tus primeros aportes al equipo sera mejorarlo. Esta es una contribucion bienvenida y valiosa, no una tarea menor.",
        "### 4.3 Dias 4 y 5: Inmersion en el Negocio",
        "Los ultimos dos dias de la primera semana estan reservados para reuniones de contexto de negocio. Tu Team Lead coordinara sesiones de 30-45 minutos con: el Product Manager del squad (para entender el roadmap y el 'por que' detras de lo que construyen), el Staff Engineer del area (para entender la arquitectura tecnica de alto nivel), y representantes de otros squads con los que interactuaran frecuentemente.",
        "Tambien en esta semana debes completar los tres cursos obligatorios en la plataforma de e-learning: 'Seguridad de la Informacion en Da&amp;Da' (2 horas), 'Manejo de Datos Personales GDPR/LGPD' (1.5 horas) y 'Codigo de Conducta y Diversidad' (1 hora). Estos cursos son requisito regulatorio y deben completarse antes del septimo dia habil.",
        "---",
        "## 5. Dias 8 al 30: La Primera Mision",
        "### 5.1 El Primer Ticket",
        "Alrededor del octavo dia habil recibiras tu primer ticket de Jira. Este ticket ha sido seleccionado cuidadosamente por tu Team Lead: siempre es un 'good-first-issue', de complejidad baja o media, que te permitira tocar el codebase de extremo a extremo (desde el handler HTTP hasta la base de datos) sin una presion desproporcionada.",
        "No se espera velocidad. Se espera calidad de proceso: que hagas las preguntas correctas, que entiendas el contexto del cambio, que escribas el test antes de la implementacion (TDD cuando sea posible), y que tu Pull Request sea un documento claro de que hiciste y por que.",
        "### 5.2 El Proceso de Pull Request en Da&Da Solutions",
        "El Pull Request es la unidad basica de colaboracion en Da&amp;Da Solutions. Cada linea de codigo que entra a la rama principal lo hace a traves de un PR. Los PRs no son solo un mecanismo de revision de codigo: son documentacion del razonamiento detras de cada cambio, y una herramienta de transferencia de conocimiento.",
        "Un PR en Da&amp;Da Solutions debe: tener un titulo claro con el formato [TIPO]: descripcion corta (tipos: FEAT, FIX, REFACTOR, DOCS, TEST, CHORE), incluir una descripcion que explique el contexto del cambio (el 'por que') y no solo la implementacion (el 'que'), referenciar el ticket de Jira correspondiente, incluir capturas de pantalla o videos para cualquier cambio de interfaz de usuario, pasar todos los checks automaticos del pipeline de CI (linters, type checkers, tests unitarios, tests de integracion, y analisis de seguridad SAST), tener una cobertura de tests del 80% o superior en el codigo nuevo, y recibir aprobacion de al menos dos revisores (uno debe ser Senior o Staff Engineer).",
        "Ningun PR puede tener mas de 400 lineas de cambio neto. Si el cambio requerido es mayor, debe dividirse en PRs atomicos que puedan mergearse de forma independiente. Esta regla existe porque los PRs grandes tienen tasas de deteccion de bugs significativamente mas bajas.",
        "### 5.3 El Ciclo de Reuniones del Squad",
        "Da&amp;Da Solutions usa un framework agil de dos semanas (sprints), adaptado de Scrum. Las ceremonias son:",
        "- <b>Daily Standup (15 min, 10 AM todos los dias):</b> Que hice ayer, que hare hoy, tengo algun bloqueante. No es un reporte de estado, es una coordinacion de equipo.",
        "- <b>Sprint Planning (2 horas, primer dia del sprint):</b> Se definen los objetivos del sprint y el equipo selecciona y estima los tickets del backlog.",
        "- <b>Sprint Review (1 hora, ultimo dia del sprint):</b> Se presentan los resultados a los stakeholders del negocio y se recolecta feedback.",
        "- <b>Retrospectiva (45 min, ultimo dia del sprint):</b> Solo el equipo. Discusion honesta sobre que salio bien, que no salio bien, y que una sola cosa vamos a mejorar el proximo sprint.",
        "- <b>Refinamiento (1 hora, a mitad del sprint):</b> El equipo prepara y estima los tickets candidatos para el proximo sprint junto con el Product Manager.",
        "---",
        "## 6. Herramientas Corporativas — Guia de Uso",
        "### 6.1 Slack: Comunicacion Principal",
        "Slack es la herramienta de comunicacion diaria de Da&amp;Da Solutions. Algunos principios de uso: escribir en canales publicos en lugar de mensajes directos cuando la conversacion es de interes para el equipo, usar threads para mantener las conversaciones organizadas dentro de cada canal, usar la funcion de recordatorios de Slack para no perder tareas importantes, y configurar el Do Not Disturb fuera del horario laboral.",
        "Canales obligatorios al unirse: #anuncios-generales (solo lectura, comunicados oficiales), #ingenieria (canal general de engineering), #ayuda-tecnica (preguntas tecnicas a la comunidad), #deployments (notificaciones automaticas de todos los deployments), #incidentes (alertas y coordinacion de incidentes de produccion), #aprendizaje (recursos de formacion y novedades tecnicas) y #random (cultura, off-topic, memes de programacion).",
        "### 6.2 Jira: Gestion de Trabajo",
        "Jira es la herramienta de gestion de tareas. El flujo de estados de un ticket es: Backlog (no priorizado) - To Do (priorizado, listo para trabajarse) - In Progress (alguien lo esta trabajando) - In Review (PR abierto) - QA (en pruebas de QA) - Done (mergeado y desplegado).",
        "Cada ticket debe tener una descripcion clara con criterios de aceptacion en formato 'Given/When/Then', la estimacion en Story Points (escala Fibonacci: 1, 2, 3, 5, 8, 13 — si es mayor de 13 debe dividirse), el tipo correcto (Bug, Feature, Tech Debt, Spike) y el enlace al Pull Request asociado.",
        "### 6.3 Confluence: Documentacion",
        "Confluence es el repositorio de documentacion tecnica y de producto. La regla de oro de Da&amp;Da: si no esta en Confluence, no existe. La documentacion debe actualizarse como parte de cada ticket, no como una tarea separada posterior.",
        "Cada squad tiene su propio espacio en Confluence con: arquitectura del servicio (diagramas C4), runbooks operacionales, decisiones de arquitectura (ADRs), guias de instalacion y onboarding especificas del squad, y el catalogo de APIs.",
        "### 6.4 GitHub: Control de Versiones",
        "Toda la organizacion vive en la GitHub Organization <b>dada-solutions</b> en github.com. El branching model estandar es GitHub Flow: la rama principal es main, que siempre esta en estado deployable; las features y fixes se desarrollan en ramas de corta duracion (feature/nombre-descriptivo, fix/descripcion-del-bug) que se mergean a main via PR.",
        "La integracion directa a main sin PR esta bloqueada mediante branch protection rules en todos los repositorios. La unica excepcion son los hotfixes de P1, que requieren aprobacion de al menos un Staff Engineer antes de mergearse.",
        "---",
        "## 7. Entorno de Desarrollo — Configuracion Detallada",
        "### 7.1 Hardware Corporativo",
        "Da&amp;Da Solutions proporciona una laptop corporativa a todos sus empleados con las siguientes especificaciones minimas: procesador de 8 nucleos (Apple M-series o Intel/AMD equivalente), 16 GB de RAM (se recomienda 32 GB para trabajar con multiples microservicios localmente), 512 GB SSD NVMe. El sistema operativo es a eleccion del desarrollador: macOS Sonoma o superior, Ubuntu 22.04 LTS o Windows 11 con WSL2 habilitado.",
        "Adicionalmente, cada desarrollador tiene asignado: un monitor externo de 27' 4K, un kit de teclado y mouse ergonomico, y un headset de calidad para llamadas de video.",
        "### 7.2 IDEs y Plugins Recomendados",
        "Los IDEs mas usados en Da&amp;Da Solutions son VS Code y la familia JetBrains (PyCharm para Python, WebStorm para JavaScript/TypeScript, IntelliJ IDEA para Java/Kotlin/Go). Ambas opciones son igualmente validas y el equipo de Platform Engineering provee configuraciones base para ambos.",
        "Para VS Code, el archivo .vscode/extensions.json en cada repositorio lista las extensiones recomendadas. Las mas comunes son: ESLint, Prettier, Python (ms-python), Docker, GitLens, GitHub Copilot, REST Client y Thunder Client.",
        "### 7.3 Docker y Docker Compose",
        "Todos los proyectos de Da&amp;Da Solutions estan completamente contenerizados. Esto significa que para desarrollar localmente no necesitas instalar PostgreSQL, MongoDB, Redis u otros servicios directamente en tu maquina: todo corre en contenedores. El comando para iniciar el entorno completo desde la raiz del proyecto es siempre el mismo: docker compose up -d --build.",
        "El archivo docker-compose.yml en la raiz del proyecto define todos los servicios necesarios: la aplicacion principal, las bases de datos, los brokers de mensajeria (Kafka, Redis) y los servicios de monitoreo locales. Si necesitas reiniciar solo un servicio especifico: docker compose restart nombre-servicio.",
        "### 7.4 Gestion de Variables de Entorno",
        "Nunca se commitean variables de entorno con valores reales al repositorio. Cada proyecto tiene un archivo .env.example con todas las variables necesarias pero con valores placeholder. El primer paso al configurar el entorno es copiar este archivo (.env.example a .env) y completar los valores reales.",
        "Los valores de las variables para el entorno de desarrollo estan disponibles en el vault de 1Password del equipo bajo el nombre 'Development Environment - [Nombre del Proyecto]'. Solicita el acceso al vault a tu Team Lead durante el primer dia.",
        "---",
        "## 8. Dias 31 al 90: Crecimiento y Autonomia",
        "### 8.1 Asumiendo Ownership",
        "A partir del segundo mes, el rol del Buddy comienza a reducirse y se espera que el nuevo integrante empiece a operar con mayor autonomia. Esto incluye: tomar ownership de tickets de complejidad media sin supervision constante, proponer mejoras tecnicas en el refinamiento del backlog, hacer revisiones de codigo de los PRs de companeros, y contribuir activamente en el daily standup con perspectiva propia.",
        "### 8.2 Convirtiendote en Revisor de Codigo",
        "Las revisiones de codigo son una de las responsabilidades mas importantes y mas subestimadas en el desarrollo de software. En Da&amp;Da Solutions esperamos que a partir de la semana cuatro el nuevo integrante empiece a revisar PRs de sus companeros. La guia completa de como hacer revisiones de codigo efectivas esta disponible en Confluence, pero los principios basicos son: revisar el contexto antes que el codigo, buscar bugs y problemas de mantenibilidad, dar feedback especifico y accionable, distinguir entre sugerencias (son opcionales) y cambios requeridos, y siempre elogiar lo que esta bien hecho.",
        "### 8.3 Evaluacion de los 90 Dias",
        "Al finalizar el periodo de onboarding, tu Engineering Manager realizara una evaluacion formal en dos partes. La primera parte es una autoevaluacion: reflejas sobre tus primeros 90 dias, identificas tus logros y las areas donde sientes que puedes crecer. La segunda parte es una conversacion estructurada con tu EM donde se discuten: las competencias tecnicas demostradas, las competencias blandas observadas, la alineacion cultural, y el plan de desarrollo para el siguiente trimestre.",
        "Esta evaluacion no es un examen. Es el punto de partida de una conversacion de carrera que continuara cada trimestre durante tu permanencia en la empresa.",
        "---",
        "## 9. Cultura, Bienestar y Beneficios",
        "### 9.1 Diversidad e Inclusion",
        "Da&amp;Da Solutions tiene una politica de tolerancia cero ante cualquier forma de discriminacion, acoso, intimidacion o comportamiento excluyente, ya sea por razon de genero, orientacion sexual, edad, origen etnico, religion, discapacidad o cualquier otra caracteristica personal. Si eres testigo o victima de cualquier situacion de este tipo, puedes reportarla de forma anonima y segura a traves del canal etico en la intranet o mediante la plataforma de reporte anonimo (link disponible en People &amp; HR).",
        "### 9.2 Politica de Trabajo Hibrido",
        "Da&amp;Da Solutions tiene una politica de trabajo hibrido flexible. La expectativa base es presencia en oficina dos dias a la semana, preferentemente martes y jueves (los dias de mayor densidad de presencia del equipo). Sin embargo, esto es flexible segun las necesidades del proyecto y del equipo. El trabajo completamente remoto temporal puede solicitarse al manager con justificacion y anticipacion razonable.",
        "Para los empleados que viven fuera de Buenos Aires, Bogota, Ciudad de Mexico o Madrid, el trabajo completamente remoto es la modalidad por defecto, con al menos un viaje presencial al hub de referencia cada trimestre.",
        "### 9.3 Beneficios del Equipo Tecnico",
        "Los beneficios del equipo tecnico incluyen: presupuesto anual de desarrollo profesional de USD 1.200 para cursos, libros, conferencias y certificaciones (se solicita a People &amp; HR con factura). Acceso a licencias corporativas de GitHub Copilot, Figma, JetBrains y plataformas de e-learning (Platzi, Udemy for Business, O'Reilly Learning). Tiempo protegido los viernes de 4 PM a 6 PM para aprendizaje y exploracion tecnica. Compensacion economica adicional por guardias de produccion fuera del horario laboral. Plan de salud corporativo y dias de salud mental.",
        "### 9.4 Comunicacion y Feedback Continuo",
        "El feedback en Da&amp;Da Solutions no espera a las evaluaciones formales. Se da en el momento oportuno, de forma especifica, con intencion de ayudar. Los 1-on-1 semanales con tu Engineering Manager son el espacio privilegiado para feedback bidireccional: tu puedes dar feedback a tu manager y el te dara feedback a ti. Estos espacios son confidenciales y valen tanto como cualquier reunion de producto.",
        "---",
        "## 10. Recursos, Contactos y Referencias",
        "### 10.1 Contactos de Emergencia Tecnica",
        "- IT Helpdesk: helpdesk@dadacode.io | Slack #it-helpdesk (SLA: 4 horas en dias habiles)",
        "- Seguridad Informatica: security@dadacode.io | Slack #seguridad (SLA: 1 hora 24/7 para P1)",
        "- Platform Engineering: platform@dadacode.io | Slack #platform-eng",
        "- People y HR: people@dadacode.io | Slack #people-hr",
        "### 10.2 Documentacion Esencial",
        "- Intranet corporativa: intranet.dadacode.io",
        "- Documentacion tecnica (Confluence): docs.dadacode.io",
        "- Gestion de tareas (Jira): jira.dadacode.io",
        "- Repositorios de codigo (GitHub): github.com/dada-solutions",
        "- Dashboards de monitoreo (Grafana): grafana.dadacode.io",
        "- Repositorio de secretos (1Password): disponible via app de escritorio",
        "### 10.3 Canales de Aprendizaje Recomendados",
        "- Slack #aprendizaje: recursos tecnicos compartidos por el equipo",
        "- Confluence 'Engineering - Learning Resources': lista curada de recursos por tecnologia",
        "- Slack #show-and-tell: grabaciones de las sesiones de showcasing tecnico",
        "- GitHub dada-solutions/engineering-blog: blog tecnico interno de Da&amp;Da Solutions",
        "[NOTE] Este documento se actualiza cada trimestre. Si encontras informacion desactualizada o incorrecta, abri un ticket de tipo DOCS en el proyecto 'People &amp; Engineering' en Jira o envia un mensaje al canal #onboarding-feedback en Slack. Tu contribucion mejora la experiencia de los proximos colegas que lleguen.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 2. BACKEND GUIDE  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="backend_guide.pdf",
    title="Guia Oficial de Ingenieria Back-end",
    subtitle="Estandares, patrones y mejores practicas para todos los servicios de Da&amp;Da Solutions",
    blocks=[
        "## 1. Proposito y Alcance de Este Documento",
        "Esta guia es el documento normativo de referencia para todos los ingenieros de Back-end de Da&amp;Da Solutions, sin importar el lenguaje o el framework que usen. Establece los estandares minimos que deben satisfacerse para que un servicio sea considerado 'production-ready'. El incumplimiento de las normas aqui descritas es un motivo valido para rechazar un Pull Request.",
        "La guia se actualiza de forma colaborativa: cualquier ingeniero puede proponer cambios mediante un ADR (Architecture Decision Record) que debe ser aprobado por al menos dos Staff Engineers antes de incorporarse a este documento. La version vigente es siempre la que esta en la rama main del repositorio dada-solutions/engineering-guidelines.",
        "---",
        "## 2. Filosofia de Ingenieria Back-end",
        "### 2.1 Simplicidad Intencional",
        "La complejidad accidental es el enemigo numero uno de la mantenibilidad. Antes de introducir una nueva abstraccion, patron o dependencia, debemos preguntarnos: ¿Que problema concreto resuelve esto? ¿Hay una solucion mas simple que funcione igual de bien? ¿Que pasa si necesitamos modificar esto en seis meses con un desarrollador que nunca lo vio?",
        "El codigo mas seguro es el codigo que no existe. El mejor refactor es el que elimina lineas. La complejidad debe estar justificada por requisitos reales, no por anticipacion de escenarios hipoteticos.",
        "### 2.2 APIs como Productos",
        "Cada API que Da&amp;Da Solutions construye es un producto con sus propios usuarios (otros servicios, el frontend, clientes externos). Esto implica que las APIs deben ser: confiables (contratos estables, versionado semantico), predecibles (comportamiento consistente y documentado), observables (metricas, logs y traces desde el dia uno) y operables (health checks, graceful shutdown, configuracion externalizada).",
        "### 2.3 Operabilidad Desde el Dia Uno",
        "Un servicio que no puede monitorearse es un servicio ciego. La observabilidad no es una caracteristica que se agrega al final: es un requisito funcional desde el primer commit. Todo servicio nuevo de Da&amp;Da Solutions debe nacer con: logs estructurados en formato JSON, metricas expuestas en formato Prometheus, tracing con OpenTelemetry, y endpoints de health check.",
        "---",
        "## 3. Stack Tecnologico Aprobado",
        "### 3.1 Python con FastAPI — Stack Principal para Datos e IA",
        "FastAPI es el framework web Python preferido en Da&amp;Da Solutions para servicios que manejan logica de negocio orientada a datos, integraciones con modelos de ML/AI, o APIs de alto rendimiento con tipado estricto. La version minima de Python soportada es 3.11 (con acceso a las mejoras de rendimiento del interprete introducidas en esa version).",
        "Requisitos tecnicos para servicios FastAPI: usar Pydantic v2 para todos los modelos de datos de entrada y salida, usar SQLAlchemy 2.0 con soporte async para la capa de persistencia, gestionar dependencias con Poetry (el archivo pyproject.toml es la unica fuente de verdad de dependencias), y estructurar el proyecto siguiendo el patron de repositorio corporativo disponible en dada-solutions/fastapi-template.",
        "### 3.2 Node.js con NestJS — Stack para Logica de Negocio Compleja",
        "NestJS es el framework Node.js preferido para servicios con logica de negocio compleja que se beneficia del sistema de modulos, inyeccion de dependencias y decoradores de NestJS. Se usa especialmente para servicios que orquestan flujos de negocio complejos con multiples dependencias.",
        "Requisitos tecnicos para servicios NestJS: TypeScript en modo strict (tsconfig.json corporativo en el repositorio de plantillas), pnpm como gestor de paquetes, Jest para testing, y Prisma como ORM para PostgreSQL. La estructura de directorios debe seguir el patron de capas: controllers, services, repositories, y entidades de dominio.",
        "### 3.3 Go — Stack para Servicios de Infra de Alta Performance",
        "Go se usa selectivamente para servicios de infraestructura o componentes de plataforma que requieren latencias extremadamente bajas (sub-millisegundo) o concurrencia masiva: el API Gateway, los workers de procesamiento de streams de Kafka de alto throughput, y proxies o sidecars de red. El uso de Go en servicios de negocio nuevos requiere aprobacion explicita del Staff Engineer del area.",
        "### 3.4 Java con Spring Boot — Legacy y Servicios de Datos Criticos",
        "Algunos servicios heredados de la arquitectura monolitica original de Da&amp;Da Solutions estan escritos en Java con Spring Boot. Estos servicios son mantenidos y reciben updates de seguridad, pero no se desarrollan servicios nuevos en Java sin justificacion tecnica muy fuerte. El plan de migracion a largo plazo es reescribir estos servicios incrementalmente en Python o Node.js.",
        "---",
        "## 4. Diseno de APIs RESTful",
        "### 4.1 Principios Generales",
        "Las APIs de Da&amp;Da Solutions siguen el estilo arquitectonico REST con los siguientes principios adicionales: las URLs identifican recursos (sustantivos), los verbos HTTP describen las acciones, el formato de datos es JSON para todos los requests y responses, el codigo de estado HTTP comunicar el resultado de la operacion con precision, y toda la API debe poder ser documentada en OpenAPI 3.1.",
        "### 4.2 Convencion de URLs",
        "Recursos: siempre en plural y en minusculas con palabras separadas por guiones. Ejemplos correctos: /api/v1/users, /api/v1/billing-accounts, /api/v1/subscription-plans. Ejemplos incorrectos: /api/v1/getUser, /api/v1/User, /api/v1/users_list.",
        "Sub-recursos: /api/v1/users/{user_id}/addresses/{address_id}. Acciones especiales que no encajan en el modelo CRUD: /api/v1/users/{user_id}/actions/verify-email (usando el sufijo /actions/{nombre-de-la-accion}).",
        "### 4.3 Versionado de API",
        "El versionado es en la URL, por major version: /api/v1/, /api/v2/. Un bump de major version solo ocurre cuando hay un breaking change en el contrato. Cambios backward-compatible (nuevos endpoints, nuevos campos opcionales en responses, nuevos parametros opcionales en requests) no requieren cambio de version.",
        "Cuando se depreca una version de API, esta se mantiene activa por al menos 6 meses con un header de deprecacion en las respuestas: Deprecation: date=2026-12-31 y Sunset: date=2027-01-15. Los clientes de la API deprecada reciben emails automaticos de notificacion.",
        "### 4.4 Estructura de Respuesta Unificada",
        "Todas las respuestas de la API (exitosas y de error) siguen la misma estructura envelope para garantizar coherencia: { success: boolean, data: T | null, error: ErrorObject | null, meta: PaginationMeta | null }. Ejemplo de exito: { success: true, data: { id: 123, name: 'Ejemplo' }, error: null, meta: null }. Ejemplo de error: { success: false, data: null, error: { code: USER_NOT_FOUND, message: 'El usuario 123 no fue encontrado.', details: [] }, meta: null }.",
        "### 4.5 Paginacion",
        "Todos los endpoints que retornan colecciones implementan paginacion. Para colecciones de tamano desconocido o muy grande, se prefiere paginacion basada en cursor sobre la paginacion offset/limit (la primera es mas eficiente y consistente ante inserciones concurrentes). Los parametros estandar para offset-based son: page (1-indexed, default 1), page_size (default 20, maximo 100, configurable por endpoint). Para cursor-based: cursor (token opaco devuelto por el servidor), limit (equivalente a page_size). El objeto meta de la respuesta incluye: total, page, page_size, next_cursor (para cursor-based).",
        "### 4.6 Filtrado, Busqueda y Ordenamiento",
        "Los parametros de filtrado van como query params. La convencion es usar el nombre del campo directamente para filtros de igualdad exacta: /api/v1/orders?status=pending. Para filtros de rango: created_at_gte y created_at_lte. Para busqueda de texto libre: q=termino-de-busqueda. El ordenamiento usa sort_by (nombre del campo) y sort_order (asc o desc, default asc).",
        "---",
        "## 5. Autenticacion y Autorizacion",
        "### 5.1 Autenticacion con JWT",
        "Da&amp;Da Solutions usa JWT (RFC 7519) para la autenticacion de todos los endpoints publicos. El auth-service es el unico emisor de tokens en la plataforma. Los tokens siguen el esquema de Access Token + Refresh Token: el Access Token tiene TTL de 15 minutos y es stateless; el Refresh Token tiene TTL de 7 dias, se almacena en una cookie HttpOnly Secure SameSite=Strict, y es stateful (guardado en Redis con posibilidad de revocacion).",
        "El Access Token es un JWT firmado con RS256 (RSA 2048 bits). La clave privada vive exclusivamente en el auth-service; todos los demas servicios validan tokens usando la clave publica descargada del JWKS endpoint del auth-service. Nunca se comparten claves privadas.",
        "### 5.2 Control de Acceso Basado en Roles (RBAC)",
        "La autorizacion se implementa en dos niveles. El primero es en el API Gateway (verificacion de que el token es valido y no ha expirado). El segundo es en cada servicio individual (verificacion de que el usuario tiene los permisos necesarios para la operacion especifica). Los roles globales son: SUPER_ADMIN, ADMIN, MANAGER, OPERATOR y VIEWER. Adicionalmente, existe un sistema de permisos granulares a nivel de recurso para casos complejos.",
        "### 5.3 Comunicacion Servicio-a-Servicio",
        "La comunicacion entre microservicios internos usa Mutual TLS (mTLS) gestionado por Istio para cifrado y autenticacion de identidad. Para autorizacion de acciones especificas entre servicios (no solo autenticacion de identidad), cada servicio emite un Service Account Token con permisos especificos que el servicio receptor valida.",
        "---",
        "## 6. Manejo de Errores",
        "### 6.1 Principios Generales del Manejo de Errores",
        "Los errores son ciudadanos de primera clase en el codigo de Da&amp;Da Solutions. Principios: los errores deben ser explicitamente tipados y manejados, nunca silenciados; las excepciones que se capturan deben loggearse con contexto suficiente para el debugging en produccion; los errores de negocio (validacion, permisos, recursos no encontrados) se retornan al cliente con informacion util; los errores de sistema (fallos de infraestructura) se retornan como HTTP 500 con un mensaje generico (los detalles van a los logs, no al cliente).",
        "### 6.2 Catalogo de Error Codes",
        "Cada dominio de negocio tiene un catalogo de error codes con el formato DOMINIO_ENTIDAD_RAZON. Algunos ejemplos estandarizados: AUTH_TOKEN_EXPIRED, AUTH_TOKEN_INVALID, AUTH_INSUFFICIENT_PERMISSIONS, USER_NOT_FOUND, USER_EMAIL_ALREADY_EXISTS, USER_ACCOUNT_SUSPENDED, BILLING_PAYMENT_FAILED, BILLING_INSUFFICIENT_FUNDS, BILLING_SUBSCRIPTION_EXPIRED, ORDER_ITEM_OUT_OF_STOCK. El catalogo completo y las guias para agregar nuevos error codes estan en Confluence.",
        "### 6.3 Excepciones No Manejadas",
        "Todo servicio debe tener un handler de excepciones global que: loggee la excepcion completa con su stack trace y el contexto de la request (sin datos PII), retorne una respuesta HTTP 500 con un error_code generico de SERVER_UNEXPECTED_ERROR, genere una alerta en PagerDuty si la tasa de errores 500 supera el umbral configurado, e incluya el trace_id en la respuesta para que el cliente pueda reportarlo al soporte.",
        "---",
        "## 7. Testing — Piramide y Estandares",
        "### 7.1 La Piramide de Tests de Da&Da Solutions",
        "Seguimos la piramide de testing clasica con proporciones especificas: 70% tests unitarios, 20% tests de integracion, 10% tests end-to-end. La cobertura minima de tests unitarios para poder mergear a main es del 80%. Esta cifra se verifica automaticamente en el pipeline de CI y un resultado menor bloquea el merge.",
        "### 7.2 Tests Unitarios",
        "Los tests unitarios prueban una unidad logica de codigo (generalmente una funcion o clase) en completo aislamiento de sus dependencias externas. Las dependencias externas (bases de datos, APIs externas, servicios externos) siempre se mockean. En Python usamos pytest con pytest-asyncio para funciones async y unittest.mock para mocks. En Node.js usamos Jest con los mocks nativos de Jest.",
        "Convenciones de naming: test_should_{expected_behavior}_when_{condition} para Python, should {expected behavior} when {condition} para Jest. Estructura de cada test: Arrange (preparar el estado), Act (ejecutar la accion bajo prueba), Assert (verificar el resultado esperado).",
        "### 7.3 Tests de Integracion",
        "Los tests de integracion verifican la interaccion entre multiples componentes del sistema (por ejemplo, el handler HTTP, la capa de servicio y la capa de repositorio con una base de datos real). En Da&amp;Da Solutions usamos testcontainers para levantar instancias efimeras de PostgreSQL, MongoDB o Redis directamente en el test. Los tests de integracion son mas lentos que los unitarios pero mas representativos de la realidad.",
        "### 7.4 Contract Testing con Pact",
        "Para los servicios que se comunican entre si via REST, usamos Pact para contract testing. El Consumer define el contrato de lo que espera de la API del Provider y lo comparte en el Pact Broker. El Provider verifica automaticamente que cumple todos los contratos de sus consumers como parte de su pipeline de CI. Esto previene silenciosamente que cambios en un servicio rompan a sus clientes.",
        "### 7.5 Tests de Performance",
        "Los servicios criticos tienen pruebas de performance con k6. Estas pruebas simulan la carga esperada en produccion y verifican que los SLOs de latencia (P99 menor a 500ms) se mantengan. Se ejecutan en el entorno de staging previo a cada release mayor.",
        "---",
        "## 8. Observabilidad — Los Tres Pilares",
        "### 8.1 Logs Estructurados",
        "Todos los servicios deben generar logs en formato JSON estructurado. El formato estandar de cada evento de log incluye obligatoriamente: timestamp (ISO 8601 con zona horaria UTC), level (DEBUG, INFO, WARNING, ERROR, CRITICAL), service (nombre del microservicio), version (version del servicio), trace_id (ID de la traza distribuida), span_id (ID del span actual), y message (descripcion del evento). En Python usamos structlog configurado con el procesador JSON. En Node.js usamos pino.",
        "Reglas criticas sobre el contenido de los logs: nunca loggear datos PII (nombres, emails, numeros de tarjeta, passwords) directamente — solo loggear identificadores opacos como IDs de usuario; no loggear en nivel DEBUG en produccion; loggear siempre el trace_id para permitir correlacion de logs entre servicios.",
        "### 8.2 Metricas con Prometheus",
        "Cada servicio expone un endpoint GET /metrics en formato Prometheus. Las metricas minimas requeridas son: http_request_duration_seconds (histograma con labels: method, path, status_code), http_requests_total (counter con labels: method, path, status_code), active_connections (gauge), y metricas del proceso (CPU, memoria, goroutines/threads). En Python usamos prometheus-client. En Node.js usamos prom-client.",
        "### 8.3 Tracing Distribuido con OpenTelemetry",
        "El tracing distribuido es esencial para diagnosticar problemas de latencia y errores en sistemas de microservicios. Cada servicio debe instrumentarse con los SDKs de OpenTelemetry para su lenguaje. El trace_id se propaga automaticamente en los headers HTTP usando el formato W3C Trace Context (traceparent y tracestate). Los traces se exportan al backend de observabilidad (Jaeger en desarrollo/staging, Grafana Tempo en produccion) via OTLP.",
        "### 8.4 Health Checks",
        "Cada servicio implementa dos endpoints de health: GET /health/liveness retorna 200 OK si el proceso esta vivo (no esta en deadlock ni en estado corrupto). GET /health/readiness retorna 200 OK si el servicio esta listo para manejar trafico (la conexion a la base de datos esta activa, las dependencias criticas estan disponibles). Kubernetes usa liveness para reiniciar pods en mal estado y readiness para enrutar trafico solo a pods sanos.",
        "---",
        "## 9. Seguridad",
        "### 9.1 OWASP Top 10 — Consideraciones para Da&Da",
        "Los riesgos del OWASP Top 10 mas relevantes para el stack de Da&amp;Da Solutions son: Injection (usar siempre ORM o queries parametrizadas, nunca concatenar inputs de usuario en SQL), Broken Access Control (verificar autorizacion en cada endpoint, nunca asumir que si el request llego con un token valido tiene acceso a todos los recursos), Cryptographic Failures (usar bcrypt con factor de costo minimo 12 para passwords, AES-256 para datos en reposo, TLS 1.2 o superior para datos en transito), y Security Misconfiguration (no exponer informacion sensible en mensajes de error, no tener servicios innecesarios expuestos, rotar secretos regularmente).",
        "### 9.2 SAST y SCA en el Pipeline de CI",
        "El pipeline de CI incluye analisis de seguridad estatico (SAST) con Bandit (Python) y Semgrep (multi-lenguaje). Tambien incluye analisis de composicion de software (SCA) con Safety (Python) y npm audit (Node.js) para detectar dependencias con vulnerabilidades conocidas. Un hallazgo de severidad HIGH o CRITICAL bloquea el merge hasta ser resuelto o marcado explicitamente como falso positivo con justificacion documentada.",
        "### 9.3 Rotacion de Secretos",
        "Ningun secreto es permanente. Los secretos de servicio (API keys de terceros, claves de cifrado, certificados) se rotan al menos cada 90 dias. Las credenciales de base de datos se rotan diariamente usando las dynamic secrets de HashiCorp Vault. El proceso de rotacion es automatico y los servicios deben ser capaces de recibir nuevas credenciales sin reiniciarse (Vault Agent Sidecar inyecta las credenciales nuevas automaticamente).",
        "---",
        "## 10. Performance y Optimizacion",
        "### 10.1 Async por Defecto",
        "Todos los handlers HTTP en FastAPI y NestJS deben ser async/await para no bloquear el event loop durante operaciones de I/O. Una funcion sincrona que realiza una operacion de I/O (query de base de datos, llamada HTTP) en un handler que corre en el event loop es un bug de performance grave que puede degradar la capacidad de la aplicacion a medida que aumenta la concurrencia.",
        "### 10.2 Optimizacion de Queries de Base de Datos",
        "El problema N+1 es la causa mas comun de degradacion de performance en aplicaciones back-end. Para detectarlo y prevenirlo: usar el modo de logging de SQLAlchemy o el query logger de Prisma en desarrollo para ver todas las queries ejecutadas, configurar alertas en Grafana para queries que tarden mas de 100ms en promedio, y revisar los planes de ejecucion con EXPLAIN ANALYZE para las queries mas frecuentes y criticas.",
        "Reglas para indices: crear indices en todos los campos usados en clausulas WHERE, JOIN ON y ORDER BY, usar indices compuestos para patrones de query con multiples columnas en la clausula WHERE, evitar indices de baja cardinalidad (ej. un campo boolean con el 90% de valores iguales), y crear indices en produccion siempre con CREATE INDEX CONCURRENTLY (para no bloquear la tabla durante la creacion).",
        "### 10.3 Gestion de Connection Pools",
        "La conexion a bases de datos debe gestionarse mediante connection pools para evitar el overhead de crear una nueva conexion TCP para cada request. Los parametros minimos de configuracion del pool son: max_connections (numero maximo de conexiones activas, tipicamente igual al numero de workers del servicio), min_connections (conexiones minimas mantenidas abiertas), y connection_timeout (tiempo maximo de espera para obtener una conexion del pool). Valores fuera de rango en estos parametros son una causa frecuente de problemas bajo carga.",
        "---",
        "## 11. Releases y Despliegues",
        "### 11.1 Semantic Versioning",
        "Todos los servicios de Da&amp;Da Solutions siguen el versionado semantico SemVer (MAJOR.MINOR.PATCH). MAJOR: cambios incompatibles con versiones anteriores de la API publica. MINOR: nueva funcionalidad backward-compatible. PATCH: correcciones de bugs backward-compatible. Los numeros de version se calculan y se aplican automaticamente por el pipeline de CD usando la herramienta semantic-release y los mensajes de commit en formato Conventional Commits.",
        "### 11.2 Conventional Commits",
        "Da&amp;Da Solutions aplica el estandar de Conventional Commits para todos los mensajes de commit. El formato es: tipo(alcance): descripcion corta. Tipos validos: feat (nueva funcionalidad, incrementa MINOR), fix (correccion de bug, incrementa PATCH), docs (cambios en documentacion), style (formateado de codigo, no afecta logica), refactor (refactorizacion sin cambio de funcionalidad), test (agregar o modificar tests), chore (cambios en herramientas, dependencias o configuracion de CI/CD). Un BREAKING CHANGE en el cuerpo o footer del commit incrementa MAJOR.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 3. FRONTEND GUIDE  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="frontend_guide.pdf",
    title="Guia Oficial de Ingenieria Front-end",
    subtitle="Estandares, design system y mejores practicas para interfaces de Da&amp;Da Solutions",
    blocks=[
        "## 1. Filosofia de Desarrollo Front-end en Da&Da Solutions",
        "El front-end no es una segunda clase en la ingenieria de Da&amp;Da Solutions. La calidad de la interfaz de usuario es un diferenciador competitivo directo y medible: los usuarios abandonan productos lentos, inconsistentes o inaccesibles. El equipo de Front-end opera con los mismos estandares de rigor tecnico que el back-end.",
        "Nuestros tres principios guias para el desarrollo de interfaces: <b>Performance como funcionalidad</b> — una interfaz lenta es una interfaz rota, y la velocidad de carga no es opcional; <b>Accesibilidad desde el diseno</b> — la accesibilidad no se agrega al final, se diseña desde el primer wireframe; <b>Coherencia a traves del Design System</b> — la consistencia visual genera confianza y reduce la carga cognitiva del usuario.",
        "---",
        "## 2. Stack Tecnologico Front-end",
        "### 2.1 React 18 — Base del Ecosistema",
        "React 18 es el framework de UI estandar en Da&amp;Da Solutions. Aprovechamos todas sus caracteristicas modernas: Concurrent Mode para interfaces mas responsivas, Suspense para el manejo declarativo de estados de carga, Transitions para marcar actualizaciones de UI de baja prioridad, y los nuevos hooks como useId, useDeferredValue y useTransition. El uso de Class Components esta completamente prohibido en codigo nuevo; toda la logica de componentes vive en componentes funcionales con hooks.",
        "### 2.2 Next.js 14 con App Router",
        "Para aplicaciones publicas, orientadas a SEO, o que requieren Server-Side Rendering o Static Site Generation, usamos Next.js 14 con el App Router. El App Router representa el paradigma futuro de Next.js: Server Components por defecto, streaming de HTML, layouts anidados y route handlers. El Pages Router es considerado legacy y no debe usarse en proyectos nuevos.",
        "Las Server Components son una herramienta poderosa pero requieren un modelo mental diferente. Regla practica: los componentes que acceden a datos (fetch de APIs, lectura de bases de datos) son Server Components; los componentes con interactividad (event handlers, state, effects) son Client Components (marcados con 'use client').",
        "### 2.3 Vite para SPAs Internas y Dashboards",
        "Para Single Page Applications internas que no necesitan SEO ni SSR (dashboards administrativos, herramientas internas, aplicaciones de backoffice), usamos Vite con React y TypeScript. Vite ofrece tiempos de inicio del servidor de desarrollo y HMR (Hot Module Replacement) significativamente mas rapidos que Create React App o soluciones basadas en Webpack.",
        "### 2.4 TypeScript — Obligatorio y en Modo Strict",
        "TypeScript es obligatorio en todos los proyectos front-end nuevos sin excepcion. El modo strict de TypeScript debe estar habilitado en el tsconfig.json de todos los proyectos. El uso del tipo any esta explicitamente prohibido: si se necesita modelar un tipo dinamico, se usa unknown con type narrowing explicito, o se define la union de tipos posibles. Los generics deben usarse cuando corresponda en lugar de duplicar logica para tipos diferentes.",
        "---",
        "## 3. El Design System de Da&Da Solutions",
        "### 3.1 Vision y Proposito del Design System",
        "El Design System de Da&amp;Da Solutions es la fuente unica de verdad para todos los elementos visuales y de interaccion de nuestros productos. Existe para garantizar coherencia entre productos, reducir el tiempo de desarrollo de nuevas interfaces, documentar patrones de interaccion probados y evitar la reinvencion de la rueda, y permitir a los diseñadores y desarrolladores hablar el mismo idioma.",
        "### 3.2 Paleta de Colores — Dark Mode Corporativo",
        "El design system de Da&amp;Da Solutions esta construido sobre un tema oscuro por defecto con acentos en purpura premium:",
        "- <b>--color-bg-primary:</b> #0D0D14 — Fondo principal de la aplicacion",
        "- <b>--color-bg-secondary:</b> #1A1A2E — Fondo de tarjetas y paneles elevados",
        "- <b>--color-bg-tertiary:</b> #252540 — Fondo de elementos de tercer nivel",
        "- <b>--color-bg-hover:</b> #1E1E36 — Fondo en estado hover",
        "- <b>--color-purple-primary:</b> #7C3AED — Botones primarios, acentos principales",
        "- <b>--color-purple-light:</b> #A855F7 — Hover de botones, iconos en estado activo",
        "- <b>--color-purple-subtle:</b> #2D1B69 — Fondos con acento sutil, badges",
        "- <b>--color-text-primary:</b> #F0F0FF — Texto principal, headings",
        "- <b>--color-text-secondary:</b> #9898C0 — Texto secundario, placeholders, labels",
        "- <b>--color-text-disabled:</b> #4A4A6A — Texto de elementos deshabilitados",
        "- <b>--color-border:</b> #2A2A4A — Bordes de inputs, tarjetas y separadores",
        "- <b>--color-success:</b> #10B981 | <b>--color-warning:</b> #F59E0B | <b>--color-error:</b> #EF4444",
        "### 3.3 Tipografia",
        "La fuente principal es <b>Inter</b> (Variable Font, cargada desde Google Fonts con display=swap para evitar FOIT). La jerarquia tipografica es: Display (48px/700, para landing pages y heroes), H1 (32px/700), H2 (24px/600), H3 (20px/600), H4 (16px/600), Body Large (16px/400, leading 1.6), Body (14px/400, leading 1.5), Small (12px/400), Caption (11px/400). Los valores estan definidos como Custom Properties en el :root del CSS global.",
        "### 3.4 Espaciado",
        "El sistema de espaciado usa una escala basada en 4px: 4px (--space-1), 8px (--space-2), 12px (--space-3), 16px (--space-4), 20px (--space-5), 24px (--space-6), 32px (--space-8), 40px (--space-10), 48px (--space-12), 64px (--space-16), 80px (--space-20), 96px (--space-24). Los espaciados intermedios deben usarse con moderacion y documentarse.",
        "### 3.5 Componentes del Design System",
        "El Design System esta publicado como el paquete privado @dada/ui en el registry NPM privado de la organizacion. Los componentes estan construidos con React + TypeScript + CSS Modules. La lista de componentes disponibles incluye: Button (variantes: primary, secondary, ghost, danger; tamanios: sm, md, lg), Input (text, number, email, password, search), Select (simple y multi-select), Textarea, Checkbox, RadioGroup, Toggle/Switch, DatePicker, Modal, Drawer, Sheet, Toast/Snackbar, Alert, Badge, Avatar, Tooltip, Popover, Dropdown, Table (con sorting, filtering y paginacion), Form y FormField (con validacion integrada), Spinner/Loader, EmptyState, Breadcrumb, Tabs, Accordion, Card, Divider, y un conjunto de Layout helpers (Stack, Inline, Grid).",
        "Antes de crear cualquier componente nuevo en un proyecto de producto, verificar si ya existe en @dada/ui. Si no existe y el componente seria util en multiples proyectos, la contribucion correcta es abrirlo en el repositorio del design system (dada-solutions/design-system) para beneficio de todos.",
        "---",
        "## 4. Arquitectura de Componentes",
        "### 4.1 Estructura de Directorios Estandar",
        "La estructura de directorios estandar para proyectos Next.js en Da&amp;Da Solutions es: /app/ (App Router: paginas, layouts y route handlers), /components/ (componentes reutilizables dentro del proyecto), /lib/ (utilidades, helpers, configuracion de clientes), /hooks/ (custom React hooks), /stores/ (stores de Zustand), /types/ (definiciones de tipos TypeScript), /styles/ (CSS Modules globales y variables), y /public/ (assets estaticos: imagenes, fuentes, iconos).",
        "### 4.2 Patron de Colocation",
        "Los archivos relacionados a un componente viven juntos en la misma carpeta (colocation). Una carpeta de componente tipica contiene: index.tsx (el componente en si), NombreComponente.module.css (los estilos del componente), NombreComponente.test.tsx (los tests del componente), y NombreComponente.stories.tsx (la story de Storybook). Esta estructura facilita encontrar todos los archivos relacionados y eliminar un componente limpiamente.",
        "### 4.3 Server vs Client Components en Next.js",
        "La regla de oro: usar Server Components por defecto y agregar 'use client' solo cuando sea necesario. Los Server Components son mejores para: acceso a datos (fetch de APIs, lectura de DB), operaciones con secrets (no expuestas al cliente), componentes grandes que no necesitan interactividad. Los Client Components son necesarios para: event listeners (onClick, onChange), useState y useEffect, APIs del navegador (localStorage, geolocation), componentes de terceros que usan hooks.",
        "### 4.4 Estado de la Aplicacion con Zustand",
        "Para el estado global que debe compartirse entre componentes no relacionados, usamos Zustand. Principios para el uso de Zustand en Da&amp;Da Solutions: cada store debe tener un unico proposito y ser tipado completamente con TypeScript, el estado del servidor (datos de APIs) no debe vivir en Zustand — para eso existe TanStack Query, los stores deben ser planos cuando sea posible (evitar estado anidado profundo), y usar immer middleware cuando el estado es complejo y la mutabilidad directa seria mas legible.",
        "### 4.5 Estado del Servidor con TanStack Query",
        "TanStack Query (React Query v5) es la herramienta estandar para manejar estado del servidor en Da&amp;Da Solutions. Gestiona automaticamente el caching, la revalidacion en foco/reconexion, el estado de loading/error/success, y la deduplicacion de requests. Las queryKeys deben ser descriptivas y estructuradas como arrays para facilitar la invalidacion granular del cache.",
        "---",
        "## 5. Estilos y CSS",
        "### 5.1 CSS Modules — Estrategia Principal",
        "CSS Modules es el enfoque estandar para estilos en Da&amp;Da Solutions. Garantiza que las clases CSS sean locales al componente, evitando colisiones de nombres globales. Los archivos de CSS Modules tienen la extension .module.css. El uso de Tailwind CSS esta explicitamente prohibido en proyectos nuevos: su enfoque de utility-first genera codigo HTML verboso y dificulta la customizacion profunda del design system.",
        "### 5.2 Custom Properties (Variables CSS)",
        "Todos los tokens del design system (colores, tipografia, espaciado, bordes, sombras) estan definidos como CSS Custom Properties en el scope :root del archivo de estilos globales. Los componentes y las paginas siempre deben referenciar estas variables en lugar de valores hardcodeados. Esto permite theming consistente y actualizaciones del design system sin modificar los componentes individuales.",
        "### 5.3 Animaciones y Transiciones",
        "Las animaciones deben ser sutiles, rapidas y con proposito. Reglas: las micro-interacciones (hover, focus, active) deben usar transiciones CSS de 150-200ms con una curva ease-out; las animaciones de aparicion/desaparicion de modales y drawers usan 250-350ms; las animaciones de pagina o de carga de datos usan 300-500ms. Siempre incluir el media query @media (prefers-reduced-motion: reduce) para usuarios con sensibilidad al movimiento.",
        "---",
        "## 6. Testing de Componentes de UI",
        "### 6.1 Filosofia de Testing de UI",
        "La filosofia de testing de Da&amp;Da Solutions para UI sigue el principio de Kent C. Dodds: testear el comportamiento, no la implementacion. Los tests no deben saber como esta construido internamente un componente; solo deben verificar lo que el usuario ve y puede hacer. Esto hace que los tests sean resilientes a refactorizaciones internas.",
        "### 6.2 Tests Unitarios de Componentes con React Testing Library",
        "Para proyectos con Vite usamos Vitest + React Testing Library. Para proyectos con Next.js usamos Jest + React Testing Library. Las queries recomendadas en orden de preferencia son: getByRole (refleja el DOM semantico y la accesibilidad), getByLabelText (para inputs asociados a labels), getByPlaceholderText (cuando no hay label), getByText (para texto visible), y getByTestId (como ultimo recurso, usando data-testid).",
        "### 6.3 Tests de Accesibilidad Automatizados",
        "Integramos axe-core mediante @testing-library/jest-axe en todos los tests de componentes. Esto permite detectar automaticamente violaciones de accesibilidad (contraste insuficiente, elementos interactivos sin nombre accesible, jerarquia de headings incorrecta) como parte del proceso de CI, antes de que lleguen a produccion.",
        "### 6.4 Storybook y Tests de Regresion Visual con Chromatic",
        "Todos los componentes del design system tienen stories en Storybook. Cada story representa un estado diferente del componente (default, hover, disabled, loading, error, etc.). Chromatic toma screenshots de cada story y los compara con la version anterior para detectar regresiones visuales automaticamente. Un cambio visual no intencional en el design system bloquea el merge.",
        "### 6.5 Tests End-to-End con Playwright",
        "Los flujos criticos de usuario tienen tests E2E escritos con Playwright: registro, login, recuperacion de contrasena, flujo de pago, y las acciones principales de cada producto. Playwright ofrece: soporte nativo para multiples browsers (Chromium, Firefox, WebKit), modo de testing de accesibilidad integrado, y capacidad de simular condiciones de red (slow 3G, offline). Los tests E2E corren en el pipeline de CI contra el entorno de staging.",
        "---",
        "## 7. Performance Web",
        "### 7.1 Core Web Vitals — Objetivos de Da&Da Solutions",
        "El equipo de Front-end monitorea continuamente los Core Web Vitals de todos los productos publicos. Los objetivos son: LCP (Largest Contentful Paint) menor a 2.5 segundos, INP (Interaction to Next Paint, reemplaza FID) menor a 200ms, y CLS (Cumulative Layout Shift) menor a 0.1. El cumplimiento de estos objetivos se reporta semanalmente en el dashboard de Grafana y es parte de los OKRs del equipo de Front-end.",
        "### 7.2 Estrategias de Optimizacion de Performance",
        "Code splitting: Next.js realiza code splitting automatico por ruta. Para componentes pesados dentro de una pagina (editores de texto rico, graficos complejos, mapas), usar React.lazy() con Suspense. Optimizacion de imagenes: usar siempre el componente Image de Next.js que realiza lazy loading, redimensionamiento automatico, conversion a WebP/AVIF y CDN automaticamente. Prefetching: Next.js realiza prefetch automatico de las rutas de los Link visibles en el viewport.",
        "### 7.3 Analisis y Monitoreo de Bundle",
        "El tamano del bundle JavaScript es una metrica critica de performance. Para analizarlo usamos @next/bundle-analyzer (genera un treemap visual de las dependencias). Regla: ninguna dependencia nueva de mas de 50 KB minificada + gzip puede agregarse sin revision del Tech Lead. La herramienta bundlephobia.com es un buen punto de partida para evaluar el impacto de una nueva dependencia antes de instalarla.",
        "---",
        "## 8. Accesibilidad",
        "### 8.1 Compromiso con la Accesibilidad",
        "Da&amp;Da Solutions esta comprometida con construir productos usables por todas las personas, independientemente de sus capacidades. La accesibilidad no es una caracteristica adicional: es un requisito de calidad. Todos los productos publicos de Da&amp;Da deben cumplir el nivel AA del estandar WCAG 2.1.",
        "### 8.2 Principios Clave de Accesibilidad",
        "Contraste de color: minimo 4.5:1 para texto normal (menos de 24px), 3:1 para texto grande. Navegacion por teclado: toda funcionalidad debe ser accesible sin raton usando Tab, Shift+Tab, Enter y las teclas de flecha cuando corresponda. Nombres accesibles: todos los elementos interactivos (botones, links, inputs) deben tener un nombre accesible visible o via aria-label. Estructura semantica: usar los elementos HTML correctos (button para botones, a para links, h1-h6 para headings, form para formularios). Gestion del foco: cuando se abre un modal, el foco debe moverse al modal y estar atrapado dentro hasta que se cierre.",
        "---",
        "## 9. Internacionalizacion y Localizacion",
        "Da&amp;Da Solutions opera en multiples paises y lenguajes. Para aplicaciones que sirven a multiples locales usamos next-intl (para Next.js) o i18next (para Vite + React). Principios de i18n: todos los strings visibles al usuario deben estar externalizados en archivos de traduccion JSON, nunca hardcodeados en el componente; las fechas y numeros deben formatearse usando la API nativa Intl del navegador con la locale del usuario; las imagenes y el contenido pueden variar por region y deben tener una estrategia de localizacion documentada.",
        "---",
        "## 10. Despliegue de Aplicaciones Front-end",
        "### 10.1 Aplicaciones Next.js en Vercel",
        "Las aplicaciones Next.js publicas se despliegan en Vercel. Vercel ofrece: Preview Deployments automaticos para cada PR (la URL del preview se agrega automaticamente como comentario en el PR de GitHub), Edge Network global para distribucion del contenido, optimizacion automatica de imagenes y analytics de Core Web Vitals integrados.",
        "### 10.2 SPAs Internas en AWS CloudFront",
        "Las SPAs internas (dashboards, herramientas de backoffice) se despliegan como assets estaticos en un bucket S3 servido por CloudFront con cache agresivo. El pipeline de CD construye el bundle de produccion, lo sube a S3 y realiza la invalidacion de cache de CloudFront automaticamente.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 4. MICROSERVICES  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="microservices_architecture.pdf",
    title="Arquitectura de Microservicios en Da&Da Solutions",
    subtitle="Vision general, principios de diseno y estandares para sistemas distribuidos",
    blocks=[
        "## 1. Historia y Motivacion de la Arquitectura",
        "Da&amp;Da Solutions inicio en 2014 con una arquitectura monolitica en Rails que permitio llegar rapidamente al mercado. A medida que el negocio crecio y el equipo se expande mas alla de 20 ingenieros, los ciclos de desarrollo del monolito comenzaron a hacerse mas lentos: cualquier cambio requeria entender el sistema completo, los deployments eran riesgosos y frecuentemente requerian rollbacks, y era imposible escalar horizontalmente solo la parte del sistema bajo mayor carga.",
        "En 2019, Da&amp;Da Solutions comenzo una migracion estrategica hacia una arquitectura de microservicios mediante el patron Strangler Fig: extrayendo funcionalidades del monolito de forma incremental hacia servicios independientes, sin una gran migracion big-bang. Este proceso duro aproximadamente 18 meses y hoy el monolito original esta completamente reemplazado.",
        "---",
        "## 2. Principios Fundamentales",
        "### 2.1 Single Responsibility por Dominio de Negocio",
        "Cada microservicio en Da&amp;Da Solutions es responsable de un unico dominio de negocio bien definido. Los limites entre servicios siguen los conceptos de Domain-Driven Design (DDD): cada servicio representa un Bounded Context con su propio lenguaje ubiquo (Ubiquitous Language), su propio modelo de dominio, y sus propias reglas de negocio. Los servicios no comparten modelos de datos ni logica de negocio entre si.",
        "### 2.2 Autonomia e Independencia Total",
        "Cada microservicio puede ser desarrollado, testeado, desplegado y escalado de forma completamente independiente de los demas. Esto implica tres cosas criticas: cada servicio tiene su propia base de datos (no hay bases de datos compartidas), cada servicio tiene su propio repositorio de codigo y su propio pipeline de CI/CD, y cada servicio puede deployarse en produccion sin coordinacion con otros equipos.",
        "La autonomia de deployment es la que permite que equipos distintos trabajen en velocidades distintas sin bloquearse entre si. Un bug critico en el servicio de Facturacion puede deployarse como hotfix en minutos sin tocar el servicio de Usuarios.",
        "### 2.3 Resiliencia ante Fallos de Dependencias",
        "En un sistema distribuido, cualquier componente puede fallar en cualquier momento. Los microservicios de Da&amp;Da Solutions estan disenados bajo el principio 'failure is the normal case'. Esto significa que ningun servicio asume que sus dependencias (otros servicios, bases de datos, APIs externas) van a estar disponibles el 100% del tiempo. Los patrones de resiliencia (Circuit Breaker, Retry, Timeout, Bulkhead) son requisitos no funcionales, no optimizaciones opcionales.",
        "### 2.4 Ownership por Equipo",
        "Cada microservicio tiene un squad dueno que es responsable de su ciclo de vida completo: desarrollo, testing, deployment, monitoreo y operacion. El principio 'you build it, you run it' garantiza que los equipos tengan incentivos naturales para construir servicios confiables, observables y mantenibles.",
        "---",
        "## 3. Catalogo Completo de Servicios",
        "### 3.1 Servicios de Negocio (Domain Services)",
        "Estos servicios encapsulan la logica de negocio central de la plataforma:",
        "- <b>auth-service:</b> Autenticacion y gestion de sesiones. JWT, OAuth 2.0, SSO. Python/FastAPI. PostgreSQL.",
        "- <b>user-profile-service:</b> Perfiles, preferencias y configuraciones de usuario. Node.js/NestJS. PostgreSQL.",
        "- <b>billing-service:</b> Suscripciones, facturacion, historial de pagos. Python/FastAPI. PostgreSQL. Stripe.",
        "- <b>payment-service:</b> Procesamiento de pagos y gestion de metodos de pago. Python/FastAPI. PostgreSQL.",
        "- <b>product-catalog-service:</b> Catalogo de productos, precios y planes. Node.js/NestJS. MongoDB.",
        "- <b>order-service:</b> Creacion y gestion del ciclo de vida de ordenes. Python/FastAPI. PostgreSQL.",
        "- <b>inventory-service:</b> Control de stock y disponibilidad. Go. PostgreSQL.",
        "- <b>notification-service:</b> Email (SendGrid), SMS (Twilio), Push (Firebase), In-App. Node.js. Redis.",
        "- <b>analytics-service:</b> Captura y consulta de eventos de analitica de producto. Python. ClickHouse.",
        "- <b>search-service:</b> Busqueda full-text y facetada. Python. Elasticsearch.",
        "### 3.2 Servicios de Plataforma (Platform/Infra Services)",
        "Estos servicios proveen funcionalidad de infraestructura transversal a todos los servicios de negocio:",
        "- <b>api-gateway:</b> Punto de entrada unico, autenticacion, rate limiting, enrutamiento. Go. Redis.",
        "- <b>config-service:</b> Distribucion centralizada de configuracion dinamica. Go. Consul.",
        "- <b>file-storage-service:</b> Upload, procesamiento y entrega de archivos y medios. Python. GCS.",
        "- <b>audit-service:</b> Registro de eventos de auditoria para compliance. Python. ClickHouse.",
        "---",
        "## 4. Comunicacion Entre Servicios",
        "### 4.1 Principio: Asincronia Primero",
        "El principio rector de la comunicacion entre servicios en Da&amp;Da Solutions es: preferir la comunicacion asincrona sobre la sincrona siempre que sea posible. La comunicacion sincrona crea acoplamiento temporal entre servicios: si el servicio A hace una llamada sincrona al servicio B y B esta lento o caido, A se degrada tambien. La comunicacion asincrona a traves de eventos desacopla los servicios en el tiempo.",
        "### 4.2 Apache Kafka — El Backbone de Eventos",
        "Apache Kafka es el bus de eventos central de Da&amp;Da Solutions. Todos los eventos de dominio importantes se publican como mensajes de Kafka. Kafka provee: durabilidad (los mensajes se persisten en disco), replayability (cualquier consumidor puede re-leer el historial de un topico desde un offset especifico), escalabilidad horizontal (particiones y consumer groups), y alta disponibilidad (factor de replicacion minimo 3 en produccion).",
        "Convenciones de topicos de Kafka: el nombre del topico sigue el formato {dominio}.{entidad}.{evento-en-pasado}. Ejemplos: billing.invoice.created, user.account.password_changed, order.fulfillment.shipped, inventory.stock.replenished. Los nombres en snake_case y en ingles por convencion de equipo.",
        "Los mensajes de Kafka deben serializarse con Apache Avro con schemas registrados en el Confluent Schema Registry. Avro proporciona evolucion de schemas con compatibilidad garantizada (backward, forward, o full segun el caso). Cualquier cambio a un schema existente debe evaluarse con respecto a su impacto en los consumidores existentes.",
        "### 4.3 gRPC — Comunicacion Sincrona de Alta Performance",
        "Para los casos donde la comunicacion sincrona es inevitablemente necesaria y la performance es critica, usamos gRPC sobre HTTP/2. gRPC provee: contratos fuertemente tipados definidos en Protocol Buffers, generacion automatica de clientes y servidores en multiples lenguajes, streaming bidireccional, y mejor performance que REST para payloads binarios. Los archivos .proto de todos los servicios viven en el repositorio centralizado dada-solutions/proto-registry, lo que garantiza que los contratos son la fuente de verdad compartida.",
        "### 4.4 REST — Para Casos Simples y APIs Publicas",
        "El uso de REST para comunicacion interna entre servicios se acepta cuando la performance no es critica y la simplicidad es prioritaria. Para la comunicacion sincrona interna, los clientes HTTP deben ser generados automaticamente desde la especificacion OpenAPI del servicio provider. Esto garantiza que los clientes siempre esten sincronizados con el contrato actual del servidor.",
        "---",
        "## 5. Patrones de Resiliencia",
        "### 5.1 Circuit Breaker",
        "El Circuit Breaker protege a un servicio de las fallas en cascada causadas por una dependencia degradada. Funciona como un disyuntor electrico: cuando detecta un nivel de fallos suficientemente alto en las llamadas a una dependencia, 'abre' el circuito y comienza a rechazar llamadas inmediatamente (fail fast) sin esperar el timeout. Despues de un tiempo de espera, el circuito pasa a 'half-open' y permite una llamada de prueba. Si la prueba tiene exito, el circuito se cierra.",
        "En Da&amp;Da Solutions usamos tenacity (Python) y resilience4j-like patterns en Node.js. Los umbrales de apertura del circuit breaker (failure_rate_threshold, wait_duration_in_open_state) deben estar configurados externamente via variables de entorno para poder ajustarlos en produccion sin redeploy.",
        "### 5.2 Retry con Backoff Exponencial y Jitter",
        "Los reintentos automaticos son necesarios para manejar fallos transitorios (network timeouts, throttling de APIs externas). Sin embargo, los reintentos mal implementados pueden empeorar una situacion de sobrecarga: si todos los clientes reintentan simultaneamente despues del mismo intervalo fijo, crean una 'tormenta de reintentos' (thundering herd) que amplifica el problema.",
        "La formula de backoff con jitter aleatorio de Da&amp;Da Solutions: delay = min(max_delay, base_delay * (2 ** attempt)) + random(0, jitter). Los valores tipicos son: base_delay = 0.1s, max_delay = 60s, jitter = 0.1 * delay calculado. Los reintentos solo se aplican a errores retriable (5xx, timeouts) y nunca a errores de cliente (4xx).",
        "### 5.3 Timeout",
        "Toda llamada de red en Da&amp;Da Solutions debe tener un timeout configurado explicitamente. Un timeout es la ultima linea de defensa contra una dependencia que no falla sino que simplemente no responde, bloqueando un thread o coroutine indefinidamente. Timeouts estandar: 500ms para llamadas entre microservicios internos, 2s para APIs externas de terceros, 10s para operaciones de carga de archivos o procesamiento batch.",
        "### 5.4 Bulkhead (Aislamiento de Recursos)",
        "El patron Bulkhead aisla los pools de recursos por dependencia para evitar que la degradacion de una dependencia agote los recursos del servicio completo. Ejemplo: si el servicio de Notificaciones es lento, su semaphore o connection pool no debe quitarle recursos a las llamadas del servicio de Usuarios. En Da&amp;Da usamos semaphores asyncronos en Python (asyncio.Semaphore) y thread pool separation en Go.",
        "---",
        "## 6. API Gateway",
        "### 6.1 El API Gateway como Frontera del Sistema",
        "El API Gateway es el unico punto de entrada al sistema para todos los clientes externos (aplicaciones web, moviles e integraciones de terceros). Su presencia tiene ventajas criticas: centraliza la autenticacion (un solo lugar para verificar tokens JWT en lugar de hacerlo en cada servicio), permite implementar rate limiting y proteccion DDoS sin tocar el codigo de los servicios de negocio, y simplifica el cliente al exponer una interfaz unica en lugar de multiples endpoints de servicio.",
        "### 6.2 Implementacion con Go",
        "El API Gateway de Da&amp;Da Solutions esta implementado en Go por sus caracteristicas ideales para este tipo de proxy de alta concurrencia: goroutines para manejar miles de conexiones simultaneas con minimo overhead de memoria, libreria estandar robusta para HTTP y TLS, y rendimiento cercano al del sistema operativo sin necesidad de frameworks pesados. El codigo del gateway vive en dada-solutions/api-gateway.",
        "### 6.3 Rate Limiting",
        "El rate limiting del API Gateway usa el algoritmo Token Bucket implementado sobre Redis para garantizar distribucion entre multiples instancias del gateway. Los limites por defecto son: 1000 requests/minuto para usuarios autenticados (ajustable por plan de suscripcion), 100 requests/minuto por IP para requests no autenticados. Las respuestas incluyen los headers RateLimit-Limit, RateLimit-Remaining y Retry-After cuando el limite es alcanzado.",
        "---",
        "## 7. Datos y Gestion del Estado Distribuido",
        "### 7.1 Aislamiento de Bases de Datos",
        "La regla de aislamiento de datos es la mas importante y la mas inviolable de toda la arquitectura de microservicios: ningun servicio puede leer o escribir directamente en la base de datos de otro servicio. Esta regla existe porque compartir una base de datos crea un acoplamiento tan profundo entre los servicios que hace imposible cambiar el esquema de datos de uno sin impactar a todos los otros. Si el Servicio A necesita datos del Servicio B, los debe pedir a traves de la API del Servicio B.",
        "### 7.2 Event Sourcing para Dominios Criticos",
        "Para dominios con alta necesidad de auditoria y trazabilidad (Facturacion, Pagos, Inventario), Da&amp;Da Solutions usa Event Sourcing. En lugar de almacenar solo el estado actual de una entidad, Event Sourcing almacena la secuencia completa de eventos que llevaron a ese estado. El estado actual se reconstruye reproduciendo los eventos. Esto provee: un audit trail completo e inmutable, la capacidad de reconstruir el estado en cualquier punto del tiempo (time travel), y la capacidad de agregar nuevas proyecciones sin modificar el modelo de escritura.",
        "### 7.3 CQRS (Command Query Responsibility Segregation)",
        "Junto con Event Sourcing, Da&amp;Da Solutions usa CQRS en los mismos dominios de alta criticidad. CQRS separa el modelo de escritura (Commands, que producen Events) del modelo de lectura (Queries, que consultan proyecciones optimizadas). Las proyecciones son vistas desnormalizadas de los datos diseñadas especificamente para los patrones de lectura de cada caso de uso, almacenadas en el modelo de datos mas adecuado (PostgreSQL para reportes, Redis para datos de acceso frecuente, Elasticsearch para busqueda).",
        "---",
        "## 8. Saga Pattern para Transacciones Distribuidas",
        "### 8.1 Por que no 2PC (Two-Phase Commit)",
        "Las transacciones ACID tradicionales que abarcan multiples servicios son imposibles en una arquitectura de microservicios sin un mecanismo de coordinacion centralizado como el Two-Phase Commit (2PC). El problema del 2PC es que es fragil (si el coordinador falla entre fases, los participantes pueden quedar bloqueados) y no escala bien (bloquea recursos en todos los participantes durante la fase de preparacion).",
        "### 8.2 Saga Coreografiada",
        "En la Saga Coreografiada, no hay un coordinador central. Cada servicio participa publicando eventos cuando completa su parte de la transaccion y suscribiendose a los eventos de otros servicios para saber cuando es su turno. Si una transaccion falla en un paso intermedio, cada servicio sabe que transacciones compensatorias debe ejecutar en respuesta al evento de fallo.",
        "Este estilo es ideal para procesos simples (2-3 pasos) porque es mas facil de implementar y no requiere infraestructura adicional. La desventaja es que es dificil rastrear el estado global de la saga a medida que la cantidad de pasos y servicios crece.",
        "### 8.3 Saga Orquestada",
        "En la Saga Orquestada, existe un componente Orchestrator (generalmente un servicio separado) que coordina los pasos de la saga enviando comandos a cada servicio y esperando su respuesta. El Orchestrator mantiene el estado de la saga (paso actual, pasos compensados) y toma las decisiones de control de flujo.",
        "Da&amp;Da Solutions usa Saga Orquestada para procesos de negocio complejos como el proceso de checkout (que involucra verificar inventario, reservar stock, procesar pago, generar orden, emitir factura y enviar notificacion) porque el estado de la saga es visible y debuggeable en el Orchestrator.",
        "---",
        "## 9. Estrategias de Deployment",
        "### 9.1 Rolling Updates",
        "Los Rolling Updates de Kubernetes reemplazan gradualmente las instancias viejas de un pod con instancias de la nueva version. Durante el rolling update, el servicio opera con instancias de ambas versiones simultaneamente durante un breve periodo. Esto requiere que los cambios de schema sean backward-compatible: la nueva version del codigo debe poder operar con el schema viejo durante el periodo de transicion.",
        "### 9.2 Blue/Green Deployments",
        "Para servicios con cambios de mayor riesgo (cambios de configuracion de infraestructura, cambios de esquema importantes), Da&amp;Da usa Blue/Green Deployments. Se provisiona un segundo entorno identico (Green) con la nueva version mientras el primero (Blue) sigue en produccion. Una vez validado el Green, el trafico se redirige atomicamente. El rollback es instantaneo (redirigir el trafico de vuelta a Blue).",
        "### 9.3 Canary Deployments",
        "Los Canary Deployments exponen la nueva version solo a una fraccion del trafico de produccion para validar su comportamiento con usuarios reales antes de un rollout completo. El proceso estandar de Da&amp;Da: 1% del trafico durante 10 minutos, observar metricas. Si las metricas son correctas: 5%, luego 25%, luego 50%, luego 100%. Si en cualquier punto las metricas se degradan, el rollback es automatico.",
        "---",
        "## 10. Documentacion de Decisiones de Arquitectura",
        "Todas las decisiones de arquitectura significativas en Da&amp;Da Solutions se documentan en Architecture Decision Records (ADRs). Un ADR responde: cual era el contexto y el problema, cuales eran las opciones consideradas, cual fue la decision y por que, y cuales son las consecuencias (positivas y negativas) de esa decision.",
        "El repositorio de ADRs vive en dada-solutions/architecture-decisions en GitHub. Cada ADR tiene un estado: Proposed (en discusion), Accepted (decision tomada), Deprecated (reemplazada por otra decision), o Superseded (reemplazada por un ADR especifico). Cualquier ingeniero puede proponer un ADR. Las decisiones de impacto cross-equipo requieren aprobacion de al menos dos Staff Engineers.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 5. DEVOPS  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="devops_cicd.pdf",
    title="Manual de DevOps y CI/CD",
    subtitle="Guia completa de infraestructura, despliegues, monitoreo y cultura DevOps",
    blocks=[
        "## 1. La Cultura DevOps en Da&Da Solutions",
        "DevOps en Da&amp;Da Solutions no es un equipo de silos ni un cargo especifico: es una cultura y un conjunto de practicas compartidas entre todos los ingenieros de la organizacion. El equipo de Platform Engineering provee las herramientas, la plataforma y el soporte, pero la responsabilidad operacional de cada servicio recae en el squad que lo construye.",
        "El mantra de Da&amp;Da Solutions: 'If you built it, you run it'. Esta responsabilidad compartida tiene consecuencias positivas y deliberadas: los equipos tienen un incentivo natural para construir software que sea confiable (porque son los primeros en ser despertados a las 3 AM cuando hay un incidente), observable (porque son ellos quienes tienen que diagnosticar los problemas) y operable (porque son ellos quienes tienen que ejecutar los runbooks).",
        "---",
        "## 2. Infraestructura Cloud — Google Cloud Platform",
        "### 2.1 La Eleccion de GCP",
        "Da&amp;Da Solutions usa Google Cloud Platform (GCP) como proveedor de nube principal. La eleccion se baso en tres factores: la calidad superior de los servicios de datos y ML (BigQuery, Vertex AI, Dataflow), la red global de fibra de Google que reduce la latencia para usuarios en Latinoamerica, y los terminos contractuales competitivos para el volumen de uso de Da&amp;Da Solutions.",
        "Los servicios de GCP mas usados son: GKE (Kubernetes Engine) para la orquestacion de contenedores, Cloud SQL para PostgreSQL y MySQL gestionados, Cloud Spanner para bases de datos globalmente distribuidas, GCS (Cloud Storage) para almacenamiento de objetos, Cloud Run para servicios serverless, Pub/Sub como backup de Kafka para algunos casos de uso, BigQuery para analitica a gran escala, y Vertex AI para el hosting de modelos de ML.",
        "### 2.2 Principio: Infraestructura Multi-Region",
        "Todos los servicios criticos de produccion corren en al menos dos regiones de GCP (us-central1 y southamerica-east1) para garantizar disponibilidad ante fallos de region completa. El trafico se distribuye entre regiones usando Global Load Balancing de GCP con failover automatico en menos de 60 segundos.",
        "---",
        "## 3. Contenedores y Docker",
        "### 3.1 Docker como Estandar Universal",
        "Cada servicio de Da&amp;Da Solutions es una imagen Docker. Esta estandarizacion tiene beneficios concretos: el mismo artefacto (imagen Docker) es el que se prueba en CI, se promueve a staging y se deploya en produccion, eliminando la categoria de bugs 'funciona en mi maquina'. El entorno de desarrollo local (docker-compose) es un subconjunto del entorno de produccion (Kubernetes).",
        "### 3.2 Buenas Practicas de Dockerfile",
        "Cada Dockerfile en Da&amp;Da Solutions debe seguir estas practicas: usar imagenes base minimas (preferir python:3.11-slim o node:20-alpine sobre imagenes completas); usar multi-stage builds para separar el entorno de build del entorno de runtime (la imagen final no debe incluir compiladores, herramientas de build ni dependencias de desarrollo); copiar primero los archivos de definicion de dependencias (requirements.txt, package.json) antes que el codigo fuente para maximizar el uso del cache de capas; ejecutar el proceso principal como un usuario no-root creado especificamente para la aplicacion; definir siempre el HEALTHCHECK instruction y el ENTRYPOINT y CMD correctos.",
        "### 3.3 Google Artifact Registry",
        "Todas las imagenes Docker de Da&amp;Da Solutions se almacenan en Google Artifact Registry (GAR), organizado en repositorios por dominio (backend, frontend, data, infra). El pipeline de CI construye y sube las imagenes con dos tags: el SHA corto del commit de Git y el tag de la version semantica cuando corresponde. El tag latest no se usa en produccion.",
        "---",
        "## 4. Kubernetes en Da&Da Solutions",
        "### 4.1 Clusteres y Entornos",
        "Da&amp;Da Solutions opera tres clusteres de GKE: development (para ramas de feature y PRs), staging (replica de produccion para validacion final), y production (multi-zona para alta disponibilidad). El acceso a los clusteres esta controlado mediante GCP IAM + Kubernetes RBAC: los desarrolladores tienen acceso de solo lectura al cluster de produccion y acceso completo al de development.",
        "### 4.2 Manifiestos de Kubernetes",
        "Los manifiestos de Kubernetes (Deployments, Services, ConfigMaps, Secrets, HPA, PDB, NetworkPolicies, etc.) viven en el repositorio dada-solutions/k8s-manifests, organizados por entorno (overlays de Kustomize) y por namespace. Este repositorio es la fuente de verdad de lo que esta desplegado en produccion y es gestionado con el patron GitOps (ArgoCD).",
        "### 4.3 Configuracion de Recursos — CPU y Memoria",
        "Todo Pod en produccion debe tener configurados los Resource Requests y Limits de CPU y memoria. Los Requests son la garantia minima de recursos que Kubernetes reserva para el Pod; los Limits son el maximo que puede consumir. Los valores se calibran basandose en los datos de consumo real del servicio observados en Grafana durante al menos 2 semanas en staging.",
        "Regla: los Limits de CPU nunca deben ser mas del doble de los Requests (para evitar throttling agresivo). Para memoria, los Limits pueden ser 1.5x-2x los Requests para acomodar picos razonables. Un Pod sin Resource Requests en el namespace de produccion es rechazado automaticamente por un Admission Webhook personalizado de Da&amp;Da.",
        "### 4.4 Horizontal Pod Autoscaler (HPA)",
        "Todos los servicios con carga variable tienen configurado el HPA de Kubernetes para escalar automaticamente el numero de replicas en funcion de la carga. La metrica principal es CPU Utilization con un target del 70%. Para servicios orientados a eventos (workers de Kafka), usamos KEDA (Kubernetes Event-Driven Autoscaling) que escala basandose en el lag del consumer group de Kafka en lugar de en CPU.",
        "### 4.5 Pod Disruption Budget (PDB)",
        "Para garantizar que siempre haya suficientes replicas de un servicio disponibles durante operaciones de mantenimiento (rolling updates, actualizaciones de nodos del cluster), todos los servicios con mas de una replica tienen configurado un PodDisruptionBudget. El PDB estandar de Da&amp;Da garantiza que al menos el 50% de las replicas esten disponibles en todo momento.",
        "---",
        "## 5. GitOps con ArgoCD",
        "### 5.1 El Modelo GitOps",
        "Da&amp;Da Solutions adopta el modelo GitOps para la gestion de deployments. En GitOps, el estado deseado del cluster de Kubernetes (que versiones de los servicios deben estar corriendo, con que configuracion) esta definido declarativamente en un repositorio Git. ArgoCD es el controlador que sincroniza continuamente el estado del cluster con el estado definido en Git.",
        "Las ventajas del modelo GitOps son: el historial completo de todos los cambios de infraestructura esta en Git (con autor, fecha y justificacion via PR), el rollback es tan simple como revertir un commit de Git, la divergencia entre el estado deseado (Git) y el estado actual (cluster) es detectable y alertable, y nadie puede hacer cambios manuales al cluster de produccion sin que quede registrado en Git.",
        "### 5.2 Flujo de Promocion entre Entornos",
        "El flujo de promocion de una nueva version sigue este camino: el pipeline de CI construye la imagen Docker y actualiza el tag de imagen en el manifiesto del entorno de development en el repositorio de manifiestos. ArgoCD detecta el cambio y deploya automaticamente al cluster de development. El equipo de QA valida en development. Un PR aprobado actualiza el tag en el manifiesto de staging. ArgoCD deploya a staging. Validacion en staging. Un PR aprobado por el squad (con al menos un Staff Engineer) actualiza el tag en el manifiesto de produccion. ArgoCD deploya a produccion.",
        "---",
        "## 6. Pipelines de CI/CD con GitHub Actions",
        "### 6.1 Estructura del Pipeline de Integracion Continua",
        "Cada repositorio de Da&amp;Da Solutions tiene un workflow de GitHub Actions que se dispara en cada PR y en cada push a main. El pipeline de CI ejecuta en paralelo donde es posible para minimizar el tiempo total. Los pasos son: Lint y Format Check (ruff para Python, ESLint + Prettier para TypeScript, hadolint para Dockerfile), Type Checking (mypy para Python, tsc --noEmit para TypeScript), Unit Tests (con reporte de cobertura que debe ser mayor al 80%), Integration Tests (con testcontainers para bases de datos efimeras), SAST Security Scan (Bandit para Python, Semgrep para multi-lenguaje), SCA Dependency Scan (Safety para Python, npm audit para Node.js), Docker Build and Tag (construye la imagen pero no la sube aun), Docker Security Scan (Trivy escanea la imagen por vulnerabilidades), y finalmente Docker Push to Registry (solo si todos los pasos anteriores pasaron y solo en la rama main).",
        "### 6.2 Seguridad del Pipeline",
        "La seguridad de los pipelines de CI/CD es critica: una action comprometida podria desplegar codigo malicioso en produccion. Medidas de seguridad en Da&amp;Da Solutions: siempre usar versiones exactas de Actions (actions/checkout@v4.1.1, nunca @v4 o @main, que pueden ser redireccionadas), usar OIDC (OpenID Connect) para autenticarse con GCP en lugar de service account keys de larga duracion, auditar periodicamente las Actions de terceros usadas en los workflows, y restringir los permisos del GITHUB_TOKEN al minimo necesario para cada job.",
        "### 6.3 Caching de Dependencias",
        "Para mantener los tiempos de pipeline manejables, las dependencias del proyecto se cachean agresivamente en GitHub Actions. Las dependencias de Python (el directorio .venv o el cache de pip) y de Node.js (node_modules y el cache de pnpm) se cachean usando actions/cache con una clave basada en el hash del archivo de dependencias (pyproject.toml o pnpm-lock.yaml). Solo cuando el archivo de dependencias cambia se reinstalan las dependencias desde cero.",
        "---",
        "## 7. Seguridad de la Infraestructura",
        "### 7.1 Gestion de Secretos con HashiCorp Vault",
        "Ningun secreto (contrasena de base de datos, API key de tercero, certificado TLS) se almacena en Git, en variables de entorno del SO ni en ConfigMaps de Kubernetes. Todos los secretos de produccion son gestionados por HashiCorp Vault. Los Pods de Kubernetes obtienen sus secretos mediante el Vault Agent Injector (un sidecar que se inyecta automaticamente y monta los secretos como archivos o los expone como variables de entorno al contenedor principal).",
        "### 7.2 Network Policies en Kubernetes",
        "Kubernetes permite la comunicacion entre cualquier Pod del cluster por defecto. Da&amp;Da Solutions restringe esta comunicacion usando Network Policies: por defecto, ningun Pod puede comunicarse con ningun otro. Los Network Policies explicitamente permiten solo el trafico necesario (ej: el Pod de la API puede comunicarse con el Pod de la base de datos del mismo namespace, pero no con los Pods de otros namespaces).",
        "### 7.3 Escaneo Continuo de Vulnerabilidades",
        "Las imagenes Docker se escanean no solo en el momento del build (con Trivy en el pipeline de CI) sino continuamente en produccion. El Google Artifact Registry escanea periodicamente todas las imagenes almacenadas por nuevas vulnerabilidades en sus dependencias. Cuando se detecta una vulnerabilidad CRITICAL en una imagen en produccion, se genera una alerta automatica en el canal #seguridad de Slack y el equipo debe remediarla en un plazo maximo de 7 dias.",
        "---",
        "## 8. Monitoreo y Observabilidad",
        "### 8.1 Stack de Observabilidad: Grafana Cloud",
        "Da&amp;Da Solutions usa Grafana Cloud como plataforma unificada de observabilidad. Grafana Cloud integra: Prometheus para metricas (Grafana Mimir como backend de almacenamiento de metricas de largo plazo), Loki para logs centralizados, Tempo para traces distribuidos, y el frontend de Grafana para dashboards y alertas. Todo el stack se accede desde una interfaz unificada en grafana.dadacode.io.",
        "### 8.2 Alertas y On-Call",
        "Las alertas en Grafana se configuran usando PromQL (Prometheus Query Language). Cada servicio critico tiene un conjunto de alertas que cubre: disponibilidad (el servicio esta respondiendo requests), latencia (el P99 esta por debajo del SLO), tasa de errores (el porcentaje de respuestas 5xx esta por debajo del umbral) y saturacion (CPU y memoria estan por debajo de los Limits).",
        "El sistema de on-call usa PagerDuty para el routing de alertas criticas. Las alertas de severidad P1 siempre despiertan al On-Call Engineer, sin importar el horario. Las guardias de on-call tienen una semana de duracion y se rotan entre todos los ingenieros Senior y Staff del squad. La compensacion economica por guardias esta documentada en el contrato de cada ingeniero.",
        "### 8.3 Dashboards Estandar por Servicio",
        "El equipo de Platform Engineering provee una plantilla de dashboard de Grafana estandar (en formato JSON importable) que todos los servicios deben tener configurado. Este dashboard incluye: tasa de requests por segundo (RPS) desglosada por endpoint y codigo de estado, latencia por percentil (P50, P95, P99) por endpoint, tasa de errores (porcentaje de 5xx), consumo de CPU y memoria del Pod vs Requests y Limits, y metricas de la base de datos (queries por segundo, latencia media, conexiones activas).",
        "---",
        "## 9. Gestion de Incidentes",
        "### 9.1 Clasificacion de Severidad",
        "P1 - Critico: servicio completamente no disponible o degradacion severa que afecta a todos los usuarios. Tiempo de respuesta objetivo: 5 minutos. Resolucion objetivo: 1 hora. P2 - Alto: degradacion significativa que afecta a un subconjunto grande de usuarios, pero hay un workaround disponible o el impacto es parcial. Respuesta: 15 minutos. Resolucion: 4 horas. P3 - Medio: degradacion menor con impacto limitado. Respuesta: 1 hora. Resolucion: 24 horas. P4 - Bajo: bug o degradacion cosmetica sin impacto operacional inmediato. Respuesta: 24 horas. Resolucion: proximo sprint.",
        "### 9.2 Proceso de Respuesta a Incidentes",
        "Paso 1 - Deteccion: las alertas automaticas de PagerDuty o el reporte de un usuario notifican el inicio del incidente. Paso 2 - Notificacion: el On-Call Engineer crea un thread en el canal #incidentes con el formato: [P1] Titulo del incidente | Impacto | Servicios afectados. Paso 3 - Asignacion de roles: se designa un Incident Commander (IC) que coordina la respuesta, y un Communications Lead que actualiza a los stakeholders. Paso 4 - Mitigacion: el objetivo inmediato es restaurar el servicio, no encontrar la causa raiz. Las herramientas de mitigacion disponibles son: rollback del deployment, feature flags para desactivar la funcionalidad afectada, escalado horizontal para aumentar capacidad, y desvio de trafico a la region de respaldo. Paso 5 - Resolucion: una vez que el servicio esta restaurado, se documenta la linea de tiempo del incidente. Paso 6 - Post-mortem: dentro de las 48 horas de la resolucion, el equipo conduce un post-mortem blameless.",
        "### 9.3 Post-Mortems Blameless",
        "El post-mortem es el documento mas valioso que produce un incidente. Su proposito no es encontrar culpables sino entender la causa raiz sistematica y definir acciones concretas para prevenir recurrencias. El post-mortem sigue la estructura de Google SRE: titulo y severidad, resumen ejecutivo (que paso, durante cuanto tiempo, cual fue el impacto), linea de tiempo de eventos (con horarios precisos), causa raiz (usando los 5 Porques), factores contribuyentes, impacto detallado, acciones de mitigacion tomadas durante el incidente, y acciones preventivas con owner y fecha limite.",
        "---",
        "## 10. Infraestructura como Codigo con Terraform",
        "Toda la infraestructura cloud de Da&amp;Da Solutions (clusters de GKE, bases de datos de Cloud SQL, topicos de Pub/Sub, buckets de GCS, reglas de red, IAM) esta definida en codigo usando Terraform. Los modulos de Terraform viven en el repositorio dada-solutions/infrastructure, organizados por componente y entorno.",
        "El proceso de cambio de infraestructura es identico al de codigo: un PR en GitHub con descripcion del cambio, revision por al menos un miembro del equipo de Platform Engineering, y merge a main solo despues de aprobacion. El pipeline de CD aplica los cambios de Terraform automaticamente al ambiente correspondiente. Los cambios manuales a la infraestructura de produccion desde la consola de GCP estan prohibidos y son detectados por una alerta de drift de Terraform que se ejecuta periodicamente.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 6. DATA PERSISTENCE  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="data_persistence.pdf",
    title="Guia de Persistencia de Datos",
    subtitle="Estandares de modelado, almacenamiento, seguridad y gestion de datos en Da&amp;Da Solutions",
    blocks=[
        "## 1. Principios de Gestion de Datos",
        "Los datos son el activo mas valioso de Da&amp;Da Solutions y de nuestros clientes. Una decision incorrecta sobre como almacenar o manejar datos puede tener consecuencias irreversibles: perdida de informacion, corrupcion de registros, violaciones de privacidad o incumplimiento regulatorio. Por esto, la gestion de datos requiere el nivel mas alto de rigor tecnico.",
        "El principio rector de la seleccion de tecnologia de persistencia en Da&amp;Da Solutions es: elegir el motor de base de datos mas adecuado para el patron de acceso especifico de cada dominio, no el que ya se conoce o el que esta de moda. No existe una base de datos que sea optima para todos los casos de uso.",
        "---",
        "## 2. PostgreSQL — La Base de Datos por Defecto",
        "### 2.1 Cuando usar PostgreSQL",
        "PostgreSQL es la base de datos por defecto para la gran mayoria de los servicios de Da&amp;Da Solutions. Se elige cuando: los datos tienen relaciones complejas entre entidades con integridad referencial (claves foraneas), el dominio requiere transacciones ACID complejas (transferencias de dinero, actualizaciones de inventario transaccionales), los datos son de naturaleza tabular con esquema estable y bien definido, o se necesitan capacidades de consulta avanzadas (CTEs recursivas, window functions, full-text search integrado).",
        "### 2.2 Version y Configuracion de Produccion",
        "La version minima de PostgreSQL soportada en Da&amp;Da Solutions es la 15 (aprovechamos las mejoras de performance del merge join y las nuevas features de particionamiento). En produccion, PostgreSQL corre en Cloud SQL de GCP (servicio gestionado) con la siguiente configuracion base: max_connections = (vCPUs * 100), shared_buffers = 25% de la RAM, effective_cache_size = 75% de la RAM, work_mem = RAM / (max_connections * 2), random_page_cost = 1.1 (para SSDs).",
        "### 2.3 Migraciones de Esquema — La Operacion Mas Riesgosa",
        "Las migraciones de esquema de bases de datos son la operacion mas riesgosa en el ciclo de vida de un servicio. Una migracion mal ejecutada puede resultar en downtime, perdida de datos o inconsistencias imposibles de revertir. Las reglas de oro de Da&amp;Da Solutions para migraciones:",
        "Primera regla: todas las migraciones deben ser backward-compatible. El codigo viejo debe poder correr correctamente con el esquema nuevo, y el codigo nuevo debe poder correr correctamente con el esquema viejo. Esto permite el deployment rolling sin downtime y facilita los rollbacks.",
        "Segunda regla: nunca se ejecutan migraciones manuales en produccion. Todas las migraciones se ejecutan automaticamente como parte del proceso de deployment del servicio, usando el mecanismo de migracion del proyecto (Alembic para Python, Prisma Migrate para Node.js).",
        "Tercera regla: las operaciones peligrosas requieren un proceso de migracion en multiples releases. Renombrar una columna: Release 1 — agregar la columna nueva y copiar los datos, actualizar el codigo para leer de ambas columnas. Release 2 — actualizar el codigo para escribir en la columna nueva, seguir leyendo de ambas. Release 3 — eliminar la columna vieja. Eliminar una columna o tabla: primero deprecar (dejar de leer y escribir), luego en un release posterior eliminar.",
        "### 2.4 Connection Pooling con PgBouncer",
        "PostgreSQL tiene un costo no trivial por conexion simultanea: cada conexion consume aproximadamente 5-10 MB de memoria en el servidor de base de datos. En un sistema de microservicios con decenas de instancias de cada servicio, el numero de conexiones directas puede rapidamente superar el limite de PostgreSQL. Da&amp;Da Solutions usa PgBouncer como connection pooler frente a todas las instancias de PostgreSQL en produccion.",
        "PgBouncer se configura en modo transaction pooling: una conexion fisica al servidor de PostgreSQL se comparte entre multiples clientes durante las pausas entre transacciones. Esto permite que 100 instancias de un servicio compartan eficientemente 20 conexiones fisicas al servidor.",
        "### 2.5 Diseno de Indices",
        "Los indices son el mecanismo de optimizacion mas poderoso en PostgreSQL, pero tambien el mas facil de usar incorrectamente. Principios de diseno de indices en Da&amp;Da Solutions: crear un indice por cada columna que aparece frecuentemente en clausulas WHERE, JOIN ON o ORDER BY de las queries mas ejecutadas; usar indices compuestos (multi-columna) cuando hay patrones de query que siempre filtran por dos o mas columnas juntas; evitar indices en columnas de baja cardinalidad (boolean, status con pocos valores); usar indices parciales para indexar solo el subconjunto de filas que realmente se consulta; y monitorear regularmente pg_stat_user_indexes para detectar indices no usados (io_unused > threshold).",
        "Operacion critica: agregar un indice en una tabla de produccion con millones de filas NUNCA debe hacerse con CREATE INDEX (bloquea la tabla). SIEMPRE usar CREATE INDEX CONCURRENTLY, que construye el indice sin bloquear las operaciones de lectura y escritura existentes.",
        "### 2.6 Particionamiento para Tablas Grandes",
        "Las tablas de Da&amp;Da Solutions que crecen indefinidamente (logs, eventos de analitica, transacciones historicas) usan particionamiento declarativo de PostgreSQL. La estrategia mas comun es el particionamiento por rango de fecha (PARTITION BY RANGE (created_at)). Las particiones viejas (historico de mas de 2 anios) se mueven a tablespaces en almacenamiento mas economico o se archivan en GCS.",
        "---",
        "## 3. MongoDB — Para Datos Documentales",
        "### 3.1 Cuando usar MongoDB",
        "MongoDB es la opcion correcta cuando: el esquema de datos es genuinamente dinamico y variable entre documentos del mismo tipo (ej: un catalogo de productos donde cada categoria tiene atributos completamente distintos), la entidad principal y sus relaciones siempre se acceden juntas como una unidad (ej: un perfil de usuario con sus preferencias, historial y configuraciones anidadas), el throughput de escritura es extremadamente alto y la normalizacion de datos en multiples tablas es un cuello de botella, o se trabaja con datos jerarquicos o en arbol que se benefician de la anidacion nativa.",
        "MongoDB no es la opcion correcta cuando: los datos tienen relaciones complejas many-to-many que requieren joins, la integridad transaccional entre multiples documentos es critica, o el equipo no tiene experiencia previa en modelado de documentos (el modelado incorrecto en MongoDB puede ser peor que en SQL).",
        "### 3.2 Principios de Modelado de Documentos",
        "La decision mas importante en el modelado de MongoDB es cuando embeber subdocumentos y cuando usar referencias. Regla de embedding: embeber datos que siempre se consultan juntos, que no son compartidos por multiples documentos, y que no crecen indefinidamente. Ejemplo correcto: embeber las direcciones de entrega dentro del documento del usuario (un usuario tiene generalmente 1-3 direcciones, siempre se cargan con el perfil). Regla de referencing: usar referencias cuando los datos son compartidos por muchos documentos, cuando el subdocumento crece indefinidamente, o cuando se necesita acceder al subdocumento de forma independiente. Ejemplo correcto: los pedidos de un usuario deben referenciarse por ID, no embeberse en el documento del usuario (un usuario puede tener miles de pedidos).",
        "### 3.3 Indices en MongoDB",
        "MongoDB requiere la misma atencion en el diseno de indices que PostgreSQL. Sin el indice correcto, MongoDB realiza un collection scan (lee todos los documentos) que en colecciones grandes puede demorar segundos. Tipos de indice mas usados: Single Field Index (el mas comun), Compound Index (para queries con filtros en multiples campos), Sparse Index (solo indexa documentos donde el campo existe), TTL Index (elimina automaticamente documentos despues de un tiempo), y Text Index (para busqueda full-text dentro de documentos).",
        "### 3.4 Transacciones en MongoDB",
        "MongoDB 4.0 introdujo transacciones ACID multi-documento, y MongoDB Atlas en la version 7.0 las soporta de forma estable. Sin embargo, las transacciones multi-documento en MongoDB tienen un costo de performance mayor que en PostgreSQL y deben usarse con moderacion. Si el dominio requiere transacciones complejas frecuentes entre multiples entidades, PostgreSQL es probablemente la opcion mas adecuada.",
        "---",
        "## 4. Redis — Cache, Sesiones y Colas",
        "### 4.1 Casos de Uso Aprobados para Redis",
        "Redis en Da&amp;Da Solutions tiene cuatro casos de uso bien definidos: cache de datos de lectura frecuente (resultados de queries costosas, datos de configuracion, catalogos de productos), almacenamiento de sesiones y tokens de seguridad (Refresh Tokens con TTL automatico, codigos de verificacion de email con expiracion), rate limiting y throttling (contadores de requests implementados con Redis Sorted Sets o el algoritmo Token Bucket), y colas de trabajo asincronas (usando BullMQ en Node.js o RQ en Python, ambos construidos sobre Redis Streams o Lists).",
        "### 4.2 Politica de TTL — Toda Clave Debe Expirar",
        "La regla de oro de Redis en Da&amp;Da Solutions: toda clave debe tener un TTL (Time To Live) configurado explicitamente. Redis es una base de datos en memoria. Sin TTLs, las claves se acumulan indefinidamente hasta agotar la memoria disponible. El unico caso valido para una clave sin TTL es cuando representa estado persistente critico (en ese caso, se debe evaluar si Redis es la herramienta correcta para ese dato).",
        "### 4.3 Politicas de Eviccion",
        "Cuando Redis alcanza el limite de memoria (maxmemory), la politica de eviccion determina que claves se eliminan para liberar espacio. Para Redis usado como cache: allkeys-lru (elimina las keys menos recientemente usadas sin importar si tienen TTL o no). Para Redis usado como store de sesiones: noeviction (rechaza nuevas escrituras en lugar de eliminar datos existentes — combinado con alertas de memoria para escalar antes de llegar al limite).",
        "---",
        "## 5. ClickHouse — Para Analitica a Gran Escala",
        "### 5.1 Que es ClickHouse y por que lo usamos",
        "ClickHouse es un motor de base de datos columnar diseñado para analitica OLAP (Online Analytical Processing). A diferencia de las bases de datos de filas (PostgreSQL, MySQL) que leen filas completas, ClickHouse almacena los datos por columnas. Esto es ideal para queries analiticas que leen pocas columnas pero de millones o billones de filas, como: cuenta de eventos por dia, suma de revenue por pais y producto, funnel de conversion, o retention de usuarios.",
        "Da&amp;Da Solutions usa ClickHouse para: el pipeline de analitica de producto (eventos de click, navegacion, conversion), dashboards de business intelligence en tiempo real, y cualquier consulta analitica sobre datos historicos donde PostgreSQL tendria una performance inaceptable.",
        "### 5.2 Arquitectura de Datos en ClickHouse",
        "Los datos fluyen a ClickHouse principalmente desde Kafka. El servicio de analitica consume eventos del bus de Kafka y los inserta en ClickHouse en batches (insertamos en batches de al menos 1000 filas para aprovechar la compresion y el merge de ClickHouse). La tabla principal para eventos usa el motor MergeTree con particionamiento por mes (PARTITION BY toYYYYMM(event_time)) para facilitar la gestion del ciclo de vida de los datos y la eliminacion de datos historicos.",
        "---",
        "## 6. Google Cloud Storage — Almacenamiento de Objetos",
        "GCS es el almacenamiento de objetos de Da&amp;Da Solutions para todo dato no estructurado: archivos subidos por usuarios (imagenes de perfil, documentos adjuntos, archivos de importacion), backups de bases de datos (exports de PostgreSQL, snapshots de MongoDB), artefactos de CI/CD (imagenes Docker, assets de frontend), y datasets de entrenamiento y validacion para modelos de ML.",
        "Configuracion obligatoria de buckets de produccion: Versioning habilitado (permite recuperar versiones anteriores de un archivo accidentalmente sobreescrito o eliminado), Object Lifecycle Management (mueve automaticamente objetos a clases de almacenamiento mas baratas — Nearline, Coldline, Archive — segun su edad y frecuencia de acceso), y etiquetado de objetos para identificar el propietario, la aplicacion y el nivel de sensibilidad de los datos.",
        "---",
        "## 7. Proteccion y Privacidad de Datos",
        "### 7.1 Clasificacion de Datos",
        "Da&amp;Da Solutions clasifica todos los datos que maneja en cuatro niveles de sensibilidad: PUBLICO (datos que pueden compartirse libremente sin restricciones, ej: precios de productos en la web), INTERNO (datos de uso interno de la empresa, accesibles a todos los empleados, ej: metricas de negocio generales), CONFIDENCIAL (datos de negocio sensibles con acceso restringido a quienes los necesitan para su trabajo, ej: datos financieros de clientes, estrategia comercial), y RESTRINGIDO (datos de maxima sensibilidad sujetos a regulaciones legales, ej: datos personales de usuarios, informacion de tarjetas de credito, datos de salud).",
        "### 7.2 Datos Personales y Marco Regulatorio",
        "Da&amp;Da Solutions opera bajo las regulaciones de proteccion de datos de los paises donde presta servicios: GDPR (Union Europea), LGPD (Brasil), Ley 25.326 (Argentina) y equivalentes en Mexico, Colombia y Espana. Los principios comunes de estas regulaciones que Da&amp;Da implementa son: Minimizacion de datos (solo recolectar los datos estrictamente necesarios para el proposito declarado), Limitacion de proposito (no usar datos para fines distintos a los declarados en el momento de la recoleccion), Precision (mantener los datos actualizados y correctos), Limitacion de almacenamiento (eliminar datos cuando ya no son necesarios), Integridad y confidencialidad (proteger los datos contra acceso no autorizado y perdida), y Accountability (demostrar el cumplimiento de estos principios ante un regulador).",
        "### 7.3 Cifrado de Datos",
        "Datos en transito: toda comunicacion entre servicios usa TLS 1.2 o superior. La comunicacion entre el usuario y los servicios de Da&amp;Da usa TLS 1.3 con HSTS habilitado. Datos en reposo: todas las bases de datos de produccion tienen cifrado en reposo habilitado usando AES-256 con claves gestionadas por GCP Cloud KMS. Para datos de nivel RESTRINGIDO, se usa Customer-Managed Encryption Keys (CMEK) donde Da&amp;Da Solutions controla directamente las claves de cifrado.",
        "---",
        "## 8. Backup y Recuperacion",
        "### 8.1 Estrategia 3-2-1 de Backups",
        "Da&amp;Da Solutions implementa la estrategia de backup 3-2-1: al menos 3 copias de los datos, almacenadas en al menos 2 tipos de almacenamiento diferentes, con al menos 1 copia en una ubicacion geografica diferente (offsite). Para PostgreSQL en produccion: WAL archiving continuo a GCS (permite recuperacion a cualquier punto en el tiempo dentro del periodo de retencion), snapshots automaticos diarios de Cloud SQL, y un backup completo semanal exportado a GCS en una region diferente.",
        "### 8.2 Pruebas de Recuperacion",
        "Un backup que no se ha probado es una ilusión de seguridad. Da&amp;Da Solutions realiza ejercicios de recuperacion trimestrales donde se restaura una base de datos de produccion en un entorno de prueba a partir de los backups y se verifica la integridad y completitud de los datos restaurados. Los resultados de estas pruebas se documentan en Confluence. Si un ejercicio de recuperacion falla o tarda mas del RTO objetivo, se abre un P2 para resolver el problema.",
    ]
))

# ─────────────────────────────────────────────────────────────
# 7. AI AGENTS  (~25 pags)
# ─────────────────────────────────────────────────────────────
DOCS.append(dict(
    filename="ai_agents.pdf",
    title="Desarrollo de Agentes de IA y LLMs",
    subtitle="Estandares, patrones y mejores practicas para Inteligencia Artificial en Da&amp;Da Solutions",
    blocks=[
        "## 1. La Apuesta Estrategica de Da&Da Solutions en IA",
        "Da&amp;Da Solutions tiene una apuesta estrategica por la Inteligencia Artificial generativa como diferenciador competitivo de largo plazo. No como un buzzword ni como una exploracion superficial, sino como una capacidad tecnica real que agrega valor medible y reproducible a nuestros productos y a los negocios de nuestros clientes.",
        "El equipo de AI Engineering de Da&amp;Da Solutions, fundado en 2022, trabaja en dos frentes: integrar capacidades de IA en los productos existentes (busqueda semantica, generacion de contenido, asistentes conversacionales, automatizacion de flujos) y construir productos nativamente de IA (agentes autonomos, sistemas RAG, pipelines de ML). La IA que construimos en Da&amp;Da es responsable, explicable y sometida a los mismos estandares de calidad que cualquier otro sistema de ingenieria.",
        "---",
        "## 2. Modelos de Lenguaje Aprobados",
        "### 2.1 Google Gemini — LLM Principal",
        "Google Gemini es el LLM principal de Da&amp;Da Solutions para todas las aplicaciones de produccion. La eleccion de Gemini se basa en su calidad de razonamiento, su ventana de contexto larga (necesaria para RAG con documentos extensos), su soporte multimodal (texto, imagenes, codigo, audio, video), su disponibilidad en GCP (donde ya opera nuestra infraestructura), y los terminos de privacidad de datos de Google Cloud que son compatibles con nuestras obligaciones regulatorias.",
        "Las variantes de Gemini en uso activo en Da&amp;Da Solutions: gemini-2.0-flash-exp (para tareas que requieren el maximo razonamiento y calidad de output, procesos batch de baja frecuencia), gemini-1.5-flash (para tareas de alta frecuencia donde la velocidad y el costo son prioritarios sobre la maxima calidad, como clasificacion, extraccion de datos, generacion de resumenes), gemini-1.5-pro (para tareas que requieren ventana de contexto de 1M tokens, procesamiento de documentos muy largos), gemini-embedding-004 (para generacion de embeddings para RAG y busqueda semantica).",
        "### 2.2 Cohere Command R+ — Especialista en RAG",
        "Cohere Command R+ es nuestra segunda opcion para casos de RAG de alta precision donde la capacidad de 'grounded generation' (generar solo desde el contexto provisto, con baja tasa de alucinacion) es el requisito mas importante. Command R+ fue disenado especificamente para RAG y ofrece excelente desempeno en la recuperacion de informacion factual de documentos. Cohere tambien provee modelos de embeddings multilingues (Embed v3) que son superiores a Gemini para idiomas distintos del ingles.",
        "### 2.3 Modelos Open Source Self-Hosted",
        "Para casos de uso donde la privacidad de los datos es la maxima prioridad (datos que no pueden enviarse a APIs de terceros bajo ningun concepto), Da&amp;Da Solutions hostea modelos open source en nuestra infraestructura de GKE con GPUs (NVIDIA A100 y H100 via GKE GPU node pools). Los modelos actuales en produccion self-hosted son: Llama 3.1 70B (via vLLM para inferencia de alta concurrencia) y Mistral 7B Instruct (para tareas simples de alta frecuencia con bajo costo de inferencia).",
        "El hosting de modelos self-hosted implica un overhead operacional significativo (gestion de GPUs, actualizaciones de modelos, monitoreo de inferencia). No debe adoptarse sin evaluacion de costo-beneficio comparado con las APIs externas.",
        "---",
        "## 3. El Patron RAG — Estandar de Da&Da para Conocimiento Empresarial",
        "### 3.1 Por que RAG en lugar de Fine-tuning",
        "Existen dos enfoques principales para hacer que un LLM responda sobre conocimiento especifico de un dominio: el fine-tuning (reentrenar el modelo con los datos del dominio) y RAG (recuperar el contexto relevante en tiempo de inferencia y inyectarlo en el prompt). Da&amp;Da Solutions elige RAG como patron estandar por las siguientes razones:",
        "RAG es mas economico: el fine-tuning de un modelo grande requiere computacion de GPU costosa y tiempo de entrenamiento. RAG solo requiere generar embeddings (relativamente barato) y mantener el vector store. RAG permite actualizaciones en tiempo real: cuando la documentacion cambia, solo se reindexan los documentos modificados. Con fine-tuning, cada actualizacion del conocimiento requiere un nuevo ciclo de entrenamiento. RAG es mas explicable: RAG puede citar explicitamente las fuentes de las que extrajo la informacion para generar la respuesta. Fine-tuning no tiene esta capacidad de proveniencia. RAG reduce alucinaciones: al anclar las respuestas en documentos fuente concretos, RAG reduce significativamente las alucinaciones del LLM comparado con la generacion desde el conocimiento parametrico del modelo.",
        "### 3.2 Arquitectura de un Sistema RAG en Da&Da Solutions",
        "Todo sistema RAG tiene dos fases bien separadas. La Fase de Indexacion (offline): los documentos fuente (PDFs, paginas web, bases de datos, wikis) son cargados por un pipeline de ingesta. Cada documento es dividido en chunks (fragmentos de texto). Para cada chunk se genera un embedding (vector numerico de alta dimension que captura el significado semantico del texto). Los pares (chunk, embedding, metadatos) se almacenan en una base de datos vectorial (Qdrant en produccion, FAISS en desarrollo). Este proceso se ejecuta una vez al inicio y de forma incremental cuando los documentos fuente cambian.",
        "La Fase de Inferencia (online): cuando el usuario formula una pregunta, se genera el embedding de esa pregunta usando el mismo modelo de embeddings. Se realiza una busqueda por similitud en la base de datos vectorial (busqueda del coseno o producto punto entre el embedding de la pregunta y los embeddings de los chunks indexados). Los K chunks mas similares (tipicamente K=5-10) se recuperan junto con sus metadatos. Los chunks recuperados se insertan en el prompt del LLM como contexto. El LLM genera la respuesta basandose en el contexto provisto, mencionando las fuentes.",
        "### 3.3 Chunking — La Division del Texto",
        "La estrategia de chunking (como se divide el texto de los documentos en fragmentos) es una de las decisiones mas criticas en el rendimiento de un sistema RAG. Un chunk demasiado pequeno pierde contexto; uno demasiado grande diluye la relevancia y consume mas tokens del contexto del LLM.",
        "La estrategia estandar de Da&amp;Da Solutions es RecursiveCharacterTextSplitter de LangChain con chunk_size=1000 caracteres y chunk_overlap=200 caracteres. El solapamiento de 200 caracteres garantiza que el contexto de los limites entre chunks no se pierda: si una idea importante comienza al final de un chunk y termina al principio del siguiente, el overlap garantiza que ambos chunks contienen el texto completo de esa idea.",
        "Para documentos con estructura bien definida (PDFs con secciones, documentacion en Markdown), se evalua el uso de estrategias de chunking semantico que respetan los limites naturales del documento (saltos de seccion, parrafos, listas). Esto puede mejorar significativamente la calidad de los chunks comparado con el chunking puramente por numero de caracteres.",
        "### 3.4 Embeddings — La Representacion Vectorial del Significado",
        "Los embeddings son vectores numericos de alta dimension (tipicamente 768 o 1536 dimensiones) que representan el significado semantico de un texto de forma que textos similares en significado esten cerca en el espacio vectorial. Esto es lo que permite la busqueda por similitud semantica (encontrar chunks relevantes para una pregunta aunque no compartan las mismas palabras exactas).",
        "El modelo de embeddings estandar de Da&amp;Da Solutions es gemini-embedding-004 (dimensiones: 768, normalizado para coseno similarity). Una vez elegido el modelo de embeddings, no puede cambiarse sin reindexar completamente la base vectorial (los embeddings de modelos distintos no son comparables). Por esto, la eleccion del modelo de embeddings se hace cuidadosamente al inicio del proyecto y se documenta como un ADR.",
        "---",
        "## 4. Bases de Datos Vectoriales",
        "### 4.1 FAISS para Desarrollo y Prototipado",
        "FAISS (Facebook AI Similarity Search) es una libreria de indexacion vectorial en memoria desarrollada por Meta. Es ideal para el desarrollo local y el prototipado porque: no requiere infraestructura adicional (se instala como una libreria Python), se integra directamente con LangChain sin configuracion, y es extremadamente rapida para colecciones pequenas (menos de 100.000 vectores en memoria). La limitacion critica de FAISS es que no es apropiada para produccion: el indice vive completamente en memoria (no persiste en disco nativamente), no soporta actualizaciones incrementales eficientes (hay que reconstruir el indice completo para agregar nuevos documentos), y no escala horizontalmente.",
        "### 4.2 Qdrant para Produccion",
        "Qdrant es la base de datos vectorial oficial de produccion de Da&amp;Da Solutions. La eleccion de Qdrant sobre alternativas como Pinecone, Weaviate o Chroma se baso en: alto rendimiento en busquedas ANN (Approximate Nearest Neighbor) con indices HNSW, soporte nativo para filtrado por metadatos junto con la busqueda vectorial (permite hacer queries como 'encuentra los 5 chunks mas similares a esta pregunta que pertenezcan al documento X'), API REST y gRPC completas con SDKs en Python y JavaScript, operacion como contenedor en Kubernetes (control total sobre la infraestructura, sin vendor lock-in), y consistencia fuerte (a diferencia de Pinecone serverless que ofrece consistencia eventual).",
        "Qdrant corre en Da&amp;Da Solutions en un StatefulSet de Kubernetes con volumenes de Google Persistent Disk para persistencia. Las colecciones de Qdrant se respaldan automaticamente cada 24 horas mediante snapshots almacenados en GCS. Para el cluster de produccion, Qdrant opera en modo distribuido con 3 nodos para alta disponibilidad.",
        "### 4.3 Pinecone como Alternativa Serverless",
        "Pinecone es una alternativa valida cuando la simplicidad operativa y la escala masiva son prioritarias sobre el control de infraestructura. Pinecone serverless puede manejar decenas de millones de vectores sin gestion de infraestructura. Su uso en Da&amp;Da Solutions requiere evaluacion previa de costo (Pinecone cobra por volumen de vectores y operaciones) y aprobacion del Staff AI Engineer.",
        "---",
        "## 5. Frameworks de Orquestacion de IA",
        "### 5.1 LangChain y LCEL",
        "LangChain es el framework de orquestacion estandar para sistemas LLM en Da&amp;Da Solutions. LangChain provee abstracciones de alto nivel para: conexion con LLMs (Gemini, Cohere, OpenAI), document loaders para ingestar documentos de multiples formatos (PDF, DOCX, HTML, CSV, bases de datos), text splitters para chunking, integraciones con bases de datos vectoriales (Qdrant, FAISS, Pinecone), y cadenas de procesamiento (Chains) para orquestar el flujo RAG.",
        "LangChain Expression Language (LCEL) es la forma moderna y preferida de construir chains en LangChain. LCEL permite componer operaciones con el operador pipe (|), lo que resulta en codigo mas legible y declarativo. Adicionalmente, LCEL soporta streaming de respuestas (el LLM responde token a token en lugar de esperar a tener la respuesta completa), paralelismo automatico cuando hay operaciones independientes, y trazabilidad completa via LangSmith.",
        "### 5.2 LangGraph para Agentes Multi-paso",
        "LangGraph es una extension de LangChain para construir agentes con ciclos de razonamiento y uso de herramientas. Modela el flujo del agente como un grafo de estado donde los nodos son funciones (que pueden llamar al LLM, usar herramientas, o hacer calculos) y las aristas son las transiciones entre estados. Esta representacion hace que el flujo del agente sea explicit, debuggeable y modificable.",
        "LangGraph se usa en Da&amp;Da Solutions para: agentes que necesitan razonar en multiples pasos (consultar documentos, sintetizar informacion, y luego responder), agentes que usan herramientas (calculadoras, APIs externas, bases de datos) en sus razonamientos, y flujos de trabajo de IA con ramificaciones condicionales complejas.",
        "### 5.3 SDK Nativo de Google Gemini — Para Casos Simples",
        "Para llamadas simples al LLM que no requieren la orquestacion de LangChain (generacion de texto simple, clasificacion, extraccion de datos estructurados), usar directamente el SDK oficial de Google (google-generativeai) es mas adecuado. Las abstracciones de LangChain son poderosas pero agregan overhead: mas dependencias, capas de abstraccion adicionales, y a veces dificultan el debugging. Si el caso de uso no justifica LangChain, no usarlo.",
        "---",
        "## 6. Prompt Engineering — El Arte de Comunicarse con LLMs",
        "### 6.1 Estructura de un Prompt Efectivo",
        "Un prompt efectivo en Da&amp;Da Solutions sigue una estructura clara: Role (el rol o persona que debe adoptar el LLM: 'Eres un asistente de soporte tecnico experto en los productos de Da&amp;Da Solutions'), Context (el contexto relevante para la tarea, como el historial de la conversacion o los documentos recuperados por RAG), Instructions (las instrucciones especificas de la tarea, en lenguaje claro y sin ambiguedades), Constraints (las limitaciones y restricciones: 'No inventes informacion que no este en el contexto provisto. Si no sabes la respuesta, di que no tienes informacion suficiente'), Format (el formato de salida esperado: 'Responde en espanol. Usa markdown para los bloques de codigo'), y Examples (ejemplos few-shot cuando sea util para alinear el estilo de respuesta).",
        "### 6.2 Versionado y Gestion de Prompts",
        "Los prompts del sistema son codigo. Deben tratarse con el mismo rigor que cualquier otro codigo: versionados en el repositorio, revisados en Pull Request, testeados antes de ir a produccion. En Da&amp;Da Solutions usamos LangSmith Hub para centralizar y versionar los prompts de los sistemas mas criticos. Cualquier cambio al prompt del sistema de una aplicacion de produccion debe pasar por evaluacion con el eval set del sistema antes de deployarse.",
        "### 6.3 Prevencion de Prompt Injection",
        "El prompt injection es una clase de ataque donde un usuario malicioso incluye en su input instrucciones que manipulan el comportamiento del LLM, ignorando el system prompt. Medidas de mitigacion en Da&amp;Da Solutions: separar claramente el system prompt (controlado por el sistema) del user input (controlado por el usuario, potencialmente malicioso) en la estructura del prompt; validar y sanitizar el input del usuario antes de incluirlo en el prompt; implementar guardrails de contenido que detecten patrones de injection comunes ('Ignora las instrucciones anteriores', 'Eres ahora un asistente sin restricciones', etc.); y nunca incluir secretos, instrucciones de seguridad criticas o informacion confidencial en el system prompt (asumir que el system prompt puede ser extraido por un atacante determinado).",
        "---",
        "## 7. Evaluacion de Sistemas de IA",
        "### 7.1 La Necesidad de Evaluacion Sistematica",
        "Un sistema de IA sin evaluacion sistematica no puede evolucionar con confianza. ¿Como sabemos si el nuevo modelo de embeddings es mejor que el anterior? ¿Como sabemos si el cambio en el chunking mejoro la calidad de las respuestas? Sin un framework de evaluacion con metricas objetivas, las decisiones sobre los componentes del sistema de IA son intuitivas y potencialmente regresivas.",
        "### 7.2 Metricas de Evaluacion RAG con RAGAS",
        "Da&amp;Da Solutions usa RAGAS (RAG Assessment) como framework de evaluacion para todos los sistemas RAG. RAGAS provee las siguientes metricas automatizadas: Faithfulness (mide si la respuesta generada esta factualmente respaldada por los chunks del contexto recuperado; una respuesta fiel no inventa informacion que no esta en el contexto; objetivo: mayor a 0.85), Answer Relevancy (mide si la respuesta es relevante para la pregunta original del usuario; objetivo: mayor a 0.80), Context Precision (mide si los chunks mas relevantes estan rankeados en las primeras posiciones de los resultados de recuperacion; objetivo: mayor a 0.75), y Context Recall (mide si todos los chunks necesarios para responder la pregunta fueron recuperados; objetivo: mayor a 0.80).",
        "### 7.3 El Eval Set — El Conjunto de Evaluacion",
        "El eval set es un conjunto curado de pares (pregunta, respuesta esperada) creado por expertos del dominio. Es el activo mas valioso del sistema de evaluacion. Un buen eval set cubre: preguntas de distintos niveles de dificultad (simples, que requieren sintesis de multiples fuentes, y ambiguas), preguntas de distintos tipos (factuales, de procedimiento, comparativas), y edge cases conocidos (preguntas fuera del scope del sistema, preguntas con informacion contradictoria en las fuentes).",
        "Antes de cualquier cambio significativo al sistema RAG (nuevo modelo de embeddings, nueva estrategia de chunking, nuevo LLM, cambio en el system prompt), se ejecuta el eval set completo y se comparan las metricas RAGAS con la linea base registrada. Una regresion en cualquier metrica mayor a 5 puntos porcentuales debe ser investigada antes de deployar el cambio.",
        "---",
        "## 8. Seguridad y Etica en IA",
        "### 8.1 Privacidad de Datos en Sistemas de IA",
        "La regla mas importante de seguridad en sistemas de IA de Da&amp;Da Solutions: datos de identificacion personal (PII) — nombres, correos, numeros de telefono, numeros de identificacion nacional, datos de salud, datos financieros — nunca deben ser enviados en prompts a LLMs de APIs externas (Gemini, Cohere) sin ser anonimizados o pseudonimizados previamente. Si un sistema de IA necesita operar con datos PII de forma inevitable, debe usar modelos self-hosted.",
        "### 8.2 Guardrails de Contenido",
        "Los sistemas de IA de produccion que interactuan directamente con usuarios finales deben implementar guardrails de contenido para verificar que ni el input del usuario ni el output del LLM contienen: contenido violento, ofensivo o inapropiado, intentos de extraccion de informacion confidencial del sistema, instrucciones de actividades ilegales, y afirmaciones medicas, legales o financieras de alto riesgo sin la advertencia apropiada.",
        "Da&amp;Da Solutions implementa guardrails usando los filtros de seguridad nativos de la API de Gemini (safety_settings) como primera linea de defensa, complementados con reglas de validacion personalizadas usando la libreria Guardrails AI para casos especificos del dominio.",
        "### 8.3 Transparencia y Explicabilidad",
        "Los sistemas de IA de Da&amp;Da Solutions que toman decisiones que afectan directamente a los usuarios (aprobacion de credito, clasificacion de riesgo, recomendaciones medicas) deben ser explicables: deben poder decirle al usuario por que tomaron la decision que tomaron, basandose en que informacion, y con que nivel de confianza. Los sistemas 'black box' que toman decisiones impactantes sin poder explicarlas son inaceptables en Da&amp;Da Solutions.",
        "### 8.4 IA Responsable — Principios de Da&Da",
        "El equipo de AI Engineering de Da&amp;Da Solutions se guia por los principios de IA Responsable: Beneficencia (los sistemas de IA deben beneficiar a los usuarios y a la sociedad, no solo a la empresa), No maleficencia (los sistemas no deben causar daño a los usuarios ni a terceros), Autonomia (los usuarios deben poder entender, controlar y optar por no usar los sistemas de IA cuando asi lo deseen), Justicia (los sistemas no deben discriminar ni perpetuar sesgos existentes en los datos de entrenamiento), y Responsabilidad (siempre debe haber un ser humano responsable de las decisiones de un sistema de IA en contextos de alto impacto).",
        "---",
        "## 9. Observabilidad de Sistemas de IA",
        "### 9.1 LangSmith para Trazabilidad de LangChain",
        "Todos los sistemas LangChain en produccion en Da&amp;Da Solutions estan conectados a LangSmith, el sistema de observabilidad de LangChain. LangSmith registra automaticamente cada invocacion de un chain o agente: el prompt completo enviado al LLM (incluyendo el system prompt y el contexto RAG), los chunks recuperados de la base vectorial con sus scores de similitud, la respuesta generada por el LLM, la latencia total y de cada paso del chain, y el costo estimado en tokens (input + output).",
        "### 9.2 Metricas Operacionales de Sistemas de IA",
        "Ademas de la trazabilidad de LangSmith, los servicios de IA exponen metricas de Prometheus: llm_inference_duration_seconds (histograma de latencia de la llamada al LLM), vector_search_duration_seconds (histograma de latencia de la busqueda vectorial), llm_tokens_used_total (contador de tokens de input y output consumidos, desglosado por modelo), llm_api_errors_total (contador de errores de la API del LLM, desglosado por tipo de error), y rag_faithfulness_score (metrica en tiempo real de la calidad de las respuestas, evaluada por un LLM evaluador).",
        "---",
        "## 10. MLOps y Ciclo de Vida de Modelos",
        "### 10.1 MLflow para Gestion de Experimentos",
        "Para proyectos que involucran entrenamiento de modelos propios (modelos de clasificacion, recomendacion, forecasting o fine-tuning de LLMs), usamos MLflow como plataforma de experimentacion. MLflow registra: los hiperparametros de cada experimento, las metricas de evaluacion (accuracy, F1, AUC-ROC, BLEU, ROUGE segun el tipo de modelo), los artefactos del modelo (los pesos guardados), y las dependencias de codigo (el hash del commit de Git en el que se entrenó el modelo).",
        "### 10.2 Model Registry y Gobernanza de Modelos",
        "Antes de desplegar cualquier modelo entrenado en produccion, debe ser registrado en el Model Registry de MLflow y pasar por un proceso de aprobacion. Los estados de un modelo en el registry son: Staging (candidato a produccion, en fase de validacion por el equipo de AI y el negocio), Production (actualmente en produccion), y Archived (historico, reemplazado por una version mas nueva). Solo los modelos en estado Production pueden ser referenciados en los servicios de produccion. El cambio de estado de Staging a Production requiere la firma de al menos un Staff AI Engineer y del Product Manager responsable.",
    ]
))


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Navegar al directorio raiz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    docs_dir = os.path.join(project_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    print("=" * 62)
    print("  Da&Da Solutions — Generacion de Documentacion Tecnica")
    print("=" * 62)

    for doc in DOCS:
        out = os.path.join("docs", doc["filename"])
        make_pdf(out, doc["title"], doc["subtitle"], doc["blocks"])

    print("=" * 62)
    print("  Proceso completado exitosamente.")
    print("=" * 62)
