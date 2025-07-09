// static/script.js (로그인/회원가입 기능만 남음)

document.addEventListener('DOMContentLoaded', () => {
    // --- 로그인 폼 처리 ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const data = { username, password };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    window.location.href = '/welcome';
                } else {
                    alert('로그인 실패: ' + (result.message || '알 수 없는 오류'));
                }

            } catch (error) {
                console.error('로그인 Fetch 에러:', error);
                alert('로그인 중 서버와 통신 오류가 발생했습니다.');
            }
        });
    }

    // --- 회원가입 폼 처리 ---
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('signupUsername').value;
            const password = document.getElementById('signupPassword').value;
            const passwordConfirm = document.getElementById('signupPasswordConfirm').value;

            if (password !== passwordConfirm) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }

            const data = { username, password };

            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    window.location.href = '/';
                } else {
                    alert('회원가입 실패: ' + (result.message || '알 수 없는 오류'));
                }

            } catch (error) {
                console.error('회원가입 Fetch 에러:', error);
                alert('회원가입 중 서버와 통신 오류가 발생했습니다.');
            }
        });
    }
});