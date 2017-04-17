import os
from stegano import lsb

UPLOAD_ENC_IMAGE = os.path.dirname(os.path.abspath(__file__)) + "/static/enc_image/"

def xterm_steg_enc(image, message):
    filename = os.path.basename(image)
    x = lsb.hide(image, message)

    if not os.path.isdir(UPLOAD_ENC_IMAGE):
        os.mkdir(UPLOAD_ENC_IMAGE)

    output = x.save('/'.join([UPLOAD_ENC_IMAGE, filename]))
    # x.save("enc.png")
    return "Data stored in image..."

def xterm_steg_dec(image):
    image = UPLOAD_ENC_IMAGE + image
    message = lsb.reveal(image)
    return message

if __name__ == "__main__":
    main()


# secret = lsb.hide("tms.png", "Hello World")
# secret.save("outp.png")
#
# x = lsb.reveal("outp.png")
# print(x)
