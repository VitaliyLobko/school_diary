const form = document.forms[1]

form.addEventListener('submit', async (e) => {
  e.preventDefault()
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: form.username.value,
      password: form.password.value,
    }),
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    localStorage.setItem('accessToken', result.access_token)
    window.location = '/students'
  }
})
