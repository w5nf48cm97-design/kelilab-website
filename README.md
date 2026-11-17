# KeliLab

Catálogo web de las aplicaciones We're Out! y GeoBlock para kelilab.es.

## Contenido

Portada original, fichas de las dos apps, imágenes de producto, búsqueda, filtros, galería de capturas y páginas de privacidad pendientes de completar.

La web es estática. No incorpora cuentas, formulario, publicidad, analítica ni fuentes externas. Las imágenes se sirven desde el propio sitio.

Los enlaces a Google Play se activan al configurar las URL oficiales de las fichas. Las páginas de privacidad todavía no son políticas definitivas y no deben presentarse como tales.

## Construcción

    python3 scripts/build.py
    python3 scripts/check_site.py

No requiere paquetes externos. El resultado se genera en dist.

## Publicación

La rama main conserva las fuentes. La rama gh-pages contiene el resultado listo para servir.

En Settings → Pages, seleccionar Deploy from a branch, la rama gh-pages y la carpeta /(root).

Después de modificar las fuentes, regenerar dist y actualizar gh-pages con su contenido.

## Catálogo

Editar site.config.json para añadir las URL oficiales de Google Play. El constructor valida que sean fichas de play.google.com.

El archivo app-ads.txt solo se genera si se introduce la línea real que facilita AdMob. Nunca se publica un identificador de ejemplo.

## Imágenes

La imagen de GeoBlock fue aportada por su propietario. Los recursos de We're Out! proceden de sus repositorios. La marca gráfica de KeliLab se creó para esta web.
