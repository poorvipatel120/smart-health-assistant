from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "health_tracker"


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    recommendation = ""
    reminder = ""
    status = ""

    health_score = 100

    bmi = 0
    bmi_category = ""

    ai_tip = ""

    if "records" not in session:
        session["records"] = []


    if request.method == "POST":

        # PATIENT DETAILS

        name = request.form["name"]
        date = request.form["date"]

        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])

        sugar = int(request.form["sugar"])

        height = float(request.form["height"])
        weight = float(request.form["weight"])

        medicine_name = request.form["medicine_name"]


        # BLOOD PRESSURE ANALYSIS

        bp_flag = "normal"

        if systolic > 140 or diastolic > 90:
            result += "⚠️ High Blood Pressure Detected\n"
            bp_flag = "high"
            health_score -= 20


        elif systolic < 80 or diastolic < 50:
            result += "🔴 Very Low Blood Pressure Detected\n"
            bp_flag = "critical"
            health_score -= 25


        elif systolic < 90 or diastolic < 60:
            result += "⚠️ Low Blood Pressure Detected\n"
            bp_flag = "low"
            health_score -= 15


        else:
            result += "✅ Blood Pressure Normal\n"



        # SUGAR ANALYSIS

        if sugar > 200:
            result += "⚠️ Sugar Level Very High\n"
            health_score -= 20


        elif sugar > 140:
            result += "⚠️ Prediabetes Risk\n"
            health_score -= 10


        else:
            result += "✅ Sugar Level Normal\n"



        # HEALTH STATUS COLOR

        if bp_flag == "critical" or sugar > 200:
            status = "red"


        elif bp_flag in ["high", "low"] or sugar > 140:
            status = "orange"


        else:
            status = "green"



        # BMI CALCULATION

        height_meter = height / 100

        bmi = weight / (height_meter * height_meter)


        if bmi < 18.5:
            bmi_category = "⚠️ Underweight"


        elif bmi < 25:
            bmi_category = "✅ Healthy"


        elif bmi < 30:
            bmi_category = "⚠️ Overweight"
            health_score -= 10


        else:
            bmi_category = "🔴 Obese"
            health_score -= 20



        # AI HEALTH SUGGESTIONS

        if sugar > 140:
            ai_tip += "🍭 Avoid sweets today.\n"


        if systolic > 140:
            ai_tip += "🧂 Reduce salty foods.\n"


        if systolic < 90:
            ai_tip += "💧 Drink more water.\n"


        if bmi > 25:
            ai_tip += "🏃 Exercise at least 30 minutes daily.\n"



        if ai_tip == "":
            ai_tip = "✅ Keep maintaining your healthy lifestyle."



        # RECOMMENDATIONS

        recommendation = """
• Drink enough water
• Exercise regularly
• Avoid excess sugar and salt
• Eat healthy food
• Sleep 7-8 hours daily
• Take medicines regularly
"""



        # MEDICINE REMINDER

        reminder = f"💊 Medicine: {medicine_name}"



        # SAVE HEALTH RECORD

        records = session["records"]

        records.append({

            "name": name,
            "date": date,

            "systolic": systolic,
            "diastolic": diastolic,

            "sugar": sugar,

            "bmi": round(bmi,1),

            "status": status,

            "medicine_name": medicine_name

        })


        session["records"] = records



    return render_template(

        "index.html",

        result=result,

        recommendation=recommendation,

        reminder=reminder,

        status=status,

        bmi=round(bmi,1),

        bmi_category=bmi_category,

        health_score=health_score,

        ai_tip=ai_tip,

        records=session.get("records", [])

    )



@app.route("/delete/<int:index>")
def delete(index):

    records = session.get("records", [])

    if 0 <= index < len(records):
        records.pop(index)


    session["records"] = records

    return redirect(url_for("home"))



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )
