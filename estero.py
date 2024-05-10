"Funciones para el manejo de señal estéreo y su codificación y descodificación"

import struct as st

def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste, 'rb') as fp_estereo:
        formato_cabecera = '<4sI4s4sIHHIIHH4sI'
        cabecera = fp_estereo.read(44)
        (riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, sample_rate, byte_rate, block_align, 
         bits_per_sample, data_id, data_size) = st.unpack(formato_cabecera, cabecera)
        
        if n_channels != 2:
            raise ValueError("El archivo debe ser estéreo.")
        
        if riff != b"RIFF" or wave != b"WAVE":
            raise TypeError("File '{fp_estereo}' is not WAV file")
        
        data = fp_estereo.read(data_size)

        formato_datos = f'<{data_size // (bits_per_sample // 8)}h'
        datos_estereo = st.unpack(formato_datos, data)

        datos_mono = []
        if canal == 0:
            # Canal izquierdo
            datos_mono = datos_estereo[0::2]
        elif canal == 1:
            # Canal derecho
            datos_mono = datos_estereo[1::2]
        elif canal == 2:
            # Promedio de ambos canales
            datos_mono = [(datos_estereo[i] + datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
        elif canal == 3:
            # Diferencia entre ambos canales
            datos_mono = [(datos_estereo[i] - datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
        else:
            raise ValueError("Canal inválido. Debe ser 0, 1, 2 o 3.")
        
    with open(ficMono, 'wb') as fp_mono:
        n_channels = 1
        if canal == 2 or canal == 3:
            sample_rate *= 2
        byte_rate = sample_rate * n_channels * bits_per_sample // 8
        block_align = n_channels * bits_per_sample // 8
        data_size = len(datos_mono) * (bits_per_sample // 8)
        riff_size = 36 + data_size

        nueva_cabecera = st.pack(formato_cabecera, riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, 
                                 sample_rate, byte_rate, block_align, bits_per_sample, data_id, data_size)
        
        fp_mono.write(nueva_cabecera)

        formato_mono = f'<{len(datos_mono)}h'
        datos_mono_packed = st.pack(formato_mono, *datos_mono)
        fp_mono.write(datos_mono_packed)

estereo2mono("D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\komm.wav", "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\komm_mono.wav", 1)

def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq, 'rb') as fp_Izq:
        formato_cabecera = '<4sI4s4sIHHIIHH4sI'
        cabecera = fp_Izq.read(44)
        (riff, riff_size, wave, fmt, fmt_size, audio_format, n_channelsI, sample_rateI, byte_rate, block_align, 
         bits_per_sampleI, data_id, data_size) = st.unpack(formato_cabecera, cabecera)
        
        if n_channelsI != 1:
            raise ValueError("El archivo debe ser mono.")

        if riff != b"RIFF" or wave != b"WAVE":
            raise TypeError("File '{fp_estereo}' is not WAV file")
        
        data = fp_Izq.read(data_size)

        formato_datos = f'<{data_size // (bits_per_sampleI // 8)}h'
        data_Izq = st.unpack(formato_datos, data)

    with open(ficDer, 'rb') as fp_Der:
        # formato_cabecera = '<4sI4s4sIHHIIHH4sI'
        cabecera = fp_Der.read(44)
        (riff, riff_size, wave, fmt, fmt_size, audio_format, n_channelsD, sample_rateD, byte_rate, block_align, 
         bits_per_sampleD, data_id, data_size) = st.unpack(formato_cabecera, cabecera)
        
        if n_channelsD != 1:
            raise ValueError("El archivo debe ser mono.")

        if riff != b"RIFF" or wave != b"WAVE":
            raise TypeError("File '{fp_estereo}' is not WAV file")
        
        data = fp_Der.read(data_size)

        formato_datos = f'<{data_size // (bits_per_sampleD // 8)}h'
        data_Der = st.unpack(formato_datos, data)

    if (n_channelsI != 1 or n_channelsD != 1 or sample_rateI != sample_rateD or bits_per_sampleI != bits_per_sampleD):
        raise ValueError("Ambos archivos mono deben tener los mismos parámetros de audio.")
        
    datos_estereo = []
    for mostraI, mostraD in zip(data_Izq, data_Der):
        datos_estereo.append(mostraI)
        datos_estereo.append(mostraD)

    formato_estereo = f'<{len(datos_estereo)}h'
    datos_estereo_packed = st.pack(formato_estereo, *datos_estereo)

    with open(ficEste, 'wb') as fp_estereo:
        n_channels = 2
        byte_rate = sample_rateI * n_channels * bits_per_sampleI // 8
        block_align = n_channels * bits_per_sampleI // 8
        data_size = len(datos_estereo) * (bits_per_sampleI // 8)
        riff_size = 36 + data_size

        nueva_cabecera = st.pack(formato_cabecera, riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, 
                                 sample_rateI, byte_rate, block_align, bits_per_sampleI, data_id, data_size)
        
        fp_estereo.write(nueva_cabecera)

        fp_estereo.write(datos_estereo_packed)

jazz = "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\jazz.wav"
trad = "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\tradicional.wav"

estereo2mono(jazz, "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\iz.wav", 0)
estereo2mono(trad, "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\der.wav", 1)
mono2estereo("D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\iz.wav", "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\der.wav", "estereo_combinado.wav")

def codEstereo(ficEste, ficCod):
    canalIz = "semisuma.wav"
    canalDer = "semidiferencia.wav"
    estereo2mono(ficEste, canalIz, 2)
    estereo2mono(ficEste, canalDer, 3)

    mono2estereo(canalIz, canalDer, ficCod)

codEstereo("trad.wav", "ficCod.wav")

def decEstereo(ficCod, ficEste):
    ficCod_monoI = "ficCod_monoI.wav"
    ficCod_monoD = "ficCod_monoD.wav"
    estereo2mono(ficCod, ficCod_monoI, 0)
    estereo2mono(ficCod, ficCod_monoD, 1)
    mono2estereo(ficCod_monoI, ficCod_monoD, ficEste)

decEstereo("ficCod.wav", "ficEste")