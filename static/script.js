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
        if (checkbox.checked) {
            form.submit();
        }
    })
})

// Setting constraints for date picker 
const datePicker = document.getElementById('datePicker');
const timePicker = document.getElementById('timePicker');

const today = new Date().toISOString().split('T')[0];
const time = new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
});

datePicker.value = today;
datePicker.min = today;

timePicker.value = time;