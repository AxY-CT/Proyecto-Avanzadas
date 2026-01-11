"""
GENERADOR DE AUDIO DE PRUEBA
Crea archivos .wav con señal pura y con ruido para pruebas

Funciones matemáticas utilizadas:
- Señal pura: x(t) = A·sin(2πft)
- Ruido blanco: n(t) ~ N(0, σ²) (distribución normal)
- Ruido tonal: r(t) = B·sin(2πf_ruido t)
- Muestreo: fs = 44100 Hz (estándar CD, Nyquist: 22050 Hz)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import sys

def generar_audio_prueba():
    """
    Genera diferentes tipos de audio para pruebas
    
    PROCESO:
    1. Pide frecuencia al usuario (20-20000 Hz recomendado)
    2. Genera 4 tipos de señales con/sin ruido
    3. Guarda archivos .wav en carpeta 'datos/'
    4. Genera gráfica comparativa
    
    MATEMÁTICAMENTE:
    - Frecuencia de Nyquist: f_max = fs/2 = 22050 Hz
    - Período de muestreo: T = 1/fs ≈ 22.68 μs
    - Normalización: mantiene amplitud en [-1, 1]
    """
    
    print("="*60)
    print("GENERADOR DE AUDIOS DE PRUEBA")
    print("="*60)
    
    # 1. SOLICITAR FRECUENCIA AL USUARIO
    print("\n[CONFIGURACIÓN] Frecuencia de la señal pura")
    print("• Rango recomendado: 20 Hz a 20000 Hz")
    print("• 440 Hz: Nota La musical (estándar)")
    print("• Presiona Enter para usar 440 Hz por defecto")
    
    frecuencia = 440.0  # Valor por defecto
    
    try:
        user_input = input("\nIngresa frecuencia en Hz: ").strip()
        if user_input:
            frecuencia = float(user_input)
            if frecuencia <= 0:
                print("  [ADVERTENCIA] Frecuencia debe ser positiva. Usando 440 Hz")
                frecuencia = 440.0
            elif frecuencia > 20000:
                print("  [ADVERTENCIA] Frecuencia > 20000 Hz puede causar aliasing")
        else:
            print("  Usando frecuencia por defecto: 440 Hz")
    except ValueError:
        print("  [ERROR] Entrada no válida. Usando 440 Hz")
        frecuencia = 440.0
    
    print(f"\n[INICIANDO] Generando audios con frecuencia base: {frecuencia} Hz")
    print("El programa creará 4 archivos .wav con diferentes tipos de ruido")
    
    # 2. CONFIGURACIÓN DE PARÁMETROS
    fs = 44100  # Frecuencia de muestreo estándar (44.1 kHz)
    duracion = 3.0  # segundos
    t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
    
    # 3. GENERACIÓN DE SEÑALES
    
    # 3.1 SEÑAL PURA (sin ruido)
    print(f"\n[1/4] Generando señal pura ({frecuencia} Hz)...")
    # Ecuación: x(t) = A·sin(2πft) con A = 0.7
    señal_pura = 0.7 * np.sin(2 * np.pi * frecuencia * t)
    
    # Normalización para evitar clipping
    señal_pura = señal_pura / np.max(np.abs(señal_pura))
    
    # Guardar como archivo .wav (16 bits, formato PCM)
    datos_wav = np.int16(señal_pura * 32767)
    wavfile.write('datos/senal_pura.wav', fs, datos_wav)
    print(f"  Guardado: datos/senal_pura.wav")
    
    # 3.2 SEÑAL CON RUIDO BLANCO (gaussiano)
    print(f"\n[2/4] Generando señal con ruido blanco...")
    # Ruido gaussiano: n(t) ~ N(0, σ²) con σ = 0.3
    ruido_blanco = 0.3 * np.random.normal(0, 1, len(t))
    señal_blanco = señal_pura + ruido_blanco
    
    # Normalizar
    señal_blanco = señal_blanco / np.max(np.abs(señal_blanco))
    
    datos_wav = np.int16(señal_blanco * 32767)
    wavfile.write('datos/senal_ruido_blanco.wav', fs, datos_wav)
    print(f"  Guardado: datos/senal_ruido_blanco.wav")
    print(f"  Nota: Ruido blanco simula interferencia aleatoria (estática)")
    
    # 3.3 SEÑAL CON RUIDO TONAL (60 Hz - interferencia eléctrica)
    print(f"\n[3/4] Generando señal con ruido tonal (60 Hz)...")
    # Ruido sinusoidal: r(t) = 0.4·sin(2π·60·t)
    ruido_60hz = 0.4 * np.sin(2 * np.pi * 60 * t)
    señal_60hz = señal_pura + ruido_60hz
    
    señal_60hz = señal_60hz / np.max(np.abs(señal_60hz))
    
    datos_wav = np.int16(señal_60hz * 32767)
    wavfile.write('datos/senal_ruido_60hz.wav', fs, datos_wav)
    print(f"  Guardado: datos/senal_ruido_60hz.wav")
    print(f"  Nota: Ruido de 60 Hz simula interferencia eléctrica (zumbido)")
    
    # 3.4 SEÑAL CON MÚLTIPLES FRECUENCIAS + RUIDO
    print(f"\n[4/4] Generando señal multifrecuencia con ruido...")
    # Suma de sinusoides: s(t) = Σ A_i·sin(2πf_i t)
    señal_multif = 0.5 * np.sin(2 * np.pi * frecuencia * t)  # Frecuencia fundamental
    señal_multif += 0.3 * np.sin(2 * np.pi * frecuencia * 2 * t)  # 2ª armónica
    señal_multif += 0.2 * np.sin(2 * np.pi * frecuencia * 3 * t)  # 3ª armónica
    
    # Añadir ruido gaussiano
    ruido_banda = 0.25 * np.random.normal(0, 1, len(t))
    señal_multif_ruido = señal_multif + ruido_banda
    
    señal_multif_ruido = señal_multif_ruido / np.max(np.abs(señal_multif_ruido))
    
    datos_wav = np.int16(señal_multif_ruido * 32767)
    wavfile.write('datos/senal_multifrecuencia.wav', fs, datos_wav)
    print(f"  Guardado: datos/senal_multifrecuencia.wav")
    print(f"  Nota: Señal con armónicos simula sonido musical complejo")
    
    # 4. GRÁFICA COMPARATIVA
    print(f"\n[+] Generando gráfica comparativa...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Señal pura (zoom primeros 0.023 segundos)
    axes[0, 0].plot(t[:1000], señal_pura[:1000], 'b-', linewidth=2)
    axes[0, 0].set_title(f'Señal Pura ({frecuencia:.0f} Hz)')
    axes[0, 0].set_xlabel('Tiempo (s)')
    axes[0, 0].set_ylabel('Amplitud')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Señal con ruido blanco
    axes[0, 1].plot(t[:1000], señal_blanco[:1000], 'orange', linewidth=2)
    axes[0, 1].set_title('Con Ruido Blanco')
    axes[0, 1].set_xlabel('Tiempo (s)')
    axes[0, 1].set_ylabel('Amplitud')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Señal con ruido 60Hz
    axes[1, 0].plot(t[:1000], señal_60hz[:1000], 'green', linewidth=2)
    axes[1, 0].set_title('Con Ruido Tonal (60 Hz)')
    axes[1, 0].set_xlabel('Tiempo (s)')
    axes[1, 0].set_ylabel('Amplitud')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Señal multifrecuencia
    axes[1, 1].plot(t[:1000], señal_multif_ruido[:1000], 'purple', linewidth=2)
    axes[1, 1].set_title(f'Multifrecuencia ({frecuencia:.0f} Hz + armónicos)')
    axes[1, 1].set_xlabel('Tiempo (s)')
    axes[1, 1].set_ylabel('Amplitud')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle(f'Audios de Prueba - Señal Base: {frecuencia:.0f} Hz', fontsize=14)
    plt.tight_layout()
    
    # Guardar gráfica
    plt.savefig('resultados/graficas/audios_prueba.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 5. RESUMEN FINAL
    print("\n" + "="*60)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60)
    
    print(f"\n ARCHIVOS GENERADOS (carpeta 'datos/'):")
    print(f"1. senal_pura.wav           - Señal limpia de {frecuencia:.0f} Hz")
    print("2. senal_ruido_blanco.wav   - Con ruido blanco gaussiano")
    print("3. senal_ruido_60hz.wav     - Con ruido tonal de 60 Hz")
    print("4. senal_multifrecuencia.wav - Con múltiples frecuencias + ruido")
    
    print(f"\n PARÁMETROS UTILIZADOS:")
    print(f"   • Frecuencia base: {frecuencia:.0f} Hz")
    print(f"   • Frecuencia de muestreo: {fs} Hz")
    print(f"   • Duración: {duracion} segundos")
    print(f"   • Formato: 16-bit PCM (.wav)")
    
    print(f"\n PARA PROCESAR (eliminar ruido):")
    print(f"   Ejecuta: python procesar.py --entrada datos/senal_ruido_blanco.wav")
    
    print(f"\n ANÁLISIS MATEMÁTICO:")
    print(f"   • Teorema de Nyquist: f_max = {fs/2:.0f} Hz")
    print(f"   • Resolución temporal: {1/fs*1000:.2f} ms por muestra")
    print(f"   • Número de muestras: {len(t)}")
    print("="*60)

def crear_archivo_licencia():
    """
    Crea archivo de licencia para los datos generados
    (Requisito del proyecto: documentar fuente y licencia)
    """
    contenido = """LICENCIA DE LOS DATOS DE PRUEBA
