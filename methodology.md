# Metodología

## Carpeta contenedora

El nombre de la carpeta será el evento al que hacen referencia las fotos.
Fotos de un evento similar en distinta fecha se almacenarán en la misma carpeta.

```
|
|__ Pirineos
|
|__ Piscina de buitrago
|
|__ Valladolid
```

## Nombrada

El nombre de la foto está formado por el evento y la fecha.

```
|
|__ Piscina Buitrago 20130824-163526.jpg
|
|__ Piscina Buitrago 20130824-194745.jpg
```

El renombrado de las fotos es automático con el script `add\_tag.py` descrito en la siguiente sección.

## Etiquetado

El etiquetado consta de una etiqueta principal relativa al evento, otras etiquetas relacionadas y el etiquetado de las
personas presentes en la foto.

### Etiqueta principal

La etiqueta principal contiene el evento (suele coincidir con el nombre usado en la carpeta).

```
> Pirineos
> Piscina Buitrago
```

El script `add\_main_tag.py` renombra todas las fotos de la carpeta y les inserta la etiqueta principal.

```bash
# Usa "Pirineos" como nombre del fichero y etiqueta principal.
$ ./add_main_tag.py Pirineos
# Usa "Pirineos" como nombre del fichero y "Montaña" como etiqueta principal.
$ ./add_main_tag.py Pirineos Montaña
```
### Etiquetas secundarias

Las etiquetas secundarias son añadidas a través del script `add_tag.py`.

```bash
# Etiquetamos la foto `prueba.jpg` con 3 etiquetas
$ ./add_tag.py prueba.jpg Montaña Playa Costa
```

### Personas

Para etiquetar las personas en una foto se usa el script `add\_people.py`, además del fichero de texto `Nombres.txt`.
En el fichero de texto se encuentran los nombre y se usa su número de línea en el script.

```bash
# Etiqueta la foto `prueba.jpg` con 3 personas
$ ./add_people.py prueba.jpg 4 7 10
```
