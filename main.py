from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_from_directory,
)

import os
import threading
from file_fun import clear_directory

app = Flask(__name__)

# 上传文件存储目录
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def perform_cleanup():
    clear_directory()
    # 每隔一段时间（例如，每小时）执行清理操作
    timer = threading.Timer(3600, perform_cleanup)
    timer.start()


@app.route("/")
def index():
    return render_template("index.html")


# 显示上传文件列表的路由
@app.route("/uploads")
def show_uploads():
    filenames = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("uploads.html", filenames=filenames)


# 处理文件上传的路由
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)

    files = request.files.getlist("file")

    for file in files:
        if file.filename == "":
            return "No selected file"

        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

    return render_template("index.html", message="Files uploaded successfully!")



@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


if __name__ == "__main__":
    # 确保上传目录存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # 启动清理操作的计时器
    perform_cleanup()

    app.run(host="0.0.0.0")
