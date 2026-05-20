.. Impacto_Ambiental documentation master file, created by
   sphinx-quickstart on Tue May 19 22:43:17 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sistema de Gestión de Impacto Ambiental
=======================================

En esta página encontrarás toda la información relacionada con el código del proyecto Impacto Ambiental, 
incluyendo su estructura, clases, funciones modularizadas y cómo se utilizan dentro del mismo.

Introducción General
====================

Este sistema proporciona una solución tecnológica modular diseñada para centralizar, auditar y cuantificar 
el impacto ambiental de las actividades operativas de una organización. A través de una metodología basada 
en listas de chequeo, el software transforma observaciones cualitativas en datos numéricos, permitiendo 
categorizar cada acción según su naturaleza (Física, Biológica o Socioeconómica).

Ponderación del Impacto
-----------------------

Para evaluar las variaciones (reales o potenciales) en el entorno, se implementa una escala de ponderación 
simplificada de tres niveles:

* **-1 (Impacto Negativo):** Actividades que degradan el parámetro ambiental.
* **0 (Impacto Neutro):** Actividades sin variaciones significativas en el entorno.
* **1 (Impacto Positivo):** Acciones que favorecen la recuperación o mejora del medio ambiente.


.. note::
   El software calcula de forma automática el impacto ambiental total y promedio de las operaciones para 
   facilitar la rápida identificación de áreas críticas.
.. toctree::
   :maxdepth: 4
   :caption: Contenidos:

   main
   controllers
   models
   views
