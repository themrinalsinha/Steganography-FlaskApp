from flask import Flask, request, url_for, render_template, jsonify, redirect
from flask_mysqldb import MySQL
import random, string, uuid, json, os

# Custom Modules.
from xterminate_enc import *
from xterminate_stegano import *
from send_mail import *

app = Flask(__name__)

# File directory.
UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + "/static/"

# Connecting to the database.
app.config['MYSQL_HOST'] = 'localhost';
app.config['MYSQL_USER'] = 'root';
app.config['MYSQL_PASSWORD'] = 'root';
app.config['MYSQL_DB'] = 'stegano_db';

mysql = MySQL(app)

# ---------------------------------------------

# GENERATING USER KEY GLOBALLY
def enc_key():
    ekey = str(uuid.uuid4())
    k = []
    for x in ekey.split('-'):
        k.append(x)
    enc_key = ''.join(k)
    return str(enc_key)

# ---------------------------------------------


@app.route("/")
def index():
    # print(UPLOAD_DIR)
    # UPLOAD_FOLDER = os.path.join(UPLOAD_DIR, 'images/')
    # print(UPLOAD_FOLDER)

    return render_template("index.html")

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':

        UPLOAD_FOLDER = os.path.join(UPLOAD_DIR, 'original_images/')
        print(UPLOAD_FOLDER)

        # Request Image
        img_file = request.files['image_file']
        img_file_name = img_file.filename

        # Checking if upload folder exists.
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        img_file_name = img_file.filename
        print(img_file_name)
        string_img_name = str(img_file_name)
        # destination = "/".join([UPLOAD_FOLDER, img_file_name])
        destination = "".join([UPLOAD_FOLDER, img_file_name])
        print(destination)
        # string_img_path = str(destination)
        img_file.save(destination)

        # Requesting Message.
        message = request.form['message']

        # Generating encryption key (256-bit)
        encryption_key = enc_key()
        string_enc_key = str(encryption_key)
        # ekey = str(uuid.uuid4())
        # k = []
        # for x in ekey.split('-'):
        #     k.append(x)
        # enc_key = ''.join(k)
        # string_enc_key = str(enc_key)

        # Generating User key.
        user_key = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(16)])
        string_user_key = str(user_key)

        # --------------------------------------------------

        # msg_with_key = message + encryption_key
        #
        # # Encrypting message before sending.
        # cipher_text = xterm_encrypt(message, string_enc_key)
        # print(cipher_text)
        # sliced_ct = cipher_text[2:-1]
        # key_with_ct = string_enc_key + str(sliced_ct)

        # --------------------------------------------------

        # Encrypting Obtained image.
        xterm_steg_enc(destination, message)

        # Inserting files into databases.
        try:
            c = mysql.connection.cursor()
            print("Connected Successfully to database...")

            c.execute("INSERT INTO stegano(user_key,enc_key,enc_image) VALUES (%s, %s, %s)""",(string_user_key, string_enc_key, string_img_name))
            # c.execute("INSERT INTO steg_tb(user_key,enc_image) VALUES (%s, %s)""",(string_user_key, string_img_name))
            mysql.connection.commit()
            print("Data inserted Successfully...")
        except Exception as e:
            print(str(e))

        # return ("User access key : {}".format(user_key))
        # return redirect(url_for('send_mail', token = user_key))
        return render_template("email.html", access_key = user_key)
        # cursor.execute()
    else:
        return "Use POST method, IDIOT..."


#----------------------------------------------------------

# Setting up email client to send token.

@app.route("/email", methods=['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        user_key = request.form['token']
        email = request.form['email']
        remark = request.form['remark_tb']
        xterm_mail(email, user_key, remark)

    return("Mail Sent...")


#----------------------------------------------------------





@app.route("/reveal")
def reveal():
    return(render_template("index1.html"))

@app.route("/retrival", methods=['GET','POST'])
def retrival():
    # global key
    key = request.form['token_id']

    ENC_FOLDER = os.path.join(UPLOAD_DIR, 'enc_images/')
    try:
        c = mysql.connection.cursor()
        print("Connected Successfully to database...")
        # global key
        print(key)
        key = str(key)
        qry = "SELECT enc_image FROM stegano WHERE user_key = %s"
        val = key
        c.execute(qry, tuple([val]))
        i = c.fetchall()
        print("------------------", i)
        im_nm = (i[0][0])
        print(im_nm)

        dec_text = xterm_steg_dec(im_nm)
        print(dec_text)
        str_img = str(im_nm)

        # -------------------------------------------------

        # Decrepting message before displaying.
        # dec_msg = xterm_steg_dec(im_nm)
        # print("Segano decrepted image : ", dec_msg)
        # print(type(dec_msg))
        # # temp_data = str.encode()
        # e_key = dec_msg[0:32]
        # print("Key : ", e_key)
        #
        # msg = dec_msg[32:]
        # print("TEST 1 :", msg)
        # msg_test = msg[2:-1]
        # print("TEST 1 :", type(msg_test))
        #
        # msg_t_enc = str.encode(msg_test)
        # # msg_encode = str.encode(msg)
        # # print("TEST 2 :", msg_encode)
        # # print("TEST 2 :", type(msg_encode))
        # # msg_x = msg_encode(msg)
        # # print(msg_x)
        # # print(type(msg_x))
        # # msg_x = "V8XxHlEneWiB9Dvcthn/tlSZPqkuSti9qxi4y"
        # print(xterm_decrypt(msg_t_enc, e_key))
        # # cut_zx = zx[34:]
        # # print(cut_zx)
        # # print(type(cut_zx))
        # # print(cut_zx)
        # # print(decrypt(cut_zx, key))
        #
        # # print("Access key : {}".format(e_key))
        # -------------------------------------------------

        # return (render_template("index1.html", i_path = str_img))
    except Exception as e:
        print(str(e))
    # return "Hello..."
    return (render_template("index1.html", i_path = str_img, dec_text = dec_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)
