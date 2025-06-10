
// 로컬 스토리지 키 상수
const STORAGE_KEYS = {
    USERS: 'app_users',
    CURRENT_USER: 'current_user',
    SESSION: 'user_session'
};

// 초기 데이터 설정
function initializeStorage() {
    if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
        const defaultUsers = [
            {
                id: 1,
                username: 'admin',
                password: 'admin123',
                createdAt: new Date().toISOString()
            },
            {
                id: 2,
                username: 'test',
                password: 'test123',
                createdAt: new Date().toISOString()
            }
        ];
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(defaultUsers));
    }
}

// 사용자 목록 가져오기
function getUsers() {
    initializeStorage();
    const users = localStorage.getItem(STORAGE_KEYS.USERS);
    return users ? JSON.parse(users) : [];
}

// 새 사용자 저장
function saveUser(user) {
    const users = getUsers();
    users.push(user);
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
}

// 사용자 찾기
function findUser(username, password) {
    const users = getUsers();
    return users.find(user => user.username === username && user.password === password);
}

// 사용자 로그인
function loginUser(user) {
    const sessionData = {
        user: user,
        loginTime: new Date().toISOString(),
        isActive: true
    };
    
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
    localStorage.setItem(STORAGE_KEYS.SESSION, JSON.stringify(sessionData));
}

// 현재 로그인된 사용자 가져오기
function getCurrentUser() {
    const userData = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
    const sessionData = localStorage.getItem(STORAGE_KEYS.SESSION);
    
    if (userData && sessionData) {
        const user = JSON.parse(userData);
        const session = JSON.parse(sessionData);
        
        // 세션이 활성상태인지 확인
        if (session.isActive) {
            return {
                ...user,
                loginTime: session.loginTime
            };
        }
    }
    
    return null;
}

// 로그인 상태 확인
function isLoggedIn() {
    return getCurrentUser() !== null;
}

// 사용자 로그아웃
function logoutUser() {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    localStorage.removeItem(STORAGE_KEYS.SESSION);
}

// 사용자 데이터 업데이트
function updateUser(userId, updatedData) {
    const users = getUsers();
    const userIndex = users.findIndex(user => user.id === userId);
    
    if (userIndex !== -1) {
        users[userIndex] = { ...users[userIndex], ...updatedData };
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
        
        // 현재 사용자가 업데이트된 사용자라면 세션 정보도 업데이트
        const currentUser = getCurrentUser();
        if (currentUser && currentUser.id === userId) {
            localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(users[userIndex]));
        }
        
        return true;
    }
    
    return false;
}

// 사용자 삭제
function deleteUser(userId) {
    const users = getUsers();
    const filteredUsers = users.filter(user => user.id !== userId);
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(filteredUsers));
    
    // 현재 사용자가 삭제된 사용자라면 로그아웃
    const currentUser = getCurrentUser();
    if (currentUser && currentUser.id === userId) {
        logoutUser();
    }
    
    return true;
}

// 메시지 표시 함수
function showMessage(text, type = 'info') {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        
        // 3초 후 메시지 제거
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = '';
        }, 3000);
    }
}

// 로컬 스토리지 데이터 검색
function searchUsers(query) {
    const users = getUsers();
    return users.filter(user => 
        user.username.toLowerCase().includes(query.toLowerCase()) ||
        user.email.toLowerCase().includes(query.toLowerCase())
    );
}

// 사용자 통계
function getUserStats() {
    const users = getUsers();
    const currentUser = getCurrentUser();
    
    return {
        totalUsers: users.length,
        currentUser: currentUser,
        recentUsers: users.slice(-5), // 최근 5명
        usersByDate: users.reduce((acc, user) => {
            const date = new Date(user.createdAt).toDateString();
            acc[date] = (acc[date] || 0) + 1;
            return acc;
        }, {})
    };
}

// 세션 만료 시간 설정 (선택사항)
function setSessionTimeout(minutes = 30) {
    const session = JSON.parse(localStorage.getItem(STORAGE_KEYS.SESSION) || '{}');
    if (session.loginTime) {
        setTimeout(() => {
            const currentSession = JSON.parse(localStorage.getItem(STORAGE_KEYS.SESSION) || '{}');
            if (currentSession.isActive) {
                logoutUser();
                alert('세션이 만료되었습니다. 다시 로그인해주세요.');
                window.location.href = '/login';
            }
        }, minutes * 60 * 1000);
    }
}

// 로컬 스토리지 초기화 (개발/테스트용)
function clearAllData() {
    localStorage.removeItem(STORAGE_KEYS.USERS);
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    localStorage.removeItem(STORAGE_KEYS.SESSION);
    initializeStorage();
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeStorage();
});