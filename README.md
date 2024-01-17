# Chinese Text-to-Image Prompt Refiner

## Files

- `demos`: Demo videos for our product.
- `backend`: The back-end source code folder.
- `front`: The front-end source code folder.
- `src`: Source file folder for data processing.
- `eval`: Source file folder for evaluation.


## Usage

Add `backend/backend/config.json` as following:

```json
{
    "kimi_api_key": "Your kimi API key" ,
    "image_sk": "Your Text2Image sk",
    "image_ak": "Your Text2Image ak"
}
```

For running the front-back end framework:

```bash
python backend/manage.py runserver 127.0.0.1:8080
streamlit run front/web_chat.py # --server.fileWatcherType none
```

## Requirements

You can get all the python packages by using `pip install -r requirements.txt`.

```
clip==0.2.0
datasets==2.16.1
diffusers==0.25.0
Django==5.0.1
matplotlib==3.6.1
numpy==1.23.4
openai==1.7.2
pandas==2.1.4
Pillow==9.3.0
Pillow==10.2.0
PyJWT==2.8.0
Requests==2.31.0
streamlit==1.30.0
streamlit_chat==0.1.1
torch==1.13.0
torchmetrics==1.3.0
torchvision==0.14.0
tqdm==4.66.1
webdataset==0.2.86
```