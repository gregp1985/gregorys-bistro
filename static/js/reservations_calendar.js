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
      modal.querySelector('.time').textContent =
      event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      modal.querySelector('.party').textContent = event.extendedProps.party_size;
      modal.querySelector('.status').textContent = event.extendedProps.status;
      modal.querySelector('.allergies').textContent =
      event.extendedProps.allergies || 'None';

      const editBtn = modal.querySelector('.edit-btn');

      editBtn.href = editBtn.dataset.editUrl.replace('/0/', `/${event.id}/`);

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
