from flask import Flask, request, send_file,jsonify
from eureka_client import EurekaClient
import qrcode
from PIL import Image

app = Flask(__name__)

@app.route('/qrservice', methods=["POST"])
def post():
   content=request.json
   userid = content["userid"]
   return createQR(userid)
@app.route('/qrservice', methods=["GET"])
def get():
   content = request.json
   userid = content["userid"]
   try:
      return getQR(userid)
   except Exception as e:
      print("Bu kullanıcıya ait QR bulunamadı")


def createQR(userid):
   code = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=50,
      border=2
   )
   code.add_data(f'www.zartzurt.com?userid={userid}')
   code.make(fit=True)
   image = code.make_image(fill_color="white", back_color="black")
   image.save(f'./images/{userid}.png','PNG')
   filename=f'{userid}.png'
   return send_file(filename,mimetype='image/png')

def getQR(userid):
   im = Image.open(f'./images/{userid}.png',)
   im.show()

if __name__ == '__main__':
   client = EurekaClient(eureka_server="http://localhost:8761/eureka")
   client.register(app_name="qr-service", host_name="localhost", port=5000)
   app.run()
