# KeliLab

Catálogo estático de We're Out! y GeoBlock para kelilab.es.

## Estado de esta entrega

Diseño original, navegación responsive, fichas de las dos apps, imágenes auténticas, búsqueda, filtros, galería ampliable, rutas de privacidad y página 404.

La web no incorpora cuentas, formulario, cookies, analítica, fuentes externas ni publicidad. Las imágenes se sirven desde el propio sitio.

Las políticas están expresamente marcadas como borradores. No presentarlas en Google Play ni AdMob hasta completar los datos del titular, contacto, versión publicada y servicios reales. Los enlaces de Play permanecen pendientes hasta recibir las URL oficiales. No se inventa un ID de AdMob.

## Construcción

Ejecutar desde esta carpeta:

    python3 scripts/build.py

No requiere paquetes externos. El resultado completo está en dist.

## Configuración

Editar site.config.json para mantener el catálogo y añadir las URL oficiales de Google Play.

- playUrl: URL HTTPS de la ficha concreta en play.google.com/store/apps/details?id=...
- publicContactEmail y legalOwner: pendientes de confirmación.
- adMobPublisherLine: copiar la línea exacta de app-ads.txt que ofrece AdMob. No usar el ID de aplicación ni el ID de bloque de anuncios.

El constructor solo genera app-ads.txt cuando hay un registro válido confirmado. Si el registro está vacío, no publica un archivo de ejemplo engañoso.

Los textos de privacidad para revisión están en content/privacy-drafts.json. Cambiar una etiqueta de estado no convierte el texto en una política definitiva: completar y contrastar su contenido antes de modificar la presentación.

## Publicación en GitHub Pages

Repositorio propuesto: w5nf48cm97-design/kelilab-website.

El flujo de publicación despliega dist. Al activar GitHub Pages, seleccionar GitHub Actions como fuente. El dominio de producción previsto es kelilab.es; dist/CNAME contiene ese dominio.

Consultar docs/PUESTA_EN_MARCHA.md para DNS y los datos de lanzamiento pendientes.

## Imágenes

- We're Out!: icono y capturas reales de los repositorios del propietario.
- GeoBlock: imagen aportada por el propietario en esta conversación.
- KeliLab: marca gráfica SVG creada para esta web.

No se incluyen reseñas, cifras de descargas, clasificaciones por edad, precios ni testimonios inventados.
