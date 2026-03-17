// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 4000);
    setTimeout(() => el.remove(), 4400);
    el.style.transition = 'opacity 0.4s';
  });

  // Status update via AJAX on application rows
  document.querySelectorAll('.status-select').forEach(sel => {
    sel.addEventListener('change', async function () {
      const appId = this.dataset.appId;
      const newStatus = this.value;
      try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const res = await fetch('/update_application_status', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ application_id: parseInt(appId), status: newStatus })
        });
        const data = await res.json();
        if (data.success) {
          // Update badge next to select
          const badge = this.closest('.app-row').querySelector('.badge');
          if (badge) {
            badge.className = 'badge ' + statusClass(newStatus);
            badge.innerHTML = statusIcon(newStatus) + ' ' + newStatus;
          }
          showToast('Status updated!', 'success');
        }
      } catch (e) {
        showToast('Failed to update status.', 'danger');
      }
    });
  });

  // Score ring animation
  document.querySelectorAll('.score-ring-circle').forEach(circle => {
    const target = parseFloat(circle.dataset.score) / 100;
    const r = parseFloat(circle.getAttribute('r'));
    const circ = 2 * Math.PI * r;
    circle.style.strokeDasharray = circ;
    circle.style.strokeDashoffset = circ;
    requestAnimationFrame(() => {
      circle.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)';
      circle.style.strokeDashoffset = circ - target * circ;
    });
  });
});

function statusClass(s) {
  if (s === 'Applied') return 'badge-applied';
  if (s === 'Interview Scheduled') return 'badge-interview';
  if (s === 'Rejected') return 'badge-rejected';
  if (s === 'Offer Received') return 'badge-offer';
  return '';
}

function statusIcon(s) {
  if (s === 'Applied') return '◎';
  if (s === 'Interview Scheduled') return '◈';
  if (s === 'Rejected') return '✕';
  if (s === 'Offer Received') return '✓';
  return '·';
}

function showToast(msg, type='info') {
  const t = document.createElement('div');
  t.className = `flash flash-${type}`;
  t.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;min-width:240px;transition:opacity .3s;';
  t.innerHTML = `<span>${msg}</span><button onclick="this.parentElement.remove()">×</button>`;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity='0'; setTimeout(()=>t.remove(),300); }, 3000);
}

// File upload label
document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('resume-input');
  if (fileInput) {
    fileInput.addEventListener('change', function() {
      const label = document.getElementById('upload-label');
      if (label && this.files.length) label.textContent = this.files[0].name;
    });
  }
});
