#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pdf_copilot_gitlab.py
Genera la Guía Maestra Técnica y de Gobernanza para Consultores Senior (+65) en Entornos Corporativos:
'GUÍA DE ARQUITECTURA, PARAMETRIZACIÓN Y GOBERNANZA EN GITHUB COPILOT & GITLAB'
(Edición Íntegra Extensa: Tabla oficial de control de versiones v1.0, equivalencia VS Code y Antigravity,
demostración exhaustiva de aislamiento respecto a TI, desmitificación de la carpeta .github en GitLab,
entorno de pruebas sandbox, protocolo de marcha atrás en 5 segundos, mitigación de las 4 D y GitLab Pages).
"""

import os
import sys
import subprocess
import shutil
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_FILE = os.path.join(BASE_DIR, "ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.pdf")
HTML_FILE = os.path.join(BASE_DIR, "ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.html")
DOCX_FILE = os.path.join(BASE_DIR, "ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.docx")
ZIP_FILE = os.path.join(BASE_DIR, "WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip")

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
        left_text = "Gobernanza Copilot & GitLab • Versión web en vivo: https://javiercursocorreo-gif.github.io/adaptacion-copilot"
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawString(36, 22, left_text)
        self.drawRightString(A4[0] - 36, 22, page_text)
        self.restoreState()

def generar_html():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Guía de Gobernanza y Productividad con Copilot & GitLab para Consultores Senior</title>
    <style>
        :root {
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #475569;
            --border: #e2e8f0;
            --primary: #1e40af;
            --primary-dark: #1e3a8a;
            --danger: #dc2626;
            --danger-bg: #fef2f2;
            --danger-border: #f87171;
            --success: #16a34a;
            --success-bg: #f0fdf4;
            --success-border: #4ade80;
            --callout-bg: #f0f9ff;
            --callout-border: #38bdf8;
            --rollback-bg: #fffbeb;
            --rollback-border: #f59e0b;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            padding: 40px;
            border: 1px solid var(--border);
        }
        .badge-corp {
            display: inline-block;
            background: #e0e7ff;
            color: #3730a3;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        h1 {
            color: #0f172a;
            font-size: 25px;
            margin-top: 0;
            margin-bottom: 8px;
            border-bottom: 3px solid var(--primary);
            padding-bottom: 12px;
        }
        .subtitle {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 20px;
            font-weight: 500;
        }
        .version-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0 25px 0;
            font-size: 12px;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            overflow: hidden;
        }
        .version-table th {
            background: #e2e8f0;
            color: #0f172a;
            padding: 8px 12px;
            text-align: left;
            font-weight: 700;
            border-bottom: 2px solid #cbd5e1;
        }
        .version-table td {
            padding: 8px 12px;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
        }
        .version-tag {
            background: #dbeafe;
            color: #1e40af;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .quote-box {
            background: #f1f5f9;
            border-left: 4px solid var(--primary);
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            font-size: 13.5px;
            color: #334155;
            margin-bottom: 28px;
        }
        .toc {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 35px;
        }
        .toc-title {
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .toc ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .toc li {
            margin-bottom: 8px;
            font-size: 13px;
        }
        .toc li ul {
            padding-left: 20px;
            margin-top: 4px;
        }
        .toc li ul li {
            margin-bottom: 4px;
            font-size: 12.5px;
        }
        .toc a {
            color: var(--primary-dark);
            text-decoration: none;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        .phase-header {
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
            color: #ffffff;
            font-size: 15px;
            font-weight: 700;
            padding: 10px 18px;
            border-radius: 8px;
            margin-top: 36px;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }
        h2 {
            font-size: 17px;
            color: #0f172a;
            margin-top: 24px;
            margin-bottom: 10px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
        }
        h3 {
            font-size: 14.5px;
            color: #1e293b;
            margin-top: 16px;
            margin-bottom: 8px;
        }
        p, li {
            font-size: 13.5px;
            color: #334155;
        }
        .danger-box {
            background: var(--danger-bg);
            border: 1px solid var(--danger-border);
            border-left: 5px solid var(--danger);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
        }
        .danger-box .title {
            font-weight: 700;
            color: #991b1b;
            font-size: 13.5px;
            margin-bottom: 4px;
        }
        .solution-box {
            background: var(--success-bg);
            border: 1px solid var(--success-border);
            border-left: 5px solid var(--success);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 22px;
        }
        .solution-box .title {
            font-weight: 700;
            color: #166534;
            font-size: 13.5px;
            margin-bottom: 4px;
        }
        .callout-blue {
            background: var(--callout-bg);
            border: 1px solid var(--callout-border);
            border-left: 5px solid #0284c7;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 18px 0;
        }
        .callout-blue .title {
            font-weight: 700;
            color: #0369a1;
            font-size: 14px;
            margin-bottom: 6px;
        }
        .rollback-box {
            background: var(--rollback-bg);
            border: 1px solid var(--rollback-border);
            border-left: 5px solid #d97706;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 18px 0;
        }
        .rollback-box .title {
            font-weight: 700;
            color: #b45309;
            font-size: 14px;
            margin-bottom: 6px;
        }
        .param-card {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #475569;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 12px;
        }
        .param-card .name {
            font-weight: 700;
            font-size: 13.5px;
            color: #0f172a;
            margin-bottom: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0 24px 0;
            font-size: 12.5px;
        }
        th {
            background: #f1f5f9;
            color: #0f172a;
            text-align: left;
            padding: 10px 12px;
            font-weight: 700;
            border: 1px solid #cbd5e1;
        }
        td {
            padding: 8px 12px;
            border: 1px solid #e2e8f0;
            color: #334155;
        }
        tr:nth-child(even) td {
            background: #f8fafc;
        }
        .kit-box {
            background: #f0fdf4;
            border: 2px solid #22c55e;
            border-radius: 12px;
            padding: 20px 24px;
            margin-top: 20px;
        }
        .kit-title {
            font-size: 16px;
            font-weight: 700;
            color: #15803d;
            margin-bottom: 10px;
        }
        footer {
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
        }
    </style>
</head>
<body>
<div class="container">
    <span class="badge-corp">Guía de Gobernanza para Consultoría Corporativa</span>
    <h1>Guía de Arquitectura, Parametrización y Gobernanza en Copilot & GitLab</h1>
    <div class="subtitle">Manual Maestro de Productividad y Control de IA para Consultores y Profesionales Senior (+65)<br/>Cómo dirigir a Copilot sobre repositorios corporativos en GitLab, generar entregables de alto impacto, blindar la confidencialidad y operar sin alterar el entorno habitual del ordenador de la empresa.</div>

    <!-- TABLA DE CONTROL DE VERSIONES -->
    <table class="version-table">
        <thead>
            <tr>
                <th style="width: 75px;">Versión</th>
                <th style="width: 85px;">Fecha</th>
                <th style="width: 130px;">Responsable</th>
                <th>Descripción Detallada del Cambio y Alcance de la Versión</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="version-tag">v1.0</span></td>
                <td>25/11/2026</td>
                <td>Marco Gobernanza IA</td>
                <td><strong>Edición Inicial Oficial Entregada:</strong> Adaptación íntegra para Consultoría Senior (+65). Aislamiento total en carpeta local (<code>.vscode/settings.json</code>) sin tocar TI en <code>AppData</code>; desmitificación de la ruta <code>.github</code> en GitLab; entorno de pruebas (Sandbox); script de marcha atrás en 5 seg (<code>desactivar_gobernanza.bat</code>); mitigación de las 4 D; publicación en GitLab Pages; y arquitectura modular de Skills reutilizables con «/» (<code>.github/prompts/</code>).</td>
            </tr>
        </tbody>
    </table>

    <div class="quote-box">
        «En consultoría estratégica y de negocio, la inteligencia artificial no sustituye al criterio del consultor: acelera la redacción de informes y el análisis de datos. El verdadero peligro es perder el gobierno sobre las fuentes, los números y los entregables. La redacción se apoya en la IA; el rigor metodológico, la confidencialidad y la verificación final jamás.»<br/>
        <strong>— Marco de Gobernanza en IA para Consultoría Senior</strong>
    </div>

    <div class="toc">
        <div class="toc-title">Índice General de Fases y Protocolos</div>
        <ul>
            <li><strong><a href="#fase0">FASE 0: EL ENTORNO DE CONSULTORÍA (RELACIÓN COPILOT - VS CODE Y SEGURIDAD)</a></strong>
                <ul>
                    <li><a href="#f0-1">0.1 ¿Por qué hablamos de VS Code? La Relación entre Copilot y el Editor de Trabajo</a></li>
                    <li><a href="#f0-2">0.2 Ajustes Globales vs. Locales: La Garantía de que tu Puesto de Trabajo NO se Desconfigura</a></li>
                    <li><a href="#f0-3">0.3 ¿Por qué aparece una carpeta llamada .github si usamos GitLab?</a></li>
                    <li><a href="#f0-4">0.4 Entorno de Pruebas Seguro (Sandbox Piloto): Cómo Experimentar sin Tocar tu Día a Día</a></li>
                    <li><a href="#f0-5">0.5 Tabla Comparativa de Parametrización Exhaustiva en settings.json</a></li>
                    <li><a href="#f0-6">0.6 El Protocolo de Marcha Atrás (Rollback en 5 Segundos para Dejar Todo como Estaba)</a></li>
                </ul>
            </li>
            <li><strong><a href="#fase1">FASE 1: FUNDAMENTOS Y GESTIÓN DE RIESGOS EN CONSULTORÍA</a></strong>
                <ul>
                    <li><a href="#f1-1">1.1 De la Ilusión del 'Vibe Coding' a la Consultoría Rigurosa con IA</a></li>
                    <li><a href="#f1-2">1.2 Las 4 D del Riesgo de la IA en Informes Corporativos (Duplicación, Drift, Deluge, Deception)</a></li>
                    <li><a href="#f1-3">1.3 Arquitectura de Carpeta Raíz: Organización Limpia de Documentos y Entregables</a></li>
                </ul>
            </li>
            <li><strong><a href="#fase2">FASE 2: EL MOTOR DE COPILOT Y DIRECTIVAS DE TRABAJO</a></strong>
                <ul>
                    <li><a href="#f2-1">2.1 Selección de Modelos para Consultoría (Claude 3.5 Sonnet para Informes vs. GPT-4o para Datos)</a></li>
                    <li><a href="#f2-2">2.2 Modificadores de Enfoque: Cómo dar Contexto a la IA sin Copiar y Pegar</a></li>
                    <li><a href="#f2-3">2.3 Las 6 Políticas Maestras de Parametrización en el Trabajo Diario</a></li>
                </ul>
            </li>
            <li><strong><a href="#fase3">FASE 3: PROTOCOLOS DE GOBERNANZA (.copilot-instructions.md)</a></strong>
                <ul>
                    <li><a href="#f3-1">3.1 Cero Interrupciones (Cero-Submits): Trabajo Desatendido sin Ventanas de Aprobación</a></li>
                    <li><a href="#f3-2">3.2 El Método de las 3 Preguntas Clave: ¿Cuándo, Cómo y Por Qué Trabajar en Silencio?</a></li>
                    <li><a href="#f3-3">3.3 Protocolo Cognitivo Elephant-Goldfish: Memoria del Proyecto vs. Revisiones Aisladas</a></li>
                    <li><a href="#f3-4">3.4 Trazabilidad de Versiones y Control de Entregables ([COMANDO XX])</a></li>
                    <li><a href="#f3-5">3.5 Cero Trozos de Código Sueltos: Entrega de Soluciones Completas y Autónomas</a></li>
                    <li><a href="#f3-6">3.6 Dashboards Ejecutivos Interactivos en HTML (Generative UI para Clientes y Directores)</a></li>
                    <li><a href="#f3-7">3.7 Publicación Automática en GitLab Pages e Intranet Corporativa sin Servidores</a></li>
                    <li><a href="#f3-8">3.8 Skills Reutilizables en Copilot (.github/prompts/): Atajos con «/» para Consultoría</a></li>
                </ul>
            </li>
            <li><strong><a href="#fase4">FASE 4: PUESTA EN MARCHA EN 1 CLIC (PLANTILLA UNIVERSAL CON ROLLBACK)</a></strong>
                <ul>
                    <li><a href="#f4-1">4.1 La Plantilla Universal de Consultoría (WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip)</a></li>
                    <li><a href="#f4-2">4.2 Activación Paso a Paso en tu Portátil Corporativo Windows o Mac</a></li>
                    <li><a href="#f4-3">4.3 Matriz Comparativa: La Consultoría Tradicional con IA vs. Metodología Gobernada</a></li>
                </ul>
            </li>
        </ul>
    </div>

    <!-- FASE 0 -->
    <div id="fase0" class="phase-header">FASE 0: EL ENTORNO DE CONSULTORÍA (RELACIÓN COPILOT - VS CODE Y SEGURIDAD)</div>

    <h2 id="f0-1">0.1 ¿Por qué hablamos de VS Code? La Relación entre Copilot y el Editor de Trabajo</h2>
    <p>Una duda habitual cuando un consultor empieza a utilizar Copilot es: <em>«¿Por qué hablamos de Visual Studio si mi empresa usa Copilot? ¿Es el mismo editor que usamos en Antigravity?»</em>. La respuesta radica en la arquitectura universal de Microsoft:</p>
    <ul>
        <li><strong>Copilot no es una aplicación independiente:</strong> No existe una ventana o programa cerrado llamado "Copilot.exe" donde se redacten informes. Copilot es un <strong>motor inteligente (un copiloto invisible)</strong> que necesita "vivir" dentro de una herramienta de trabajo.</li>
        <li><strong>Visual Studio Code (VS Code) es el "vehículo" y Copilot es el "motor":</strong> VS Code es la aplicación de escritorio líder desarrollada por Microsoft donde se integra Copilot para leer los documentos del proyecto, abrir el panel lateral de conversación y modificar los archivos en tiempo real.</li>
        <li><strong>Equivalencia con Google Antigravity IDE:</strong> Sí, <strong>Antigravity IDE está construido exactamente sobre el mismo motor de código abierto de Microsoft VS Code (Code-OSS)</strong>. Google tomó la base de VS Code y le integró los modelos de Gemini DeepMind. Por tanto, los atajos de teclado, el árbol de archivos lateral, la terminal integrada y la estructura de configuración <code>settings.json</code> son 100% idénticos entre ambos entornos. Lo que aprendes en uno funciona directamente en el otro.</li>
    </ul>

    <h2 id="f0-2">0.2 Ajustes Globales vs. Locales: La Garantía de que tu Puesto de Trabajo NO se Desconfigura</h2>
    <p>En el ordenador Windows que te ha facilitado la empresa, el departamento de Sistemas/IT ya tiene configuradas directivas corporativas. Es fundamental tener la certeza absoluta de que seguir esta guía <strong>no romperá tu configuración diaria ni te impedirá trabajar en tus tareas habituales</strong>.</p>
    <p>VS Code gestiona su configuración en dos niveles estrictamente separados:</p>
    <ol>
        <li><strong>Ajustes Globales de Usuario (User Settings):</strong> Se guardan en una carpeta protegida del sistema operativo (en <code>AppData\\Roaming\\Code\\User\\settings.json</code> de Windows). Definen el comportamiento general de tu programa para toda la empresa. <strong>Nuestra metodología NUNCA toca ni modifica estos ajustes globales.</strong></li>
        <li><strong>Ajustes Locales de Proyecto (Workspace Settings):</strong> Se guardan dentro de la carpeta concreta en la que estés trabajando, dentro de una subcarpeta llamada <code>.vscode/settings.json</code>. <strong>Solo tienen efecto mientras esa carpeta esté abierta en pantalla.</strong></li>
    </ol>

    <div class="solution-box">
        <div class="title">🛡️ Garantía de Integridad Corporativa:</div>
        Al cerrar la carpeta del proyecto piloto y abrir cualquier otro trabajo de tu empresa, VS Code vuelve al 100% a su estado estándar habitual. No queda ningún ajuste residual ni modificación que afecte a tus otras herramientas.
    </div>

    <h2 id="f0-3">0.3 ¿Por qué aparece una carpeta llamada .github si usamos GitLab?</h2>
    <p>Otra fuente lógica de confusión es ver una carpeta llamada <code>.github</code> cuando la empresa utiliza exclusivamente <strong>GitLab</strong>. La explicación es puramente técnica y no implica ninguna conexión con GitHub:</p>
    <ul>
        <li>Como la extensión fue desarrollada por el equipo de GitHub (Microsoft), sus programadores fijaron en el código interno de VS Code que el archivo donde se leen las instrucciones obligatorias debe llamarse por defecto <code>.github/copilot-instructions.md</code> en el disco local.</li>
        <li><strong>Es únicamente un nombre de carpeta en tu disco duro:</strong> No conecta con internet ni sube datos a GitHub. Cuando sincronices tu trabajo con GitLab, esa carpetita viaja y se almacena en el servidor privado de GitLab de tu empresa exactamente igual que cualquier otra carpeta de informes.</li>
    </ul>

    <h2 id="f0-4">0.4 Entorno de Pruebas Seguro (Sandbox Piloto): Cómo Experimentar sin Tocar tu Día a Día</h2>
    <p>Para mayor tranquilidad, un consultor no debe realizar experimentos directamente sobre los proyectos críticos de la empresa. Existen dos formas impecables de crear un "laboratorio seguro":</p>
    <ul>
        <li><strong>Opción 1: Carpeta Piloto Aislada (Recomendada):</strong> Crea en tu disco local una carpeta llamada <code>C:\\Piloto-Consultoria-IA\\</code>. Descomprime allí la plantilla y abre únicamente esa carpeta en VS Code (<code>code .</code>). Todo lo que pruebes ocurrirá dentro de esa caja de arena; tus repositorios reales de GitLab no se verán afectados.</li>
        <li><strong>Opción 2: Perfiles Nativos de VS Code (Profiles):</strong> VS Code permite crear "perfiles de usuario" estancos. En el icono de engranaje (abajo a la izquierda), haz clic en <strong>Profiles ➔ Create Profile</strong> con el nombre <em>"Pruebas Gobernanza IA"</em>. Esto crea un espacio totalmente limpio, con su propia configuración, que puedes eliminar con un solo clic cuando termines tus pruebas.</li>
    </ul>

    <h2 id="f0-5">0.5 Tabla Comparativa de Parametrización Exhaustiva en settings.json</h2>
    <p>Los parámetros que la plantilla inyecta en <code>.vscode/settings.json</code> actúan exclusivamente dentro de la carpeta del proyecto, optimizando la velocidad y garantizando el cumplimiento normativo:</p>

    <table>
        <thead>
            <tr>
                <th>Parámetro (settings.json local)</th>
                <th>Valor Recomendado</th>
                <th>Justificación Técnica y Beneficio en Consultoría</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>chat.editing.autoAcceptDelay</code></td>
                <td><code>0</code></td>
                <td><strong>Cero-Submits:</strong> Aplica las modificaciones de Copilot Edits de forma desatendida sin obligarte a pulsar "Accept" en cada párrafo.</td>
            </tr>
            <tr>
                <td><code>terminal.integrated.allowChaining</code></td>
                <td><code>true</code></td>
                <td>Permite encadenar verificaciones automáticas y sincronizaciones con GitLab sin alertas intermedias.</td>
            </tr>
            <tr>
                <td><code>chat.projectContext.enabled</code></td>
                <td><code>true</code></td>
                <td>Habilita la indexación local para que <code>@workspace</code> reconozca todos los documentos y actas del cliente.</td>
            </tr>
            <tr>
                <td><code>debug.filterGitIgnored</code></td>
                <td><code>true</code></td>
                <td><strong>Blindaje de Confidencialidad:</strong> Impide que Copilot lea archivos protegidos o ignorados en <code>.gitignore</code>.</td>
            </tr>
            <tr>
                <td><code>telemetry.telemetryLevel</code></td>
                <td><code>"off"</code></td>
                <td>Desactiva el envío de diagnósticos hacia el exterior, garantizando el cumplimiento estricto del secreto profesional y GDPR.</td>
            </tr>
            <tr>
                <td><code>files.watcherExclude</code></td>
                <td>Exclusiones masivas</td>
                <td>Optimiza la memoria del portátil corporativo ignorando carpetas de sistema pesadas y cachés.</td>
            </tr>
        </tbody>
    </table>

    <h2 id="f0-6">0.6 El Protocolo de Marcha Atrás (Rollback en 5 Segundos para Dejar Todo como Estaba)</h2>
    <div class="rollback-box">
        <div class="title">⏪ PROTOCOLO DE DESACTIVACIÓN Y MARCHA ATRÁS (ROLLBACK):</div>
        <p>Toda la gobernanza que inyectamos reside exclusivamente en dos carpetas dentro del proyecto:</p>
        <ul>
            <li>La carpeta <code>.vscode/</code> (que contiene los parámetros locales).</li>
            <li>La carpeta <code>.github/</code> o <code>.gitlab/</code> (que contiene el archivo de instrucciones).</li>
        </ul>
        <p><strong>Para anular todo en 5 segundos:</strong> Solo tienes que borrar esas dos carpetas de tu proyecto (o hacer doble clic en el archivo <code>desactivar_gobernanza.bat</code> que hemos incluido en la plantilla). En ese mismo instante, Copilot vuelve a funcionar en modo estándar como si nada hubiera pasado.</p>
    </div>

    <!-- FASE 1 -->
    <div id="fase1" class="phase-header">FASE 1: FUNDAMENTOS Y GESTIÓN DE RIESGOS EN CONSULTORÍA</div>

    <h2 id="f1-1">1.1 De la Ilusión del 'Vibe Coding' a la Consultoría Rigurosa con IA</h2>
    <p>En el uso no profesional de la IA está de moda el <em>"Vibe Coding"</em>: dialogar con el asistente como si fuera un colega de charla y aceptar sus respuestas sin contrastar. En consultoría de negocio, estrategia o procesos, esto es inaceptable.</p>
    <p>La inteligencia artificial genera texto convincente basándose en probabilidades estadísticas, no en conocimiento verificado de tu cliente. Si no se le imponen directivas férreas, la IA inventará datos demográficos, citará normativas derogadas o mezclará metodologías incompatibles. Nuestro marco de <strong>Gobernanza</strong> transforma a Copilot en un redactor analítico disciplinado que respeta escrupulosamente los datos aportados por el consultor.</p>

    <h2 id="f1-2">1.2 Las 4 D del Riesgo de la IA en Informes Corporativos (Duplicación, Drift, Deluge, Deception)</h2>
    <p>En consultoría, los cuatro grandes riesgos de trabajar con modelos de IA son:</p>

    <div class="danger-box">
        <div class="title">⚠️ 1. DUPLICACIÓN (Reinvención de Metodologías ya Existentes)</div>
        Al redactar una propuesta o un entregable, la IA tiende a inventar nuevos marcos de trabajo o glosarios cuando la firma de consultoría ya dispone de metodologías estándar homologadas. Esto confunde al cliente y fragmenta la coherencia del equipo.
    </div>
    <div class="solution-box">
        <div class="title">🛡️ SOLUCIÓN EN CONSULTORÍA:</div>
        Inyectar en el contexto los manuales metodológicos existentes en el repositorio de GitLab (mediante el comando <code>#file</code>) para que la IA aplique siempre los estándares y formatos oficiales de tu empresa.
    </div>

    <div class="danger-box">
        <div class="title">⚠️ 2. DRIFT (Desviación del Alcance del Proyecto)</div>
        Conforme el chat se alarga, la IA sufre fatiga de contexto: olvida los objetivos del pliego técnico o la propuesta comercial, y empieza a proponer iniciativas que exceden el presupuesto o el alcance pactado con el cliente.
    </div>
    <div class="solution-box">
        <div class="title">🛡️ SOLUCIÓN EN CONSULTORÍA:</div>
        Fijar el alcance en un documento inmutable (<code>ALCANCE_PROYECTO.md</code>) e iniciar conversaciones limpias para cada fase del informe, asegurando que la IA no arrastre ruido conversacional.
    </div>

    <div class="danger-box">
        <div class="title">⚠️ 3. DELUGE (Diluvio de Palabrería y 'Paja' Documental)</div>
        Los modelos generativos tienden a rellenar páginas con prosa grandilocuente pero vacía de contenido práctico. Un informe de 80 páginas que no aporta soluciones ejecutivas concretas deteriora la reputación del consultor.
    </div>
    <div class="solution-box">
        <div class="title">🛡️ SOLUCIÓN EN CONSULTORÍA:</div>
        Regla de Síntesis Ejecutiva: Directivas estrictas que obligan a la IA a estructurar la información en tablas comparativas, matrices DAFO, cuadros de mando y planes de acción con plazos y responsables cuantificados.
    </div>

    <div class="danger-box">
        <div class="title">⚠️ 4. DECEPTION (Datos Inventados y Alucinaciones Estadísticas)</div>
        El informe luce visualmente impecable, pero incluye porcentajes de mercado inventados, artículos de ley inexistentes o gráficos con datos falsos que no resisten una reunión con el comité de dirección del cliente.
    </div>
    <div class="solution-box">
        <div class="title">🛡️ SOLUCIÓN EN CONSULTORÍA:</div>
        Obligación de Trazabilidad: Prohibido admitir datos o cifras que no provengan de los documentos fuente aportados por el consultor. Verificación previa y poda inmediata de cualquier aserción no fundamentada.
    </div>

    <h2 id="f1-3">1.3 Arquitectura de Carpeta Raíz: Organización Limpia de Documentos y Entregables</h2>
    <p>Para que Copilot entienda la totalidad del encargo de consultoría, todo el material del proyecto (antecedentes, entrevistas, actas de reuniones, pliegos y borradores) debe residir bajo una <strong>carpeta raíz única</strong> sincronizada con GitLab. Al abrir esa carpeta con <code>code .</code>, Copilot tiene visión 360º de toda la documentación del cliente sin perderse en carpetas ajenas.</p>

    <!-- FASE 2 -->
    <div id="fase2" class="phase-header">FASE 2: EL MOTOR DE COPILOT Y DIRECTIVAS DE TRABAJO</div>

    <h2 id="f2-1">2.1 Selección de Modelos para Consultoría (Claude 3.5 Sonnet para Informes vs. GPT-4o para Datos)</h2>
    <p>En la barra superior de Copilot Chat, el consultor puede seleccionar el motor según el tipo de entregable:</p>
    <ul>
        <li><strong>Claude 3.5 Sonnet (Recomendado para Redacción Ejecutiva e Informes):</strong> Es el modelo con mayor rigor conceptual, mejor prosa empresarial y menor tendencia a inventar datos. Ideal para informes estratégicos, diagnósticos organizativos y propuestas de consultoría.</li>
        <li><strong>GPT-4o (Recomendado para Tratamiento de Datos y Hojas de Cálculo):</strong> Gran velocidad para procesar tablas complejas, transformar listados de requerimientos o extraer resúmenes ejecutivos a partir de transcripciones de entrevistas.</li>
    </ul>
    <p><strong>Alcance realista en Copilot:</strong> A diferencia de plataformas de enjambre masivo (<code>/swarm</code>), Copilot opera en VS Code mediante un <strong>único agente asistente sobre tu carpeta</strong>, apoyado por atajos <code>/</code> y modificadores <code>#file</code>, lo que lo hace directo, predecible y seguro para el consultor.</p>

    <h2 id="f2-2">2.2 Modificadores de Enfoque: Cómo dar Contexto a la IA sin Copiar y Pegar</h2>
    <p>El consultor senior no debe perder el tiempo copiando y pegando fragmentos de documentos en el chat. En su lugar, utiliza los comandos directos de VS Code:</p>
    <ul>
        <li><strong><code>#file:entrevistas/acta_direccion.md</code>:</strong> Inyecta el acta exacta de la reunión con el cliente para que el informe refleje sus peticiones literales.</li>
        <li><strong><code>#selection</code>:</strong> Selecciona con el ratón un párrafo del borrador y pide: <em>"Haz este párrafo más directo y enfocado a un Director Financiero"</em>.</li>
        <li><strong><code>@workspace</code>:</strong> Pregunta a Copilot sobre el conjunto de todos los documentos: <em>"@workspace ¿cuáles son los 3 principales riesgos normativos detectados en los informes de auditoría?"</em>.</li>
    </ul>

    <h2 id="f2-3">2.3 Las 6 Políticas Maestras de Parametrización en el Trabajo Diario</h2>
    <p>Los parámetros que inyectamos en <code>.vscode/settings.json</code> garantizan una experiencia limpia y ejecutiva:</p>
    <div class="param-card"><div class="name">1. Edición Directa de Documentos (autoAcceptDelay: 0)</div>Permite que la IA actualice los borradores de tus informes sin obligarte a confirmar palabra por palabra.</div>
    <div class="param-card"><div class="name">2. Confidencialidad Blindada (debug.filterGitIgnored: true)</div>Asegura que Copilot jamás lea ni envíe a la nube archivos con datos personales de clientes o información financiera sensible.</div>
    <div class="param-card"><div class="name">3. Telemetría Desactivada (telemetry: "off")</div>Cumplimiento riguroso de las cláusulas de confidencialidad y secreto profesional de la consultora.</div>
    <div class="param-card"><div class="name">4. Enfoque Documental Limpio</div>Indexación de archivos Markdown, Word, PDF y HTML, excluyendo carpetas de sistema que ralentizan la máquina.</div>
    <div class="param-card"><div class="name">5. Modelo de Redacción Calibrado</div>Uso prioritario de Claude 3.5 Sonnet para garantizar un tono ejecutivo sobrio y formal.</div>
    <div class="param-card"><div class="name">6. Prevalencia de las Reglas (.copilot-instructions.md)</div>Las directivas del manual de estilo de tu empresa tienen prioridad absoluta sobre cualquier sugerencia que la IA formule en el chat.</div>

    <!-- FASE 3 -->
    <div id="fase3" class="phase-header">FASE 3: PROTOCOLOS DE GOBERNANZA (.copilot-instructions.md)</div>

    <h2 id="f3-1">3.1 Cero Interrupciones (Cero-Submits): Trabajo Desatendido sin Ventanas de Aprobación</h2>
    <p>En el flujo de trabajo moderno, la IA no debe pedir confirmación por cada línea redactada. Si le pides actualizar la sección de conclusiones de un informe, la IA debe reescribir la sección directamente en el archivo y guardar el cambio. El consultor revisa el resultado final completo con calma en pantalla, eliminando la fatiga de clics.</p>

    <h2 id="f3-2">3.2 El Método de las 3 Preguntas Clave: ¿Cuándo, Cómo y Por Qué Trabajar en Silencio?</h2>
    <div class="callout-blue">
        <div class="title">📋 LA OPERATIVA EN SILENCIO ADAPTADA A CONSULTORÍA</div>
        <p><strong>1. ¿En qué momento se usa?</strong> En toda sesión de redacción, estructuración de informes, análisis de pliegos y preparación de presentaciones.</p>
        <p><strong>2. ¿Cómo lo usamos?</strong> El consultor plantea la solicitud (ej. <em>"Elabora el Plan de Mitigación de Riesgos a partir de la auditoría"</em>). La IA trabaja en silencio absoluto (sin saludos ni preámbulos vacíos), actualiza el documento final y, al concluir, entrega un reporte claro de lo modificado.</p>
        <p><strong>3. ¿Por qué lo usamos?</strong> Porque un consultor valora su tiempo. Elimina la charla innecesaria de la IA y permite centrarse en validar si el entregable cumple con las expectativas del cliente.</p>
    </div>

    <h2 id="f3-3">3.3 Protocolo Cognitivo Elephant-Goldfish: Memoria del Proyecto vs. Revisiones Aisladas</h2>
    <p>El consultor actúa como el <strong>Elefante</strong>: conserva la memoria de las reuniones, las sensaciones con el cliente y la visión estratégica. Para tareas analíticas intensas (ej. revisar si un informe de 50 páginas tiene incoherencias de fechas), se abre una subsesión limpia (<strong>Goldfish</strong>) que audita el texto con mente fresca y se cierra tras emitir su dictamen, sin saturar la conversación principal.</p>

    <h2 id="f3-4">3.4 Trazabilidad de Versiones y Control de Entregables ([COMANDO XX])</h2>
    <p>Cada versión del informe o cambio significativo se asocia a un identificador correlativo (ej. <code>[VERSIÓN 04: PLAN DE ACCIÓN]</code>) registrado en GitLab. Si el cliente solicita comparar la versión entregada en la reunión del martes con la del viernes, el consultor puede rastrear con exactitud matemática qué párrafos cambiaron y en qué fecha.</p>

    <h2 id="f3-5">3.5 Cero Trozos de Código Sueltos: Entrega de Soluciones Completas y Autónomas</h2>
    <p>Un consultor no debe manipular código ni parches manuales. Todo lo que el asistente entregue debe ser <strong>un producto terminado y autónomo</strong>: documentos íntegros en Markdown/Word listos para exportar a PDF, o aplicaciones web interactivas completas que abren con un doble clic en cualquier ordenador o iPad.</p>

    <h2 id="f3-6">3.6 Dashboards Ejecutivos Interactivos en HTML (Generative UI para Clientes y Directores)</h2>
    <p>Una de las mayores ventajas de esta metodología para un consultor es la generación de <strong>Cuadros de Mando Interactivos (HTML)</strong>. En lugar de enviar un informe estático de 60 páginas que nadie lee, la IA compila una página web interactiva (autónoma, en un único archivo, con diseño corporativo elegante) que incluye:</p>
    <ul>
        <li>Filtros interactivos por departamento o fase del proyecto.</li>
        <li>Matrices de riesgo clicables (rojo / amarillo / verde) con desplegables explicativos.</li>
        <li>Gráficos visuales de avance de hitos y cronogramas.</li>
    </ul>
    <p>Este archivo HTML se puede enviar por correo o abrir directamente en una reunión con un proyector o tablet, causando un impacto profesional extraordinario. Antes de dar por cerrado un dashboard HTML o informe, Copilot ejecuta una <strong>auto-auditoría previa</strong> (verificando enlaces, estructura y coherencia de datos) para evitar fallos en vivo.</p>

    <h2 id="f3-7">3.7 Publicación Automática en GitLab Pages e Intranet Corporativa sin Servidores</h2>
    <p>Al sincronizar tu carpeta con GitLab, el pipeline <code>.gitlab-ci.yml</code> toma automáticamente tus dashboards e informes HTML y los publica en una dirección web privada de tu empresa (<strong>GitLab Pages</strong>). Esto permite que tus directores o tu equipo puedan consultar el estado del proyecto en tiempo real desde cualquier dispositivo simplemente abriendo un enlace web seguro, sin necesidad de configurar servidores ni pagar licencias extra.</p>

    <h2 id="f3-8">3.8 Skills Reutilizables en Copilot (.github/prompts/): Atajos con «/» para Consultoría</h2>
    <p>Para evitar la fatiga de escribir prompts largos cada vez que inicias un informe o auditas un documento, y para no olvidar restricciones clave (<em>Drift</em>), Copilot en VS Code permite guardar <strong>Skills reutilizables</strong> como archivos de plantilla dentro de la carpeta <code>.github/prompts/</code> (por ejemplo, <code>resumen-ejecutivo.prompt.md</code>). Basta con escribir <strong><code>/</code></strong> en el chat de Copilot para invocar al instante toda la metodología:</p>
    <ul>
        <li><strong>Anatomía de 4 Bloques:</strong> Cada atajo define: 1) Rol y Objetivo, 2) Restricciones Negativas (<em>Never Do</em>: cero charla, cero cifras inventadas), 3) Estructura de Entrada (anclada con <code>#file</code> al informe o Excel del cliente) y 4) Formato de Entrega (tabla ejecutiva, resumen de 3 puntos o HTML autónomo).</li>
        <li><strong>Portabilidad en GitLab:</strong> Al ser archivos Markdown normales dentro de la carpeta del proyecto, viajan en GitLab para que todo tu equipo de consultoría trabaje con exactamente los mismos atajos y estándares de calidad.</li>
    </ul>

    <!-- FASE 4 -->
    <div id="fase4" class="phase-header">FASE 4: PUESTA EN MARCHA EN 1 CLIC (PLANTILLA UNIVERSAL CON ROLLBACK)</div>

    <h2 id="f4-1">4.1 La Plantilla Universal de Consultoría (WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip)</h2>
    <p>Hemos empaquetado toda esta arquitectura en un kit descargable de 1 clic para que no tengas que escribir ningún archivo de configuración técnica:</p>
    <div class="kit-box">
        <div class="kit-title">📦 CONTENIDO DEL KIT UNIVERSAL:</div>
        <ul>
            <li><code>.vscode/settings.json</code>: Parámetros de Cero-Submits y confidencialidad precalibrados para consultoría.</li>
            <li><code>.github/copilot-instructions.md</code>: Las directivas maestras de estilo, rigor analítico y cero duplicación.</li>
            <li><code>.gitlab-ci.yml</code>: Automatización para publicar dashboards en GitLab Pages.</li>
            <li><code>desactivar_gobernanza.bat</code>: <strong>El botón de marcha atrás en 1 clic para Windows</strong> (restaura el estado original instantáneamente).</li>
            <li><code>LEEME_PRIMERO.txt</code>: Guía rápida ejecutiva en 3 pasos explicada sin tecnicismos.</li>
        </ul>

        <h3 id="f4-2">4.2 Activación Paso a Paso en tu Portátil Corporativo Windows o Mac</h3>
        <p><strong>• EN WINDOWS CORPORATIVO (3 Pasos):</strong></p>
        <ol>
            <li>Crea una carpeta para tu proyecto o piloto (ej. <code>C:\\Piloto-Consultoria\\</code>) y copia allí el archivo <code>WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip</code>.</li>
            <li>Haz clic derecho sobre el ZIP y pulsa en <em>"Extraer todo..."</em> en esa misma carpeta.</li>
            <li>Abre <strong>VS Code</strong>, ve a <strong>Archivo ➔ Abrir carpeta...</strong> y selecciona esa carpeta.</li>
        </ol>
        <p style="font-weight:700; color:#15803d; margin-top:10px;">🎉 ¡Listo! Ya estás en un entorno de consultoría blindado. Copilot operará de inmediato bajo las reglas de gobernanza sin interferir en tus otros proyectos.</p>
    </div>

    <h2 id="f4-3">4.3 Matriz Comparativa: La Consultoría Tradicional con IA vs. Metodología Gobernada</h2>
    <table>
        <thead>
            <tr>
                <th>Dimensión del Trabajo</th>
                <th>Uso Tradicional de Copilot ('Vibe Coding')</th>
                <th>Con Metodología de Gobernanza y GitLab</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Fiabilidad de los Datos</strong></td>
                <td>Riesgo continuo de cifras inventadas o alucinadas por la IA.</td>
                <td><strong>Trazabilidad Estricta:</strong> La IA se ancla exclusivamente a las fuentes del proyecto.</td>
            </tr>
            <tr>
                <td><strong>Impacto del Entregable</strong></td>
                <td>Documentos de texto estáticos y áridos de difícil lectura.</td>
                <td><strong>Generative UI:</strong> Dashboards HTML interactivos para directores y clientes.</td>
            </tr>
            <tr>
                <td><strong>Seguridad de tu Puesto</strong></td>
                <td>Inseguridad por alterar la configuración global del portátil.</td>
                <td><strong>Aislamiento Local + Marcha Atrás:</strong> Rollback en 5 segundos sin tocar tu sistema.</td>
            </tr>
            <tr>
                <td><strong>Flujo de Trabajo</strong></td>
                <td>Pausas continuas pulsando botones de aceptar en cada párrafo.</td>
                <td><strong>Cero-Submits:</strong> Redacción desatendida y revisión en frío de documentos completos.</td>
            </tr>
            <tr>
                <td><strong>Colaboración en Equipo</strong></td>
                <td>Archivos dispersos por correo electrónico o carpetas compartidas.</td>
                <td><strong>GitLab Inmutable + Pages:</strong> Historial de versiones y web privada instantánea.</td>
            </tr>
        </tbody>
    </table>

    <footer>
        Guía de Gobernanza y Productividad con Copilot & GitLab para Consultores Senior • Marco Metodológico Corporativo
    </footer>
</div>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML generado para consultoría: {HTML_FILE}", flush=True)

def compilar_pdf_reportlab():
    doc = SimpleDocTemplate(
        PDF_FILE,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=34,
        bottomMargin=36
    )
    PAGE_WIDTH = A4[0] - 72

    styles = getSampleStyleSheet()

    c_blue = colors.HexColor('#1E40AF')
    c_dark_blue = colors.HexColor('#1E3A8A')
    c_navy = colors.HexColor('#0F172A')
    c_slate = colors.HexColor('#334155')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15.5,
        textColor=c_navy,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=10,
        textColor=c_slate,
        spaceAfter=3
    )

    phase_style = ParagraphStyle(
        'PhaseStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#FFFFFF'),
        backColor=c_blue,
        borderPadding=3.5,
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark_blue,
        spaceBefore=6,
        spaceAfter=2.5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=c_navy,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=10.2,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.8,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=10,
        spaceAfter=2
    )

    toc_title = ParagraphStyle('TT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_navy, spaceAfter=3)
    toc_phase = ParagraphStyle('TP', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9.5, textColor=c_dark_blue, spaceBefore=1.5)
    toc_sub = ParagraphStyle('TS', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=c_slate, leftIndent=8)

    danger_title = ParagraphStyle('DT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=10, textColor=colors.HexColor('#B91C1C'), spaceAfter=1.5)
    danger_body = ParagraphStyle('DB', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.8, textColor=colors.HexColor('#7F1D1D'))
    sol_title = ParagraphStyle('ST', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=10, textColor=colors.HexColor('#15803D'), spaceAfter=1.5)
    sol_body = ParagraphStyle('SB', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.8, textColor=colors.HexColor('#14532D'), leftIndent=6, spaceAfter=1.5)

    rollback_title = ParagraphStyle('RT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=10, textColor=colors.HexColor('#B45309'), spaceAfter=1.5)
    rollback_body = ParagraphStyle('RB', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.8, textColor=colors.HexColor('#78350F'))

    feat_title = ParagraphStyle('FT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8, leading=10.5, textColor=c_dark_blue, spaceAfter=2)
    feat_body = ParagraphStyle('FB', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.8, textColor=colors.HexColor('#0F172A'), spaceAfter=2.5)

    param_title = ParagraphStyle('PT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8, leading=10.5, textColor=colors.HexColor('#0F172A'), spaceAfter=1.5)
    param_body = ParagraphStyle('PB', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.8, textColor=colors.HexColor('#334155'), spaceAfter=1.5)

    table_header = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=9, textColor=c_navy)
    table_cell = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8.8, textColor=colors.HexColor('#334155'))
    table_cell_bold = ParagraphStyle('TCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.8, textColor=c_navy)

    story = []

    # PAGE 1: PORTADA, CONTROL DE VERSIONES Y CABECERA
    story.append(Paragraph("Guía de Arquitectura, Parametrización y Gobernanza en Copilot & GitLab", title_style))
    story.append(Paragraph("<b>Manual Maestro de Productividad y Control de IA para Consultores y Profesionales Senior (+65)</b><br/>Cómo dirigir a Copilot sobre repositorios corporativos en GitLab, generar entregables de alto impacto, blindar la confidencialidad y operar sin alterar el entorno habitual del ordenador de la empresa.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_blue, spaceBefore=0, spaceAfter=4))

    # TABLA DE CONTROL DE VERSIONES (TOP OF PAGE 1)
    ver_header = ParagraphStyle('VH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=c_navy)
    ver_cell = ParagraphStyle('VC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.2, leading=8.2, textColor=colors.HexColor('#334155'))
    ver_cell_bold = ParagraphStyle('VCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.2, leading=8.2, textColor=c_blue)

    t_version_data = [
        [Paragraph("Versión", ver_header), Paragraph("Fecha", ver_header), Paragraph("Responsable", ver_header), Paragraph("Descripción Detallada del Cambio y Alcance de la Versión", ver_header)],
        [Paragraph("<b>v1.0</b>", ver_cell_bold), Paragraph("25/11/2026", ver_cell), Paragraph("Marco Gobernanza IA", ver_cell), Paragraph("<b>Edición Inicial Oficial Entregada:</b> Adaptación íntegra para Consultoría Senior (+65). Aislamiento total en carpeta local (<code>.vscode/settings.json</code>) sin tocar TI en <code>AppData</code>; desmitificación de la ruta <code>.github</code> en GitLab; entorno de pruebas (Sandbox); script de marcha atrás en 5 seg (<code>desactivar_gobernanza.bat</code>); mitigación de las 4 D; GitLab Pages; y Skills reutilizables con «/» (<code>.github/prompts/</code>).<br/>🌐 <b>Versión viva online siempre actualizada:</b> <a href=\"https://javiercursocorreo-gif.github.io/adaptacion-copilot/ARQUITECTURA_Y_SOLUCIONES_COPILOT_GITLAB.html\" color=\"#1d4ed8\"><u><b>https://javiercursocorreo-gif.github.io/adaptacion-copilot ↗</b></u></a>", ver_cell)]
    ]
    t_version = Table(t_version_data, colWidths=[45, 60, 95, 323.27])
    t_version.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_version)
    story.append(Spacer(1, 4))

    # CITA
    p_quote = [
        Paragraph("«En consultoría estratégica y de negocio, la inteligencia artificial no sustituye al criterio del consultor: acelera la redacción de informes y el análisis de datos. El verdadero peligro es perder el gobierno sobre las fuentes, los números y los entregables. La redacción se apoya en la IA; el rigor metodológico, la confidencialidad y la verificación final jamás.»<br/><b>— Marco de Gobernanza en IA para Consultoría Senior</b>", ParagraphStyle('QC', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.2, leading=9.8, textColor=colors.HexColor('#334155')))
    ]
    t_quote = Table([[p_quote]], colWidths=[PAGE_WIDTH])
    t_quote.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_quote)
    story.append(Spacer(1, 4))

    # TOC
    p_toc = [
        Paragraph("<b>ÍNDICE GENERAL DE FASES Y PROTOCOLOS</b>", toc_title),
        Paragraph("<b>FASE 0: EL ENTORNO DE CONSULTORÍA (RELACIÓN COPILOT - VS CODE Y SEGURIDAD)</b>", toc_phase),
        Paragraph("0.1 ¿Por qué hablamos de VS Code? La Relación entre Copilot y el Editor de Trabajo", toc_sub),
        Paragraph("0.2 Ajustes Globales vs. Locales: La Garantía de que tu Puesto de Trabajo NO se Desconfigura", toc_sub),
        Paragraph("0.3 ¿Por qué aparece una carpeta llamada .github si usamos GitLab?", toc_sub),
        Paragraph("0.4 Entorno de Pruebas Seguro (Sandbox Piloto): Cómo Experimentar sin Tocar tu Día a Día", toc_sub),
        Paragraph("0.5 Tabla Comparativa de Parametrización Exhaustiva en settings.json", toc_sub),
        Paragraph("0.6 El Protocolo de Marcha Atrás (Rollback en 5 Segundos para Dejar Todo como Estaba)", toc_sub),
        Spacer(1, 1.5),
        Paragraph("<b>FASE 1: FUNDAMENTOS Y GESTIÓN DE RIESGOS EN CONSULTORÍA</b>", toc_phase),
        Paragraph("1.1 De la Ilusión del 'Vibe Coding' a la Consultoría Rigurosa con IA", toc_sub),
        Paragraph("1.2 Las 4 D del Riesgo de la IA en Informes Corporativos (Duplicación, Drift, Deluge, Deception)", toc_sub),
        Paragraph("1.3 Arquitectura de Carpeta Raíz: Organización Limpia de Documentos y Entregables", toc_sub),
        Spacer(1, 1.5),
        Paragraph("<b>FASE 2: EL MOTOR DE COPILOT Y DIRECTIVAS DE TRABAJO</b>", toc_phase),
        Paragraph("2.1 Selección de Modelos para Consultoría (Claude 3.5 Sonnet para Informes vs. GPT-4o para Datos)", toc_sub),
        Paragraph("2.2 Modificadores de Enfoque: Cómo dar Contexto a la IA sin Copiar y Pegar", toc_sub),
        Paragraph("2.3 Las 6 Políticas Maestras de Parametrización en el Trabajo Diario", toc_sub),
        Spacer(1, 1.5),
        Paragraph("<b>FASE 3: PROTOCOLOS DE GOBERNANZA (.copilot-instructions.md)</b>", toc_phase),
        Paragraph("3.1 Cero Interrupciones (Cero-Submits): Trabajo Desatendido sin Ventanas de Aprobación", toc_sub),
        Paragraph("3.2 El Método de las 3 Preguntas Clave: ¿Cuándo, Cómo y Por Qué Trabajar en Silencio?", toc_sub),
        Paragraph("3.3 Protocolo Cognitivo Elephant-Goldfish: Memoria del Proyecto vs. Revisiones Aisladas", toc_sub),
        Paragraph("3.4 Trazabilidad de Versiones y Control de Entregables ([COMANDO XX])", toc_sub),
        Paragraph("3.5 Cero Trozos de Código Sueltos: Entrega de Soluciones Completas y Autónomas", toc_sub),
        Paragraph("3.6 Dashboards Ejecutivos Interactivos en HTML (Generative UI para Clientes y Directores)", toc_sub),
        Paragraph("3.7 Publicación Automática en GitLab Pages e Intranet Corporativa sin Servidores", toc_sub),
        Paragraph("3.8 Skills Reutilizables en Copilot (.github/prompts/): Atajos con «/» para Consultoría", toc_sub),
        Spacer(1, 1.5),
        Paragraph("<b>FASE 4: PUESTA EN MARCHA EN 1 CLIC (PLANTILLA UNIVERSAL CON ROLLBACK)</b>", toc_phase),
        Paragraph("4.1 La Plantilla Universal de Consultoría (WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip)", toc_sub),
        Paragraph("4.2 Activación Paso a Paso en tu Portátil Corporativo Windows o Mac", toc_sub),
        Paragraph("4.3 Matriz Comparativa: La Consultoría Tradicional con IA vs. Metodología Gobernada", toc_sub)
    ]
    t_toc = Table([[p_toc]], colWidths=[PAGE_WIDTH])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 6))

    # FASE 0: EL ENTORNO DE CONSULTORÍA
    story.append(Paragraph("FASE 0: EL ENTORNO DE CONSULTORÍA (RELACIÓN COPILOT - VS CODE Y SEGURIDAD)", phase_style))
    story.append(Paragraph("0.1 ¿Por qué hablamos de VS Code? La Relación entre Copilot y el Editor de Trabajo", h1_style))
    story.append(Paragraph("Copilot no es un programa cerrado con ventana propia que se abra como Word o Excel: es un <b>motor inteligente (un copiloto invisible)</b> que necesita integrarse dentro de un entorno de trabajo. <b>Visual Studio Code (VS Code) es el 'vehículo' oficial de Microsoft donde reside Copilot</b>, permitiendo consultar los documentos del proyecto, abrir el panel lateral de conversación y modificar archivos en tiempo real. Además, <b>Google Antigravity IDE está construido exactamente sobre el mismo motor de código abierto de Microsoft VS Code (Code-OSS)</b>: comparten los mismos atajos, el árbol de archivos lateral y la arquitectura de <code>settings.json</code>. Lo que aprendes en uno funciona directamente en el otro.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("0.2 Ajustes Globales vs. Locales: La Garantía de que tu Puesto de Trabajo NO se Desconfigura", h1_style))
    story.append(Paragraph("En el ordenador de la empresa, el departamento de TI ya tiene configuradas directivas corporativas. Es esencial saber que <b>nuestra metodología NUNCA toca los Ajustes Globales del sistema (User Settings en AppData de Windows)</b>. Todos los parámetros se aplican única y exclusivamente a nivel de carpeta local (Workspace Settings en <code>.vscode/settings.json</code>). Al cerrar la carpeta del proyecto y abrir tu trabajo habitual, VS Code vuelve al 100% a su estado estándar corporativo sin dejar ningún rastro.", body_style))

    p_rec = [
        Paragraph("🛡️ <b>Garantía de Integridad Corporativa:</b> Tu configuración global de la empresa queda totalmente protegida e inalterada. Las reglas de gobernanza solo tienen efecto mientras mantengas abierta la carpeta de trabajo específica.", sol_body)
    ]
    t_rec = Table([[p_rec]], colWidths=[PAGE_WIDTH])
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#4ADE80')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 4))
    story.append(PageBreak())

    # PAGE 2: .GITHUB, SANDBOX, TABLA, ROLLBACK Y FASE 1
    story.append(Paragraph("0.3 ¿Por qué aparece una carpeta llamada .github si usamos GitLab?", h1_style))
    story.append(Paragraph("Como la extensión fue desarrollada por el equipo de GitHub (Microsoft), sus programadores fijaron en el código interno de VS Code que el archivo donde se leen las instrucciones obligatorias debe llamarse por defecto <code>.github/copilot-instructions.md</code> en el disco local. <b>Es únicamente un nombre de carpeta en tu disco duro</b>: no conecta con internet ni sube datos a GitHub. Cuando sincronices tu trabajo con GitLab, esa carpetita viaja y se almacena en el servidor privado de GitLab de tu empresa exactamente igual que cualquier otra carpeta de informes.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("0.4 Entorno de Pruebas Seguro (Sandbox Piloto): Cómo Experimentar sin Tocar tu Día a Día", h1_style))
    story.append(Paragraph("Para experimentar con total tranquilidad, el consultor no debe tocar sus carpetas habituales. Se recomienda crear una carpeta de laboratorio dedicada (ej. <code>C:\\Piloto-Consultoria\\</code>) o utilizar los <b>Perfiles Nativos de VS Code (Profiles)</b> desde el icono de engranaje (abajo a la izquierda) ➔ <i>Profiles ➔ Create Profile</i>, creando una burbuja virtual independiente que se puede eliminar con un solo clic al terminar las pruebas.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("0.5 Tabla Comparativa de Parametrización en settings.json", h1_style))
    table_inst_data = [
        [Paragraph("Parámetro en settings.json", table_header), Paragraph("Valor Recomendado", table_header), Paragraph("Justificación Técnica y Beneficio en Consultoría", table_header)],
        [Paragraph("<code>chat.editing.autoAcceptDelay</code>", table_cell_bold), Paragraph("<code>0</code>", table_cell), Paragraph("<b>Cero-Submits:</b> Aplica ediciones de informes de forma desatendida sin confirmar línea a línea.", table_cell)],
        [Paragraph("<code>terminal.integrated.allowChaining</code>", table_cell_bold), Paragraph("<code>true</code>", table_cell), Paragraph("Permite ejecutar secuencias de comprobación y subida a GitLab sin pausas ni interrupciones.", table_cell)],
        [Paragraph("<code>chat.projectContext.enabled</code>", table_cell_bold), Paragraph("<code>true</code>", table_cell), Paragraph("Habilita la indexación local para que <code>@workspace</code> reconozca todos los documentos del cliente.", table_cell)],
        [Paragraph("<code>debug.filterGitIgnored</code>", table_cell_bold), Paragraph("<code>true</code>", table_cell), Paragraph("<b>Blindaje de Confidencialidad:</b> Impide que Copilot lea archivos protegidos en <code>.gitignore</code>.", table_cell)],
        [Paragraph("<code>telemetry.telemetryLevel</code>", table_cell_bold), Paragraph("<code>\"off\"</code>", table_cell), Paragraph("Desactiva telemetría hacia el exterior cumpliendo el secreto profesional y normativas GDPR.", table_cell)],
        [Paragraph("<code>files.watcherExclude</code>", table_cell_bold), Paragraph("Exclusiones masivas", table_cell), Paragraph("Optimiza la memoria del portátil corporativo ignorando carpetas de sistema pesadas y cachés.", table_cell)]
    ]
    t_inst = Table(table_inst_data, colWidths=[120, 85, 318.27])
    t_inst.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_inst)
    story.append(Spacer(1, 3))

    story.append(Paragraph("0.6 El Protocolo de Marcha Atrás (Rollback en 5 Segundos para Dejar Todo como Estaba)", h1_style))
    p_rb = [
        Paragraph("⏪ <b>PROTOCOLO DE DESACTIVACIÓN Y MARCHA ATRÁS (ROLLBACK):</b>", rollback_title),
        Paragraph("Toda la configuración reside exclusivamente en dos subcarpetas dentro del proyecto: <code>.vscode/</code> (parámetros locales) y <code>.github/</code> o <code>.gitlab/</code> (reglas de gobernanza). Si deseas revertir todo en cualquier momento, basta con borrar esas dos carpetas (o hacer doble clic en el archivo <code>desactivar_gobernanza.bat</code> incluido en el kit). En ese mismo instante, el proyecto vuelve a ser 100% estándar sin dejar ninguna modificación residual.", rollback_body)
    ]
    t_rb = Table([[p_rb]], colWidths=[PAGE_WIDTH])
    t_rb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBEB')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rb)
    story.append(Spacer(1, 5))

    # FASE 1: FUNDAMENTOS Y GESTIÓN DE RIESGOS EN CONSULTORÍA
    story.append(Paragraph("FASE 1: FUNDAMENTOS Y GESTIÓN DE RIESGOS EN CONSULTORÍA", phase_style))
    story.append(Paragraph("1.1 De la Ilusión del 'Vibe Coding' a la Consultoría Rigurosa con IA", h1_style))
    story.append(Paragraph("El llamado <i>'Vibe Coding'</i> (charlar informalmente con la IA aceptando sus respuestas sin contrastar) es inaceptable en consultoría de negocio, estrategia o auditoría. La IA genera respuestas estadísticamente verosímiles pero no necesariamente ciertas: puede inventar datos de mercado, citar leyes derogadas o sugerir soluciones inviables. Nuestro modelo de <strong>Gobernanza</strong> asegura que el consultor senior retenga el 100% del control sobre las fuentes, el alcance y los entregables finales.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("1.2 Las 4 D del Riesgo de la IA en Informes Corporativos (Duplicación, Drift, Deluge, Deception)", h1_style))

    def make_detailed_4d_box(num_str, title_str, danger_text, sol_bullets):
        p_danger = [
            Paragraph(f"⚠️ {num_str} RIESGO DE LA IA: {title_str.upper()}", danger_title),
            Paragraph(danger_text, danger_body)
        ]
        t_danger = Table([[p_danger]], colWidths=[PAGE_WIDTH])
        t_danger.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#F87171")),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))

        p_sol = [Paragraph("🛡️ NUESTRAS SOLUCIONES DE GOBERNANZA EN CONSULTORÍA:", sol_title)]
        for b in sol_bullets:
            p_sol.append(Paragraph(f"• {b}", sol_body))
        t_sol = Table([[p_sol]], colWidths=[PAGE_WIDTH])
        t_sol.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#4ADE80")),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        return KeepTogether([t_danger, Spacer(1, 1.5), t_sol, Spacer(1, 3.5)])

    story.append(make_detailed_4d_box(
        "1.", "DUPLICACIÓN (Reinvención de Metodologías ya Existentes)",
        "Al redactar una propuesta o diagnóstico, la IA tiende por impulso a crear marcos de trabajo o glosarios inventados cuando la firma de consultoría ya dispone de metodologías estándar homologadas. Esto confunde al cliente y fragmenta la coherencia del equipo.",
        [
            "<b>Manual Metodológico Centralizado:</b> Conservar las plantillas y metodologías oficiales en la raíz del repositorio para que la IA las reutilice obligatoriamente.",
            "<b>Inyección de Contexto con #file:</b> Forzar a Copilot a comprobar las directrices existentes (ej. <code>#file:metodologia_oficial.md</code>) antes de redactar.",
            "<b>Reutilización Estándar:</b> Prohibir la invención de terminología redundante o formatos divergentes."
        ]
    ))

    story.append(make_detailed_4d_box(
        "2.", "DRIFT (Desviación del Alcance del Proyecto)",
        "A medida que la conversación en el chat se alarga, la IA sufre fatiga de contexto: olvida los objetivos del pliego técnico y empieza a proponer iniciativas que exceden el presupuesto o el alcance pactado con el cliente.",
        [
            "<b>Protocolo Elephant-Goldfish:</b> El consultor (Elefante) mantiene la visión estratégica; las revisiones específicas se ejecutan en conversaciones limpias (Goldfish) que se cierran al concluir.",
            "<b>Documento de Alcance Inmutable:</b> Definición clara de límites en <code>ALCANCE_PROYECTO.md</code>, blindando las directivas contra el olvido del modelo.",
            "<b>Trazabilidad de Hitos:</b> Registro correlativo de cada avance para evitar desvíos del calendario de entregables."
        ]
    ))
    story.append(PageBreak())

    # PAGE 3: D3, D4, CARPETA RAÍZ Y FASE 2
    story.append(make_detailed_4d_box(
        "3.", "DELUGE (Diluvio de Palabrería y 'Paja' Documental)",
        "Los modelos generativos tienden a rellenar páginas con prosa grandilocuente pero vacía de contenido práctico. Un informe de 80 páginas que no aporta soluciones ejecutivas concretas deteriora la reputación del consultor.",
        [
            "<b>Regla de Síntesis Ejecutiva:</b> Obligación estricta de estructurar la información en tablas comparativas, matrices DAFO y cuadros de mando.",
            "<b>Planes de Acción Cuantificados:</b> Exigir siempre responsables, plazos e indicadores clave de rendimiento (KPIs) en cada propuesta.",
            "<b>Visualización Autónoma Directa:</b> Sustituir memorias farragosas por resúmenes ejecutivos y dashboards interactivos de 1 página."
        ]
    ))

    story.append(make_detailed_4d_box(
        "4.", "DECEPTION (Datos Inventados y Alucinaciones Estadísticas)",
        "El informe luce visualmente impecable y elegante, pero internamente incluye porcentajes de mercado inventados, artículos de ley inexistentes o gráficos con datos falsos que no resisten una reunión con el comité de dirección del cliente.",
        [
            "<b>Obligación de Trazabilidad de Fuentes:</b> Prohibido admitir datos o cifras que no provengan de los documentos fuente aportados por el consultor.",
            "<b>Verificación de Hechos y Poda Temprana:</b> Si una cifra o dato estadístico no puede ser contrastado documentalmente, se elimina de raíz.",
            "<b>Copias de Respaldo Garantizadas en GitLab:</b> Todo informe validado se archiva en el repositorio remoto para consulta del equipo."
        ]
    ))

    story.append(Paragraph("1.3 Arquitectura de Carpeta Raíz: Organización Limpia de Documentos y Entregables", h1_style))
    story.append(Paragraph("Para que Copilot entienda la totalidad del encargo de consultoría, todo el material del proyecto (antecedentes, actas de reuniones, pliegos, datos y borradores) debe colgar de un <b>único directorio raíz en tu disco local</b>. Al abrir esa carpeta con <code>code .</code>, <b>Copilot tiene visión 360º de toda la documentación del cliente</b>, indexando antecedentes y requerimientos sin perderse en carpetas ajenas ni disparar alertas de permisos.", body_style))
    story.append(Spacer(1, 6))

    # FASE 2: MOTOR DE COPILOT Y DIRECTIVAS DE TRABAJO
    story.append(Paragraph("FASE 2: EL MOTOR DE COPILOT Y DIRECTIVAS DE TRABAJO", phase_style))
    story.append(Paragraph("2.1 Selección de Modelos para Consultoría (Claude 3.5 Sonnet para Informes vs. GPT-4o para Datos)", h1_style))
    story.append(Paragraph("En la barra superior de Copilot Chat, el consultor puede seleccionar el motor según el tipo de entregable: <b>Claude 3.5 Sonnet (NUESTRO ESTÁNDAR PARA REDACCIÓN EJECUTIVA)</b> destaca por su máxima precisión conceptual, excelente tono formal y nula propensión a alucinar datos en informes estratégicos y diagnósticos; mientras que <b>GPT-4o</b> sobresale por su velocidad para transformar tablas, procesar listados y extraer resúmenes de actas. A diferencia de entornos con enjambres paralelos (<code>/swarm</code>), Copilot opera mediante un <b>único agente asistente</b> sobre la carpeta abierta, ofreciendo control directo y predecible.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("2.2 Modificadores de Enfoque: Cómo dar Contexto a la IA sin Copiar y Pegar", h1_style))
    story.append(Paragraph("El consultor senior no debe perder tiempo copiando y pegando fragmentos en el chat. En su lugar, utiliza modificadores directos de VS Code: <code>#file:acta_reunion.md</code> para inyectar los requerimientos literales del cliente; <code>#selection</code> para afinar un párrafo específico del borrador con el ratón; y <code>@workspace</code> para preguntas globales sobre toda la documentación del proyecto.", body_style))
    story.append(Spacer(1, 2.5))

    story.append(Paragraph("2.3 Las 6 Políticas Maestras de Parametrización en el Trabajo Diario", h1_style))

    def make_param_card(num_str, title_str, text_str):
        p_card = [
            Paragraph(f"⚙️ <b>{num_str} {title_str}</b>", param_title),
            Paragraph(text_str, param_body)
        ]
        t_card = Table([[p_card]], colWidths=[PAGE_WIDTH])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        return KeepTogether([t_card, Spacer(1, 2)])

    story.append(make_param_card(
        "Política 1:", "Edición Directa de Documentos (chat.editing.autoAcceptDelay: 0)",
        "Permite que la IA actualice los borradores de tus informes y tablas directamente en el disco sin obligarte a confirmar palabra por palabra. El control se mantiene revisando el documento completo con calma en pantalla."
    ))

    story.append(make_param_card(
        "Política 2:", "Confidencialidad Blindada (debug.filterGitIgnored: true)",
        "Garantiza que Copilot jamás indexe ni envíe a servidores externos archivos confidenciales de clientes, datos personales o información financiera protegida por directivas corporativas."
    ))

    story.append(make_param_card(
        "Política 3:", "Telemetría Desactivada (telemetry: 'off')",
        "Desactiva el envío de diagnósticos hacia el exterior, garantizando el cumplimiento riguroso de las cláusulas de confidencialidad y secreto profesional de la consultora."
    ))

    story.append(make_param_card(
        "Política 4:", "Enfoque Documental Limpio (files.watcherExclude)",
        "Optimiza la memoria del ordenador excluyendo carpetas de sistema y cachés, centrando la atención de la IA exclusivamente en informes (Markdown, Word, PDF, HTML)."
    ))

    story.append(make_param_card(
        "Política 5:", "Modelo de Redacción Calibrado",
        "Asignación prioritaria de Claude 3.5 Sonnet para garantizar una prosa ejecutiva sobria, libre de coloquialismos y adaptada a comités de dirección."
    ))

    story.append(make_param_card(
        "Política 6:", "Prevalencia de las Reglas (.copilot-instructions.md)",
        "Las directrices del manual de estilo de tu empresa tienen prioridad absoluta sobre cualquier sugerencia que la IA formule en el chat."
    ))
    story.append(PageBreak())

    # PAGE 4: FASE 3 PROTOCOLOS DE GOBERNANZA
    story.append(Paragraph("FASE 3: PROTOCOLOS DE GOBERNANZA (.copilot-instructions.md)", phase_style))
    story.append(Paragraph("3.1 Cero Interrupciones (Cero-Submits): Trabajo Desatendido sin Ventanas de Aprobación", h1_style))
    story.append(Paragraph("En el flujo de trabajo moderno queda prohibido el uso de ventanas emergentes de confirmación interactiva. Si solicitas actualizar la sección de conclusiones de un informe, la IA debe reescribir la sección directamente en el archivo y guardar el cambio. El consultor revisa el resultado completo con calma en pantalla, eliminando la fatiga de clics y las pausas continuas.", body_style))

    story.append(Paragraph("3.2 El Método de las 3 Preguntas Clave: ¿Cuándo, Cómo y Por Qué Trabajar en Silencio?", h1_style))
    story.append(Paragraph("Uno de los mayores hallazgos metodológicos de nuestro ecosistema es la articulación del <b>flujo de trabajo 100% desatendido</b>: el asistente realiza todo el esfuerzo técnico de forma silenciosa e invisible y, únicamente al concluir con éxito, entrega el resultado completo.", body_style))

    p_feat_silence = [
        Paragraph("<b>¿EN QUÉ MOMENTO SE USA, CÓMO OPERA Y POR QUÉ SE DISEÑÓ ESTA METODOLOGÍA?</b>", feat_title),
        Spacer(1, 2),
        Paragraph("<b>1. ¿En qué momento se usa?</b> En toda sesión de redacción, estructuración de informes, análisis de pliegos, preparación de propuestas y dashboards ejecutivos.", feat_body),
        Paragraph("<b>2. ¿Cómo lo usamos? (Mecánica de Trabajo):</b> El consultor plantea la solicitud en lenguaje de negocio (ej. <i>'Elabora la matriz de riesgos a partir de las entrevistas'</i>). La IA trabaja en silencio absoluto (sin saludos ni preámbulos vacíos), actualiza el documento final y, al terminar, entrega un reporte claro de lo modificado con su resumen ejecutivo.", feat_body),
        Paragraph("<b>3. ¿Por qué lo usamos? (Beneficios de Control y Productividad):</b>", feat_body),
        Paragraph("• <i>Eliminación Total de Ruido:</i> Se suprime la charla intrascendente de la IA para centrarse en la calidad del entregable.", feat_body),
        Paragraph("• <i>Soberanía del Consultor:</i> El consultor valida en frío si el documento responde a la estrategia del cliente antes de presentarlo.", feat_body),
        Paragraph("• <i>Trazabilidad Cronológica Limpia:</i> Cada versión queda registrada y vinculada a la bitácora del proyecto de consultoría.", feat_body)
    ]
    t_feat_silence = Table([[p_feat_silence]], colWidths=[PAGE_WIDTH])
    t_feat_silence.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([t_feat_silence, Spacer(1, 4)]))

    story.append(Paragraph("3.3 Protocolo Cognitivo Elephant-Goldfish: Memoria del Proyecto vs. Revisiones Aisladas", h1_style))
    story.append(Paragraph("El consultor actúa como el <b>Elefante</b>: conserva la memoria de las reuniones, la relación con el cliente y los objetivos estratégicos. Para tareas analíticas intensas (ej. auditar si un informe de 50 páginas tiene incoherencias de fechas), se abre una subsesión limpia (<b>Goldfish</b>) que revisa el texto con mente fresca y se cierra tras emitir su dictamen, sin saturar la conversación principal.", body_style))

    story.append(Paragraph("3.4 Trazabilidad de Versiones y Control de Entregables ([COMANDO XX])", h1_style))
    story.append(Paragraph("Cada avance significativo se asocia a un identificador secuencial (ej. <code>[VERSIÓN 04: PLAN DE ACCIÓN]</code>) registrado en GitLab. Si el cliente solicita comparar la versión de hace dos semanas con la actual, el consultor puede rastrear con exactitud qué párrafos cambiaron y bajo qué requerimiento.", body_style))

    story.append(Paragraph("3.5 Cero Trozos de Código Sueltos: Entrega de Soluciones Completas y Autónomas", h1_style))
    story.append(Paragraph("Un consultor no debe manipular código ni parches manuales ('copia esto en la línea 45'). Todo lo entregado por la IA debe ser <b>un producto terminado y autónomo</b>: documentos completos en Markdown/Word listos para exportar a PDF, o micro-aplicaciones HTML autónomas que abren con un doble clic en cualquier ordenador o tablet sin servidores intermedios.", body_style))

    story.append(Paragraph("3.6 Dashboards Ejecutivos Interactivos en HTML (Generative UI para Clientes y Directores)", h1_style))
    story.append(Paragraph("En lugar de presentar memorias áridas de 80 páginas que nadie lee, la IA compila <b>Cuadros de Mando Interactivos (HTML)</b> en un único archivo con diseño corporativo elegante: filtros por departamento, matrices de riesgo clicables (rojo / amarillo / verde) y cronogramas visuales que causan un impacto profesional extraordinario en comités de dirección, realizando siempre una <b>auto-auditoría previa</b> de enlaces y coherencia antes de entregar.", body_style))

    story.append(Paragraph("3.7 Publicación Automática en GitLab Pages e Intranet Corporativa sin Servidores", h1_style))
    story.append(Paragraph("Al sincronizar tu carpeta con GitLab, el pipeline <code>.gitlab-ci.yml</code> toma automáticamente tus dashboards e informes HTML y los publica en una dirección web privada de tu empresa (<b>GitLab Pages</b>), accesible desde cualquier dispositivo para tus directivos y equipo sin necesidad de configurar servidores web manuales ni pagar licencias extra.", body_style))

    story.append(Paragraph("3.8 Skills Reutilizables en Copilot (.github/prompts/): Atajos con «/» para Consultoría", h1_style))
    story.append(Paragraph("Para no reescribir prompts largos ni olvidar restricciones clave (<i>Drift</i>), Copilot en VS Code permite guardar <b>Skills reutilizables</b> en <code>.github/prompts/*.prompt.md</code> (ej. <code>resumen-ejecutivo.prompt.md</code>) e invocarlos al instante escribiendo <b><code>/</code></b> en el chat. Cada atajo sigue la estructura de 4 bloques (<b>Rol</b>, <b>Restricciones Negativas <i>Never Do</i></b>, <b>Entrada con <code>#file</code></b> y <b>Formato de Entrega</b>) y viaja dentro de GitLab para que todo el equipo de consultoría comparta los mismos estándares.", body_style))
    story.append(PageBreak())

    # PAGE 5: FASE 4 PUESTA EN MARCHA Y MATRIZ
    story.append(Paragraph("FASE 4: PUESTA EN MARCHA EN 1 CLIC (PLANTILLA UNIVERSAL CON ROLLBACK)", phase_style))

    p_kit_intro = [
        Paragraph("🟢 <b>MÉTODO OFICIAL Y UNIVERSAL PARA CONSULTORÍA CORPORATIVA</b>", ParagraphStyle('UKIT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#16A34A'))),
        Paragraph("<b>4.1 La Plantilla Universal de Consultoría (WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip)</b>", h2_style),
        Paragraph("Para empezar en cualquier ordenador corporativo (Windows o Mac) sin complicaciones técnicas, hemos empaquetado toda la arquitectura en el archivo comprimido: <a href=\"https://javiercursocorreo-gif.github.io/adaptacion-copilot/WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip\" color=\"#1d4ed8\"><u><b>WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip (Clic para Descargar) ↗</b></u></a>.<br/>Este paquete <b>ya incluye todo configurado por dentro</b>: la carpeta <code>.vscode/settings.json</code> precalibrada, las reglas de gobernanza en <code>.github/copilot-instructions.md</code>, el pipeline <code>.gitlab-ci.yml</code> para GitLab Pages, el script de marcha atrás <code>desactivar_gobernanza.bat</code> y la guía rápida <code>LEEME_PRIMERO.txt</code>.", feat_body),
        Spacer(1, 2),
        Paragraph("<b>4.2 Activación Paso a Paso en tu Portátil Corporativo Windows o Mac</b>", h2_style),
        Spacer(1, 1),
        Paragraph("<b>• EN WINDOWS CORPORATIVO (3 Pasos):</b>", ParagraphStyle('W1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=10.5, textColor=colors.HexColor('#15803D'))),
        Paragraph("<b>Paso 1:</b> Crea una carpeta para tu proyecto o piloto (ej. <code>C:\\Piloto-Consultoria\\</code>) y copia allí el archivo <code>WORKSPACE-COPILOT-GITLAB-PLANTILLA.zip</code>.", bullet_style),
        Paragraph("<b>Paso 2:</b> Haz clic derecho sobre el archivo ZIP y pulsa en <i>'Extraer todo...'</i> en esa misma carpeta.", bullet_style),
        Paragraph("<b>Paso 3:</b> Abre <b>VS Code</b>, ve a <b>Archivo ➔ Abrir carpeta...</b> y selecciona esa carpeta.", bullet_style),
        Spacer(1, 2),
        Paragraph("<b>• EN MAC CORPORATIVO:</b>", ParagraphStyle('M1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=10.5, textColor=colors.HexColor('#15803D'))),
        Paragraph("<b>Paso 1:</b> Crea tu carpeta de proyecto y descomprime allí el archivo ZIP.", bullet_style),
        Paragraph("<b>Paso 2:</b> Abre <b>VS Code</b> mediante <b>Archivo ➔ Abrir carpeta...</b> seleccionando esa carpeta.", bullet_style),
        Spacer(1, 3),
        Paragraph("🎉 <b>¡Entorno Blindado y Operativo!</b> Copilot detectará automáticamente las reglas de gobernanza sin alterar el resto de tu máquina. Y si en algún momento deseas desactivarlo, basta con hacer doble clic en <code>desactivar_gobernanza.bat</code>.", ParagraphStyle('Done', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.4, leading=10.5, textColor=colors.HexColor('#166534')))
    ]
    t_kit = Table([[p_kit_intro]], colWidths=[PAGE_WIDTH])
    t_kit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#16A34A')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([t_kit, Spacer(1, 5)]))

    # MATRIZ COMPARATIVA
    story.append(Paragraph("4.3 Matriz Comparativa: La Consultoría Tradicional con IA vs. Metodología Gobernada", h1_style))
    table_cat_data = [
        [Paragraph("Dimensión del Trabajo", table_header), Paragraph("Uso Tradicional de Copilot ('Vibe Coding')", table_header), Paragraph("Con Metodología de Gobernanza y GitLab", table_header)],
        [Paragraph("<b>Fiabilidad de Datos</b>", table_cell_bold), Paragraph("Riesgo continuo de cifras inventadas o alucinadas por la IA.", table_cell), Paragraph("<b>Trazabilidad Estricta:</b> La IA se ancla exclusivamente a las fuentes aportadas.", table_cell)],
        [Paragraph("<b>Impacto del Entregable</b>", table_cell_bold), Paragraph("Documentos de texto estáticos y áridos de difícil lectura.", table_cell), Paragraph("<b>Generative UI:</b> Dashboards HTML interactivos para directores y clientes.", table_cell)],
        [Paragraph("<b>Seguridad del Puesto</b>", table_cell_bold), Paragraph("Inseguridad por alterar la configuración global del portátil.", table_cell), Paragraph("<b>Aislamiento + Rollback:</b> Marcha atrás en 5 segundos sin tocar tu sistema.", table_cell)],
        [Paragraph("<b>Flujo de Trabajo</b>", table_cell_bold), Paragraph("Pausas continuas pulsando botones de aceptar en cada párrafo.", table_cell), Paragraph("<b>Cero-Submits:</b> Redacción desatendida y revisión en frío de documentos completos.", table_cell)],
        [Paragraph("<b>Colaboración en Equipo</b>", table_cell_bold), Paragraph("Archivos dispersos por correo electrónico o carpetas compartidas.", table_cell), Paragraph("<b>GitLab Inmutable + Pages:</b> Historial de versiones y web privada instantánea.", table_cell)]
    ]
    t_cat = Table(table_cat_data, colWidths=[115, 185, 223.27])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cat)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ PDF generado para consultoría: {PDF_FILE}", flush=True)

def compilar_docx():
    try:
        cmd = ["textutil", "-convert", "docx", HTML_FILE, "-output", DOCX_FILE]
        subprocess.run(cmd, check=True)
        print(f"✅ DOCX generado: {DOCX_FILE}", flush=True)
    except Exception as e:
        print(f"⚠️ No se pudo compilar DOCX con textutil: {e}", flush=True)

def empaquetar_plantilla_zip():
    temp_dir = os.path.join(BASE_DIR, "TEMP_WORKSPACE_ZIP")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(os.path.join(temp_dir, ".vscode"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, ".github"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, ".gitlab"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "informes"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "fuentes_datos"), exist_ok=True)

    # 1. settings.json
    settings_content = """{
  "chat.editing.autoAcceptDelay": 0,
  "terminal.integrated.allowChaining": true,
  "chat.projectContext.enabled": true,
  "github.copilot.advanced": {
    "debug.filterGitIgnored": true
  },
  "telemetry.telemetryLevel": "off",
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true,
    "**/.venv/**": true,
    "**/dist/**": true,
    "**/build/**": true
  }
}
"""
    with open(os.path.join(temp_dir, ".vscode", "settings.json"), "w", encoding="utf-8") as f:
        f.write(settings_content)

    # 2. copilot-instructions.md
    instructions_content = """# REGLAS DE GOBERNANZA PARA CONSULTORÍA SENIOR (GITHUB COPILOT & GITLAB)

