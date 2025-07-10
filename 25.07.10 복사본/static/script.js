// script.js

// 바다 건강 데이터 불러오기 비동기 함수 정의
async function loadOceanData() {
    // HTML 요소들을 ID로 선택하여 변수에 할당합니다.
    const loadingEl = document.getElementById('loading'); // 로딩 메시지를 담는 요소
    const errorEl = document.getElementById('error');     // 에러 메시지를 담는 요소
    const gridEl = document.getElementById('ocean-grid'); // 바다 카드들이 표시될 그리드 요소
    const updateTimeEl = document.getElementById('update-time'); // 업데이트 시간을 표시하는 요소

    // 데이터를 불러오는 동안 로딩 상태를 표시합니다.
    loadingEl.style.display = 'block'; // 로딩 메시지를 보이게 합니다.
    errorEl.style.display = 'none';    // 에러 메시지는 숨깁니다.
    gridEl.style.display = 'none';     // 그리드(데이터 표시 영역)도 숨깁니다.

    try {
        // Flask 서버의 '/api/ocean-data' 엔드포인트에서 데이터를 가져옵니다.
        const response = await fetch('/api/ocean-data'); // 비동기적으로 데이터를 요청합니다.
        const result = await response.json(); // 응답을 JSON 형태로 파싱합니다.

        if (result.success) { // 서버 응답이 성공(success: true)인 경우
            // 성공적으로 데이터를 가져온 경우
            displayOceanData(result.data); // 가져온 데이터를 화면에 표시하는 함수를 호출합니다.
            updateTimeEl.textContent = `📅 마지막 업데이트: ${result.update_time}`; // 마지막 업데이트 시간을 업데이트합니다.
            
            loadingEl.style.display = 'none'; // 로딩 메시지를 숨깁니다.
            gridEl.style.display = 'grid'; // 그리드를 보이게 합니다. (CSS display: grid 속성 적용)
        } else {
            // 서버 응답이 실패(success: false)인 경우 에러를 발생시킵니다.
            throw new Error(result.error);
        }
    } catch (error) {
        // 데이터 로딩 중 네트워크 오류나 서버에서 발생한 에러를 처리합니다.
        console.error('데이터 로딩 에러:', error); // 콘솔에 에러를 기록합니다.
        loadingEl.style.display = 'none'; // 로딩 메시지를 숨깁니다.
        errorEl.style.display = 'block'; // 에러 메시지를 보이게 합니다.
    }
}

// 바다 건강 데이터를 화면에 표시하는 함수 정의
function displayOceanData(data) {
    const gridEl = document.getElementById('ocean-grid'); // 바다 카드들이 표시될 그리드 요소
    gridEl.innerHTML = ''; // 기존에 표시되던 카드들을 모두 제거하여 초기화합니다.

    // 각 해역별로 카드 생성
    // 데이터 객체의 각 키(해역 이름)에 대해 반복합니다.
    Object.keys(data).forEach(region => {
        const regionData = data[region]; // 해당 해역의 상세 데이터를 가져옵니다.
        const card = createOceanCard(region, regionData); // 해역 데이터로 카드 HTML 요소를 생성합니다.
        gridEl.appendChild(card); // 생성된 카드를 그리드에 추가합니다.
    });
}

// 바다 건강 카드 HTML 요소를 생성하는 함수 정의
function createOceanCard(region, data) {
    const card = document.createElement('div'); // 새로운 div 요소를 생성합니다.
    card.className = 'ocean-card'; // 생성된 div에 'ocean-card' 클래스를 추가합니다. (스타일 적용을 위함)
    
    // 수온 차이를 표시할 텍스트를 결정합니다. 양수일 경우 '+'를 붙입니다.
    const tempDiffText = data.temp_diff >= 0 ? 
        `+${data.temp_diff}°C` : `${data.temp_diff}°C`; // 삼항 연산자를 사용하여 양수/음수 포맷을 결정

    // 카드 내부의 HTML 구조를 백틱(템플릿 리터럴)을 사용하여 정의합니다.
    card.innerHTML = `
        <div class="ocean-name">${region}</div> <div class="temp-display">${data.current_temp}°C</div> <div class="temp-info"> 평년 평균: ${data.normal_temp}°C<br> 평년 대비: <strong>${tempDiffText}</strong> </div>
        <div class="health-score"> <div class="score-circle" style="background-color: ${data.color}"> ${data.score} </div>
            <div>
                <div class="status-badge" style="background-color: ${data.color}"> ${data.status} </div>
            </div>
        </div>
        <div class="status-message"> ${data.message} </div>
    `;
    
    return card; // 완성된 카드 요소를 반환합니다.
}

// 페이지 로드 시 데이터 불러오기
window.addEventListener('load', loadOceanData); // 웹 페이지가 완전히 로드되면 `loadOceanData` 함수를 한 번 호출합니다.

// 30초마다 자동 새로고침
setInterval(loadOceanData, 30000); // 30000ms (30초)마다 `loadOceanData` 함수를 자동으로 반복 실행하여 데이터를 새로고침합니다.