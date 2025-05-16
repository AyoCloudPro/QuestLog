document.addEventListener('DOMContentLoaded', () => {
    // Add Task
    document.getElementById('add-task-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('new-task-title').value;
        const response = await fetch('/add-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        });
        const result = await response.json();
        if (result.success) {
            location.reload();
        } else {
            alert(result.message);
        }
    });

    // Add Note
    document.getElementById('add-note-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('new-note-title').value;
        const content = document.getElementById('new-note-content').value;
        const response = await fetch('/add-note', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
        });
        const result = await response.json();
        if (result.success) {
            location.reload();
        } else {
            alert(result.message);
        }
    });

    // Task Buttons
    document.querySelectorAll('#task-list li').forEach(li => {
        const id = li.dataset.id;

        li.querySelector('.progress-btn').addEventListener('click', async () => {
            const response = await fetch(`/progress-task/${id}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                location.reload();
            } else {
                alert(result.message);
            }
        });

        li.querySelector('.complete-btn').addEventListener('click', async () => {
            const response = await fetch(`/complete-task/${id}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                location.reload();
            } else {
                alert(result.message);
            }
        });

        li.querySelector('.delete-btn').addEventListener('click', async () => {
            const response = await fetch(`/delete-task/${id}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                location.reload();
            } else {
                alert(result.message);
            }
        });
    });

    // Note Buttons
    document.querySelectorAll('#note-list li').forEach(li => {
        const id = li.dataset.id;

        li.querySelector('.edit-btn').addEventListener('click', () => {
            const title = prompt('Edit title:', li.querySelector('h3').textContent);
            const content = prompt('Edit content:', li.querySelector('p').textContent);
            if (title && content) {
                fetch(`/edit-note/${id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, content })
                }).then(response => response.json())
                  .then(result => {
                      if (result.success) {
                          location.reload();
                      } else {
                          alert(result.message);
                      }
                  });
            }
        });

        li.querySelector('.delete-btn').addEventListener('click', async () => {
            const response = await fetch(`/delete-note/${id}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                location.reload();
            } else {
                alert(result.message);
            }
        });
    });
});