## 1. PROTOCOLO DE CERO-SUBMITS ABSOLUTO
- Aplica las ediciones directamente en los archivos de informes sin solicitar confirmaciones parciales ('Accept', 'Submit').
- El consultor revisa el entregable completo en frío una vez terminado el turno.

## 2. PATRÓN DE TRABAJO EN SILENCIO Y TONO EJECUTIVO
- Cero Charlas ni Explicaciones Innecesarias: Prohibido redactar preámbulos vacíos o comentarios de relleno.
- Tono Formal y Ejecutivo: Prosa sobria, precisa y adaptada a comités de dirección y clientes corporativos.

## 3. MITIGACIÓN DE RIESGOS EN CONSULTORÍA (LAS 4 D)
- Anti-Duplicación: Reutiliza la terminología y marcos metodológicos oficiales del repositorio.
- Anti-Drift: Respeta estrictamente el alcance pactado en los pliegos del proyecto.
- Anti-Deluge: Prioriza tablas comparativas, matrices DAFO y cuadros de mando interactivos sobre memorias farragosas.
- Anti-Deception: Cero datos inventados. Toda cifra o porcentaje debe provenir de las fuentes aportadas por el consultor.

## 4. ENTREGABLES AUTÓNOMOS DE ALTO IMPACTO
- Prohibido entregar fragmentos sueltos de código o instrucciones manuales complejas.
- Entrega informes completos en Markdown/Word o cuadros de mando interactivos en HTML único listos para proyectar en reuniones.
"""
    with open(os.path.join(temp_dir, ".github", "copilot-instructions.md"), "w", encoding="utf-8") as f:
        f.write(instructions_content)
    with open(os.path.join(temp_dir, ".gitlab", "copilot-instructions.md"), "w", encoding="utf-8") as f:
        f.write(instructions_content)

    # 3. .gitlab-ci.yml
    gitlab_ci_content = """# Publicación Automática de Dashboards e Informes en GitLab Pages
