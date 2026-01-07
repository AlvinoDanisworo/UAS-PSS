// JWT Authentication Middleware
const AUTH_CHECK_PAGES = [
    '/',
    '/courses/',
    '/enrollments/',
    '/profile/',
    '/courses/create/',
    '/materials/',
];

const PUBLIC_PAGES = [
    '/auth/login/',
    '/auth/register/',
    '/apihtml/',
    '/api-docs/',
];

async function checkAuth() {
    const currentPath = window.location.pathname;
    
    // Check if current page is public first
    const isPublicPage = PUBLIC_PAGES.some(page => 
        currentPath === page || currentPath.startsWith(page)
    );
    
    if (isPublicPage) {
        return; // Public page, no auth check needed
    }
    
    // Check if current page requires authentication
    const requiresAuth = AUTH_CHECK_PAGES.some(page => 
        currentPath === page || currentPath.startsWith(page)
    );
    
    if (!requiresAuth) {
        return; // Page doesn't require auth
    }
    
    const accessToken = localStorage.getItem('access_token');
    
    if (!accessToken) {
        // No token, redirect to login
        redirectToLogin();
        return;
    }
    
    // Verify token with backend
    try {
        const response = await fetch('/api/v1/auth/verify', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (!response.ok) {
            // Token invalid, try to refresh
            const refreshed = await tryRefreshToken();
            if (!refreshed) {
                redirectToLogin();
            }
        } else {
            const data = await response.json();
            // Store user data
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Update UI with user info if element exists
            updateUserUI(data.user);
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        redirectToLogin();
    }
}

async function tryRefreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
        return false;
    }
    
    try {
        const response = await fetch('/api/v1/auth/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    
    return false;
}

function redirectToLogin() {
    const currentPath = window.location.pathname;
    // Clear tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Redirect to login with next parameter
    window.location.href = `/auth/login/?next=${encodeURIComponent(currentPath)}`;
}

function updateUserUI(user) {
    // Update username display if element exists
    const usernameEl = document.getElementById('current-username');
    if (usernameEl) {
        usernameEl.textContent = user.username;
    }
    
    // Update full name if element exists
    const fullNameEl = document.getElementById('current-user-fullname');
    if (fullNameEl && user.first_name) {
        fullNameEl.textContent = `${user.first_name} ${user.last_name}`.trim();
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/auth/login/';
}

// Update navbar with user info
function updateNavbar() {
    const user = localStorage.getItem('user');
    const jwtUserSection = document.getElementById('jwt-user-section');
    const loginSection = document.getElementById('login-section');
    const usernameSpan = document.getElementById('current-username');
    
    if (user && jwtUserSection && loginSection && usernameSpan) {
        try {
            const userData = JSON.parse(user);
            usernameSpan.textContent = userData.username || 'User';
            jwtUserSection.style.display = 'block';
            loginSection.style.display = 'none';
        } catch (e) {
            console.error('Failed to parse user data:', e);
            if (jwtUserSection) jwtUserSection.style.display = 'none';
            if (loginSection) loginSection.style.display = 'block';
        }
    } else if (loginSection) {
        if (jwtUserSection) jwtUserSection.style.display = 'none';
        loginSection.style.display = 'block';
    }
}

// Add logout function to window for global access
window.logoutUser = logout;

// Initialize auth check and navbar update
function initAuth() {
    const currentPath = window.location.pathname;
    
    // Check if current page is public
    const isPublicPage = PUBLIC_PAGES.some(page => 
        currentPath === page || currentPath.startsWith(page)
    );
    
    // Run auth check for protected pages
    if (!isPublicPage) {
        checkAuth();
    }
    
    // Update navbar if elements exist (regardless of page type)
    if (document.getElementById('jwt-user-section') || document.getElementById('login-section')) {
        updateNavbar();
    }
}

// Run on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}
