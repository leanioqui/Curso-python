# 🌍 Sistema de Gestión de Impacto Ambiental

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

![CI Status](https://img.shields.io/github/actions/workflow/status/leanioqui/Curso-python/ci.yml?branch=main&label=CI)
![Install Status](https://img.shields.io/github/actions/workflow/status/leanioqui/Curso-python/ci.yml?branch=main&label=Install&event=push)
![Lint Status](https://img.shields.io/github/actions/workflow/status/leanioqui/Curso-python/ci.yml?branch=main&label=Lint&event=push)
![Format Status](https://img.shields.io/github/actions/workflow/status/leanioqui/Curso-python/ci.yml?branch=main&label=Format&event=push)
![Docs Status](https://img.shields.io/github/actions/workflow/status/leanioqui/Curso-python/ci.yml?branch=main&label=Docs&event=push)

Este proyecto nace como una solución tecnológica diseñada para empresas que necesitan centralizar, registrar y auditar el impacto ambiental de sus actividades operativas. El sistema permite almacenar acciones ambientales, categorizarlas según su naturaleza (Física, Biológica o Socioeconómica) y cuantificar su incidencia de manera sistemática mediante métricas simples y procesables.

El objetivo principal es ofrecer una herramienta intuitiva, educativa y funcional para la gestión de información ambiental utilizando tecnologías modernas del ecosistema Python.

---

# 🚀 Funcionalidades Principales

## 📌 Gestión Integral de Registros (CRUD)

### Interfaz completa para:

- Alta de registros ambientales
- Modificación de datos existentes
- Eliminación de registros
- Consulta y visualización de información almacenada

Toda la información es persistida en una base de datos relacional SQLite.

---

## 🌡️ Datos Ambientales en Tiempo Real

### El sistema implementa técnicas de Web Scraping utilizando `Requests` y `BeautifulSoup` para obtener la temperatura actual de CABA (Ciudad Autónoma de Buenos Aires), proporcionando contexto ambiental dinámico dentro de la aplicación.

---

## 🔐 Validaciones y Seguridad

### Se utilizan expresiones regulares (Regex) para validar entradas del usuario y evitar inconsistencias en los datos almacenados.

### Además, la interfaz incorpora:

- 🌙 Modo Oscuro
- ☀️ Modo Claro

con el objetivo de mejorar la experiencia y ergonomía visual del usuario.

---

## 📊 Análisis Estadístico

### El sistema calcula automáticamente:

- Impacto ambiental total
- Impacto promedio
- Estadísticas generales de los registros

permitiendo identificar rápidamente tendencias e impactos críticos.

---

# 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
| :--- | :--- |
| **Python 3** | Lógica principal del sistema |
| **Tkinter** | Interfaz gráfica |
| **SQLite3** | Persistencia de datos |
| **BeautifulSoup** | Web Scraping |
| **Requests** | Solicitudes HTTP |
| **Regex** | Validaciones |
| **Sphinx** | Documentación técnica |

---

# 📋 Metodología de Medición

### Se implementa un método de lista de chequeo para transformar observaciones cualitativas en datos cuantitativos procesables mediante una escala de ponderación simplificada:

| Valor | Clasificación | Descripción |
| :--- | :--- | :--- |
| **-1** | Impacto Negativo | Actividades que degradan el parámetro ambiental |
| **0** | Impacto Neutro | Actividades sin variaciones significativas |
| **1** | Impacto Positivo | Acciones que favorecen la recuperación o mejora del entorno |

---

# 🧩 Arquitectura del Proyecto

### El sistema fue desarrollado siguiendo una estructura basada en el patrón MVC (Modelo - Vista - Controlador), permitiendo una mejor organización del código y separación de responsabilidades.

Estructura general:

```bash
Curso-python/
│
├── src/
│   ├── controllers/
│   ├── models/
│   ├── views/
│   └── main.py
│
├── para_sphinx/
├── requirements.txt
└── README.md
```

# ⚙️ Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/leanioqui/Curso-python.git
   cd Curso-python
   ```


2. **Crear y activar un entorno virtual:**
   En Windows (CMD o PowerShell)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En Git Bash / Linux / macOS
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```


3. **Instalar dependencias:**
   Con el entorno virtual activo:
   ```bash
   pip install -r requirements.txt
   ```


4. **Ejecutar la aplicación:**
   Debido a la estructura MVC del proyecto, el punto de entrada se encuentra dentro de `src/:`
   ```bash
   python src/main.py
   ```


---

# 📖 Generación de Documentación Técnica

### El proyecto incluye documentación generada con Sphinx.

**Instalar dependencias:**
```bash
python src/main.py
```

**Los archivos HTML generados se encontrarán en:**
```bash
para_sphinx/archivos/docs/_build/html/
```

---

## 👨‍💻 Autores (UTN E-Learning)

* **Franco Gimenez**
* **Fernando Gallego**
* **Leandro Quintela**

---

## 📄 Licencia

## Este proyecto está bajo la Licencia MIT.

---

## 🌱 Objetivo Académico

### Este sistema fue desarrollado como proyecto académico integrador, aplicando conocimientos de:

* **Programación Orientada a Objetos en Python**
* **Bases de datos relacionales**
* **Arquitectura MVC**
* **Interfaces gráficas**
* **Web Scraping**
* **Validaciones de datos**
* **Documentación técnica**

orientados al desarrollo de soluciones tecnológicas aplicadas a la gestión ambiental.
