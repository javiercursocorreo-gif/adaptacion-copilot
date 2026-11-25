import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas

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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        # Header
        self.drawString(36, 810, "GUÍA DE ARQUITECTURA Y GOBERNANZA · COPILOT & GITLAB")
        self.drawRightString(559, 810, "ENLACES OFICIALES Y DESCARGAS")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 804, 559, 804)
        # Footer
        self.line(36, 36, 559, 36)
        self.drawString(36, 24, "Entorno de Consultoría Estratégica · Servidor Web GitHub Pages")
        self.drawRightString(559, 24, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def build_pdf():
    pdf_path = "/Users/externo/Library/Mobile Documents/com~apple~CloudDocs/PERSONAL/CLASES DE TECNOLOGÍA/00. ADAPTACION_EMPRESA_COPILOT/ACCESO_Y_DESCARGAS_COPILOT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    intro_style = ParagraphStyle(
        'IntroText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=10
    )

    cell_title = ParagraphStyle(
        'CellTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0f172a")
    )

    cell_link = ParagraphStyle(
        'CellLink',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1d4ed8")
    )

    cell_desc = ParagraphStyle(
        'CellDesc',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569")
    )

    h2_style = ParagraphStyle(
        'H2Style',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=6
    )

    box_text = ParagraphStyle(
        'BoxText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Marco de Gobernanza y Arquitectura con GitHub Copilot", title_style))
    story.append(Paragraph("<b>Entregables Oficiales y Enlaces de Acceso Directo</b> · Versión v1.0 (Lanzamiento Inicial)", subtitle_style))
    story.append(Spacer(1, 4))

    # Intro
    intro_p = ("Esta ficha centraliza el acceso directo a la documentación oficial, el entorno web y el kit de "
               "automatización preparado para consultoría estratégica. Todos los recursos están optimizados para operar "
               "en <b>VS Code</b> con <b>GitHub Copilot</b> y repositorios corporativos en <b>GitLab</b>, garantizando "
               "aislamiento total frente a las políticas de TI y reversión inmediata en caso de necesidad.")
    story.append(Paragraph(intro_p, intro_style))
    story.append(Spacer(1, 6))

    # Links Table via GitHub Pages (Clean web, zero code interfaces)
    story.append(Paragraph("📋 Recursos Oficiales Directos (Vía Web y Descarga)", h2_style))

    pages_base = "https://javiercursocorreo-gif.github.io/adaptacion-copilot"

    table_data = [
        [
            Paragraph("<b>Recurso Ejecutivo</b>", cell_title),
            Paragraph("<b>Acceso en 1 Clic</b>", cell_title),
            Paragraph("<b>Descripción del Entregable</b>", cell_title)
        ],
        [
            Paragraph("📄 <b>Guía Maestra Oficial (PDF)</b>", cell_title),
            Paragraph(f'<a href="{pages_base}/ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.pdf" color="#1d4ed8"><u><b>Descargar PDF (5 págs) ↗</b></u></a>', cell_link),
            Paragraph("Documento integral de gobernanza: las 4 D, aislamiento de TI en AppData, parámetros de motor y ciclo de vida.", cell_desc)
        ],
        [
            Paragraph("📦 <b>Kit de Inicio en 1 Clic (ZIP)</b>", cell_title),
            Paragraph(f'<a href="{pages_base}/WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip" color="#1d4ed8"><u><b>Descargar Kit ZIP ↗</b></u></a>', cell_link),
            Paragraph("Plantilla universal con <code>.vscode</code>, <code>copilot-instructions</code>, pipeline de GitLab y script <code>desactivar_gobernanza.bat</code>.", cell_desc)
        ],
        [
            Paragraph("🌐 <b>Visor Web Interactivo (HTML)</b>", cell_title),
            Paragraph(f'<a href="{pages_base}/ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.html" color="#1d4ed8"><u><b>Abrir Visor Web (HTML) ↗</b></u></a>', cell_link),
            Paragraph("Versión web completa maquetada y responsive para lectura interactiva desde navegador, iPad o PC sin descargas.", cell_desc)
        ]
    ]

    t = Table(table_data, colWidths=[150, 160, 213])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Fast Start Box
    story.append(Paragraph("⚡ Puesta en Marcha en 3 Pasos (Sin Complicaciones)", h2_style))
    steps_data = [
        [
            Paragraph("<b>Paso 1: Descarga y Extracción</b>", cell_title),
            Paragraph("Descarga el <a href='" + pages_base + "/WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip' color='#1d4ed8'><u>Kit ZIP</u></a> y descomprímelo en una carpeta de prueba en tu equipo (ej. <code>C:\\Piloto-Consultoria\\</code>).", cell_desc)
        ],
        [
            Paragraph("<b>Paso 2: Apertura en VS Code</b>", cell_title),
            Paragraph("Abre VS Code y selecciona <i>Archivo → Abrir carpeta...</i> apuntando a la carpeta descomprimida. La gobernanza de Copilot se activa de inmediato solo para ese proyecto.", cell_desc)
        ],
        [
            Paragraph("<b>Paso 3: Marcha Atrás (Rollback)</b>", cell_title),
            Paragraph("Si deseas desactivar la gobernanza en cualquier momento, haz doble clic en <code>desactivar_gobernanza.bat</code> dentro de la carpeta. Copilot vuelve a su estado de fábrica en 5 segundos.", cell_desc)
        ]
    ]
    t_steps = Table(steps_data, colWidths=[170, 353])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 12))

    # Security Guarantee Box
    sec_html = ("<b>🛡️ Garantía de Seguridad y Cumplimiento de TI Corporativo:</b><br/>"
                "• <b>Cero alteración de directivas corporativas:</b> Los parámetros se aplican exclusivamente a nivel de carpeta local (<code>.vscode/settings.json</code>) y jamás modifican la configuración global de TI de la empresa (<code>%APPDATA%\\Code\\User</code>).<br/>"
                "• <b>Compatibilidad nativa con GitLab:</b> El estándar <code>.github/copilot-instructions.md</code> es una convención local exigida por el motor de Microsoft en disco que se sube limpiamente a GitLab como cualquier otra carpeta de proyecto.")
    
    sec_table = Table([[Paragraph(sec_html, box_text)]], colWidths=[523])
    sec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (0,0), 1, colors.HexColor("#86efac")),
        ('TOPPADDING', (0,0), (0,0), 9),
        ('BOTTOMPADDING', (0,0), (0,0), 9),
        ('LEFTPADDING', (0,0), (0,0), 10),
        ('RIGHTPADDING', (0,0), (0,0), 10),
    ]))
    story.append(sec_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generado con exito:", pdf_path)

if __name__ == "__main__":
    build_pdf()
