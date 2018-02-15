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

### Etiquetas

Para etiquetar se usa el script `add\_tag.py`.

La etiqueta principal (Subject) contiene el evento (suele coincidir con el nombre usado en la carpeta).

```
> Pirineos
> Piscina Buitrago
```

Con la opción `-s` se especifica el evento principal.
Además con la opción `-r` se renombran las fotos usando la etiqueta principal.

```bash
# Usa "Pirineos" como nombre del fichero y etiqueta principal.
$ ./add_tag.py -r -s Pirineos
# Usa "Pirineos" como nombre del fichero y "Montaña" como etiqueta principal.
$ ./add_main_tag.py -R Pirineos -s Montaña
```
El resto de parámetros son etiquetas secundarias que se añadirán en las fotografías.

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
