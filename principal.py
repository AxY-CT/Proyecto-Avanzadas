"""
SCRIPT PRINCIPAL PARA PROBAR TODAS LAS FUNCIONALIDADES
"""

import os
import subprocess
import sys

# Variable global para recordar la última frecuencia usada
ultima_frecuencia = 440.0

def verificar_instalacion():
    """Verifica que todas las librerías estén instaladas"""
    print("Verificando instalacion...")
    
    requerimientos = ['numpy', 'scipy', 'matplotlib']
    
    for lib in requerimientos:
        try:
            __import__(lib)
            print(f"OK {lib} instalado")
        except ImportError:
            print(f"ERROR {lib} NO instalado")
            return False
    
    return True

def crear_estructura():
    """Crea la estructura de carpetas necesaria"""
    carpetas = ['datos', 'resultados/graficas', 'resultados/audios_procesados']
    
    print("\nCreando estructura de carpetas...")
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)
        print(f"OK Carpeta creada: {carpeta}")
    
    return True

def ejecutar_pruebas():
    """Ejecuta pruebas de filtrado (usa audios ya generados)"""
    print("\n" + "="*60)
    print("PRUEBAS COMPLETAS DE FILTRADO")
    print("="*60)
    print("REQUISITO: Audios ya generados en carpeta 'datos/'")
    print("          (Si no existen, usa primero la Opción 1)\n")
    
    # Verificar que existan los archivos
    archivos_necesarios = [
        'datos/senal_ruido_blanco.wav',
        'datos/senal_ruido_60hz.wav',
        'datos/senal_multifrecuencia.wav'
    ]
    
    print("Verificando archivos de prueba...")
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"  OK {archivo}")
        else:
            print(f"  FALTA {archivo}")
            print("\nERROR: No hay audios de prueba.")
            print("SOLUCIÓN: Usa la Opción 1 para generar audios primero.")
            return
    
    # Pruebas de filtrado
    pasos = [
        ("1. Filtro pasa-bajas (elimina frecuencias > 800 Hz)", 
         "python procesar.py --entrada datos/senal_ruido_blanco.wav --filtro pasa_bajas --corte 800 --graficas False --salida resultados/audios_procesados/test_pasabajas.wav"),
        
        ("2. Filtro pasa-altas (elimina frecuencias < 200 Hz)", 
         "python procesar.py --entrada datos/senal_ruido_blanco.wav --filtro pasa_altas --corte 200 --graficas False --salida resultados/audios_procesados/test_pasaaltas.wav"),
        
        ("3. Filtro notch (elimina zumbido 60 Hz)", 
         "python procesar.py --entrada datos/senal_ruido_60hz.wav --filtro notch --rango 55-65 --graficas False --salida resultados/audios_procesados/test_notch.wav"),
        
        ("4. Filtro pasa-banda (aisla frecuencias 400-1200 Hz)", 
         "python procesar.py --entrada datos/senal_multifrecuencia.wav --filtro pasa_banda --rango 400-1200 --graficas False --salida resultados/audios_procesados/test_banda.wav")
    ]
    
    print("\n" + "="*60)
    print("INICIANDO PRUEBAS DE FILTRADO")
    print("="*60)
    
    for descripcion, comando in pasos:
        print(f"\n{descripcion}")
        
        try:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print("  RESULTADO: OK - Filtro aplicado correctamente")
                # Extraer métricas importantes del output
                for linea in resultado.stdout.split('\n'):
                    if 'MSE:' in linea or 'SNR:' in linea or 'Parseval' in linea:
                        print(f"  {linea.strip()}")
            else:
                print(f"  RESULTADO: ERROR")
                if resultado.stderr:
                    print(f"  {resultado.stderr[:100]}")
                    
        except Exception as e:
            print(f"  RESULTADO: ERROR - {e}")
    
    print("\n" + "="*60)
    print("PRUEBAS COMPLETADAS")
    print("="*60)
    print("\nResumen:")
    print("- 4 tipos de filtros probados")
    print("- Archivos procesados guardados en 'resultados/audios_procesados/'")
    print("- Para ver gráficas detalladas, ejecuta individualmente cada filtro")
    print("  Ejemplo: python procesar.py --entrada datos/senal_ruido_blanco.wav --filtro pasa_bajas --corte 800")

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    print("\n" + "="*60)
    print("INSTRUCCIONES DE USO")
    print("="*60)
    
    instrucciones = """
    USO BASICO:
    -----------
    1. Primero genera audios de prueba:
       python audio.py
    
    2. Luego procesa algun audio:
       python procesar.py --entrada datos/senal_ruido_blanco.wav
    
    OPCIONES AVANZADAS:
    ------------------
    • Cambiar tipo de filtro:
      --filtro pasa_bajas|pasa_altas|pasa_banda|notch
    
    • Especificar frecuencia de corte:
      --corte 1000  (para pasa_bajas/pasa_altas)
    
    • Especificar rango:
      --rango 500-1500  (para pasa_banda/notch)
    
    • Cambiar archivo de salida:
      --salida mi_resultado.wav
    
    • Desactivar graficas:
      --graficas False
    
    EJEMPLOS:
    ---------
    1. Filtro pasa-bajas a 800Hz:
       python procesar.py --entrada datos/senal_ruido_blanco.wav --filtro pasa_bajas --corte 800
    
    2. Eliminar ruido de 60Hz:
       python procesar.py --entrada datos/senal_ruido_60hz.wav --filtro notch --rango 55-65
    
    3. Aislar frecuencias medias:
       python procesar.py --entrada datos/senal_multifrecuencia.wav --filtro pasa_banda --rango 400-1200
    """
    
    print(instrucciones)
    print("="*60)

