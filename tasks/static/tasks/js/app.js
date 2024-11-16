// Task Management Functions
class TaskManager {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Delete task confirmation
        document.querySelectorAll('.delete-task').forEach(button => {
            button.addEventListener('click', (e) => {
                if (!confirm('Are you sure you want to delete this task?')) {
                    e.preventDefault();
                }
            });
        });

        // Task status update
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', (e) => {
                this.updateTaskStatus(e.target);
            });
        });

        // Task form validation
        const taskForm = document.getElementById('taskForm');
        if (taskForm) {
            taskForm.addEventListener('submit', (e) => {
                this.validateTaskForm(e);
            });
        }
    }

    validateTaskForm(event) {
        const form = event.target;
        const title = form.querySelector('[name="title"]').value;
        const deadline = form.querySelector('[name="deadline"]').value;

        if (!title.trim()) {
            event.preventDefault();
            alert('Please enter a task title');
            return false;
        }

        if (!deadline) {
            event.preventDefault();
            alert('Please select a deadline');
            return false;
        }

        return true;
    }

    updateTaskStatus(selectElement) {
        const taskId = selectElement.dataset.taskId;
        const newStatus = selectElement.value;

        fetch(`/api/tasks/${taskId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            body: JSON.stringify({
                status: newStatus
            })
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to update status');
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update task status');
        });
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize Task Manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TaskManager();
});

// Bootstrap Tooltips Initialization
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});