# 🚀 Proyecto Apprende

> **Asistente Inteligente para la Gestión y Planificación de Talleres**

Este repositorio aloja el código fuente de una plataforma diseñada para facilitar la creación de talleres educativos. La aplicación utiliza **Inteligencia Artificial** para analizar descripciones de talleres y automatizar la búsqueda de profesores capacitados y materiales necesarios en tiendas reales mediante Web Scraping.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Selenium](https://img.shields.io/badge/Selenium-Automation-yellow)
![OpenAI](https://img.shields.io/badge/AI-OpenAI_API-orange)

---

## 📋 Características Principales

El sistema expone una API REST que ofrece las siguientes funcionalidades:

* **🤖 Análisis con IA:** Utiliza la API de OpenAI (GPT) para extraer palabras clave y listas de materiales a partir de una descripción en lenguaje natural.
* **👨‍🏫 Buscador de Profesores (Scraping):** Busca automáticamente en **Superprof** perfiles relevantes y extrae sus tarifas.
* **🛒 Cotizador de Insumos (Scraping):** Identifica los materiales necesarios y busca precios/disponibilidad en tiempo real en **Lider.cl** y **MercadoLibre**.
* **💾 Historial de Talleres:** Persistencia de datos en archivos CSV para guardar talleres planificados.

---

## 🛠️ Arquitectura y Tecnologías

El proyecto está dividido en Backend (API) y Frontend (Web).

* **Backend:** Python 3.11, FastAPI, Uvicorn.
* **Web Scraping:** Selenium WebDriver (Chrome).
* **Inteligencia Artificial:** OpenAI API (`text-davinci-003`).
* **Base de Datos:** Sistema de archivos CSV (`DB.csv`).
* **Frontend:** HTML5, CSS3 y JavaScript Vanilla.

---

## 📂 Estructura del ProyectoPlaintextproyectoApprende/

```bash
├── API/
│   ├── main.py          # Lógica principal, endpoints y configuración de Selenium
│   └── app.py           # (Archivos auxiliares)
├── web/                 # Frontend simple para consumir la API
├── Modelos/             # Diagramas y documentación de diseño
├── tests/               # Pruebas unitarias y de integración
├── DB.csv               # Base de datos local (generada automáticamente)
└── requirements.txt     # Lista de dependencias Python
```