pages:
  stage: deploy
  script:
    - mkdir -p public
    - cp -r informes/* public/ 2>/dev/null || true
    - cp *.html public/ 2>/dev/null || true
  artifacts:
    paths:
      - public
  only:
    - main
"""
    with open(os.path.join(temp_dir, ".gitlab-ci.yml"), "w", encoding="utf-8") as f:
        f.write(gitlab_ci_content)

    # 4. desactivar_gobernanza.bat (Botón de Marcha Atrás en Windows)
    bat_content = """@echo off
echo ========================================================
echo === DESACTIVANDO GOBERNANZA PILOTO (MARCHA ATRAS) ===
echo ========================================================
if exist .vscode (
    rename .vscode .vscode_desactivado
    echo [OK] Carpeta .vscode desactivada con exito.
)
if exist .github (
    rename .github .github_desactivado
    echo [OK] Carpeta .github desactivada con exito.
)
if exist .gitlab (
    rename .gitlab .gitlab_desactivado
    echo [OK] Carpeta .gitlab desactivada con exito.
)
echo ========================================================
echo Tu proyecto ha vuelto 100% al modo estandar de Copilot.
echo Puedes reabrir VS Code normalmente.
echo ========================================================
pause
"""
    with open(os.path.join(temp_dir, "desactivar_gobernanza.bat"), "w", encoding="utf-8") as f:
        f.write(bat_content)

    # 5. LEEME_PRIMERO.txt
    leeme_content = """======================================================================
PLANTILLA DE GOBERNANZA EN COPILOT & GITLAB PARA CONSULTORES SENIOR
======================================================================

¡Bienvenido a tu entorno de trabajo seguro con Copilot y GitLab!

INSTRUCCIONES DE ACTIVACIÓN RÁPIDA (3 PASOS):

1. COPIAR Y EXTRAER:
   Crea una carpeta de pruebas en tu disco local (ej. C:\\Piloto-Consultoria\\)
   y descomprime allí el contenido de este archivo ZIP.

2. ABRIR EN VS CODE:
   Abre Visual Studio Code, ve a 'Archivo > Abrir carpeta...' y selecciona
   esa carpeta. VS Code cargará automáticamente los ajustes sin tocar
   tu configuración habitual de la empresa.

3. OPERACIÓN CON LA IA:
   Abre Copilot Chat y pide tus informes ejecutivos, análisis de actas
   o cuadros de mando. Copilot redactará en silencio y con rigor.

----------------------------------------------------------------------
¿CÓMO DAR MARCHA ATRÁS SI DESEAS VOLVER AL MODO NORMAL?
----------------------------------------------------------------------
Haz doble clic en el archivo 'desactivar_gobernanza.bat' dentro de la carpeta
(o borra las subcarpetas .vscode y .github). En 5 segundos todo volverá a ser
un proyecto estándar sin ninguna regla especial.
======================================================================
"""
    with open(os.path.join(temp_dir, "LEEME_PRIMERO.txt"), "w", encoding="utf-8") as f:
        f.write(leeme_content)

    # Crear ZIP
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
    
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, temp_dir)
                zipf.write(abs_path, rel_path)
    
    shutil.rmtree(temp_dir)
    print(f"✅ Plantilla ZIP generada: {ZIP_FILE}", flush=True)

if __name__ == "__main__":
    print("="*70)
    print("🚀 GENERANDO GUÍA MAESTRA PARA CONSULTORÍA SENIOR: COPILOT & GITLAB")
    print("="*70)
    generar_html()
    compilar_pdf_reportlab()
    compilar_docx()
    empaquetar_plantilla_zip()
    print("="*70)
    print("✅ PROCESO COMPLETADO AL 100% EN: " + BASE_DIR)
    print("="*70)
