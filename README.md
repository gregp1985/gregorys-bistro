# Gregory’s Bistro

Gregory’s Bistro is a restaurant website with a fully automated online table booking system. Authenticated users can create, edit, and cancel reservations, while staff and administrators can manage bookings through dedicated interfaces. The system enforces opening hours, prevents double bookings, and assigns the most appropriate available table automatically.

---

## Live Site & Repository

- **Live site:** https://gregorys-bistro-99ab41086172.herokuapp.com/
- **Repository:** https://github.com/gregp1985/gregorys-bistro

---

## Project Goals

### User Goals
- View information about Gregory’s Bistro, including menu imagery and contact details.
- Create an account quickly using a simple registration process.
- Verify their email address via an automated confirmation email.
- Log in to make a table booking at an available time.
- Edit or cancel existing bookings independently.

### Business Goals
- Provide a professional online presence for the bistro.
- Reduce manual workload by automating reservations.
- Prevent booking conflicts and human error.
- Allow staff and administrators to manage reservations efficiently.
- Improve customer experience through secure self-service booking management.

---

## Target Users

- **Customers**
  - View site content and gallery.
  - Register, verify their email, and log in.
  - Make, edit, and cancel their own bookings.

- **Staff Users**
  - Access a reservations page when logged in.
  - View and edit all bookings when required.

- **Admin Users**
  - Full access to the Django admin panel.
  - Manage bookings, tables, and opening hours.
  - Use a fully filterable bookings list for efficient administration.

---

## Features

### Authentication & Authorisation
- Only logged-in users can create bookings.
- Automated email verification ensures valid user accounts.
- Role-based access separates customer, staff, and admin functionality.
- If Admin cancels a booking an email with custom notificatiojn is sent to the customer.

### Booking System
- Users select a date, party size, and available time slot.
- Available slots are generated dynamically based on:
  - Opening hours
  - Booking duration
  - Existing reservations
- Users can edit or cancel their own bookings.
- Staff can edit bookings if required.

### Validation & Business Rules
- Bookings cannot be made outside opening hours.
- Bookings cannot be made in the past.
- Double bookings are prevented at both application and database level.
- The smallest suitable available table is assigned automatically.

---

## Data Model Overview

### Table
- Stores table number and seating capacity.

### OpeningHours
- Stores opening and closing times per weekday.
- One entry per weekday enforced.

### Booking
- Linked to a user and a table.
- Stores party size, allergies, start time, status, and unique reference.
- Uses a stored time range for overlap detection.

---

## Booking Logic (Technical Overview)

1. Opening hours are retrieved for the selected date.
2. Time slots are generated from opening to closing time at fixed intervals.
3. Slots in the past are excluded for same-day bookings.
4. For each slot, the system checks whether at least one suitable table exists without an overlapping booking.
5. On save, the booking is assigned the smallest available table that meets the party size requirement.
6. PostgreSQL exclusion constraints prevent overlapping bookings for the same table.

---

## Tech Stack

### Backend
- **Python**
- **Django**
- **Javascript**

### Database
- **PostgreSQL**
  - Uses range fields and exclusion constraints to prevent overlapping bookings.

### Frontend
- **Bootstrap**
  - Responsive layout and styling.

### Media Storage
- **Cloudinary**
  - Used for image storage and delivery.

### Deployment
- **Heroku**
  - Hosts the live application with integrated PostgreSQL and Cloudinary services.

---

## Testing

### HTML, Javascript and CSS and Lighthouse

All have been parsed through HTML, CSS and Javascript validators respectively and no problems were found.

Lighthouse returned figures of 90 for Accessibility and 100 for Best Practice. Due to an issue with Lighthouse it was not able to return a Performance score.

### Automated Testing

Automated tests were written using Django’s built-in testing framework.

Automated tests cover:
- Booking form validation
- Required field enforcement
- Valid time slot selection
- Editing bookings without triggering false overlap errors
- Prevention of overlapping bookings
- Available Slot Generation
- Booking to Table allocation
- Cancellation of Bookings

All automated tests pass successfully.


---

### Manual Testing

Manual testing was carried out to verify core user journeys and system behaviour.  
The table below can be used as a checklist to confirm functionality.

| Feature | Steps | Expected Result | Result |
|-------|------|----------------|--------|
| Account registration | Register with valid email | Verification email sent | Pass |
| Email verification | Click verification link | Account activated | Pass |
| Change Password | Allows User to change password when logged in | Password changed | Pass |
| Reset Password | Allows unauthenticated user to reset password by email | Password reset | Pass |
| Login required | Access booking page while logged out | Only visible when logged in | Pass |
| View gallery/menu | Navigate site pages | Content displays correctly | Pass |
| Create booking | Select date, party size, slot | Booking created successfully | Pass |
| Booking reference | Submit booking | Unique reference generated | Pass |
| Outside opening hours | Attempt invalid time | Slot unavailable | Pass |
| Booking in the past | Attempt same-day past slot | Slot unavailable | Pass |
| Prevent double booking | Unable to make overlapping booking | Slot Unavailable | Pass |
| Edit booking | Edit booking and keep same slot | Booking updates successfully | Pass |
| Cancel booking | Cancel existing booking | Booking cancelled | Pass |
| Staff reservations | Login as staff | All bookings visible | Pass |
| Staff edit booking | Edit booking as staff | Booking updates | Pass |
| Admin access | Login as admin | Admin panel accessible | Pass |
| Admin Cancel Booking | Emails user cancellation notice | Email received | Pass |
| Admin filtering | Filter bookings in admin | Results filtered correctly | Pass |

---

### Validation Testing

The following validation rules were manually verified:
- Date field must be provided.
- Party size must be numeric and greater than zero.
- Selected time slot must be one of the available options.
- Booking time must fall within opening hours.
- Bookings cannot be made in the past.
- Double bookings for the same table and time are prevented.

---

### Responsiveness & Browser Compatibility

The site was tested for responsiveness using browser developer tools and physical devices.

- Screen sizes tested:
  - Mobile
  - Tablet
  - Desktop
- Browsers tested:
  - Google Chrome
  - Mozilla Firefox
  - Safari

Bootstrap ensures a consistent and responsive layout across all supported devices.

---

### Bugs & Fixes

- **Edit booking overlap issue:**  
  Editing an existing booking initially failed due to the booking being included in overlap validation.  
  This was resolved by excluding the booking itself from overlap checks while editing.

---

## Deployment

The project was deployed to **Heroku** using the following steps:

1. Create a Heroku application.
2. Configure environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `CLOUDINARY_URL`
3. Attach a Heroku PostgreSQL database.
4. Deploy the application from GitHub.
5. Run database migrations and create a superuser.

---

## Credits

- Django Documentation
- PostgreSQL Documentation
- Heroku Documentation
- Cloudinary Documentation
- Bootstrap Documentation

---

## Acknowledgements

This project was developed by **Greg Phillips** as part of a Code Institute coursework submission.