from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
#from flask_uploads import UploadSet
from google.cloud import storage
import settings

app = Flask(__name__)
logger = settings.getLogger("Function_Subida_API")
#media = UploadSet('media', ('mp4'))

@app.route('/upload_video', methods=['POST'])
def upload_video(request=request):
    try:
        if "video" in request.files:
            logger.info("Uploading the video")
            video = request.files["video"]
            filename = video.name
            filename = f"/tmp/{filename}b.mp4"
            video.save(filename)
            client = storage.Client()
            bucket = client.get_bucket('dona_sonrisa')
            blob = bucket.blob(filename)
            blob.upload_from_filename(filename)
            return "Ok"

    except Exception as err:
        raise err

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(port=8080, debug=True, threaded=True)