=====================================

Estos archivos de audio han sido generados sintéticamente
para fines educativos del proyecto terminal:

"Denoising de Audio con FFT - Aplicación de Transformada de Fourier"

Curso: Matemáticas Avanzadas para la Ingeniería 26-1
Escuela Superior de Cómputo - IPN

AUTOR:
[Sanchez Gonzalez Axel]

LICENCIA:
Se permite el uso, modificación y distribución de estos archivos
exclusivamente para fines educativos, académicos y de investigación.

Se prohíbe el uso comercial sin autorización expresa de los autores.

GENERACIÓN:
- Señales sinusoidales: x(t) = A·sin(2pift)
- Ruido gaussiano: n(t) ~ N(0, (sigma)²)
- Ruido tonal: r(t) = B·sin(2pif_ruido t)
- Frecuencia de muestreo: 44100 Hz (estándar CD)
- Cuantización: 16 bits (formato PCM)
- Duración: 3.0 segundos por archivo
"""
    
    with open('datos/LICENCIA.txt', 'w') as f:
        f.write(contenido)
    print("[INFO] Archivo de licencia creado: datos/LICENCIA.txt")

if __name__ == "__main__":
    # Crear estructura de carpetas necesaria
    os.makedirs('datos', exist_ok=True)
    os.makedirs('resultados/graficas', exist_ok=True)
    
    # Ejecutar generación de audios
    generar_audio_prueba()
    crear_archivo_licencia()