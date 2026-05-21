# Sonido estéreo y ficheros WAVE

## Xavi Fernández Rodríguez

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Xavi Fernández Rodríguez

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

Ejecutamos el archivo .py en la consola de JupyterLab para commprobar el funcionamiento del codigo
<img width="513" height="248" alt="image" src="https://github.com/user-attachments/assets/fee5f171-40b3-47f6-a1c4-7bf20c22b5a3" />


#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).



##### Código de `estereo2mono()`
```python
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
 ```


##### Código de `mono2estereo()`
```python
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
```

##### Código de `codEstereo()`
```python 
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
```

##### Código de `decEstereo()`
```python
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
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
