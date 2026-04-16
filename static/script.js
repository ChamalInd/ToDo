// Hide / View Password Option
function viewPassword(id) {
    textInput = document.getElementById(id);
    btn = document.querySelector('.' + id);
    
    isPassword = textInput.type === 'password';
    
    textInput.type = isPassword ? 'text' : 'password';
    btn.textContent = isPassword ? 'Hide' : 'Show';
}

// Remove completed tasks by checkboxes
const form = document.getElementById('ongoing-form');
const checkboxes = document.querySelectorAll('.ongoing-tasks')

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        form.submit();
    })
})