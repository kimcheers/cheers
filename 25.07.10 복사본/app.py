# app.py

from flask import Flask, render_template, jsonify
import requests # 웹에서 데이터를 가져오기 위한 HTTP 요청 라이브러리입니다.
from bs4 import BeautifulSoup # HTML/XML 파싱을 위한 라이브러리입니다.
import json
import time
from datetime import datetime

app = Flask(__name__) # Flask 애플리케이션을 초기화합니다. 이 인스턴스가 웹 서버의 핵심이 됩니다.

# 해역별 평년 평균 수온 데이터 (실제로는 DB에서 가져올 데이터)
# 실제 애플리케이션에서는 이 데이터가 데이터베이스나 외부 설정 파일에서 로드될 것입니다.
NORMAL_TEMPS = {
    "동해": 20.5, # 동해의 평년 평균 수온 (섭씨)
    "서해": 18.2, # 서해의 평년 평균 수온 (섭씨)
    "남해": 19.8, # 남해의 평년 평균 수온 (섭씨)
    "제주": 21.1 # 제주 해역의 평년 평균 수온 (섭씨)
}

def get_ocean_temp_data():
    """국립수산과학원 사이트에서 수온 데이터 크롤링"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        url = "https://www.nifs.go.kr/risa/main.risa" # 국립수산과학원 해양수온정보 URL
        
        # 실제 웹 페이지에 요청을 보냅니다. 타임아웃을 10초로 설정합니다.
        response = requests.get(url, headers=headers, timeout=10) 
        # HTTP 응답 상태 코드가 200 (성공)이 아니면 예외를 발생시킵니다.
        response.raise_for_status() 
        # 응답받은 HTML 내용을 'html.parser'를 사용하여 파싱합니다.
        soup = BeautifulSoup(response.content, 'html.parser') 
        
        current_data = {} # 현재 수온 데이터를 저장할 딕셔너리입니다.

        # --- 이 부분은 국립수산과학원 웹사이트의 실제 HTML 구조를 분석하여 수정해야 합니다. ---
        # 아래는 예시 코드이며, 웹사이트의 HTML 요소 ID나 클래스명이 다를 경우 작동하지 않습니다.
        # F12 개발자 도구 (크롬 기준) -> Elements 탭에서 수온 데이터를 찾아 해당 요소의 정확한 선택자를 확인하세요.
        # 예시:
        # 동해 수온이 <span id="sea_temp_east">23.2</span> 와 같이 있다면:
        # donghae_temp_el = soup.select_one('#sea_temp_east')
        # if donghae_temp_el: current_data["동해"] = float(donghae_temp_el.text.strip())
        
        # 현재는 웹사이트의 정확한 HTML 구조를 알 수 없으므로, 일반적인 패턴을 가정합니다.
        # 예를 들어, 각 해역별 수온이 어떤 특정 테이블이나 div 안에 나열되어 있을 수 있습니다.

        # 임시로 각 해역별 수온을 추출하는 예시 선택자 (수정 필요)
        # 이 선택자들은 일반적인 웹사이트 구조를 가정한 것이므로, 실제 사이트와 다를 수 있습니다.
        # 실제 사이트에서 '동해', '서해', '남해', '제주' 해역의 수온 데이터가 어떻게 표시되는지 확인해야 합니다.
        
        # 예시: 특정 CSS 클래스를 가진 요소에서 텍스트를 가져온다고 가정
        # <div class="region-temp" data-region="동해">23.2</div>
        # <div class="region-temp" data-region="서해">21.5</div>
        
        # 각 해역별로 데이터를 찾기 위한 반복문
        # 실제 사이트에서는 각 해역의 수온을 나타내는 요소가 어떤 규칙성을 가지는지 파악해야 합니다.
        regions_mapping = {
            "동해": "donghae-temp-selector", # 동해 수온을 나타내는 CSS 선택자 (예: '#donghae-temp', '.temp-region-1')
            "서해": "seohae-temp-selector",  # 서해 수온을 나타내는 CSS 선택자
            "남해": "namhae-temp-selector",  # 남해 수온을 나타내는 CSS 선택자
            "제주": "jeju-temp-selector"     # 제주 수온을 나타내는 CSS 선택자
        }

        for region, selector in regions_mapping.items():
            temp_element = soup.select_one(selector)
            if temp_element:
                try:
                    # 텍스트에서 숫자만 추출하고 '°C' 같은 문자 제거 후 float으로 변환
                    temp_value = float("".join(filter(str.isdigit or str == '.', temp_element.text))) 
                    current_data[region] = temp_value
                except ValueError:
                    print(f"Failed to parse temperature for {region} from '{temp_element.text}'")
                    current_data[region] = None # 파싱 실패 시 None으로 설정
            else:
                print(f"Selector '{selector}' for {region} not found.")
                current_data[region] = None # 요소를 찾지 못한 경우 None으로 설정

        # 데이터 업데이트 시간 추가
        current_data["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 만약 크롤링으로 데이터를 전혀 가져오지 못했다면, 초기 기본값을 반환하도록 예외 처리
        if all(value is None for key, value in current_data.items() if key != "update_time"):
            raise ValueError("No temperature data extracted from the website.")
        
        return current_data
        
    except requests.exceptions.RequestException as req_e:
        print(f"HTTP 요청 에러: {req_e}") # 네트워크 문제, 타임아웃 등
        # 요청 관련 에러 발생 시 기본값 반환
        return {
            "동해": 22.0,
            "서해": 20.0,
            "남해": 20.5,
            "제주": 21.8,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"크롤링 또는 파싱 에러: {e}") # HTML 파싱 실패, 예상치 못한 데이터 형식 등
        # 그 외의 에러 발생 시 기본값 반환
        return {
            "동해": 22.0,
            "서해": 20.0,
            "남해": 20.5,
            "제주": 21.8,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def calculate_health_score(current_temp, normal_temp):
    """수온 차이로 건강 점수 계산"""
    diff = abs(current_temp - normal_temp) # 현재 수온과 평년 수온의 절대적인 차이를 계산합니다.
    
    if diff <= 0.5:
        return 95  # 차이가 0.5도 이하면 매우 건강 (높은 점수)
    elif diff <= 1.5:
        return 85  # 차이가 1.5도 이하면 건강
    elif diff <= 2.5:
        return 65  # 차이가 2.5도 이하면 주의
    elif diff <= 3.5:
        return 40  # 차이가 3.5도 이하면 경고
    else:
        return 20  # 그 외의 경우 (차이가 3.5도 초과) 위험 (낮은 점수)

def get_status_info(score):
    """점수에 따른 상태 정보"""
    # 계산된 점수에 따라 해양의 건강 상태, 색상, 메시지를 결정합니다.
    if score >= 80:
        return {"status": "건강", "color": "#28a745", "message": "바다가 건강해요!"} # 초록색 계열
    elif score >= 60:
        return {"status": "주의", "color": "#ffc107", "message": "조금 주의가 필요해요"} # 주황색 계열
    elif score >= 40:
        return {"status": "경고", "color": "#fd7e14", "message": "바다가 위험해요!"} # 진한 주황색 계열
    else:
        return {"status": "위험", "color": "#dc3545", "message": "매우 위험한 상태예요!"} # 빨간색 계열

@app.route('/') # 루트 URL ('/')로 접근했을 때 이 함수를 실행하도록 합니다.
def index():
    """메인 페이지"""
    return render_template('index.html') # templates 폴더에 있는 'index.html' 파일을 렌더링하여 반환합니다.

@app.route('/api/ocean-data') # '/api/ocean-data' URL로 접근했을 때 이 함수를 실행하도록 합니다.
def get_ocean_data():
    """바다 건강 데이터 API"""
    try:
        # 실시간 수온 데이터 크롤링
        current_temps = get_ocean_temp_data() # 현재 수온 데이터를 가져옵니다.
        
        # 각 해역별 건강 점수 계산
        ocean_health = {} # 각 해역의 건강 정보를 저장할 딕셔너리입니다.
        
        for region in ["동해", "서해", "남해", "제주"]: # 미리 정의된 해역들에 대해 반복합니다.
            current_temp = current_temps.get(region) # 해당 해역의 현재 수온을 가져옵니다. (None일 수 있음)
            normal_temp = NORMAL_TEMPS[region] # 해당 해역의 평년 평균 수온을 가져옵니다.
            
            # 크롤링이 실패하여 current_temp가 None인 경우 처리
            if current_temp is None:
                # 데이터를 가져오지 못한 경우 기본값이나 오류 상태로 처리
                ocean_health[region] = {
                    "current_temp": "N/A", # 현재 수온을 '알 수 없음'으로 표시
                    "normal_temp": normal_temp,
                    "temp_diff": "N/A", # 수온 차이도 '알 수 없음'
                    "score": 0, # 점수를 0으로 설정 (가장 낮은 점수)
                    "status": "알 수 없음", # 상태를 '알 수 없음'으로 표시
                    "color": "#6c757d", # 회색 (데이터 없음 또는 오류)
                    "message": "데이터를 가져올 수 없어요." # 메시지
                }
                continue # 다음 해역으로 넘어갑니다.

            score = calculate_health_score(current_temp, normal_temp) # 건강 점수를 계산합니다.
            status_info = get_status_info(score) # 점수에 따른 상태 정보를 가져옵니다.
            
            ocean_health[region] = { # 각 해역의 상세 정보를 딕셔너리에 저장합니다.
                "current_temp": current_temp, # 현재 수온
                "normal_temp": normal_temp, # 평년 평균 수온
                "temp_diff": round(current_temp - normal_temp, 1), # 평년 대비 수온 차이 (소수점 첫째 자리까지 반올림)
                "score": score, # 건강 점수
                "status": status_info["status"], # 건강 상태 (예: 건강, 주의)
                "color": status_info["color"], # 상태에 따른 색상 코드
                "message": status_info["message"] # 상태에 따른 메시지
            }
        
        return jsonify({ # 계산된 모든 데이터를 JSON 형식으로 반환합니다.
            "success": True, # 요청 성공 여부
            "data": ocean_health, # 해역별 건강 데이터
            "update_time": current_temps.get("update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 데이터 업데이트 시간 (없으면 현재 시간)
        })
        
    except Exception as e:
        return jsonify({ # 에러 발생 시 실패 메시지와 에러 내용을 JSON 형식으로 반환합니다.
            "success": False, # 요청 실패 여부
            "error": str(e) # 에러 메시지
        })

if __name__ == '__main__':
    app.run(debug=True, port=5050) # 스크립트가 직접 실행될 때 Flask 앱을 실행합니다.
                                  # debug=True는 개발 중 디버깅 정보를 제공하고 코드 변경 시 자동 재시작합니다.
                                  # port=5000은 5000번 포트에서 서버를 실행하도록 설정합니다.