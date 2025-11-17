import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from telethon import TelegramClient
from telethon.tl import types, functions
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_path = os.path.join(os.getcwd(), "erich.session")

app = FastAPI()

client = TelegramClient(session_path, api_id, api_hash)


# ===============================
#   ARRANCAR TELETHON
# ===============================
@app.on_event("startup")
async def startup():
    print("Iniciando Telegram Client…")
    await client.start()
    print("Telegram Client LISTO.")

# ===============================
#   ENDPOINT /story
# ===============================
@app.post("/story")
async def story(payload: dict):
    if "imageUrl" not in payload:
        return JSONResponse({"ok": False, "error": "imageUrl es requerido"}, status_code=400)

    image_url = payload["imageUrl"]
    caption = payload.get("caption", "")

    print("Descargando imagen:", image_url)
    r = requests.get(image_url)

    if r.status_code >= 400:
        return JSONResponse({"ok": False, "error": "No se pudo descargar imagen"}, status_code=400)

    img_bytes = r.content

    try:
        print("Subiendo imagen…")
        uploaded = await client.upload_file(img_bytes, file_name="story.jpg")

        print("Enviando Story…")
        result = await client(functions.stories.SendStoryRequest(
            # peer=await client.get_input_entity("me"),
			peer=await client.get_input_entity("@qvapay"),
            media=types.InputMediaUploadedPhoto(file=uploaded),
            caption=caption,
            privacy_rules=[types.InputPrivacyValueAllowAll()]
        ))

        print("Story enviada!")
        return {"ok": True, "result": str(result)}

    except Exception as e:
        print("ERROR:", e)
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.get("/health")
async def health():
    return {"ok": True, "status": "running"}
