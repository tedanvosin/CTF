// Function to make authenticated API calls
const makeAuthenticatedRequest = async (url, options = {}) => {
    const token = localStorage.getItem('token');
    
    if (!token) {
        window.location.href = '/next?url=/unauthorized';
        return;
    }

    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };

    try {
        const response = await fetch(url, { ...options, headers });
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('jku');
            window.location.href = '/next?url=/unauthorized';
            return;
        }
        return response;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};


document.addEventListener('DOMContentLoaded', () => {
    const cameraGrid = document.getElementById('cameraGrid');
    const logoutBtn = document.getElementById('logoutBtn');
    const flagContainer = document.getElementById('flag-container');

    // Function to update camera status
    async function updateCameraStatus(cameraId, enable) {
        try {
            const response = await fetch(`/api/cameras/${cameraId}/${enable ? 'enable' : 'disable'}`, {
                method: 'POST',
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Failed to update camera status');
            }
            
            const data = await response.json();
            console.log(data.message);
            
            // Refresh camera grid
            loadCameras();
            
            // Check if all cameras are disabled
            checkFlag();
        } catch (error) {
            console.error('Error updating camera status:', error);
            alert('Failed to update camera status');
        }
    }

    // Function to check if we can get the flag
    async function checkFlag() {
        try {
            const response = await fetch('/api/cameras', {
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Failed to get camera status');
            }
            
            const cameras = await response.json();
            const allDisabled = cameras.every(camera => camera.status === 'disabled');
            
            if (allDisabled) {
                const flagResponse = await fetch('/api/cameras/flag', {
                    credentials: 'include'
                });
                
                if (!flagResponse.ok) {
                    throw new Error('Failed to get flag');
                }
                
                const flagData = await flagResponse.json();
                flagContainer.textContent = `Flag: ${flagData.flag}`;
                flagContainer.style.display = 'block';
            } else {
                flagContainer.style.display = 'none';
            }
        } catch (error) {
            console.error('Error checking flag:', error);
        }
    }

    // Function to load cameras
    async function loadCameras() {
        try {
            const response = await fetch('/api/cameras', {
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Failed to load cameras');
            }
            
            const cameras = await response.json();
            cameraGrid.innerHTML = '';
            
            cameras.forEach(camera => {
                const isActive = camera.status === 'active';
                const card = document.createElement('div');
                card.className = 'bg-gray-800 rounded-xl shadow-xl overflow-hidden border border-gray-700 transform hover:scale-[1.02] transition-transform duration-300';
                
                card.innerHTML = `
                    <div class="camera-feed ${!isActive ? 'disabled' : ''}" id="camera-${camera.id}">
                        <img src="${camera.url}" alt="${camera.name}">
                    </div>
                    <div class="p-5">
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="text-lg font-semibold text-white">${camera.name}</h3>
                            <span class="px-2 py-1 text-xs rounded-full ${isActive ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}">
                                ${isActive ? 'Active' : 'Disabled'}
                            </span>
                        </div>
                        <p class="text-sm text-gray-400 mb-4">${camera.location}</p>
                        <div class="flex justify-end">
                            <button 
                                class="toggle-camera px-4 py-2 text-sm rounded-lg font-medium transition-colors duration-150 ease-in-out
                                ${isActive 
                                    ? 'bg-red-900/50 text-red-300 hover:bg-red-900' 
                                    : 'bg-green-900/50 text-green-300 hover:bg-green-900'}"
                                data-camera-id="${camera.id}"
                                data-enabled="${isActive}"
                            >
                                ${isActive ? 'Disable Camera' : 'Enable Camera'}
                            </button>
                        </div>
                    </div>
                `;
                
                cameraGrid.appendChild(card);
            });
            
            // Check flag status after loading cameras
            checkFlag();
        } catch (error) {
            console.error('Error loading cameras:', error);
            alert('Failed to load cameras');
        }
    }

    // Event delegation for camera toggle buttons
    cameraGrid.addEventListener('click', (e) => {
        const button = e.target.closest('.toggle-camera');
        if (button) {
            const cameraId = button.dataset.cameraId;
            const isEnabled = button.dataset.enabled === 'true';
            updateCameraStatus(cameraId, !isEnabled);
        }
    });

    // Handle logout
    logoutBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Logout failed');
            }
            
            window.location.href = '/next?url=/';
        } catch (error) {
            console.error('Error logging out:', error);
            alert('Failed to logout');
        }
    });

    // Initial load
    loadCameras();
});