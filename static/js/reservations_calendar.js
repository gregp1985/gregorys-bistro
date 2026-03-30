function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}

document.addEventListener('DOMContentLoaded', function () {

  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;

  const eventsUrl = calendarEl.dataset.eventsUrl;
  const adminChangeUrl = calendarEl.dataset.adminChangeUrl;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'en-gb',

    initialView: 'timeGridWeek',
    navLinks: true,
    eventInteractive: true,
    nowIndicator: true,
    height: 'auto',

    headerToolbar: {
    right: 'prev,next',
    center: 'title',
    left: 'today timeGridDay,timeGridWeek'
    },

    slotMinTime: '11:00:00',
    slotMaxTime: '23:00:00',

    dayHeaderFormat: {
    weekday: 'short',
    day: '2-digit',
    month: '2-digit'
    },

    dateClick: function(info) {
      calendar.changeView('timeGridDay', info.dateStr);
    },

    events: eventsUrl,

    eventClick: function(info) {
      info.jsEvent.preventDefault();

      const event = info.event;

      const modal = document.getElementById('booking-modal');
      modal.querySelector('.ref').textContent = event.extendedProps.reference;
      modal.querySelector('.name').textContent = event.extendedProps.name;
      modal.querySelector('.table').textContent = event.extendedProps.table;
      modal.querySelector('.date').textContent = event.start.toLocaleDateString('en-GB', {
        weekday: 'short',  // optional, e.g., "Mon"
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
      modal.querySelector('.time').textContent =
      event.start.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
      });
      
      modal.querySelector('.party').textContent = event.extendedProps.party_size;
      modal.querySelector('.status').textContent = event.extendedProps.status;
      modal.querySelector('.allergies').textContent =
      event.extendedProps.allergies || 'None';

      const editBtn = modal.querySelector('.edit-btn');

      editBtn.href = editBtn.dataset.editUrl.replace('/0/', `/${event.id}/`);

      const cancelBtn = modal.querySelector('#cancel-btn');

      cancelBtn.onclick = function () {
        if (!confirm("Are you sure you want to cancel this booking?")) return;
        const url = `/staff/cancel/${event.extendedProps.reference}/`;
        fetch(`/staff/cancel/${event.extendedProps.reference}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken(),
          }
        })
        .then(response => {
          if (response.ok) {
            alert('Booking cancelled!');
            event.remove(); // remove event from calendar
            modal.classList.remove('open');
          } else {
            alert('Failed to cancel booking.');
          }
        })
        .catch(error => {
          console.error('Error cancelling booking:', error);
          alert('An error occurred.');
        });
      };

      modal.classList.add('open');
    },

    eventDidMount: function(info) {
      info.el.title =
        `Ref: ${info.event.extendedProps.reference}\n` +
        `Status: ${info.event.extendedProps.status}\n` +
        `Allergies: ${info.event.extendedProps.allergies || 'None'}`;
    },

    allDaySlot: false,
    expandRows: true,
    stickyHeaderDates: true,
    firstDay: 1,
  });

  calendar.render();
});
