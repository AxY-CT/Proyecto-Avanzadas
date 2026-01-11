"""
PROYECTO TERMINAL: DENOISING DE AUDIO CON FFT
Opción 1: Filtrado en frecuencia + validación con Parseval

Autor: [Sanchez Gonzalez Axel]
Curso: Matemáticas Avanzadas para la Ingeniería 26-1
Escuela Superior de Cómputo - IPN
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft, fftfreq
import argparse

def cargar_audio(ruta_archivo):
    """
    Carga un archivo de audio .wav y lo normaliza
    
    Args:
        ruta_archivo: Ruta del archivo .wav
    
    Returns:
        frecuencia_muestreo: Frecuencia de muestreo en Hz
        datos_audio: Señal normalizada [-1, 1]
    """
    frecuencia_muestreo, datos_audio = wavfile.read(ruta_archivo)
    
    # Normalizar a rango [-1, 1] (como en tu código original)
    if datos_audio.dtype == np.int16:
        datos_audio = datos_audio.astype(np.float32) / 32767.0
    elif datos_audio.dtype == np.int32:
        datos_audio = datos_audio.astype(np.float32) / 2147483647.0
    
    # Normalizar máximo absoluto
    max_valor = np.max(np.abs(datos_audio))
    if max_valor > 0:
        datos_audio = datos_audio / max_valor
    
    return frecuencia_muestreo, datos_audio

def guardar_audio(datos_audio, frecuencia_muestreo, ruta_archivo):
    """
    Guarda datos de audio en un archivo .wav
    
    Args:
        datos_audio: Señal a guardar
        frecuencia_muestreo: Frecuencia de muestreo
        ruta_archivo: Ruta de salida
    """
    # Normalizar antes de guardar
    max_valor = np.max(np.abs(datos_audio))
    if max_valor > 0:
        datos_audio = datos_audio / max_valor
    
    # Convertir a int16
    datos_int16 = np.int16(datos_audio * 32767)
    wavfile.write(ruta_archivo, frecuencia_muestreo, datos_int16)

def crear_mascara_filtro(frecuencias, tipo_filtro='pasa_bajas', 
                        frecuencia_corte=1000, rango_frecuencias=(500, 1500)):
    """
    Crea una máscara para diferentes tipos de filtros
    
    Args:
        frecuencias: Array de frecuencias
        tipo_filtro: 'pasa_bajas', 'pasa_altas', 'pasa_banda', 'notch'
        frecuencia_corte: Frecuencia de corte para pasa_bajas/pasa_altas
        rango_frecuencias: Tupla (min, max) para pasa_banda/notch
    
    Returns:
        mascara: Array de 1s y 0s
    """
    mascara = np.ones_like(frecuencias, dtype=float)
    
    if tipo_filtro == 'pasa_bajas':
        # Conserva frecuencias bajas
        mascara[np.abs(frecuencias) > frecuencia_corte] = 0.0
    
    elif tipo_filtro == 'pasa_altas':
        # Conserva frecuencias altas
        mascara[np.abs(frecuencias) < frecuencia_corte] = 0.0
    
    elif tipo_filtro == 'pasa_banda':
        # Conserva solo un rango
        min_freq, max_freq = rango_frecuencias
        mascara[(np.abs(frecuencias) < min_freq) | (np.abs(frecuencias) > max_freq)] = 0.0
    
    elif tipo_filtro == 'notch':
        # Elimina un rango específico
        min_freq, max_freq = rango_frecuencias
        mascara[(np.abs(frecuencias) >= min_freq) & (np.abs(frecuencias) <= max_freq)] = 0.0
    
    else:
        raise ValueError(f"Tipo de filtro no válido: {tipo_filtro}")
    
    return mascara

def calcular_metricas(original, procesada):
    """
    Calcula métricas de calidad entre señales
    
    Args:
        original: Señal original
        procesada: Señal procesada
    
    Returns:
        dict: Diccionario con métricas
    """
    # Asegurar misma longitud
    min_len = min(len(original), len(procesada))
    original = original[:min_len]
    procesada = procesada[:min_len]
    
    # MSE (Error Cuadrático Medio)
    mse = np.mean((original - procesada) ** 2)
    
    # SNR (Relación Señal-Ruido)
    ruido = original - procesada
    potencia_senal = np.mean(procesada ** 2)
    potencia_ruido = np.mean(ruido ** 2)
    
    if potencia_ruido > 0:
        snr = 10 * np.log10(potencia_senal / potencia_ruido)
    else:
        snr = float('inf')
    
    # PSNR (Relación Señal a Ruido Pico)
    if mse > 0:
        psnr = 10 * np.log10(1.0 / mse)
    else:
        psnr = float('inf')
    
    return {
        'mse': mse,
        'snr_db': snr,
        'psnr_db': psnr,
        'ruido_removido': ruido
    }

def verificar_parseval(señal_tiempo, espectro_frecuencia):
    """
    Verifica el Teorema de Parseval
    
    Args:
        señal_tiempo: Señal en dominio del tiempo
        espectro_frecuencia: Espectro de la señal
    
    Returns:
        dict: Resultados de Parseval
    """
    N = len(señal_tiempo)
    
    # Energía en dominio del tiempo
    energia_tiempo = np.sum(señal_tiempo ** 2)
    
    # Energía en dominio de la frecuencia
    energia_frecuencia = np.sum(np.abs(espectro_frecuencia) ** 2) / N
    
    # Error porcentual
    if energia_tiempo > 0:
        error_porcentual = 100 * abs(energia_tiempo - energia_frecuencia) / energia_tiempo
    else:
        error_porcentual = 0.0
    
    return {
        'energia_tiempo': energia_tiempo,
        'energia_frecuencia': energia_frecuencia,
        'error_porcentual': error_porcentual,
        'se_cumple': error_porcentual < 1.0  # Menos de 1% de error
    }

def graficar_resultados(datos_original, datos_filtrada, espectro_original, 
                       espectro_filtrado, frecuencias, fs, tipo_filtro):
    """
    Genera gráficas de resultados (similar a tu código original)
    """
    fig = plt.figure(figsize=(12, 10))
    
    # 1. Señales en tiempo
    plt.subplot(3, 2, 1)
    tiempo = np.arange(len(datos_original)) / fs
    zoom = min(500, len(datos_original))
    plt.plot(tiempo[:zoom], datos_original[:zoom], 'gray', alpha=0.7, label='Original')
    plt.plot(tiempo[:zoom], datos_filtrada[:zoom], 'blue', label='Filtrada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Dominio del Tiempo')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Diferencia (ruido removido)
    plt.subplot(3, 2, 2)
    diferencia = datos_original - datos_filtrada
    plt.plot(tiempo[:zoom], diferencia[:zoom], 'red', alpha=0.7)
    plt.fill_between(tiempo[:zoom], 0, diferencia[:zoom], alpha=0.3, color='red')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Ruido Removido')
    plt.grid(True, alpha=0.3)
    
    # 3. Espectro original
    plt.subplot(3, 2, 3)
    rango = (frecuencias > 0) & (frecuencias < 3000)
    plt.plot(frecuencias[rango], np.abs(espectro_original[rango]), 
             'gray', alpha=0.6, label='Original')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.title('Espectro Original')
    plt.grid(True, alpha=0.3)
    
    # 4. Espectro filtrado
    plt.subplot(3, 2, 4)
    plt.plot(frecuencias[rango], np.abs(espectro_filtrado[rango]), 
             'green', alpha=0.7, label='Filtrado')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.title(f'Espectro Filtrado ({tipo_filtro})')
    plt.grid(True, alpha=0.3)
    
    # 5. Comparación de espectros
    plt.subplot(3, 2, 5)
    plt.plot(frecuencias[rango], np.abs(espectro_original[rango]), 
             'gray', alpha=0.5, label='Original')
    plt.plot(frecuencias[rango], np.abs(espectro_filtrado[rango]), 
             'blue', alpha=0.7, label='Filtrado')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.title('Comparación de Espectros')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 6. Respuesta del filtro
    plt.subplot(3, 2, 6)
    mascara = np.abs(espectro_filtrado) / (np.abs(espectro_original) + 1e-10)
    mascara = np.where(mascara > 1, 1, mascara)  # Limitar a 1
    plt.plot(frecuencias[rango], mascara[rango], 'purple')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Ganancia')
    plt.title('Respuesta del Filtro')
    plt.grid(True, alpha=0.3)
    
    plt.suptitle(f'Resultados: Denoising con Filtro {tipo_filtro}', fontsize=14)
    plt.tight_layout()
    
    return fig

def main():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(description='Denoising de audio con FFT')
    
    parser.add_argument('--entrada', type=str, default='datos/senal_ruido_blanco.wav',
                       help='Archivo de audio de entrada')
    parser.add_argument('--salida', type=str, default='resultados/audios_procesados/resultado_limpio.wav',
                       help='Archivo de audio de salida')
    parser.add_argument('--filtro', type=str, default='pasa_bajas',
                       choices=['pasa_bajas', 'pasa_altas', 'pasa_banda', 'notch'],
                       help='Tipo de filtro a aplicar')
    parser.add_argument('--corte', type=float, default=1000.0,
                       help='Frecuencia de corte para pasa_bajas/pasa_altas')
    parser.add_argument('--rango', type=str, default='500-1500',
                       help='Rango para pasa_banda/notch (formato: min-max)')
    parser.add_argument('--graficas', type=bool, default=True,
                       help='Mostrar gráficas')
    
    args = parser.parse_args()
    
    print("="*60)
    print("PROYECTO TERMINAL: DENOISING DE AUDIO CON FFT")
    print("="*60)
    
    # 1. Cargar audio
    print(f"\n[1/6] Cargando audio: {args.entrada}")
    fs, datos = cargar_audio(args.entrada)
    N = len(datos)
    print(f"   • Muestras: {N}")
    print(f"   • Frecuencia de muestreo: {fs} Hz")
    print(f"   • Duración: {N/fs:.2f} segundos")
    
    # 2. Calcular FFT
    print(f"\n[2/6] Calculando Transformada de Fourier...")
    espectro = fft(datos)
    frecuencias = fftfreq(N, 1/fs)
    
    # 3. Crear y aplicar filtro
    print(f"\n[3/6] Aplicando filtro {args.filtro}...")
    
    # Parsear rango si es necesario
    if '-' in args.rango:
        rango_min, rango_max = map(float, args.rango.split('-'))
        rango_tuple = (rango_min, rango_max)
    else:
        rango_tuple = (500, 1500)
    
    # Crear máscara
    mascara = crear_mascara_filtro(frecuencias, args.filtro, args.corte, rango_tuple)
    
    # Aplicar filtro
    espectro_filtrado = espectro * mascara
    
    # 4. Reconstruir señal
    print(f"\n[4/6] Reconstruyendo señal con IFFT...")
    datos_filtrados = np.real(ifft(espectro_filtrado))
    
    # 5. Calcular métricas
    print(f"\n[5/6] Calculando métricas de calidad...")
    
    # Métricas de calidad
    metricas = calcular_metricas(datos, datos_filtrados)
    print(f"   • MSE: {metricas['mse']:.6f}")
    print(f"   • SNR: {metricas['snr_db']:.2f} dB")
    print(f"   • PSNR: {metricas['psnr_db']:.2f} dB")
    
    # Verificación de Parseval
    parseval_original = verificar_parseval(datos, espectro)
    parseval_filtrado = verificar_parseval(datos_filtrados, espectro_filtrado)
    
# MODIFICADO: Todo en una línea para que principal.py capture los datos
    print(f"\n   • Parseval (Original): T={parseval_original['energia_tiempo']:.4f} | F={parseval_original['energia_frecuencia']:.4f} | Error: {parseval_original['error_porcentual']:.2f}%")
    print(f"   • Parseval (Filtrado): T={parseval_filtrado['energia_tiempo']:.4f} | F={parseval_filtrado['energia_frecuencia']:.4f} | Error: {parseval_filtrado['error_porcentual']:.2f}%")
    
    # 6. Guardar resultado
    print(f"\n[6/6] Guardando audio procesado...")
    guardar_audio(datos_filtrados, fs, args.salida)
    print(f"    Audio guardado como: {args.salida}")
    
    # 7. Generar gráficas
    if args.graficas:
        print(f"\n[+] Generando gráficas...")
        fig = graficar_resultados(datos, datos_filtrados, espectro, 
                                espectro_filtrado, frecuencias, fs, args.filtro)
        
        # Guardar gráficas con nombre único basado en el filtro
        nombre_archivo = f'resultados_completos_{args.filtro}'
        if args.filtro in ['pasa_bajas', 'pasa_altas']:
            nombre_archivo += f'_{args.corte}Hz'
        else:
            nombre_archivo += f'_{args.rango.replace("-", "_")}Hz'
        
        # Añadir extensión
        nombre_archivo += '.png'
        ruta_completa = f'resultados/graficas/{nombre_archivo}'
        
        plt.savefig(ruta_completa, dpi=150, bbox_inches='tight')
        print(f"    Gráfica guardada como: {ruta_completa}")
        plt.show()
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DEL PROCESAMIENTO")
    print("="*60)
    print(f"Filtro aplicado: {args.filtro}")
    if args.filtro in ['pasa_bajas', 'pasa_altas']:
        print(f"Frecuencia de corte: {args.corte} Hz")
    else:
        print(f"Rango de frecuencias: {rango_tuple[0]}-{rango_tuple[1]} Hz")
    print(f"MSE: {metricas['mse']:.6f}")
    print(f"SNR: {metricas['snr_db']:.2f} dB")
    print(f"Error Parseval: {parseval_filtrado['error_porcentual']:.2f}%")
    print(f"Archivo de salida: {args.salida}")
    print("="*60)

if __name__ == "__main__":
    # Crear carpetas necesarias
    import os
    os.makedirs('resultados/graficas', exist_ok=True)
    os.makedirs('resultados/audios_procesados', exist_ok=True)
    
    main()