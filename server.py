import os
import requests
from datetime import datetime
# from flask import send_file
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from telethon import TelegramClient
from telethon.tl import types, functions
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_path = os.path.join(os.getcwd(), "erich.session")
app = FastAPI()
client = TelegramClient(session_path, api_id, api_hash)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_RUBIK_BOLD = os.path.join(BASE_DIR, "fonts", "Rubik-Bold.ttf")
FONT_RUBIK_REGULAR = os.path.join(BASE_DIR, "fonts", "Rubik-Regular.ttf")

def render_rates_video(
    input_path="rates.mp4",
    output_path="rates_final.mp4",
    cup=None,
    mlc=None,
    cla=None,
    etecsa=None,
	tropical=None
):
    """
    Renderiza el video de tasas con valores CUP / MLC / CLA / ETECSA
    """

    # ================================
    # Tamaño del video 1080x1920
    # ================================
    VIDEO_W = 1080
    VIDEO_H = 1920

    # Coordenadas EXACTAS detectadas en tu plantilla
    CUP_POS = (90, 640)
    MLC_POS = (90, 790)
    CLA_POS = (90, 940)
    ETECSA_POS = (90, 1090)
    TROPICAL_POS = (90, 1240)

    # FONT = "Rubik-Bold"   # Fuente instalada en el sistema
    FONTSIZE = 100        # Tamaño ajustado para tu video

    clip = VideoFileClip(input_path)
    overlays = []

    if cup:
        txt_cup = TextClip(
            f"CUP: {cup}",
            fontsize=FONTSIZE,
            color="white",
            font=FONT_RUBIK_BOLD,
            kerning=2
        ).set_position(CUP_POS).set_duration(clip.duration)
        overlays.append(txt_cup)

    if mlc:
        txt_mlc = TextClip(
            f"MLC: {mlc}",
            fontsize=FONTSIZE,
            color="white",
            font=FONT_RUBIK_BOLD,
            kerning=2
        ).set_position(MLC_POS).set_duration(clip.duration)
        overlays.append(txt_mlc)

    if cla:
        txt_cla = TextClip(
            f"CLA: {cla}",
            fontsize=FONTSIZE,
            color="white",
            font=FONT_RUBIK_BOLD,
            kerning=2
        ).set_position(CLA_POS).set_duration(clip.duration)
        overlays.append(txt_cla)

    if etecsa:
        txt_etecsa = TextClip(
            f"ETECSA: {etecsa}",
            fontsize=FONTSIZE,
            color="white",
            font=FONT_RUBIK_BOLD,
            kerning=2
        ).set_position(ETECSA_POS).set_duration(clip.duration)
        overlays.append(txt_etecsa)

    if tropical:
        txt_tropical = TextClip(
            f"Tropical: {tropical}",
            fontsize=FONTSIZE,
            color="white",
            font=FONT_RUBIK_BOLD,
            kerning=2
        ).set_position(TROPICAL_POS).set_duration(clip.duration)
        overlays.append(txt_tropical)

    today = datetime.now().strftime('%d/%m/%Y')
    date_label = TextClip(
        f"Actualizado: {today}",
        fontsize=35,                 # tamaño elegante y legible
        color="white",
        font="Rubik-Bold",
        stroke_color="black",        # para contraste
        stroke_width=2
    ).set_position(
        ("center", 1875)
    ).set_duration(clip.duration)
    overlays.append(date_label)

    final = CompositeVideoClip([clip] + overlays)
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset="slow",
        bitrate="2500k",
        threads=4,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-profile:v", "main", "-level:v", "3.1", "-movflags", "+faststart"]
    )

    return output_path

# ===============================
#   SEND STORY VIDEO
# ===============================
async def send_story_video_async(video_path, caption, entity):

    with open(video_path, "rb") as f:
        data = f.read()

    uploaded = await client.upload_file(data, file_name="rates_final.mp4")

    result = await client(functions.stories.SendStoryRequest(
        peer=entity,
        media=types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type="video/mp4",
            attributes=[
                types.DocumentAttributeVideo(
                    duration=25,
                    w=1080,
                    h=1920,
                    supports_streaming=True
                )
            ]
        ),
        caption=caption,
        privacy_rules=[types.InputPrivacyValueAllowAll()]
    ))

    return result

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

@app.post("/storyVideo")
async def story_video_handler(payload: dict):

    cup = payload.get("cup", "0")
    mlc = payload.get("mlc", "0")
    cla = payload.get("cla", "0")
    etecsa = payload.get("etecsa", "0")
    tropical = payload.get("tropical", "0")
    caption = payload.get("caption", "")

    video_in = "rates.mp4"
    video_out = "rates_final.mp4"

    print("Renderizando video con valores dinámicos…")
    render_rates_video(
        input_path=video_in,
        output_path=video_out,
        cup=cup,
        mlc=mlc,
        cla=cla,
        etecsa=etecsa,
        tropical=tropical
    )

    print("Subiendo Story…")
    # entity = await client.get_input_entity("me")
    entity = await client.get_input_entity("@qvapay")
    result = await send_story_video_async(video_out, caption, entity)

    # return {"ok": True, "result": str(result)}
    return {"ok": True, "result": "Story enviada!"}