def main():
    """Funcion principal"""
    global ultima_frecuencia  # Para modificar la variable global
    
    print("="*60)
    print("PROYECTO TERMINAL: DENOISING DE AUDIO CON FFT")
    print("="*60)
    
    # Verificar instalacion
    if not verificar_instalacion():
        print("\nERROR Faltan librerias. Instala con:")
        print("pip install -r requerimientos.txt")
        sys.exit(1)
    
    # Crear estructura
    crear_estructura()
    
    # Menu principal
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Generar audios de prueba")
        print("2. Procesar audio (denoising)")
        print("3. Ejecutar prueba completa")
        print("4. Ver instrucciones")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opcion (1-5): ")
        
        if opcion == '1':
            print("\n[CONFIGURACIÓN] Frecuencia de la señal pura")
            print("• Rango recomendado: 20 Hz a 20000 Hz")
            print("• 440 Hz: Nota La musical (estándar)")
            print("• Presiona Enter para usar 440 Hz por defecto")
            # Preguntar y guardar la frecuencia
            
            try:
                freq_input = input("\nFrecuencia para los audios (Hz, Enter para 440): ").strip()
                if freq_input:
                    ultima_frecuencia = float(freq_input)
                    print(f"Usando frecuencia: {ultima_frecuencia} Hz")
                else:
                    ultima_frecuencia = 440.0
                    print("Usando frecuencia por defecto: 440 Hz")
            except ValueError:
                print("Entrada no valida. Usando 440 Hz")
                ultima_frecuencia = 440.0
            
            # Ejecutar audio.py con la frecuencia elegida
            print(f"\nEjecutando con frecuencia {ultima_frecuencia} Hz...")
            os.system(f'echo {ultima_frecuencia} | python audio.py')
        
        elif opcion == '2':
            archivo = input("Archivo de entrada (default: datos/senal_ruido_blanco.wav): ")
            if not archivo:
                archivo = 'datos/senal_ruido_blanco.wav'
            
            print("\nTipos de filtro disponibles:")
            print("1. pasa_bajas (elimina altas frecuencias)")
            print("2. pasa_altas (elimina bajas frecuencias)")
            print("3. pasa_banda (conserva un rango)")
            print("4. notch (elimina un rango)")
            
            filtro_opcion = input("\nSelecciona filtro (1-4, default: 1): ")
            filtros = ['pasa_bajas', 'pasa_altas', 'pasa_banda', 'notch']
            filtro = filtros[int(filtro_opcion)-1] if filtro_opcion in ['1','2','3','4'] else 'pasa_bajas'
            
            if filtro in ['pasa_bajas', 'pasa_altas']:
                corte = input(f"Frecuencia de corte para {filtro} (default: 1000): ")
                corte = float(corte) if corte else 1000.0
                comando = f'python procesar.py --entrada {archivo} --filtro {filtro} --corte {corte}'
            else:
                rango = input(f"Rango para {filtro} (ej: 500-1500, default: 500-1500): ")
                rango = rango if rango else '500-1500'
                comando = f'python procesar.py --entrada {archivo} --filtro {filtro} --rango {rango}'
            
            print(f"\nEjecutando: {comando}")
            os.system(comando)
        
        elif opcion == '3':
            # Mostrar qué frecuencia se usará
            print(f"\n[INFO] Pruebas usaran audios con frecuencia: {ultima_frecuencia} Hz")
            print("[INFO] Si quieres cambiar la frecuencia, usa primero la Opcion 1")
            confirmar = input("¿Continuar? (s/n): ").lower()
            if confirmar == 's':
                ejecutar_pruebas()
            else:
                print("Prueba cancelada")
        
        elif opcion == '4':
            mostrar_instrucciones()
        
        elif opcion == '5':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("\nOpcion no valida. Intenta de nuevo.")

if __name__ == "__main__":
    main()