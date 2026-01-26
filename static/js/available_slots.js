document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('booking-form');
    const dateField = document.getElementById('id_date');
    const partyField = document.getElementById('id_party_size');
    const slotField = document.getElementById('id_slot');

    function loadSlots() {
        const date = dateField.value;
        const party = partyField.value;
        const bookingId = form?.dataset.bookingId;

        if (!date || !party) {
            slotField.innerHTML = '';
            return;
        }

        let url = `/booking/available-slots/?date=${date}&party_size=${party}`
        if (bookingId) {
            url += `&exclude=${bookingId}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                slotField.innerHTML = '';

                if (!data.slots || data.slots.length === 0) {
                    const opt = document.createElement('option');
                    opt.textContent = 'No availability';
                    slotField.appendChild(opt);
                    return;
                }

                data.slots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.value;
                    option.textContent = slot.label
                    slotField.appendChild(option);
                });
            });
    }

    dateField.addEventListener('change', loadSlots);
    partyField.addEventListener('change', loadSlots);
});
