import os
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'


users = [
    {"username": "yaacov", "password": "star", "uploaded_images": []},
    {"username": "anaelle", "password": "star10", "uploaded_images": []},
    {"username": "batsi", "password": "star20", "uploaded_images": []}
]

@app.route("/")
def start():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_form():
    print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Do something with the form data (e.g., validate, process, save to a database)
    print(f"username is : {username}")
    print(f"password is : {password}")
    for user in users:
        if username == user["username"] and password == user["password"]:
            return redirect(url_for('user_images', username=username))
    not_found = True
    return render_template("login.html", not_found=not_found)


@app.route("/upload", methods=["POST"])
def upload():
    username = request.form.get('username')  # Get the username from the form
    print(f"username is currently {username}")
    for user in users:
        print(f"current user is {user}")
        if username == user["username"]:
            if "photo" in request.files:
                photo = request.files["photo"]
                if photo:
                    # Save the uploaded photo to the user's list of uploaded_images
                    user["uploaded_images"].append(photo.filename)
                    print(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
                    print(user["uploaded_images"])
                    return redirect(url_for('user_images', username=username))  # Redirect to user_images page
    return "No file provided."

@app.route("/user_images/<username>")
def user_images(username):
    for user in users:
        if username == user["username"]:
            uploaded_images = user["uploaded_images"]
            return render_template("user_images.html", username=username, uploaded_images=uploaded_images)
    return "User not found"

if __name__ == "__main__":
    app.run(debug=True)


