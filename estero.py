"Funciones para el manejo de señal estéreo y su codificación y descodificación"

import struct as st

formato_cabecera = '<4sI4s4sIHHIIHH4sI'

def leer_datos(fichero, num_canales):
    with open(fichero, 'rb') as fp_fichero:
        cabecera = fp_fichero.read(44)
        (riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, sample_rate, byte_rate, 
         block_align, bits_per_sample, data_id, data_size) = st.unpack(formato_cabecera, cabecera)
        
        cabecera = [riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, sample_rate, 
                    byte_rate, block_align, bits_per_sample, data_id, data_size]
        
        if n_channels != num_canales:
            raise ValueError("El archivo debe ser estéreo.")
        
        if riff != b"RIFF" or wave != b"WAVE":
            raise TypeError("File '{fp_estereo}' is not WAV file")
        
        data = fp_fichero.read(data_size)

        formato_datos = f'<{data_size // (bits_per_sample // 8)}h'
        datos = st.unpack(formato_datos, data)

    return cabecera, datos

def escribir_fichero(fichero_out, n_channels, canal, cabecera, datos):
    with open(fichero_out, 'wb') as fp_out:
        if canal == 2 or canal == 3:
            cabecera[7] *= 2 
        byte_rate = cabecera[7] * n_channels * cabecera[10] // 8
        block_align = n_channels * cabecera[10] // 8
        data_size = len(datos) * (cabecera[10] // 8)
        riff_size = 36 + data_size

        nueva_cabecera = st.pack(formato_cabecera, cabecera[0], riff_size, cabecera[2], cabecera[3], cabecera[4], cabecera[5], 
                                 n_channels, cabecera[7], byte_rate, block_align, cabecera[10], cabecera[11], data_size)
        
        fp_out.write(nueva_cabecera)

        formato_out = f'<{len(datos)}h'
        datos_packed = st.pack(formato_out, *datos)
        fp_out.write(datos_packed)

def estereo2mono(ficEste, ficMono, canal=2):
    cabecera, datos_estereo = leer_datos(ficEste, 2)

    datos_mono = []
    if canal == 0:
        # Canal izquierdo
        datos_mono = datos_estereo[0::2]
    elif canal == 1:
        # Canal derecho
        datos_mono = datos_estereo[1::2]
    elif canal == 2:
        # Promedio de ambos canales (semisuma)
        datos_mono = [(datos_estereo[i] + datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
    elif canal == 3:
        # Diferencia entre ambos canales (semidiferencia)
        datos_mono = [(datos_estereo[i] - datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
    else:
        raise ValueError("Canal inválido. Debe ser 0, 1, 2 o 3.")
    
    escribir_fichero(ficMono, 1, canal, cabecera, datos_mono)
    
estereo2mono("APA-T5\wav\komm.wav", "APA-T5\wav\komm_mono.wav", 1)

def mono2estereo(ficIzq, ficDer, ficEste):
    cabeceraI, datos_Izq = leer_datos(ficIzq, 1)
    cabeceraD, datos_Der = leer_datos(ficDer, 1)

    if cabeceraI[7] != cabeceraD[7] or cabeceraI[10] != cabeceraD[10]:
        raise ValueError("Ambos archivos mono deben tener los mismos parámetros de audio.")
    
    if cabeceraI[5] != 16 or cabeceraD[5] != 16 or cabeceraI[6] != 1 or cabeceraD[6] != 1:
        raise ValueError("Ambos archivos mono deben estar codificados con PCM lineal con 16 bits.")

    datos_estereo = []
    for mostraI, mostraD in zip(datos_Izq, datos_Der):
        datos_estereo.append(mostraI)
        datos_estereo.append(mostraD)

    escribir_fichero(ficEste, 2, -1, cabeceraI, datos_estereo)

jazz = "APA-T5\wav\jazz.wav"
trad = "APA-T5\wav\tradicional.wav"
iz = "APA-T5\wav\iz.wav"
der = "APA-T5\wav\der.wav"
estereo_combinado = "APA-T5\wav\estereo_combinado.wav"

estereo2mono(jazz, iz, 0)
estereo2mono(trad, der, 1)
mono2estereo(iz, der, estereo_combinado)

def codEstereo(ficEste, ficCod):
    canalIz = "APA-T5\wav\semisuma_estereo.wav"
    canalDer = "APA-T5\wav\semidiferencia_estereo.wav"

    estereo2mono(ficEste, canalIz, 2)
    estereo2mono(ficEste, canalDer, 3)
    mono2estereo(canalIz, canalDer, ficCod)

codEstereo("APA-T5\wav\komm.wav", "APA-T5\wav\ficCod.wav")

def decEstereo(ficCod, ficEste):
    ficCod_monoI = "APA-T5\wav\ficCod_monoI.wav"
    ficCod_monoD = "APA-T5\wav\ficCod_monoD.wav"
    estereo2mono(ficCod, ficCod_monoI, 0)
    estereo2mono(ficCod, ficCod_monoD, 1)
    mono2estereo(ficCod_monoI, ficCod_monoD, ficEste)

decEstereo("APA-T5\wav\ficCod.wav", "APA-T5\wav\ficEste.wav")