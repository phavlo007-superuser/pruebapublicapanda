# Tu kit para publicar en hatchvps

Este kit YA está listo y conectado (incluye tu llave de acceso .hatch_key).

## Qué hacer
1. Copia TODOS estos archivos a la carpeta de tu proyecto.
2. Para publicar, corre:   ./deploy.sh   (o dile a Claude Code: "despliega mi proyecto")

## Tus enlaces
- Tu sitio:          https://hatchvps.com/iaang01/pablodavila/
- Tu base de datos:  https://hatchvps.com/db/?pgsql=alumnos-db&username=iaang01_pablodavila&db=iaang01_pablodavila_db  (usuario y clave en el archivo .env)

----------------------------------------
CONECTARTE A TU BASE DESDE TU COMPUTADORA
----------------------------------------
Tu base no esta abierta a internet, para que nadie mas que tu la toque.
Para que tu agente pueda cargarle datos:

   1. Abre una terminal y corre:   ./tunel.sh
   2. DEJA ESA VENTANA ABIERTA mientras trabajes.
   3. En otra terminal trabaja normal.

El archivo db.py ya sabe conectarse solo; no tienes que configurar nada.
Tu app, una vez publicada, se conecta sola y NO necesita el tunel.

Si tu agente dice "connection refused": casi siempre es que falta el tunel.

----------------------------------------
CADA VEZ QUE CAMBIES ALGO
----------------------------------------
   Editas tu codigo  ->  ./deploy.sh  ->  ~10 segundos  ->  ya esta en linea

No hay que reiniciar nada: el servidor vuelve a levantar tu app solo.
Si no ves el cambio, recarga forzando (Cmd+Shift+R o Ctrl+F5).

OJO: tu CODIGO se sube cada vez. Tus DATOS no: viven solo en el servidor,
asi que cuando tu agente los carga por el tunel ya quedaron ahi. No hay
que "subir la base" despues.

----------------------------------------
LO QUE TRAE ESTE KIT
----------------------------------------
- tunel.sh         abre el paso a tu base de datos
- db.py            la conexion ya resuelta (no lo toques)
- app.py           tu front en Streamlit, listo para modificar
- bot.py           tu bot de Telegram (pon el token en .env)
- requirements.txt las librerias de tu proyecto
- deploy.sh        publica todo

## Importante
- NO borres el archivo `.hatch_key` — es tu llave de acceso.
- NO subas tu kit a un repositorio público (contiene tu llave y tu .env).
- ⚠️ Al terminar el curso (15/12/2026) se ELIMINARÁ todo: tus archivos, tu base de datos y tus accesos. Respalda tu trabajo antes de esa fecha.

> Guía completa en línea, siempre actualizada: https://hatchvps.com/guia
