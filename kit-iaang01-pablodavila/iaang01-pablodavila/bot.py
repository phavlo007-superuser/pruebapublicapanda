"""Tu bot de Telegram. Usa la MISMA base y la misma función de lectura.

Antes de publicarlo:
  1. Pídele un token a @BotFather en Telegram.
  2. Pégalo en el archivo .env, en TELEGRAM_TOKEN.
  3. ./deploy.sh
"""
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import db

TABLA = "ventas"   # <- la misma tabla que usa tu front


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hola. Comandos:\n"
        "/total  — cuántos registros hay\n"
        "/resumen — un resumen de tus datos"
    )


async def total(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    datos = db.leer_tabla(TABLA)
    if datos is None:
        await update.message.reply_text(
            f"Todavía no existe la tabla «{TABLA}». Cárgala primero."
        )
        return
    await update.message.reply_text(f"{len(datos):,} registros en «{TABLA}».")


async def resumen(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    datos = db.leer_tabla(TABLA)
    if datos is None:
        await update.message.reply_text(f"Todavía no existe la tabla «{TABLA}».")
        return
    numericas = datos.select_dtypes("number")
    if numericas.empty:
        await update.message.reply_text("Tu tabla no tiene columnas numéricas.")
        return
    lineas = [f"{c}: suma {numericas[c].sum():,.2f} · media {numericas[c].mean():,.2f}"
              for c in numericas.columns[:5]]
    await update.message.reply_text("\n".join(lineas))


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN") or db.os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("Falta TELEGRAM_TOKEN en tu archivo .env")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("total", total))
    app.add_handler(CommandHandler("resumen", resumen))
    app.run_polling()


if __name__ == "__main__":
    main()
