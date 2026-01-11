# Proyecto Terminal: Denoising de Audio mediante Transformada Rápida de Fourier (FFT)

**Instituto Politécnico Nacional**
**Escuela Superior de Cómputo (ESCOM)**
**Unidad de Aprendizaje:** Matemáticas Avanzadas para la Ingeniería (Grupo 26-1)

---

## 1. Descripción del Proyecto

Este proyecto implementa una herramienta computacional para la reducción de ruido en señales de audio (*Denoising*) operando en el dominio de la frecuencia. La herramienta utiliza la **Transformada Rápida de Fourier (FFT)** para descomponer señales temporales en sus componentes espectrales, aplica filtros selectivos (máscaras ideales) y reconstruye la señal mediante la **Transformada Inversa (IFFT)**.

El sistema incluye módulos para la generación de datos sintéticos controlados, procesamiento digital de señales y una **validación numérica rigurosa** basada en el **Teorema de Parseval**, métricas de error cuadrático medio (MSE) y relación señal a ruido (SNR).

### Objetivos Específicos
* Implementar algoritmos de filtrado Pasa-Bajas, Pasa-Altas, Pasa-Banda y Notch (Rechaza-Banda).
* Validar la conservación de la energía entre los dominios del tiempo y la frecuencia (Teorema de Parseval).
* Proporcionar visualización comparativa de espectrogramas y formas de onda.

---

## 2. Marco Matemático

El núcleo del procesamiento se basa en los siguientes principios matemáticos:

1.  **Transformada Discreta de Fourier (DFT/FFT):**
    Permite transformar la señal discreta $x[n]$ al dominio de la frecuencia $X[k]$.
    
2.  **Filtrado en Frecuencia:**
    Aplicación de una máscara $H[k]$ (vector de ceros y unos) sobre el espectro:
    $$Y[k] = X[k] \cdot H[k]$$

3.  **Teorema de Parseval:**
    Se utiliza como mecanismo de validación numérica para asegurar que la transformación es unitaria (salvo factores de escala) y que la energía se conserva:
    $$\sum_{n=0}^{N-1} |x[n]|^2 = \frac{1}{N} \sum_{k=0}^{N-1} |X[k]|^2$$
    El software reporta el error porcentual de esta igualdad en cada ejecución.

---

## 3. Estructura del Proyecto

La arquitectura del software es modular y se organiza de la siguiente manera:

```text
├── principal.py       # Orquestador principal (Menú CLI y automatización)
├── procesar.py        # Núcleo matemático: FFT, Filtros, IFFT, Métricas
├── audio.py           # Generador de datos sintéticos (Señales + Ruido)
├── requerimientos.txt # Dependencias del entorno
├── datos/             # Almacén de señales de entrada (Generadas automáticamente)
├── resultados/        # Salida del sistema
│   ├── audios_procesados/  # Archivos .wav resultantes del filtrado
│   └── graficas/           # Visualizaciones espectrales (PNG)
└── README.md          # Documentación técnica

---

## 4. Requisitos e Instalación

Este proyecto ha sido desarrollado y validado utilizando **Visual Studio Code (VS Code)** como entorno de desarrollo integrado (IDE). Para garantizar la correcta ejecución del código, se recomienda seguir el siguiente flujo de instalación:

### 4.1. Prerrequisitos del Sistema
1.  **Visual Studio Code:** Descargar e instalar la última versión estable desde [code.visualstudio.com](https://code.visualstudio.com/).
2.  **Intérprete de Python:** Instalar Python (versión 3.8 o superior) desde [python.org](https://www.python.org/).
    * *Nota:* Durante la instalación, asegúrese de marcar la casilla **"Add Python to PATH"**.

### 4.2. Configuración en VS Code
1.  Abra la carpeta del proyecto en Visual Studio Code.
2.  Acceda a la sección de **Extensiones** (Ctrl+Shift+X) e instale la extensión oficial:
    * **Python** (Microsoft).
3.  Seleccione el intérprete correcto presionando `F1` > escribir `Python: Select Interpreter` > Seleccionar la versión instalada (ej. Python 3.x.x).

### 4.3. Instalación de Dependencias
El proyecto incluye un archivo `requerimientos.txt` que lista todas las librerías matemáticas necesarias (`numpy`, `scipy`, `matplotlib`).

Para instalarlas, abra la terminal de su dispositivo *cmd/powershell* y ejecute el siguiente comando:
pip install -r requerimientos.txt

Posteriormente, dentro de la misma terminal ejecute el siguiente comando:
pip install numpy scipy matplotlib

Y por último, el siguiente:
python -m pip install numpy scipy matplotlib  

---

## 5. Compilación
1.  Abra la carpeta del proyecto en Visual Studio Code.
2.  Una vez que se abra el proyecto, seleccione el archivo nombrado como "principal.py".
3.  Una vez hecho lo anterior, en la parte superior derecha de la herramienta VS Code, abra un triángulo el cual tiene el nombre de "Run Python File", tiene que dar click en él.
4. Se ejecutará automáticamente la terminal de VS Code, y ella se desplegará un menú de 5 opciones, con estas, podremos realizar las pruebas necesarias.
