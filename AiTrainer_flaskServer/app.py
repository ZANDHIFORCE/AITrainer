from flask import Flask, request, render_template
import sys
import subprocess

app = Flask(__name__)

# HTML 폼 페이지
@app.route('/')
def index():
    return '''
        <form action="/process" method="post">
            <label for="image_url">이미지 URL 입력:</label>
            <input type="text" id="image_url" name="image_url" required>
            <button type="submit">전송</button>
        </form>
    '''

# URL 처리 및 결과 표시
@app.route('/process', methods=['POST'])
def process():
    image_url = request.form['image_url']
    try:
        result = subprocess.run(
            [ sys.executable, 'ask2GTP.py', image_url],
            capture_output=True, text=True
        )
        
        # # 디버깅용 출력
        # print("STDOUT:", result.stdout)  # 정상 출력 확인
        # print("STDERR:", result.stderr)  # 에러 메시지 확인
        
        if result.returncode == 0:  # 성공적으로 실행된 경우
            output = result.stdout.strip()
        else:  # 실행 실패
            output = f"Error: {result.stderr.strip()}"
    except Exception as e:
        output = f"Exception occurred: {e}"
    
    return f'''
        <h1>처리 결과</h1>
        <img src="{image_url}" alt="입력된 이미지" style="max-width: 100%; height: auto;">
        <p>{output}</p>
        <a href="/">다시 입력</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)
