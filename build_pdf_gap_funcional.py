#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pdf_gap_funcional.py
Documento operativo independiente (Trabajo de Campo):
'PROCEDIMIENTO DE ANÁLISIS DE GAP FUNCIONAL DETERMINISTA CON COPILOT'
"""

import os
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILE = os.path.join(BASE_DIR, "PROCEDIMIENTO_GAP_FUNCIONAL_DETERMINISTA_COPILOT.pdf")
HTML_FILE = os.path.join(BASE_DIR, "PROCEDIMIENTO_GAP_FUNCIONAL_DETERMINISTA_COPILOT.html")
DOCX_FILE = os.path.join(BASE_DIR, "PROCEDIMIENTO_GAP_FUNCIONAL_DETERMINISTA_COPILOT.docx")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 32, A4[0] - 36, 32)
        self.drawString(36, 22, "Trabajo de Campo · Procedimiento de Gap Funcional Determinista (Copilot & Excel)")
        self.drawRightString(A4[0] - 36, 22, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()


def generar_html():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Procedimiento de Gap Funcional Determinista con Copilot</title>
  <style>
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:#f8fafc; color:#0f172a; margin:0; padding:32px 16px; line-height:1.6; }
    .container { max-width:960px; margin:0 auto; background:#fff; padding:40px 48px; border-radius:12px; box-shadow:0 4px 16px rgba(15,23,42,0.06); }
    .badge { display:inline-block; background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; font-size:11px; font-weight:700; padding:4px 10px; border-radius:999px; text-transform:uppercase; margin-bottom:10px; }
    h1 { font-size:24px; color:#0f172a; margin:0 0 8px 0; }
    .subtitle { font-size:14px; color:#475569; border-bottom:2px solid #1e40af; padding-bottom:14px; margin-bottom:20px; }
    h2 { font-size:17px; color:#1e3a8a; margin:24px 0 10px 0; border-left:4px solid #2563eb; padding-left:10px; }
    .box-warn { background:#fef2f2; border-left:4px solid #dc2626; padding:12px 16px; border-radius:6px; margin:14px 0; font-size:13.5px; }
    .box-ok { background:#f0fdf4; border-left:4px solid #16a34a; padding:12px 16px; border-radius:6px; margin:14px 0; font-size:13.5px; }
    .box-info { background:#f0f9ff; border-left:4px solid #0284c7; padding:12px 16px; border-radius:6px; margin:14px 0; font-size:13.5px; }
    table { width:100%; border-collapse:collapse; margin:14px 0; font-size:12.5px; }
    th, td { border:1px solid #cbd5e1; padding:8px 10px; text-align:left; vertical-align:top; }
    th { background:#f1f5f9; color:#0f172a; font-weight:700; }
    code { background:#f1f5f9; padding:2px 5px; border-radius:4px; font-size:12px; color:#0f172a; }
    ul, ol { padding-left:20px; }
    li { margin-bottom:6px; font-size:13.5px; }
  </style>
</head>
<body>
<div class="container">
  <span class="badge">Trabajo de Campo · Ingeniería de Requisitos (Copilot &amp; Excel)</span>
  <h1>Procedimiento de Análisis de Gap Funcional Determinista</h1>
  <div class="subtitle">Cómo comparar nuevos requisitos de clientes frente a los análisis funcionales del producto, controlar el porcentaje cubierto en Excel y garantizar resultados repetibles sin deriva probabilística.</div>

  <table>
    <thead><tr><th>Versión</th><th>Fecha</th><th>Estado</th><th>Alcance</th></tr></thead>
    <tbody><tr><td><b>v1.0</b></td><td>27/11/2026</td><td>Borrador de Campo Inicial</td><td>Definición de matriz Excel/CSV (9 columnas), las 5 reglas de determinismo, modelo de porcentajes y combinación Agente + Skill en Copilot.</td></tr></tbody>
  </table>

  <h2>1. El Problema: Por qué la IA cambia porcentajes y detecta diferencias distintas en cada ejecución</h2>
  <div class="box-warn">
    <strong>⚠️ El fallo clásico (Deriva Numérica e Interpretativa):</strong> Si pides a Copilot <em>«compara estos requisitos nuevos con mis análisis funcionales y dime qué porcentaje cubren»</em>, cada vez que lances la consulta no solo dará un porcentaje distinto (hoy 62%, mañana 71%), sino que <strong>puede interpretar y detectar diferencias distintas cada vez</strong> (hoy dar por <code>CUBIERTO</code> un requisito por una frase genérica y mañana marcarlo como <code>PARCIAL</code> al fijarse en otro matiz). Esto ocurre porque el motor es <strong>probabilístico</strong> y en Copilot Chat (VS Code) no se puede fijar <code>temperature=0</code>. Por ello, <strong>la fiabilidad y el determinismo deben imponerse mediante evidencia literal, descomposición atómica y fórmula matemática, nunca confiando en la interpretación libre de la IA</strong>.
  </div>

  <h2>2. Estructura de la Tabla Tipo Excel / CSV (<code>plantilla_matriz_gap_funcional.csv</code>)</h2>
  <table>
    <thead><tr><th>Columna</th><th>Contenido y Regla Estricta</th><th>Objetivo de Control</th></tr></thead>
    <tbody>
      <tr><td><strong>1. ID_Req</strong></td><td><code>REQ-001</code>, <code>REQ-002</code>...</td><td>Identificador único e inmutable por requisito atómico.</td></tr>
      <tr><td><strong>2. Requisito_Cliente</strong></td><td>Texto breve literal del cliente (1 sola acción).</td><td>Evita mezclar varias funcionalidades en una misma fila.</td></tr>
      <tr><td><strong>3. Modulo</strong></td><td>Área funcional (ej. <em>Facturación</em>, <em>Permisos</em>).</td><td>Permite filtrar y repartir el encargo entre analistas funcionales.</td></tr>
      <tr><td><strong>4. Doc_Producto_Ref</strong></td><td>Archivo y apartado exacto (o <code>NINGUNO</code>).</td><td>Trazabilidad directa al análisis funcional vigente.</td></tr>
      <tr><td><strong>5. Evidencia_Literal</strong></td><td>Cita textual exacta encontrada (o <code>NO EXISTE</code>).</td><td><strong>Candado anti-alucinación:</strong> sin cita literal no está cubierto.</td></tr>
      <tr><td><strong>6. Estado_Cobertura</strong></td><td>Lista cerrada de 4 valores: <code>CUBIERTO</code> | <code>PARCIAL</code> | <code>GAP_NUEVO</code> | <code>AMBIGUO</code></td><td>Elimina descripciones ambiguas o porcentajes inventados.</td></tr>
      <tr><td><strong>7. %_Cobertura</strong></td><td><strong>Fórmula Excel:</strong> <code>=SI(F2="CUBIERTO";100%;SI(F2="PARCIAL";50%;0%))</code></td><td><strong>100% determinista:</strong> el porcentaje lo calcula Excel, no la IA.</td></tr>
      <tr><td><strong>8. Gap_Para_Analistas</strong></td><td>Qué parte exacta falta implementar (vacío si <code>CUBIERTO</code>).</td><td>Encargo directo y accionable para los analistas funcionales.</td></tr>
      <tr><td><strong>9. Validado_Humano</strong></td><td><code>PENDIENTE</code> | <code>APROBADO</code></td><td>Congela las filas revisadas para no reevaluarlas en el futuro.</td></tr>
    </tbody>
  </table>

  <h2>3. Las 5 Reglas de Oro para Asegurar el Determinismo</h2>
  <ol>
    <li><strong>Descomposición Atómica Previa:</strong> Antes de comparar nada, trocea el pliego del cliente en requisitos de 1 sola acción verificable (<code>1 fila = 1 requisito</code>) y congela esa lista en GitLab. Si un párrafo pide «exportar a PDF y enviar por email», se divide en dos filas independientes.</li>
    <li><strong>Prohibido que la IA calcule porcentajes:</strong> Copilot solo elige una de las 4 etiquetas cerradas (<code>CUBIERTO</code>, <code>PARCIAL</code>, <code>GAP_NUEVO</code>, <code>AMBIGUO</code>). Excel calcula el porcentaje por fila y el promedio total del proyecto (<code>=PROMEDIO(...)</code>).</li>
    <li><strong>Regla <em>Quote-First</em> (Sin evidencia literal = <code>GAP_NUEVO</code>):</strong> Prohibido marcar <code>CUBIERTO</code> o <code>PARCIAL</code> si Copilot no copia en <code>Evidencia_Literal</code> la frase exacta del análisis funcional vigente.</li>
    <li><strong>Ejecución Incremental sobre GitLab:</strong> Las filas marcadas como <code>APROBADO</code> por el consultor quedan bloqueadas. Al llegar cambios futuros, Copilot solo analiza filas nuevas o en estado <code>PENDIENTE</code>.</li>
    <li><strong>Doble Pase <em>Elephant-Goldfish</em>:</strong> Una segunda pasada en un chat limpio revisa únicamente si las citas de <code>Evidencia_Literal</code> coinciden de verdad con el análisis funcional.</li>
  </ol>

  <h2>4. Cómo se miden los requisitos a medias (<code>PARCIAL</code>): 50% fijo vs. Subcriterios</h2>
  <div class="box-info">
    <strong>📊 Dos niveles de precisión según lo que necesite el consultor:</strong><br/>
    • <strong>Estándar Base (Simple — <code>0% / 50% / 100%</code>):</strong> Todo requisito <code>CUBIERTO</code> suma 100%, todo <code>GAP_NUEVO</code> suma 0% y todo requisito que existe solo a medias (<code>PARCIAL</code>) suma fijo un <strong>50%</strong> mediante fórmula de Excel.<br/>
    • <strong>Modo Alta Precisión (Descomposición en Sub-piezas):</strong> Si un requisito grande está a medias (ej. <em>pantalla hecha, cálculo hecho, pero falta el informe</em>), se divide en 3 filas atómicas (<code>REQ-010a</code>, <code>REQ-010b</code>, <code>REQ-010c</code>). Así dos filas suman 100% y una 0%, dando exactamente <strong>66,7%</strong> matemático sin subjetividad.
  </div>

  <h2>5. ¿Skill o Agente dedicado en Copilot? (Cómo implementarlo)</h2>
  <div class="box-ok">
    <strong>🧩 No son excluyentes, trabajan juntos:</strong><br/>
    • El <strong>Agente</strong> (Modo Agente en Copilot VS Code, o un <em>Custom Agent</em> en <code>.github/agents/</code>) es el <strong>trabajador autónomo</strong> capaz de leer tu carpeta de análisis funcionales y rellenar el archivo CSV.<br/>
    • El <strong>Skill</strong> (archivo <code>.github/prompts/analizar-gap-requisitos.prompt.md</code> con <code>mode: agent</code>) es la <strong>receta obligatoria</strong> con las 9 columnas y las 5 reglas de determinismo que ese Agente debe seguir paso a paso.<br/>
    Al lanzarlo, el Agente ejecuta siempre exactamente el mismo procedimiento determinista sobre tus documentos sin improvisar.
  </div>
</div>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado:", HTML_FILE)


def generar_pdf():
    doc = SimpleDocTemplate(
        PDF_FILE, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=38, bottomMargin=42
    )
    styles = getSampleStyleSheet()
    PAGE_WIDTH = A4[0] - 72

    c_navy = colors.HexColor("#0F172A")
    c_blue = colors.HexColor("#1E40AF")

    title_style = ParagraphStyle("T", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=c_navy, spaceAfter=3)
    sub_style = ParagraphStyle("S", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#475569"), spaceAfter=5)
    h1_style = ParagraphStyle("H1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12.5, textColor=c_blue, spaceBefore=6, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle("B", parent=styles["Normal"], fontName="Helvetica", fontSize=7.8, leading=10.8, textColor=colors.HexColor("#1E293B"), spaceAfter=3)
    bullet_style = ParagraphStyle("BL", parent=styles["Normal"], fontName="Helvetica", fontSize=7.6, leading=10.5, textColor=colors.HexColor("#1E293B"), leftIndent=10, spaceAfter=2)
    th_style = ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.2, leading=9.5, textColor=c_navy)
    td_style = ParagraphStyle("TD", parent=styles["Normal"], fontName="Helvetica", fontSize=7.0, leading=9.2, textColor=colors.HexColor("#334155"))
    td_bold = ParagraphStyle("TDB", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.0, leading=9.2, textColor=c_navy)

    story = []
    story.append(Paragraph("Procedimiento de Análisis de Gap Funcional Determinista (Copilot & Excel)", title_style))
    story.append(Paragraph("<b>Trabajo de Campo · Ingeniería de Requisitos:</b> Comparación controlada de nuevos requisitos de cliente frente al análisis funcional vigente del producto, cálculo exacto de cobertura y control anti-variabilidad.", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_blue, spaceBefore=0, spaceAfter=5))

    # Version box
    t_ver = Table([
        [Paragraph("Versión", th_style), Paragraph("Fecha", th_style), Paragraph("Estado", th_style), Paragraph("Alcance del Documento de Campo", th_style)],
        [Paragraph("<b>v1.0</b>", td_bold), Paragraph("27/11/2026", td_style), Paragraph("Inicial (Campo)", td_style), Paragraph("Matriz Excel/CSV (9 columnas), 5 reglas de determinismo, porcentajes (0%/50%/100% vs. sub-piezas) y arquitectura Skill + Agente.", td_style)]
    ], colWidths=[45, 58, 72, 348.27])
    t_ver.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#94A3B8")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0,0), (-1,-1), 2.5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2.5),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(t_ver)
    story.append(Spacer(1, 5))

    # 1. El Problema
    story.append(Paragraph("1. El Problema: Por qué la IA cambia porcentajes y detecta diferencias distintas", h1_style))
    p_warn = Table([[Paragraph("<b>⚠️ Causa raíz (Deriva Numérica e Interpretativa):</b> Si se pide a Copilot <i>«compara estos requisitos nuevos con mis documentos»</i>, en cada ejecución no solo baila el porcentaje (62% vs. 71%), sino que <b>puede ver diferencias distintas cada vez</b> (hoy marcar <code>CUBIERTO</code> por una frase genérica y mañana <code>PARCIAL</code> por un matiz), al ser un motor probabilístico sin <code>temperature=0</code> en VS Code. <b>Justificación de fiabilidad:</b> la <i>Evidencia Literal</i> + <i>Descomposición Atómica</i> + <i>Congelación</i> + <i>Fórmula Excel</i> eliminan esa subjetividad interpretativa.", body_style)]], colWidths=[PAGE_WIDTH])
    p_warn.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#DC2626")),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(p_warn)

    # 2. Tabla Excel
    story.append(Paragraph("2. Estructura de la Matriz Excel / CSV (plantilla_matriz_gap_funcional.csv)", h1_style))
    cols_data = [
        [Paragraph("Columna", th_style), Paragraph("Contenido y Regla Estricta", th_style), Paragraph("Objetivo de Control", th_style)],
        [Paragraph("<b>1. ID_Req</b>", td_bold), Paragraph("<code>REQ-001</code>, <code>REQ-002</code>...", td_style), Paragraph("Identificador único e inmutable por requisito atómico.", td_style)],
        [Paragraph("<b>2. Requisito_Cliente</b>", td_bold), Paragraph("Texto breve literal del cliente (1 sola acción).", td_style), Paragraph("Evita mezclar varias funcionalidades en una misma fila.", td_style)],
        [Paragraph("<b>3. Modulo</b>", td_bold), Paragraph("Área funcional (ej. Facturación, Permisos).", td_style), Paragraph("Permite filtrar y repartir trabajo entre analistas.", td_style)],
        [Paragraph("<b>4. Doc_Producto_Ref</b>", td_bold), Paragraph("Archivo y apartado exacto (o <code>NINGUNO</code>).", td_style), Paragraph("Trazabilidad directa al análisis funcional vigente.", td_style)],
        [Paragraph("<b>5. Evidencia_Literal</b>", td_bold), Paragraph("Cita textual exacta encontrada (o <code>NO EXISTE</code>).", td_style), Paragraph("<b>Candado anti-alucinación:</b> sin cita literal no está cubierto.", td_style)],
        [Paragraph("<b>6. Estado_Cobertura</b>", td_bold), Paragraph("Lista cerrada: <code>CUBIERTO</code> | <code>PARCIAL</code> | <code>GAP_NUEVO</code> | <code>AMBIGUO</code>", td_style), Paragraph("Elimina descripciones ambiguas o porcentajes inventados.", td_style)],
        [Paragraph("<b>7. %_Cobertura</b>", td_bold), Paragraph("<b>Fórmula Excel:</b> <code>=SI(F2=\"CUBIERTO\";100%;SI(F2=\"PARCIAL\";50%;0%))</code>", td_style), Paragraph("<b>100% determinista:</b> lo calcula Excel, nunca la IA.", td_style)],
        [Paragraph("<b>8. Gap_Para_Analistas</b>", td_bold), Paragraph("Qué parte exacta falta implementar (vacío si <code>CUBIERTO</code>).", td_style), Paragraph("Encargo directo y accionable para analistas funcionales.", td_style)],
        [Paragraph("<b>9. Validado_Humano</b>", td_bold), Paragraph("<code>PENDIENTE</code> | <code>APROBADO</code>", td_style), Paragraph("Congela filas revisadas para no reevaluarlas en el futuro.", td_style)],
    ]
    t_cols = Table(cols_data, colWidths=[100, 215, 208.27])
    t_cols.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#94A3B8")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0,0), (-1,-1), 2.5), ("BOTTOMPADDING", (0,0), (-1,-1), 2.5),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(t_cols)

    # 3. Las 5 Reglas de Determinismo
    story.append(Paragraph("3. Las 5 Reglas de Oro para Asegurar el Determinismo", h1_style))
    story.append(Paragraph("• <b>1. Descomposición Atómica Previa:</b> Trocear primero el documento del cliente en requisitos de 1 sola acción verificable (<code>1 fila = 1 requisito</code>) y congelar esa lista base en GitLab.", bullet_style))
    story.append(Paragraph("• <b>2. Prohibido que la IA estime porcentajes:</b> Copilot solo clasifica en una de las 4 etiquetas cerradas. Excel calcula cada fila y el porcentaje total del proyecto (<code>=PROMEDIO(...)</code>).", bullet_style))
    story.append(Paragraph("• <b>3. Regla Quote-First (Sin cita literal = GAP_NUEVO):</b> Prohibido marcar <code>CUBIERTO</code> o <code>PARCIAL</code> si no copia la frase exacta del análisis funcional vigente.", bullet_style))
    story.append(Paragraph("• <b>4. Ejecución Incremental sobre GitLab:</b> Las filas <code>APROBADO</code> quedan congeladas; en futuras rondas Copilot solo evalúa filas nuevas o en estado <code>PENDIENTE</code>.", bullet_style))
    story.append(Paragraph("• <b>5. Doble Pase Elephant-Goldfish:</b> Una segunda revisión en chat limpio audita exclusivamente que las citas en <code>Evidencia_Literal</code> existan de verdad.", bullet_style))

    # 4. Porcentajes
    story.append(Paragraph("4. Cómo se miden los requisitos a medias (PARCIAL): 50% fijo vs. Sub-piezas", h1_style))
    story.append(Paragraph("• <b>Estándar Base (Simple — 0% / 50% / 100%):</b> <code>CUBIERTO</code> suma 100%, <code>GAP_NUEVO</code> suma 0% y cualquier requisito a medias (<code>PARCIAL</code>) suma fijo un <b>50%</b> por fórmula de Excel.<br/>• <b>Modo Alta Precisión (Descomposición en Sub-piezas):</b> Si un requisito complejo está a medias (ej. pantalla y cálculo hechos, pero falta el informe), se parte en 3 filas atómicas (<code>REQ-010a/b/c</code>): dos dan 100% y una 0%, obteniendo un <b>66,7%</b> matemático exacto sin subjetividad.", body_style))

    # 5. Skill vs Agente
    story.append(Paragraph("5. ¿Skill o Agente dedicado en Copilot? (Trabajan juntos)", h1_style))
    p_ok = Table([[Paragraph("<b>🧩 Arquitectura Combinada (Agente + Receta):</b> El <b>Agente</b> (Modo Agente en Copilot VS Code o <i>Custom Agent</i> en <code>.github/agents/</code>) es el trabajador autónomo que lee tus documentos funcionales y rellena el CSV. El <b>Skill</b> (<code>.github/prompts/analizar-gap-requisitos.prompt.md</code> con <code>mode: agent</code>) es la receta estricta con las 9 columnas y 5 reglas que ese Agente obedece paso a paso para no improvisar.", body_style)]], colWidths=[PAGE_WIDTH])
    p_ok.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#16A34A")),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([p_ok]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("✅ PDF generado:", PDF_FILE)


def compilar_docx():
    try:
        subprocess.run(["textutil", "-convert", "docx", HTML_FILE, "-output", DOCX_FILE], check=True)
        print("✅ DOCX generado:", DOCX_FILE)
    except Exception as e:
        print("⚠️ No se pudo generar DOCX:", e)


if __name__ == "__main__":
    generar_html()
    generar_pdf()
    compilar_docx()
