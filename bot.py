import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import re
from urllib.parse import quote
from scraper import CarScraper
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")

# Initialize scraper
scraper = CarScraper()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚗  CARDZSCRAP  🚗\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "France Auto Export Sourcing Agent\n\n"
        "Enter your maximum price in EUR:\n\n"
        "🔍 Sources: AutoScout24.fr, Leboncoin.fr & LaCentrale.fr\n"
        "⛽ Fuel: Essence / Hybride only\n"
        "📅 Year: 2023+\n"
        "🛠️ Condition: Non-accidenté\n"
        "📦 Export Ready\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )


async def search_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle price input and scrape car listings."""
    text = update.message.text.strip()

    price_match = re.search(r'\d+', text.replace(" ", "").replace(",", "").replace(".", ""))
    if not price_match:
        await update.message.reply_text("Please enter a valid price (number only). Example: 10000")
        return

    max_price = int(price_match.group())
    if max_price < 1000 or max_price > 100000:
        await update.message.reply_text("Please enter a price between 1,000€ and 100,000€.")
        return

    # Send processing message
    processing_msg = await update.message.reply_text(
        "🔍 Searching for cars on all websites...\n"
        "This may take a few seconds⏳"
    )

    try:
        # Run scraping in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, scraper.scrape_all, max_price)

        # Build response
        today = datetime.now().strftime("%d/%m/%Y")

        response_text = (
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🚗  CARDZSCRAP RESULTS  🚗\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Date: {today}\n"
            f"💰 Max Price: {max_price:,}€\n"
            f"⛽ Fuel: Essence / Hybride\n"
            f"📅 Year: 2023 → {datetime.now().year}\n"
            f"🛠️ Condition: Non-accidenté\n"
            f"📦 Export Ready\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        # AutoScout24 results
        if results['autoscout24']:
            response_text += "🔗 <b>AutoScout24.fr</b> - Found {} cars:\n\n".format(
                len(results['autoscout24'])
            )
            for i, car in enumerate(results['autoscout24'], 1):
                response_text += (
                    f"{i}. <b>{car['title']}</b>\n"
                    f"   💰 {car['price']}\n"
                    f"   🔗 <a href='{car['link']}'>View listing</a>\n\n"
                )
        else:
            response_text += "❌ <b>AutoScout24.fr</b> - No cars found\n\n"

        # Leboncoin results
        if results['leboncoin']:
            response_text += "🔗 <b>Leboncoin.fr</b> - Found {} cars:\n\n".format(
                len(results['leboncoin'])
            )
            for i, car in enumerate(results['leboncoin'], 1):
                response_text += (
                    f"{i}. <b>{car['title']}</b>\n"
                    f"   💰 {car['price']}\n"
                    f"   🔗 <a href='{car['link']}'>View listing</a>\n\n"
                )
        else:
            response_text += "❌ <b>Leboncoin.fr</b> - No cars found\n\n"

        # LaCentrale results
        if results['lacentrale']:
            response_text += "🔗 <b>LaCentrale.fr</b> - Found {} cars:\n\n".format(
                len(results['lacentrale'])
            )
            for i, car in enumerate(results['lacentrale'], 1):
                response_text += (
                    f"{i}. <b>{car['title']}</b>\n"
                    f"   💰 {car['price']}\n"
                    f"   🔗 <a href='{car['link']}'>View listing</a>\n\n"
                )
        else:
            response_text += "❌ <b>LaCentrale.fr</b> - No cars found\n\n"

        response_text += (
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ All listings direct links!\n"
            "Click any link to view full details.\n\n"
            "💡 Tip: Save this message to check\n"
            "new listings daily.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Powered by CARDZSCRAP 🚗"
        )

        # Delete processing message and send results
        await processing_msg.delete()
        await update.message.reply_text(response_text, parse_mode='HTML')

    except Exception as e:
        logger.error(f"Scraping error: {e}")
        await processing_msg.delete()
        await update.message.reply_text(
            f"❌ Error searching for cars: {str(e)}\n\n"
            "Please try again later."
        )


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_cars))
    logger.info("CARDZSCRAP Bot started - Scraping AutoScout24.fr, Leboncoin.fr & LaCentrale.fr")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
