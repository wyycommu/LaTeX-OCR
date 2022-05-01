# Adapted from https://github.com/kingyiusuen/image-to-latex/blob/main/api/app.py

from http import HTTPStatus
from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image
from io import BytesIO
from pix2tex.cli import LatexOCR

model = None
app = FastAPI(title='pix2tex API')


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


@app.on_event('startup')
async def load_model():
    global model
    if model is None:
        model = LatexOCR()


@app.get('/')
def root():
    '''Health check.'''
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
        'data': {},
    }
    return response


@app.post('/predict/')
async def predict(file: UploadFile = File(...)):
    global model
    image = Image.open(file.file)
    return model(image)


@app.post('/bytes/')
async def predict_from_bytes(file: bytes = File(...)): #, size: str = Form(...)
    global model
    #size = tuple(int(a) for a in size.split(','))
    image = Image.open(BytesIO(file))
    return model(image, resize=False)