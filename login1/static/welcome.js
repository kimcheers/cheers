// static/welcome.js

document.addEventListener('DOMContentLoaded', () => {
    // --- 로그아웃 버튼 처리 (welcome.html에 있을 때) ---
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            // 서버의 /logout 엔드포인트로 이동 (GET 요청)
            window.location.href = '/logout';
        });
    }
});

// static/exit.js

document.addEventListener('DOMContentLoaded', () => {
    // --- 회원 탈퇴 폼 처리 ---
    const exitForm = document.getElementById('exitForm');
    if (exitForm) {
        exitForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // 폼의 기본 제출 동작 막기

            const password = document.getElementById('exitPassword').value; // 입력된 비밀번호 가져오기
            const data = { password }; // 서버로 보낼 데이터 준비

            try {
                // 서버의 /delete_account 엔드포인트로 POST 요청
                const response = await fetch('/delete_account', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json(); // 서버 응답 파싱

                if (response.ok) { // 성공 응답 (HTTP 200)
                    alert(result.message); // 서버 메시지 표시
                    window.location.href = '/'; // 탈퇴 성공 후 로그인 페이지로 리디렉션
                } else { // 실패 응답 (HTTP 401 등)
                    alert('회원 탈퇴 실패: ' + (result.message || '알 수 없는 오류'));
                }

            } catch (error) {
                console.error('회원 탈퇴 Fetch 에러:', error);
                alert('회원 탈퇴 중 서버와 통신 오류가 발생했습니다.');
            }
        });
    }
});