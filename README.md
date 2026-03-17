# 🌍 Sistema de Gestión de Impacto Ambiental

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Este proyecto nace como una solución integral para empresas que buscan auditar y centralizar el control de su huella ecológica. Mediante una interfaz intuitiva, permite registrar actividades operativas, categorizarlas y cuantificar su impacto ambiental de manera sistemática.

---

## 🚀 Funcionalidades Principales

* **Gestión de Datos (CRUD):** Control total sobre el ciclo de vida de los registros (Altas, Bajas, Modificaciones y Consultas).
* **Análisis Estadístico:** Cálculo automático del impacto ambiental total y promedio para identificar áreas críticas de la operación.
* **Contexto en Tiempo Real:** Integración con servicios meteorológicos mediante Web Scraping para visualizar la temperatura de CABA al momento de la carga.
* **Ergonomía Visual:** Soporte nativo para Modo Claro y Modo Oscuro, adaptándose a las preferencias del usuario.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter
* **Persistencia:** SQLite3
* **Web Scraping:** BeautifulSoup & Requests
* **Validaciones:** Expresiones Regulares (Regex)

---

## 📋 Metodología de Medición

El sistema utiliza una escala de ponderación simplificada para transformar observaciones cualitativas en datos cuantitativos procesables:

| Valor | Clasificación | Descripción |
| :--- | :--- | :--- |
| **-1** | Impacto Negativo | Actividades que degradan el parámetro ambiental. |
| **0** | Impacto Neutro | Actividades sin variaciones significativas. |
| **1** | Impacto Positivo | Acciones que favorecen la recuperación del entorno. |

---

## 👨‍💻 Autores (UTN FRBA)

* **Franco Gimenez**
* **Fernando Gallego**
* **Leandro Quintela**

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
