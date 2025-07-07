// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- 로그인 폼 처리 ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // 폼의 기본 제출 동작(페이지 새로고침)을 막습니다.

            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const data = { username, password };
            console.log('로그인 시도 데이터:', data); // 개발자 도구 콘솔에 전송 데이터 출력

            try {
                // Flask 서버의 /login 엔드포인트로 POST 요청을 보냅니다.
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }, // JSON 형식으로 데이터를 보낸다고 알립니다.
                    body: JSON.stringify(data) // JavaScript 객체를 JSON 문자열로 변환하여 보냅니다.
                });

                // 서버로부터의 응답을 JSON 형태로 파싱합니다.
                const result = await response.json();
                console.log('로그인 서버 응답:', result); // 개발자 도구 콘솔에 서버 응답 출력

                if (response.ok) { // HTTP 상태 코드 200번대 (성공)
                    alert(result.message);
                    // 로그인 성공 후 welcome.html로 리디렉션
                    window.location.href = '/welcome';
                } else { // HTTP 상태 코드 400번대 (클라이언트 오류) 또는 500번대 (서버 오류)
                    alert('로그인 실패: ' + (result.message || '알 수 없는 오류'));
                }

            } catch (error) {
                console.error('로그인 Fetch 에러:', error); // 네트워크 오류 등 발생 시 콘솔에 출력
                alert('로그인 중 서버와 통신 오류가 발생했습니다.');
            }
        });
    }

    // --- 회원가입 폼 처리 ---
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // 폼의 기본 제출 동작(페이지 새로고침)을 막습니다.

            const username = document.getElementById('signupUsername').value;
            const password = document.getElementById('signupPassword').value;
            const passwordConfirm = document.getElementById('signupPasswordConfirm').value;

            // --- 클라이언트 측 비밀번호 일치 여부 확인 ---
            if (password !== passwordConfirm) {
                alert('비밀번호가 일치하지 않습니다.');
                return; // 함수 실행 중단
            }

            const data = { username, password }; // 비밀번호 확인은 서버로 보낼 필요 없음
            console.log('회원가입 시도 데이터:', data); // 개발자 도구 콘솔에 전송 데이터 출력

            try {
                // Flask 서버의 /signup 엔드포인트로 POST 요청을 보냅니다.
                const response = await fetch('/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                // 서버로부터의 응답을 JSON 형태로 파싱합니다.
                const result = await response.json();
                console.log('회원가입 서버 응답:', result); // 개발자 도구 콘솔에 서버 응답 출력

                if (response.ok) { // HTTP 상태 코드 200번대 (성공)
                    alert(result.message);
                    // 회원가입 성공 후 로그인 페이지로 리디렉션
                    window.location.href = '/';
                } else { // HTTP 상태 코드 400번대 또는 500번대
                    alert('회원가입 실패: ' + (result.message || '알 수 없는 오류'));
                }

            } catch (error) {
                console.error('회원가입 Fetch 에러:', error); // 네트워크 오류 등 발생 시 콘솔에 출력
                alert('회원가입 중 서버와 통신 오류가 발생했습니다.');
            }
        });
    }

    // --- 로그아웃 버튼 처리 (welcome.html에 있을 때) ---
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            // 서버의 /logout 엔드포인트로 이동 (GET 요청)
            // 실제 로그아웃은 세션 클리어 등 서버 측 작업이 필요할 수 있습니다.
            // 현재는 Flask에서 단순 리디렉션을 처리합니다.
            window.location.href = '/logout';
        });
    }
});