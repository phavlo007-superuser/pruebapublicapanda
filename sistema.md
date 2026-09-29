# S.I.S.T.E.M.A. · Avance de pendientes Ventas/Ingenieria · Etapa 1: construir mi sistema

Lee este documento completo antes de escribir código. Trabaja por fases:
antes de cada una dime qué vas a hacer y espera mi aprobación.
Mis datos: lo que se cuenta está en datos/ (Excel .xlsx o .csv) y lo que se lee
en contexto/ (.md). No uses ninguna otra fuente.

## S · Situación
Cada lunes el director comercial pide el avance de pendientes de clientes  y alguien tarda la mañana cruzando el excel con la tabla de datos, pendientes

## I · Identidad del usuario
Quién lo usa: El director comercial, los lunes, antes de la junta con gerentes.
Quién más lo consulta: Equipo comercial y de ingenieria, entre visitas, previo a la junta semanal.

## S · Sistema objetivo
Voy a construir una automatización. En la etapa 2 se conecta a Telegram.

## T · Tablas y datos
Qué entra: Export de oportunidades por cliente, RFQs, actividades del año y la tabla de pendientes por cada persona del equipo comercial y por cliente.
Lo que se lee (contexto/):
- archivo general de pendientes de cada persona del equipo comercial
Lo que se cuenta (datos/):
- Cliente
- Actividad
- Responsable
- Tipo de pendiente
- Sector
- Fecha de apertura
- Fecha de cierre
- Comentarios
- proyecto
Lo que no entra:
- todo entra
Para cuadrar: separar los pendientes por responsable, cliente, tipo de pendiente
Tablas que quiero en mi base: propónmelas tú, una por cada .csv de datos/.

## E · Experiencia
Qué hace, paso a paso:
- Revisa el archivo de pendientes, agrupa los pendientes, por cliente, responsable, tipo de pendiente (tooling, entregas, RFQ), crea una tabla para colocar las fechas de inicio, fin, semaforo, columna de comentarios
Qué me entrega: un dashboard interactivo que se puede actualizar por cada responsable para el llenado de sus actividades.
Cuándo corre: cada que el excel se actualiza.
Al inicio del resultado, un párrafo corto que redacta la IA con lo más importante.

## M · Modelo técnico (ya viene en mi kit; no lo cambies)
- Esta carpeta es mi kit de hatchvps. Lee CLAUDE.md y LEEME.md y respeta sus reglas.
- Base PostgreSQL propia. Conéctate solo con db.py (db.conectar(), db.leer_tabla()).
  Desde mi laptop necesita ./tunel.sh abierto en otra terminal: si da
  "connection refused", avísame que falta el túnel.
- Carga los .csv por lotes (chunksize=1000), nombres de tabla en minúsculas y
  sin espacios. Antes de reemplazar una tabla que ya tiene datos, pregúntame.
- Automatización: un script automatizacion.py que lee mi base con db.py y
  escribe su resultado en salidas/ (un reporte .html de una página, o un .csv).
  No uses app.py. Que corra en menos de 150 segundos.
- Publicación: ./deploy.sh. El servidor ejecuta el script al subirlo y la salida
  queda en la dirección de LEEME.md. Si falla, revisa _ejecucion.log.
- Librerías: ya están instaladas en el servidor (streamlit, pandas, plotly,
  psycopg). No agregues nada a requirements.txt salvo que sea indispensable.
- IA: Claude Haiku 4.5 (claude-haiku-4-5) con el SDK anthropic, que ya está instalado en el servidor.
- Llave de IA: ANTHROPIC_API_KEY en .env (yo ya pegué el valor al final del archivo).
- Crea ia.py con una función preguntar(instruccion, datos) que use esa llave.
  Todo lo que use IA en este sistema, y el agente de la etapa 2, pasa por ahí.
  Respuestas en español; si la llamada falla, que el sistema siga funcionando.
- Fuente de datos: solo mis archivos de datos/ y contexto/, cargados a mi base.
  No te conectes a otros servicios, APIs externas ni MCP en esta versión.
- Nunca escribas llaves ni contraseñas en el código ni me las muestres.
- Después de publicar, cada cambio que te pida y yo apruebe súbelo con
  ./deploy.sh y dame la URL. No me dejes cambios sin subir.

## A · Acciones y entregables
Lo que hace y lo que entrega: Dashboard de avances por responsable, cliente, tipo de pendiente, fecha de apertura, fecha de cierre. estatus, graficas,.
No entra en la v1:
- Ranking público entre responsables
Preguntas que le haré por Telegram en la etapa 2:
- ¿que pendiente esta vencido?
- ¿que cliente esta afectado?
- ¿Que tipo de pendiente es, cotizacion, contrato, tooling, calidad, entregas?

Fases de esta etapa:
1. Plan: revisa el kit, contexto/ y datos/. Dime qué tablas vas a crear, con
   cuántas filas cada una, y qué vas a construir. Revisa en .env (solo nombres,
   nunca valores) que mi llave de IA tenga valor.
2. Datos: lee mis archivos de datos/ (si hay .xlsx y falta openpyxl, instálalo
   solo en mi laptop), límpialos según la letra T, guárdalos como .csv y
   cárgalos a mi base. Confírmame el conteo de cada tabla,
   y que cuadre con lo que dice «Para cuadrar».
3. IA: crea ia.py y pruébala una vez con una pregunta corta sobre mis datos.
   Dime qué contestó (sin mostrar la llave).
4. Automatización: construye automatizacion.py y córrela en mi laptop.
   Muéstrame la salida y las cifras que trae.
5. Publicación: súbela con ./deploy.sh y dame la URL de la salida.
6. Cierre: lista de archivos que creaste o cambiaste.