# 🌍 Sistema de Gestión de Impacto Ambiental

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Este proyecto nace como una solución tecnológica diseñada para empresas que necesitan centralizar y auditar el impacto ambiental de sus actividades operativas. El sistema permite registrar acciones, categorizarlas según su naturaleza (Física, Biológica o Socioeconómica) y cuantificar su incidencia de manera sistemática.

---

## 🚀 Funcionalidades Principales

* **Gestión Integral (CRUD):** Interfaz completa para el alta, baja, modificación y consulta de registros almacenados en una base de datos relacional SQLite.
* **Datos en Tiempo Real:** Uso de técnicas de Web Scraping para capturar la temperatura actual de CABA, brindando un contexto ambiental dinámico.
* **Validación y Seguridad:** Implementación de expresiones regulares (Regex) para el filtrado de entradas y un sistema de Modo Oscuro/Claro para optimizar la ergonomía visual.
* **Análisis Estadístico:** Funciones automáticas para el cálculo del impacto ambiental total y promedio, permitiendo identificar rápidamente áreas críticas de la operación.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Interfaz Gráfica:** Tkinter
* **Persistencia:** SQLite3
* **Web Scraping:** BeautifulSoup & Requests
* **Validaciones:** Expresiones Regulares (Regex)

---

## 📋 Metodología de Medición

Se implementa un método de lista de chequeo para transformar observaciones cualitativas en datos cuantitativos procesables mediante una escala de ponderación simplificada:

| Valor | Clasificación | Descripción |
| :--- | :--- | :--- |
| **-1** | Impacto Negativo | Actividades que degradan el parámetro ambiental. |
| **0** | Impacto Neutro | Actividades sin variaciones significativas. |
| **1** | Impacto Positivo | Acciones que favorecen la recuperación o mejora del entorno. |

---

## ⚙️ Instalación y Ejecución

Para correr este proyecto en tu máquina local, seguí estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/leanioqui/Curso-python.git
   ```

2. **Instalar dependencias:**
   Asegurate de tener Python instalado y ejecutá:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python entrega_final.py
   ```

---

## 👨‍💻 Autores (UTN E-Learning)

* **Franco Gimenez**
* **Fernando Gallego**
* **Leandro Quintela**

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
