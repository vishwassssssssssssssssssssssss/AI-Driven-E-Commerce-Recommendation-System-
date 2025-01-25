document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const locationForm = document.getElementById('locationForm');
    const locationInput = document.getElementById('locationInput');
    const weatherInfo = document.getElementById('weatherInfo');
    const recommendationSection = document.getElementById('recommendationSection');
    const recommendationList = document.getElementById('recommendationList');
    const errorMessage = document.getElementById('errorMessage');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loginForm = document.getElementById('loginFormElement');
    const registerForm = document.getElementById('registerFormElement');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const authForms = document.getElementById('authForms');
    const loginFormDiv = document.getElementById('loginForm');
    const registerFormDiv = document.getElementById('registerForm');
    const mainContent = document.getElementById('mainContent');
    const logoutButton = document.getElementById('logoutButton');
    const userInfo = document.getElementById('userInfo');

    // Check authentication status on page load
    checkAuth();

    async function checkAuth() {
        try {
            const response = await fetch('/api/user');
            if (!response.ok) {
                showAuthForms();
                return;
            }
            const userData = await response.json();
            showMainContent(userData);
        } catch (error) {
            showAuthForms();
        }
    }

    function showAuthForms() {
        authForms.classList.remove('hidden');
        mainContent.classList.add('hidden');
        logoutButton.classList.add('hidden');
        userInfo.textContent = '';
    }

    function showMainContent(userData) {
        authForms.classList.add('hidden');
        mainContent.classList.remove('hidden');
        logoutButton.classList.remove('hidden');
        userInfo.textContent = `Welcome, ${userData.username} (Age: ${userData.age}, Gender: ${userData.gender})`;
    }

    // Authentication related functions
    showRegisterLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginFormDiv.classList.add('hidden');
        registerFormDiv.classList.remove('hidden');
    });

    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        registerFormDiv.classList.add('hidden');
        loginFormDiv.classList.remove('hidden');
    });

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Login failed');
            }

            checkAuth(); // This will update the UI
        } catch (error) {
            showError(error.message);
        }
    });

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        const age = document.getElementById('registerAge').value;
        const gender = document.getElementById('registerGender').value;

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, age, gender })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Registration failed');
            }

            // Switch to login form after successful registration
            registerFormDiv.classList.add('hidden');
            loginFormDiv.classList.remove('hidden');
            showError('Registration successful! Please login.');
        } catch (error) {
            showError(error.message);
        }
    });

    logoutButton.addEventListener('click', async function(e) {
        e.preventDefault();
        try {
            await fetch('/api/logout');
            showAuthForms();
        } catch (error) {
            showError('Logout failed');
        }
    });

    // Location form submission
    locationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const location = locationInput.value.trim();
        
        if (!location) {
            showError('Please enter a location');
            return;
        }

        // Show loading
        loadingIndicator.classList.remove('hidden');
        errorMessage.classList.add('hidden');
        weatherInfo.classList.add('hidden');
        recommendationSection.classList.add('hidden');

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ location })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to get recommendations');
            }

            // Display weather information
            weatherInfo.innerHTML = `
                <h3>Current Weather in ${data.weather.location}</h3>
                <div class="weather-details">
                    <div class="weather-detail">
                        <span>${data.weather.condition}</span>
                        <div>Condition</div>
                    </div>
                    <div class="weather-detail">
                        <span>${Math.round(data.weather.temperature)}°C</span>
                        <div>Temperature</div>
                    </div>
                </div>
            `;

            // Display recommendations
            recommendationList.innerHTML = data.recommendations
                .map(product => createProductCard(product))
                .join('');

            // Show the sections
            weatherInfo.classList.remove('hidden');
            recommendationSection.classList.remove('hidden');
        } catch (error) {
            showError(error.message);
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    });

    function createProductCard(product) {
        return `
            <div class="product-card">
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>${product.description}</p>
                <p class="price">$${product.price}</p>
            </div>
        `;
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }
});
