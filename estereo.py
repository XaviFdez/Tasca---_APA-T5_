"""
estereo.py
 
Autor: Xavi Fernandez Rodriguez
 
Descripción:
    Módulo para el manejo de señales de audio estéreo en formato WAVE PCM lineal
    de 16 bits. Incluye funciones para:
 
    - Separar/mezclar los canales de una señal estéreo (estereo2mono, mono2estereo).
    - Codificar/decodificar una señal estéreo usando los 16 bits más significativos
      para la semisuma y los 16 bits menos significativos para la semidiferencia,
      de forma compatible con sistemas monofónicos (codEstereo, decEstereo).
 
    Solo se usa la biblioteca estándar struct para la lectura y escritura de
    datos binarios. No se importa ningún otro módulo externo.
"""
 
import struct
 
 
# ---------------------------------------------------------------------------
# Constantes y helpers de cabecera WAVE
# ---------------------------------------------------------------------------
 
_FMT_RIFF_HDR  = '<4sI4s'          # 'RIFF', tamaño, 'WAVE'
_FMT_CHUNK_HDR = '<4sI'            # identificador, tamaño
_FMT_PCM_BODY  = '<HHIIHH'         # audioFmt, nCh, sRate, bRate, blkAlign, bps
 
 
def _lee_cabecera(f):
    """
    Lee y valida la cabecera completa de un fichero WAVE PCM.
 
    Devuelve un diccionario con los campos de la cabecera fmt y el
    offset (en bytes desde el inicio del fichero) donde comienzan
    los datos del cacho 'data', junto con su tamaño.
 
    Eleva ValueError si el fichero no es un WAVE PCM válido.
    """
    # Cacho RIFF
    riff_raw = f.read(struct.calcsize(_FMT_RIFF_HDR))
    if len(riff_raw) < struct.calcsize(_FMT_RIFF_HDR):
        raise ValueError("Fichero demasiado corto para ser WAVE.")
    riff_id, riff_size, wave_id = struct.unpack(_FMT_RIFF_HDR, riff_raw)
    if riff_id != b'RIFF':
        raise ValueError(f"No es un fichero RIFF (encontrado: {riff_id}).")
    if wave_id != b'WAVE':
        raise ValueError(f"No es un fichero WAVE (encontrado: {wave_id}).")
 
    hdr = {}
    data_offset = None
    data_size   = None
 
    # Recorremos los subcachos hasta encontrar 'fmt ' y 'data'
    while True:
        chunk_hdr_raw = f.read(struct.calcsize(_FMT_CHUNK_HDR))
        if len(chunk_hdr_raw) < struct.calcsize(_FMT_CHUNK_HDR):
            break
        chunk_id, chunk_size = struct.unpack(_FMT_CHUNK_HDR, chunk_hdr_raw)
 
        if chunk_id == b'fmt ':
            fmt_raw = f.read(chunk_size)
            fields = struct.unpack_from(_FMT_PCM_BODY, fmt_raw)
            hdr['audioFmt']  = fields[0]   # 1 = PCM lineal
            hdr['nChannels'] = fields[1]
            hdr['sRate']     = fields[2]   # frecuencia de muestreo
            hdr['bRate']     = fields[3]   # bytes por segundo
            hdr['blkAlign']  = fields[4]   # alineamiento de bloque
            hdr['bps']       = fields[5]   # bits por muestra
            if hdr['audioFmt'] != 1:
                raise ValueError("Solo se admite PCM lineal (audioFmt=1).")
        elif chunk_id == b'data':
            data_offset = f.tell()
            data_size   = chunk_size
            break                          # los datos siguen a continuación
        else:
            # Cacho desconocido: lo saltamos
            f.seek(chunk_size, 1)
 
    if not hdr:
        raise ValueError("No se encontró el subcacho 'fmt '.")
    if data_offset is None:
        raise ValueError("No se encontró el subcacho 'data'.")
 
    hdr['dataOffset'] = data_offset
    hdr['dataSize']   = data_size
    return hdr
 
 
