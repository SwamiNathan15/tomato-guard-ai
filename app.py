from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ---------------- SOLUTIONS DATABASE ----------------
solutions_db = {
    "Tomato_Bacterial_spot": [
        "Spray with a copper-based organic fungicide.",
        "Remove and destroy infected plant parts.",
        "Avoid overhead watering."
    ],
    "Tomato_Early_blight": [
        "Prune lower leaves to improve airflow.",
        "Apply neem oil or baking soda spray.",
        "Use mulch to prevent soil splash."
    ],
    "Tomato_Late_blight": [
        "Remove infected plants immediately.",
        "Apply copper spray preventively.",
        "Ensure wide plant spacing."
    ],
    "Tomato_Leaf_Mold": [
        "Increase air circulation.",
        "Water at the base only.",
        "Apply sulfur-based fungicide."
    ],
    "Tomato_Septoria_leaf_spot": [
        "Remove fallen infected leaves.",
        "Apply copper-based fungicides.",
        "Rotate crops every 2–3 years."
    ],
    "Tomato_Spider_mites_Two_spotted_spider_mite": [
        "Introduce ladybugs.",
        "Spray leaves with water.",
        "Use neem oil or insecticidal soap."
    ],
    "Tomato_Target_Spot": [
        "Remove infected debris.",
        "Improve air circulation.",
        "Avoid excess nitrogen fertilizer."
    ],
    "Tomato_Tomato_YellowLeaf__Curl_Virus": [
        "Control whiteflies with sticky traps.",
        "Use reflective mulch.",
        "Remove infected plants."
    ],
    "Tomato_Tomato_mosaic_virus": [
        "Disinfect tools regularly.",
        "Remove infected plants.",
        "Control aphids and weeds."
    ],
    "Tomato_healthy": [
        "Plant appears healthy.",
        "Continue regular monitoring.",
        "Maintain good soil nutrition."
    ]
}

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- UPLOAD (GET REDIRECT) ----------------
@app.route("/upload", methods=["GET"])
def upload_redirect():
    return redirect("/")

# ---------------- UPLOAD (POST) ----------------
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return redirect("/")

    image = request.files["image"]
    if image.filename == "":
        return redirect("/")

    filename = secure_filename(image.filename)
    image_path = os.path.join("static", "uploads", filename)
    os.makedirs("static/uploads", exist_ok=True)
    image.save(image_path)

    image_url = "/" + image_path.replace("\\", "/")

    # 🔴 TEMP SIMULATION (replace with model later)
    predicted_class = "Tomato_Septoria_leaf_spot"
    confidence = 94.24

    solutions = solutions_db.get(
        predicted_class,
        ["Consult an agricultural expert."]
    )

    return render_template(
        "index.html",
        result=predicted_class,
        confidence=f"{confidence:.2f}%",
        danger="🟠 ACT SOON",
        solution=solutions,
        image_url=image_url
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
