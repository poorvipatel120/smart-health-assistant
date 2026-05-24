from flask import Flask, render_template, request, session ,redirect, url_for


app = Flask(__name__)
app.secret_key = "health_tracker"


@app.route('/', methods=['GET', 'POST'])
def home():

    result = ""
    recommendation = ""
    reminder = ""
    status = ""

    health_score = 100
    bmi = 0
    bmi_category = ""
    ai_tip = ""

    if 'records' not in session:
        session['records'] = []

    if request.method == 'POST':
        date = request.form.get('date', 'No Date')
        systolic = int(request.form['systolic'])
        diastolic = int(request.form['diastolic'])
        sugar = int(request.form['sugar'])

        height = float(request.form['height'])
        weight = float(request.form['weight'])

        medicine_name = request.form['medicine_name']
        medicine_time = request.form['medicine_time']

        # ---------------- BLOOD PRESSURE ANALYSIS ----------------

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
            bp_flag = "normal"

        # ---------------- SUGAR ANALYSIS ----------------

        if sugar > 200:
            result += "⚠️ Sugar Level Very High\n"
            health_score -= 20

        elif sugar > 140:
            result += "⚠️ Prediabetes Risk\n"
            health_score -= 10

        else:
            result += "✅ Sugar Level Normal\n"

        # ---------------- STATUS ----------------

        if bp_flag == "critical":
            status = "red"

        elif bp_flag == "high":
            status = "orange"

        elif sugar > 200:
            status = "red"

        elif sugar > 140 or bp_flag == "low":
            status = "orange"

        else:
            status = "green"

        # ---------------- BMI ----------------

        height_in_meter = height / 100
        bmi = weight / (height_in_meter * height_in_meter)

        if bmi < 18.5:
            bmi_category = "⚠️ Underweight"
        elif bmi < 25:
            bmi_category = "✅ Healthy"
        elif bmi < 30:
            bmi_category = "⚠️ Overweight"
        else:
            bmi_category = "🔴 Obese"

        if bmi > 25:
            health_score -= 15

        # ---------------- AI TIPS ----------------

        if sugar > 140:
            ai_tip += "🍭 Avoid sweets today.\n"

        if systolic > 140:
            ai_tip += "🧂 Reduce salty foods.\n"

        if systolic < 90:
            ai_tip += "💧 Increase hydration.\n"

        if bmi > 25:
            ai_tip += "🏃 Exercise daily.\n"

        if ai_tip == "":
            ai_tip = "✅ Keep maintaining a healthy lifestyle."

        # ---------------- STORE RECORD ----------------

        records = session['records']

        records.append({
            "date": date,
            "systolic": systolic,
            "diastolic": diastolic,
            "sugar": sugar,
            "bmi": round(bmi, 1),
            "status": status,
            "medicine_name": medicine_name,
            "medicine_time": medicine_time
        })

        session['records'] = records

        # ---------------- RECOMMENDATION ----------------

        recommendation = """
• Drink enough water
• Exercise regularly
• Avoid excess sugar and salt
• Sleep properly
• Take medicines on time
"""

        # ---------------- REMINDER ----------------

        reminder = f"💊 Take {medicine_name} at {medicine_time}"

    return render_template(
        'index.html',
        result=result,
        recommendation=recommendation,
        reminder=reminder,
        status=status,
        bmi=round(bmi, 1),
        bmi_category=bmi_category,
        health_score=health_score,
        ai_tip=ai_tip,
        records=session.get('records', [])
    )

@app.route('/delete/<int:index>')
def delete(index):

    records = session.get('records', [])

    if 0 <= index < len(records):
        records.pop(index)

    session['records'] = records

    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
