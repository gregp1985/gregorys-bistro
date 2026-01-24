document.addEventListener('DOMContentLoaded', function () {

  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;

  const eventsUrl = calendarEl.dataset.eventsUrl;
  const adminChangeUrl = calendarEl.dataset.adminChangeUrl;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'en-gb',

    initialView: 'timeGridWeek',
    nowIndicator: true,
    height: "auto",

    slotMinTime: "11:00:00",
    slotMaxTime: "23:00:00",

    dayHeaderFormat: {
    weekday: 'short',
    day: '2-digit',
    month: '2-digit'
    },

    events: eventsUrl,

    eventClick: function(info) {
      window.location.href =
        adminChangeUrl.replace("BOOKING_ID", info.event.id);
    },

    eventDidMount: function(info) {
      info.el.title =
        `Ref: ${info.event.extendedProps.reference}\n` +
        `Status: ${info.event.extendedProps.status}\n` +
        `Allergies: ${info.event.extendedProps.allergies || "None"}`;
    },

    allDaySlot: false,
    expandRows: true,
    stickyHeaderDates: true,
    firstDay: 1,
  });

  calendar.render();
});
