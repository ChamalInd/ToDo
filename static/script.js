function viewPassword(id) {
    textInput = document.getElementById(id);
    btn = document.querySelector('.' + id);
    
    isPassword = textInput.type === 'password';
    
    textInput.type = isPassword ? 'text' : 'password';
    btn.textContent = isPassword ? 'Hide' : 'Show';
}