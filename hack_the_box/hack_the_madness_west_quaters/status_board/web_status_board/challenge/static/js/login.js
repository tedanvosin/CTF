const login    = document.getElementById('login');
const response = document.getElementById('response');

login.addEventListener('submit', e => {
    response.style.display = "none";
	e.preventDefault();
    console.log(new FormData(e.target));
	fetch('/api/login', {
		method: 'POST',
		body: new URLSearchParams(new FormData(e.target))
	})
        .then(resp => resp.json())
        .then(data => {
            if (data.logged) {
                login.remove();
                response.innerHTML = data.message;
                response.style.display = "block";
                window.setTimeout(function() {
                        window.location.href = '/dashboard';
                    }, 500);
                return;
            } else {
                response.style.display = "block";
                response.innerHTML = data.message;
            }
	});
});