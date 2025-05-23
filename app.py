from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Thay bằng chuỗi bí mật an toàn

df = pd.read_csv("quy_doi_diem_hsa.csv", encoding='latin1')

def convert_hsa_to_thpt(hsa_score):
    try:
        hsa_rounded = round(hsa_score)
        if hsa_rounded in df["HSA"].values:
            row = df[df["HSA"] == hsa_rounded].iloc[0]
            return {
                "A00": row["A00"],
                "B00": row["B00"],
                "C00": row["C00"],
                "D01": row["D01"],
                "A01": row["A01"]
            }
        else:
            return {"error": f"Không có dữ liệu cho điểm HSA {hsa_rounded}"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    last_hsa_score = session.get('last_hsa_score', None)

    if request.method == "POST":
        try:
            hsa_score = float(request.form["hsa_score"])
            if 17 <= hsa_score <= 129:
                result = convert_hsa_to_thpt(hsa_score)
                session['last_hsa_score'] = hsa_score
                last_hsa_score = hsa_score
            else:
                result = {"error": "Chỉ hỗ trợ điểm HSA từ 17 đến 129"}
        except:
            result = {"error": "Vui lòng nhập điểm hợp lệ"}

    return render_template("index.html", result=result, last_hsa_score=last_hsa_score)