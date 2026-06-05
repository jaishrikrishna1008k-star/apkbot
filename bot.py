from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import zipfile
import os
import re
import shutil

TOKEN = "8866550012:AAEJ09ND5FX6AMAUxER678q1FHbEGs2lhh0"
ADMIN_ID = 8616765325

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚀 New User Started Bot\n\n"
                 f"👤 Name: {user.first_name}\n"
                 f"🆔 ID: {user.id}\n"
                 f"📛 Username: @{user.username if user.username else 'None'}"
        )
    except:
        pass

    await update.message.reply_text(
        "🗂️Please send apk."
    )

async def apk(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.document:
        return

    file = update.message.document

    if not file.file_name.lower().endswith(".apk"):
        await update.message.reply_text(
            "❌ Only send apk file."
        )
        return

    await update.message.reply_text(
        "🔍 Wait scanning in processing..."
    )

    tgfile = await file.get_file()
    apk_name = file.file_name

    await tgfile.download_to_drive(apk_name)

    extract_dir = "scan"

    try:

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        os.mkdir(extract_dir)

        with zipfile.ZipFile(apk_name, "r") as z:
            z.extractall(extract_dir)

        firebase_links = []

        for root, dirs, files in os.walk(extract_dir):

            for f in files:

                path = os.path.join(root, f)

                try:

                    with open(path, "rb") as fp:
                        content = fp.read().decode(errors="ignore")

                    links = re.findall(
                        r'https://[^\s"\']*firebaseio\.com',
                        content
                    )

                    firebase_links.extend(links)

                except:
                    pass

        firebase_links = list(set(firebase_links))

        if firebase_links:

            result = "🔥 FIREBASE FOUND\n\n"

            for link in firebase_links:
                result += f"🔗 {link}\n\n"

            result += "🌐 Now Analyze Pass :\n"
            result += "https://klvsh100.42web.io\n\n"

            await update.message.reply_text(result)

        else:

            await update.message.reply_text(
                "❌ Firebase link nahi mila."
            )

    except Exception as e:

        await update.message.reply_text(
            f"⚠️ Error:\n{e}"
        )

    finally:

        try:

            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)

            if os.path.exists(apk_name):
                os.remove(apk_name)

        except:
            pass

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        apk
    )
)

print("Bot Running...")

app.run_polling()
