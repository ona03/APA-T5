"Funciones para el manejo de señal estéreo y su codificación y descodificación"

import struct as st
# import soundfile as sf
# import sounddevice as sd

def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste, "rb") as fp_estereo:
        format = "<4sI4s" #little endian
        buffer = fp_estereo.read(st.calcsize(format))
        chunk_id, chunk_size, riff_format = st.unpack(format, buffer)
        
        if chunk_id != b"RIFF" or riff_format != b"WAVE":
            raise TypeError("File '{wav_file}' is not WAV file")

        fp_estereo.seek(36, 0)
        format = "<4sI"
        buffer = fp_estereo.read(st.calcsize(format))
        subchunk_id, subchunk2_size = st.unpack(format, buffer)

        fp_estereo.seek(0, os.SEEK_END)
        llarg = fp_estereo.tell() - 44
        format = "<4s"
        buffer = fp_estereo.read(llarg)
        print(buffer)
        dataE = st.unpack(format, buffer)
        print(dataE)

        # print(fp_estereo.tell())
        # sample_num = subchunk2_size // 2
        # sabem que per cada canal tenim 2 bytes de cada mostra
        # format = "<"
        # fp_estereo.read(44)
        # buffer = bin(int(fp_estereo.read(), 16))
        # buffer = int(fp_estereo.read(), 16)
        # buffer = [int(str(data), 16) for data in buffer]
        
        # fp_estereo.seek(44, 0)
        # format = "<4s"
        # buffer = [fp_estereo[i].read(st.calcsize(format)) for i in range(subchunk2_size)]
        # buffer = fp_estereo.read()
        # buffer = [buffer[i] for i in range(int(buffer))]
        # print(buffer)
        # dataE = st.unpack(format, buffer)
        # buffer = bytes.fromhex(fp_estereo.read())
        # for byte in fp_estereo.read():
        #     buffer = format(byte, '08b')
        # a = fp_estereo.read(44)
        # bytese = bytes(a) + bytes(buffer)
        # print(buffer)
#         dataE = st.unpack(format, buffer)

#     with open(ficMono, "wb") as fp_mono:
#         # capçalera
#         format = "<4sI4s"
#         buffer = st.pack(format, b'RIFF', 36 + 2*len(dataE), b"WAVE")
#         fp_mono.write(buffer)
#         fp_mono.write(b"fmt")
#         format = "<I2H2I2H"
#         buffer = st.pack(format, 16, 1, 1, 22050, 44100, 16, 16)
#         fp_mono.write(buffer)
#         fp_mono.write(b"data")
#         format = "<I"
#         buffer = st.pack(format, 2*len(dataE))
#         fp_mono.write(buffer)
#         format = "<2s"

#         if canal == 0:
#             dataM = dataE[::2]
#             buffer = st.pack(format, dataM)
#             fp_mono.write(buffer)
#         elif canal == 1:
#             dataM = dataE[1::2]
#             buffer = st.pack(format, dataM)
#             fp_mono.write(buffer)
#         elif canal == 2:
#             dataM = [(L+R)/2 for L, R in dataE] #semisuma
#             buffer = st.pack(format, dataM)
#             fp_mono.write(buffer)
#         elif canal == 3:
#             dataM = [(L-R)/2 for L, R in dataE] #semidiferència
#             buffer = st.pack(format, dataM)
#             fp_mono.write(buffer)

#     return ficMono

# sortida = []
import os 
os.getcwd()
ficEste = "D:\Enginyeria de Sistemes Audiovisuals\Algorísmia i Programació Audiovisual\APA-T5\wav\komm.wav"
estereo2mono(ficEste, "kommoo.wav", 1)