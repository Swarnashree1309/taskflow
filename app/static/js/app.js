const modal = new bootstrap.Modal ? null : null; // placeholder, bootstrap handles via data attrs

function loadTasks() {
  fetch('/api/tasks')
    .then(r => r.json())
    .then(tasks => {
      const body = document.getElementById('task-table-body');
      body.innerHTML = '';
      tasks.forEach(t => {
        const badgeColor = { Low: 'secondary', Medium: 'warning', High: 'danger' }[t.priority];
        const statusColor = { Pending: 'warning', 'In Progress': 'info', Done: 'success' }[t.status];
        body.innerHTML += `
          <tr>
            <td>${t.title}</td>
            <td>${t.category}</td>
            <td><span class="badge bg-${badgeColor}">${t.priority}</span></td>
            <td><span class="badge bg-${statusColor}">${t.status}</span></td>
            <td>${t.due_date || '-'}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary" onclick='editTask(${JSON.stringify(t)})'><i class="bi bi-pencil"></i></button>
              <button class="btn btn-sm btn-outline-danger" onclick="deleteTask(${t.id})"><i class="bi bi-trash"></i></button>
            </td>
          </tr>`;
      });
    });
}

function openNewTaskModal() {
  document.getElementById('task-id').value = '';
  document.getElementById('task-title').value = '';
  document.getElementById('task-description').value = '';
  document.getElementById('task-category').value = 'General';
  document.getElementById('task-priority').value = 'Medium';
  document.getElementById('task-status').value = 'Pending';
  document.getElementById('task-due').value = '';
}

function editTask(t) {
  document.getElementById('task-id').value = t.id;
  document.getElementById('task-title').value = t.title;
  document.getElementById('task-description').value = t.description || '';
  document.getElementById('task-category').value = t.category;
  document.getElementById('task-priority').value = t.priority;
  document.getElementById('task-status').value = t.status;
  document.getElementById('task-due').value = t.due_date || '';
  new bootstrap.Modal(document.getElementById('taskModal')).show();
}

function saveTask() {
  const id = document.getElementById('task-id').value;
  const payload = {
    title: document.getElementById('task-title').value,
    description: document.getElementById('task-description').value,
    category: document.getElementById('task-category').value,
    priority: document.getElementById('task-priority').value,
    status: document.getElementById('task-status').value,
    due_date: document.getElementById('task-due').value || null,
  };

  const url = id ? `/api/tasks/${id}` : '/api/tasks';
  const method = id ? 'PUT' : 'POST';

  fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).then(() => {
    bootstrap.Modal.getInstance(document.getElementById('taskModal')).hide();
    loadTasks();
  });
}

function deleteTask(id) {
  if (!confirm('Delete this task?')) return;
  fetch(`/api/tasks/${id}`, { method: 'DELETE' }).then(loadTasks);
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('task-table-body')) loadTasks();
});
