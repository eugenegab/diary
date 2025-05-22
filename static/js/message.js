export function setMessage(text, error=false) {
    const message = document.getElementById('message')
    if (!error) {
        message.classList.remove('hidden')
        message.classList.add('success-message')
        message.innerHTML = text
    } else {
        message.classList.remove('hidden')
        message.classList.add('error-message')
        message.innerHTML = text
    }
}