def _escribe_cabecera(f, n_channels, srate, bps, data_size):
    """
    Escribe la cabecera WAVE completa (RIFF + fmt + data) en el fichero f,
    que debe estar abierto en modo escritura binaria y posicionado al inicio.
    """
    blk_align = n_channels * (bps // 8)
    byte_rate  = srate * blk_align
 
    fmt_body = struct.pack(_FMT_PCM_BODY,
                           1,           # PCM lineal
                           n_channels,
                           srate,
                           byte_rate,
                           blk_align,
                           bps)
 
    fmt_chunk  = struct.pack(_FMT_CHUNK_HDR, b'fmt ', len(fmt_body)) + fmt_body
    data_chunk_hdr = struct.pack(_FMT_CHUNK_HDR, b'data', data_size)
 
    # Tamaño RIFF = 4 bytes ('WAVE') + tamaño fmt chunk + tamaño data chunk
    riff_size = 4 + len(fmt_chunk) + struct.calcsize(_FMT_CHUNK_HDR) + data_size
    riff_chunk = struct.pack(_FMT_RIFF_HDR, b'RIFF', riff_size, b'WAVE')
 
    f.write(riff_chunk + fmt_chunk + data_chunk_hdr)
 
 
# ---------------------------------------------------------------------------
# estereo2mono
# ---------------------------------------------------------------------------
 
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y escribe en ficMono
    una señal monofónica de 16 bits según el valor de canal:
 
        canal=0  ->  canal izquierdo  L
        canal=1  ->  canal derecho    R
        canal=2  ->  semisuma         (L+R)//2   [por defecto]
        canal=3  ->  semidiferencia   (L-R)//2
 
    Eleva ValueError si el fichero de entrada no es WAVE estéreo PCM 16 bits,
    o si canal no está en {0,1,2,3}.
    """
    if canal not in (0, 1, 2, 3):
        raise ValueError(f"canal debe ser 0, 1, 2 o 3 (recibido: {canal}).")
 
    with open(ficEste, 'rb') as fe:
        hdr = _lee_cabecera(fe)
        if hdr['nChannels'] != 2:
            raise ValueError("El fichero de entrada no es estéreo.")
        if hdr['bps'] != 16:
            raise ValueError("Solo se admiten ficheros de 16 bits por muestra.")
 
        n_muestras = hdr['dataSize'] // (2 * 2)   # 2 bytes × 2 canales
        fmt_par    = f'<{2 * n_muestras}h'         # alternando L, R, L, R, …
        raw        = fe.read(hdr['dataSize'])
 
    pares = struct.unpack(fmt_par, raw)
 
    # Separamos L y R con slicing (sin bucles)
    L = pares[0::2]
    R = pares[1::2]
 
    mono = (
        L                                           if canal == 0 else
        R                                           if canal == 1 else
        tuple((l + r) // 2 for l, r in zip(L, R))  if canal == 2 else
        tuple((l - r) // 2 for l, r in zip(L, R))
    )
 
    data_bytes = struct.pack(f'<{n_muestras}h', *mono)
 
    with open(ficMono, 'wb') as fm:
        _escribe_cabecera(fm, 1, hdr['sRate'], 16, len(data_bytes))
        fm.write(data_bytes)
 
 
# ---------------------------------------------------------------------------
# mono2estereo
# ---------------------------------------------------------------------------
 
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros WAVE monofónicos ficIzq (canal izquierdo) y ficDer
    (canal derecho), ambos PCM de 16 bits y con la misma frecuencia de
    muestreo, y construye con ellos un fichero WAVE estéreo ficEste.
 
    Eleva ValueError si alguno de los ficheros no cumple los requisitos o
    si sus frecuencias de muestreo difieren.
    """
    with open(ficIzq, 'rb') as fi:
        hdr_i = _lee_cabecera(fi)
        if hdr_i['nChannels'] != 1:
            raise ValueError("ficIzq no es monofónico.")
        if hdr_i['bps'] != 16:
            raise ValueError("ficIzq no es de 16 bits.")
        raw_i = fi.read(hdr_i['dataSize'])
 
    with open(ficDer, 'rb') as fd:
        hdr_d = _lee_cabecera(fd)
        if hdr_d['nChannels'] != 1:
            raise ValueError("ficDer no es monofónico.")
        if hdr_d['bps'] != 16:
            raise ValueError("ficDer no es de 16 bits.")
        raw_d = fd.read(hdr_d['dataSize'])
 
    if hdr_i['sRate'] != hdr_d['sRate']:
        raise ValueError("Las frecuencias de muestreo de ficIzq y ficDer difieren.")
 
    n = min(hdr_i['dataSize'], hdr_d['dataSize']) // 2
    L = struct.unpack(f'<{n}h', raw_i[:n * 2])
    R = struct.unpack(f'<{n}h', raw_d[:n * 2])
 
    # Entrelazamos L y R: L[0], R[0], L[1], R[1], …
    entrelazado = [v for par in zip(L, R) for v in par]
    data_bytes  = struct.pack(f'<{2 * n}h', *entrelazado)
 
    with open(ficEste, 'wb') as fe:
        _escribe_cabecera(fe, 2, hdr_i['sRate'], 16, len(data_bytes))
        fe.write(data_bytes)
 
 
# ---------------------------------------------------------------------------
# codEstereo
# ---------------------------------------------------------------------------
 
def codEstereo(ficEste, ficCod):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y genera ficCod,
    un fichero WAVE monofónico de 32 bits donde:
 
        bits 31..16  (más significativos)  ->  semisuma   (L+R)//2
        bits 15..0   (menos significativos) ->  semidiferencia (L-R)//2
 
    El resultado es compatible con reproductores monofónicos, que ven
    prácticamente la semisuma, con la semidiferencia como ruido inaudible
    (≈ 90 dB por debajo).
 
    Eleva ValueError si ficEste no es WAVE estéreo PCM 16 bits.
    """
    with open(ficEste, 'rb') as fe:
        hdr = _lee_cabecera(fe)
        if hdr['nChannels'] != 2:
            raise ValueError("El fichero de entrada no es estéreo.")
        if hdr['bps'] != 16:
            raise ValueError("Solo se admiten ficheros de 16 bits por muestra.")
 
        n_muestras = hdr['dataSize'] // 4
        raw        = fe.read(hdr['dataSize'])
 
    pares = struct.unpack(f'<{2 * n_muestras}h', raw)
    L = pares[0::2]
    R = pares[1::2]
 
    # Empaquetamos semisuma en los 16 bits altos y semidiferencia en los bajos
    # usando un entero con signo de 32 bits: (semisuma << 16) | (semidif & 0xFFFF)
    cod = tuple(
        (((l + r) // 2) << 16) | (((l - r) // 2) & 0xFFFF)
        for l, r in zip(L, R)
    )
    data_bytes = struct.pack(f'<{n_muestras}i', *cod)
 
    with open(ficCod, 'wb') as fc:
        _escribe_cabecera(fc, 1, hdr['sRate'], 32, len(data_bytes))
        fc.write(data_bytes)
 
 
# ---------------------------------------------------------------------------
# decEstereo
# ---------------------------------------------------------------------------
 
def decEstereo(ficCod, ficEste):
    """
    Lee el fichero WAVE monofónico ficCod de 32 bits (codificado con
    codEstereo) y reconstruye el fichero WAVE estéreo ficEste con PCM
    de 16 bits.
 
    Los 16 bits más significativos contienen la semisuma M = (L+R)//2 y
    los 16 bits menos significativos la semidiferencia D = (L-R)//2.
    La reconstrucción es:  L = M + D,  R = M - D.
 
    Eleva ValueError si ficCod no es WAVE monofónico PCM 32 bits.
    """
    with open(ficCod, 'rb') as fc:
        hdr = _lee_cabecera(fc)
        if hdr['nChannels'] != 1:
            raise ValueError("ficCod no es monofónico.")
        if hdr['bps'] != 32:
            raise ValueError("ficCod no es de 32 bits por muestra.")
 
        n_muestras = hdr['dataSize'] // 4
        raw        = fc.read(hdr['dataSize'])
 
    cod = struct.unpack(f'<{n_muestras}i', raw)
 
    # Extraemos semisuma (bits 31..16) y semidiferencia (bits 15..0, con signo)
    M = tuple(c >> 16          for c in cod)          # semisuma, con signo
    # semidiferencia: extendemos el signo desde el bit 15
    D = tuple(
        (c & 0xFFFF) if (c & 0x8000) == 0 else (c & 0xFFFF) - 0x10000
        for c in cod
    )
 
    L = tuple(m + d for m, d in zip(M, D))
    R = tuple(m - d for m, d in zip(M, D))
 
    # Saturamos a [-32768, 32767] por si hay desbordamiento
    clamp = lambda v: max(-32768, min(32767, v))
    L = tuple(clamp(v) for v in L)
    R = tuple(clamp(v) for v in R)
 
    entrelazado = [v for par in zip(L, R) for v in par]
    data_bytes  = struct.pack(f'<{2 * n_muestras}h', *entrelazado)
 
    with open(ficEste, 'wb') as fe:
        _escribe_cabecera(fe, 2, hdr['sRate'], 16, len(data_bytes))
        fe.write(data_bytes)