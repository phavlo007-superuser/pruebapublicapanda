# Proyecto de capacitación — despliegue en hatchvps

Ayudas al alumno a construir y publicar dashboards, apps y agentes en Python.
El alumno NO necesariamente programa: explica en palabras simples lo que haces.

## La base de datos es SOLO de este alumno

- Conéctate **siempre** con las variables del archivo `.env`. Usa el módulo
  `db.py` que ya viene en el kit: `db.conectar()` y `db.leer_tabla("nombre")`.
- **Nunca** pidas, inventes ni uses otras credenciales, ni te conectes a otra base.
- Dentro de esta base puedes crear, modificar y borrar tablas con libertad.
- **Nunca** ejecutes `DROP DATABASE`, `CREATE ROLE`, `ALTER ROLE`, `GRANT` ni
  `REVOKE`. No tienes permiso y solo vas a generar errores confusos.
- **Antes de borrar o reemplazar una tabla que ya tiene datos, pregúntale al
  alumno.** Puede ser el trabajo de toda su sesión.

## Cómo conectarte, según dónde corra el código

| Dónde corre | Qué usa | Requisito |
|---|---|---|
| En tu computadora (limpiar y cargar datos) | `DATABASE_URL_LOCAL` | tener `./tunel.sh` corriendo en otra terminal |
| Ya desplegado en el servidor (app, bot) | `DATABASE_URL` | nada, es automático |

`db.py` elige la correcta solo. Si al conectarte desde la laptop da
"connection refused", casi siempre es que **falta abrir el túnel**: dile al
alumno que corra `./tunel.sh` y lo deje abierto.

## Al cargar datos

- Carga **por lotes** (`chunksize=1000` en pandas). Una sola sentencia que tarde
  más de 60 segundos se corta sola: es un freno del servidor, no un error tuyo.
- No abras una transacción y la dejes esperando: a los 120 segundos ociosa se
  cierra, porque una transacción abierta bloquea tablas para todos.

## Desplegar

Cuando el alumno diga «publica», «despliega» o «súbelo», ejecuta:

```
./deploy.sh
```

Es lo único que hace falta: sube todo por SFTP y **el servidor se encarga del
resto solo** (publica los estáticos, ejecuta los `.py` y levanta `app.py` como
app en vivo). No hay commit, ni git push, ni nada que tocar en el servidor.

**Cada vez que cambies el código hay que volver a correrlo.** No hay sincronía
automática: el servidor solo ve lo que le subes. Si el alumno dice «no se ve mi
cambio», lo primero es comprobar si ya publicaste después de editar.

El ciclo completo es: editas → `./deploy.sh` → unos 10 segundos → está en línea.
**No relances la app ni reinicies nada**: al subir un `.py`, el servidor la
vuelve a levantar solo. Si el alumno no ve el cambio en el navegador después de
esos segundos, pídele que recargue forzando (Cmd+Shift+R / Ctrl+F5).

## La base de datos NO se sube

Es la confusión más común, y conviene que se la aclares al alumno:

- **Su código** vive en su computadora y se copia al servidor con `./deploy.sh`.
- **Sus datos** viven SOLO en el servidor. No hay copia local, así que **no hay
  nada que subir**: cuando cargas datos por el túnel, ya los estás escribiendo
  directamente en la base que usa su app publicada.

Consecuencia que importa: lo que le hagas a la base **pasa de inmediato y es
real**. Un `DROP TABLE` borra el trabajo del alumno sin deshacer posible. Por eso
hay que preguntarle antes de borrar o reemplazar cualquier tabla con datos.

Si responde `permission denied`, la primera vez hay que dar permiso:
`chmod +x deploy.sh`.

Queda publicado en:
- Estático / salidas de scripts:  https://hatchvps.com/iaang01/pablodavila/
- App en vivo (Streamlit):        https://hatchvps.com/iaang01/pablodavila/app/

## Qué hace el servidor solo, al subir

- **Archivos estáticos** (index.html, css, imágenes): se publican tal cual.
- **Script .py que genera archivos**: el servidor lo ejecuta en unos segundos.
  Revisa `_ejecucion.log` si algo falla.
- **App web en vivo**: el archivo principal debe llamarse **`app.py`**.
  Dependencias extra → `requirements.txt` (ya viene uno).

## El front de Streamlit

Usa la plantilla `app.py` que ya está en el kit. **Conserva `@st.cache_resource`
en la función de conexión**: sin eso Streamlit abre una conexión nueva cada vez
que el usuario mueve un filtro, y con 36 alumnos a la vez se agota la base.
No abras conexiones dentro de los callbacks ni en cada recarga.

## El bot de Telegram

Plantilla en `bot.py`. El token va en `.env` (`TELEGRAM_TOKEN`), se lo da
@BotFather. Lee la misma tabla con la misma función `db.leer_tabla`.

## Convenciones

- Ya instaladas: pandas, numpy, matplotlib, plotly, requests, beautifulsoup4,
  streamlit, gradio, flask, fastapi, uvicorn, sqlalchemy, psycopg, python-dotenv,
  python-telegram-bot, anthropic, openai.
- Panel web de la base (para mirar datos a mano):
  https://hatchvps.com/db/?pgsql=alumnos-db&username=iaang01_pablodavila&db=iaang01_pablodavila_db
- **Secretos**: en `.env`. Nunca los escribas dentro del código ni los pegues
  en un chat. Nunca subas el kit a un repositorio público.

## Problemas que vas a tener que resolver tú, no el alumno

- **El sitio responde 403.** Falta un `index.html` en la raíz. El servidor no
  inventa portada. Crea uno y vuelve a publicar.
- **«no space left on device» al publicar.** Se llenaron los 500 MB. Lo que casi
  siempre sobra: `venv/`, `node_modules/`, videos y CSV grandes. **No subas
  `venv` ni `node_modules`**: el servidor instala lo que haga falta. `deploy.sh`
  ya los excluye, pero revisa que no haya copias con otro nombre.
- **La app no levanta.** En orden: que el archivo se llame exactamente `app.py`,
  que lo que importas exista, y que no se caiga al arrancar por una variable
  faltante en `.env`. El registro del último intento está en `_ejecucion.log`,
  dentro de la carpeta publicada.
- **«too many connections».** Son 8 por alumno. Suele ser que quedaron procesos
  abiertos, o que el front abre conexión en cada recarga: revisa que la función
  de conexión conserve `@st.cache_resource`.
- **El alumno no ve su cambio.** Primero comprueba si publicaste después de
  editar; si sí, pídele que recargue forzando (Cmd+Shift+R / Ctrl+F5).

## Límites por alumno

500 MB de archivos · 200 MB de base de datos · 8 conexiones simultáneas ·
consultas máx 60 s · scripts máx 150 s · apps 1 GB RAM / 1 CPU.
