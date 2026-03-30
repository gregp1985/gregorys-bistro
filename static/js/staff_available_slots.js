document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('booking-form');
    const dateField = document.getElementById('id_date');
    const partyField = document.getElementById('id_party_size');
    const userField = document.getElementById('id_name');
    const slotField = document.getElementById('id_slot');
    const submitBtn = form.querySelector('button[type="submit"]');
    const slotContainer = document.getElementById('slot-container');

    function loadSlots() {
        submitBtn.disabled = true;
        const date = dateField.value;
        const party = partyField.value;
        const userId = userField.value;  // Get the user ID from the form
        const bookingId = form?.dataset.bookingId;

        if (!date || !party || !userId) {
            slotField.innerHTML = '';
            slotContainer.style.display = 'none';
            return;
        }

        let url = `/booking/available-slots/?date=${date}&party_size=${party}&user=${userId}`;
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
                    opt.value = '';
                    slotField.appendChild(opt);
                    slotContainer.style.display = 'none';
                    submitBtn.disabled = true;
                    return;
                }

                data.slots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.value;
                    option.textContent = slot.label;
                    slotField.appendChild(option);
                });
                slotContainer.style.display = 'block';
                submitBtn.disabled = false;
            })
            .catch(() => {
                slotField.innerHTML = '';
                const opt = document.createElement('option');
                opt.textContent = 'Error loading availability';
                opt.disabled = true;
                slotField.appendChild(opt);
                submitBtn.disabled = true;
            });
    }

    dateField.addEventListener('change', loadSlots);
    partyField.addEventListener('change', loadSlots);
    userField.addEventListener('change', loadSlots);

    loadSlots();
});