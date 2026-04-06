from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from mypgvector.embed_image import pg_store_image

VOICE_FOLDER = "uploads/voice"
IMAGE_FOLDER = "uploads/images"
DOC_FOLDER = "uploads/docs"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

UPLOAD_TYPE = ["IMAGE", "VOICE", "DOCS"]

# Create folder if not exists
os.makedirs(VOICE_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(DOC_FOLDER, exist_ok=True)

# Allowed file extensions (optional)
IMAGE_ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
# Allowed file extensions (optional)
VOICE_ALLOWED_EXTENSIONS = {"webm", "wav"}
DOCS_ALLOWED_EXTENSIONS = {"pdf", "xls"}


def allowed_file(filename, file_type):
    print("File Type is ", file_type)
    if file_type == UPLOAD_TYPE[0]:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
    elif file_type == UPLOAD_TYPE[1]:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in VOICE_ALLOWED_EXTENSIONS
    elif file_type == UPLOAD_TYPE[2]:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in DOCS_ALLOWED_EXTENSIONS


def check_upload_file(request_file):
    if "file" not in request_file:
        return jsonify({"error": "No file part in request"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    return file


# os.chdir("..")
print("Folder Path is :", os.getcwd())
app = Flask(__name__, template_folder=os.getcwd() + "/templates")
CORS(app)


@app.route("/")
def home():
    print("current path:", request.full_path)
    return render_template("upload.html")


@app.route("/chat")
def my_chat():
    print("current path:", request.full_path)
    return render_template("chat.html")


@app.route("/upload")
def my_upload():
    print("current path:", request.full_path)
    return render_template("upload.html")


@app.route("/list")
def my_files():
    print("current path:", request.full_path)
    return render_template("files.html")


@app.route("/record")
def my_record():
    print("current path:", request.full_path)
    return render_template("myrecord.html")


def get_folder(file_type):
    if file_type is None:
        file_type = "docs"
    if file_type.upper() == UPLOAD_TYPE[0]:
        folder_path = os.getcwd() + "/" + IMAGE_FOLDER
    elif file_type.upper() == UPLOAD_TYPE[1]:
        folder_path = os.getcwd() + "/" + VOICE_FOLDER
    else:
        folder_path = os.getcwd() + "/" + DOC_FOLDER
    return folder_path


@app.route("/files")
def get_files():
    response = jsonify({"error": "valid query types are ?type=[docs/image/voice]"})
    file_type = request.args.get('type')
    print("File Type  is :", file_type)
    folder_path = get_folder(file_type)
    print("Folder Path :", folder_path)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        pdf_files = [f for f in os.listdir(folder_path)]
        response = json.dumps({i: v for i, v in enumerate(pdf_files)})
    return response


@app.route("/deletefile", methods=["DELETE"])
def delete_file():
    response = jsonify({"error": "select file name"})
    file_type = request.args.get('type')
    folder_path = get_folder(file_type)
    filename = request.args.get('file')
    print("File name ", filename)
    if filename is not None:
        file_path = folder_path + "/" + filename
        print(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)
            response = jsonify({"message": "File deleted successfully", "filename": filename}), 200
    return response


def save_file(file, folder):
    print("file is saving,", file.filename)
    filepath = os.path.join(folder, file.filename)
    file.save(filepath)


@app.route("/upload_docs", methods=["POST"])
def upload_docs():
    print("in Upload docs method")
    file_type = request.headers.get("type")
    print("File TYoe is :", file_type)
    file = check_upload_file(request.files)
    # Check if type is image
    if file_type.upper() == UPLOAD_TYPE[0]:
        if file and allowed_file(file.filename, UPLOAD_TYPE[0]):
            save_file(file, IMAGE_FOLDER)
            return jsonify({"message": "File uploaded and inserted to Vector Database successfully",
                            "filename": file.filename}), 200
        else:
            print("in else part")
            return jsonify({"error": "File type not allowed"}), 400
    elif file_type.upper() == UPLOAD_TYPE[1]:  # check if file type voice
        if file and allowed_file(file.filename, UPLOAD_TYPE[1]):
            save_file(file, VOICE_FOLDER)
            return jsonify({"message": "File uploaded and inserted to Vector Database successfully",
                            "filename": file.filename}), 200
        else:
            print("in else part")
            return jsonify({"error": "File type not allowed"}), 400
    elif file_type.upper() == UPLOAD_TYPE[2]:  # check if file type doc
        if file and allowed_file(file.filename, UPLOAD_TYPE[2]):
            save_file(file, DOC_FOLDER)
            return jsonify({"message": "File uploaded and inserted to Vector Database successfully",
                            "filename": file.filename}), 200
        else:
            print("in else part")
            return jsonify({"error": "File type not allowed"}), 400


@app.route("/embedimage", methods=["POST"])
def embed_image():
    response = jsonify({"error": "select file name"})
    file_type = request.args.get('type')
    upload_folder = get_folder(file_type)
    filename = request.args.get('file')
    if filename is not None:
        file_path = upload_folder + "/" + filename
        if os.path.isfile(file_path):
            pg_store_image(file_path)
            response = jsonify({"message": "Image File Embeded successfully", "filename": filename}), 200
        else:
            response = jsonify({"message": "File not found", "filename": filename}), 200
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7890, debug=True)
