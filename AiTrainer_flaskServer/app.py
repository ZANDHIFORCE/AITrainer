from flask import Flask, request, render_template
import sys
import subprocess

app = Flask(__name__)

# HTML 폼 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 자세교정
@app.route('/posture')
def posture():
    return render_template('1_posture_correction.html')

# 강도추천
@app.route('/intensity')
def intensity():
    return render_template('2_intensity_recommendation.html')

# 식단제안
@app.route('/diet')
def diet():
    return render_template('3_diet suggestions.html')


#자세교정과정
@app.route('/process', methods=['POST'])
def process():
    image_url = request.form['image_url']
    try:
        result = subprocess.run(
            [ sys.executable, 'ask2GTP_posture.py', image_url],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:  # 성공적으로 실행된 경우
            output = result.stdout.strip()
        else:  # 실행 실패
            output = f"Error: {result.stderr.strip()}"
    except Exception as e:
        output = f"Exception occurred: {e}"
    
    return render_template('1_posture_correction_result.html', image_url=image_url, output=output)

#골격근계산 및 스쿼트 강도 추천
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        smm = float(request.form['smm'])

        if gender == 'male':
            muscle_mass = 0.244 * weight + 0.078 * height - 2.2
        elif gender == 'female':
            muscle_mass = 0.197 * weight + 0.072 * height - 2.5
        else:
            raise ValueError("Invalid gender selected.")
        
        if muscle_mass*1.1 < smm:
            level = "Strong Novice"
            intensity = weight*1.25 if gender=='male' else weight*0.75
        else:
            level = "Beginner"
            intensity = weight*0.75 if gender=='male' else weight*0.5
        
        result = f"You are {level}. The squat weight we recommend is {intensity:.2f} kg."
    except Exception as e:
        result = f"Error: {e}"

    return render_template('2_intensity_recommendation_result.html', result=result)

@app.route('/process_2', methods=['POST'])
def process_2():
    muscle_mass = request.form['muscle_mass']
    foods = request.form['foods']
    
    try:
        result = subprocess.run(
            [sys.executable, 'ask2GTP_diet.py', muscle_mass, foods],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            output = result.stdout.strip()
        else:
            output = f"Error: {result.stderr.strip()}"
    except Exception as e:
        output = f"Exception occurred: {e}"

    # 결과 페이지로 출력값 전달
    return render_template('3_diet suggestions_result.html', muscle_mass=muscle_mass, foods=foods, output=output)
    


if __name__ == '__main__':
    app.run(debug=True)
