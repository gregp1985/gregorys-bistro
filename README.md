# Gregory’s Bistro

Gregory’s Bistro is a fictional restaurant website with a fully automated online table booking system. Authenticated users can create, edit, and cancel reservations, while staff and administrators can manage bookings through dedicated interfaces. The system enforces opening hours, prevents double bookings, and assigns the most appropriate available table automatically.

**Developer: Greg Phillips**

---

## Table of Contents
- [Live Site & Repository](#live-site--repository)
- [Project Goals](#project-goals)
- [Target Users](#target-users)
- [Agile Project Management](#agile-project-management)
- [Design](#design)
  - [Colours](#colours)
  - [Fonts](#fonts)
  - [Structure](#structure)
    - [Website Pages](#website-pages)
    - [Database](#database)
  - [Wireframes](#wireframes)
- [Features](#features)
- [Booking Logic](#booking-logic-technical-overview)
- [Tech Stack](#tech-stack)
- [Testing](#testing)
  - [HTML, Javascript and CSS and Lighthouse](#html-javascript-and-css-and-lighthouse)
  - [Automated Testing](#automated-testing)
  - [Manual Testing](#manual-testing)
  - [Validation](#validation-testing)
  - [Responsiveness](#responsiveness--browser-compatibility)
  - [Bugs & Fixes](#bugs--fixes)
- [Deployment](#deployment-1)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)


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
  - Access the Cancellations page when logged in.
  - View, edit, cancel and delete all bookings when required.

- **Admin Users**
  - Full access to the Django admin panel.
  - Manage registered user accounts.
  - Manage bookings, tables, and opening hours.
  - Use a fully filterable bookings list for efficient administration.

---

## Agile Project Management

### Kanban, Epics & User Stories

- GitHub Kanban was used to track all open user stories
- Epics were created using the milestones feature
- Backlog, In Progress, Done headings were used in the kanban

- **Project (Kanban) Board:** Using Github: https://github.com/users/gregp1985/projects/4

<details><summary>Kanban</summary>
<img src='/readmefiles/kanban.png'>
</details>
<details><summary>User Stories</summary>
<img src='/readmefiles/user_stories.png'>
</details>
<details><summary>Milestones</summary>
<img src='/readmefiles/milestones.png'>
</details>

### User Stories

1. As a user I can login to the website so that my details are stored for future bookings (must-have)
2. As a user, I can login to make bookings, edit bookings and cancel bookings so that bookings can be self managed (must-have)
3. As a user, whether logged in or not, I can view or download the Menu so that users can decide if the food and price point is right for them (could-have)
4. As a user without being logged in I can view Opening Times, Restaurant Location and Contact Details so that users can determine if the location is suitable as well as times for bookings. And if they want they can contact the restaurant (could-have)
5. As Site Admin, when logged in, I can view current and cancelled bookings so that i can determine how busy or popular the restaurant is (must-have)
6. As Site Admin I can log in to get a list of registered users and see their previous booking history so that admin can manage registered user accounts (should-have)
7. As Site Admin I can log in to adjust restaurant opening hours so that bookings are not made out of open hours (could-have)
8. As Site Admin I will be able to view any booking clashes or issues (inc due to opening hours changes) so that if this does happen the user can be notified (should-have)
9. As Site Admin I can manage existing booking including cancelling with custom notifications so that users are made aware of cancellations to their reservations and have the opportunity to rebook (should-have)
10. As a staff member I can log in to view, edit, cancel and delete bookings so that when open the restaurant bookings can be managed in real time and allow for walkins (must-have)

---

## Design

### Colours

Having looked at other similar websites I decided on a warm yellow and deep reds feel to the website, as this is supposed to give a feeling of a cosy bistro.
The initial colour scheme didn't pass the contrast checkers so they were adjusted to use #E2A428 for the background and #470606 for the foreground. This passes all contrast criteria with a ratio of 7.38:1.

### Fonts

The fonts selected were from Google Fonts, Playfair Display with sans-serif as a backup font.

### Structure

#### Website Pages

The site was designed for the user to be familiar with the layout such as a navigation bar along the top of the pages and a hamburger menu button for smaller screen.

The footer contains all relevant social media links that the business has so the user can visit any social media site and follow the business there to expand the businesses followers, likes and shares.

- The site consists of the following pages:
  - Homepage with links to Login or to Book a table, depending on whether the user is already logged in or not. There is also some info about the restaurant and some featured dishes
  - Gallery which has images of some of the food as well as images of the restaurant
  - Menu Page which has the current list of all available items with filters and an option to download the menu as PDF
  - Contact Page allows the user to contact us from the displayed email and phone number or visit the address listed.
  - Book a Table page (appears only if user is logged in) allows registered users to book a table based on party size, date and time requested. and allows them to enter any allergies. This page also allows user to see previous bookings and upcoming bookings with options to edit or cancel bookings
  - Staff Bookings (appears if staff member is logged in) allows staff members to book a new table or edit an existing booking. This has an extra selection box for the user for the booking
  - Reservations Page (appears if staff member is logged in) allows staff to view a calendar with all existing bookings which upon click can be cancelled or editted (via the Staff bookings page)
  - Cancellations Page (appears if staff member is logged in) allows staff to view cancelled bookings and acknowledge and delete the bookings
  - Login / Logout allows users to login to make bookings, view, edit, and cancel bookings
  - Register allows the user to regiser so they can use the booking system
  - Account Page allows logged in users to view their account, and change the email or password

#### Database

- Built with Python and the Django framework with a Postgres database for the deployed Heroku version(production)
- Three database models show all the fields stored in the database

<details><summary>Show diagram</summary>
<img src='/readmefiles/database_models.jpg'>
</details>

##### Table model
- Stores table number and seating capacity.
- The table model contains:
  - number
  - seats

##### OpeningHours model
- Stores opening and closing times per weekday.
- One entry per weekday enforced.
- The OpeningHours model contains:
  - weekday
  - open_time
  - close_time

##### Booking model
- Linked to a user and a table.
- Stores party size, allergies, start time, status, and unique reference.
- Uses a stored time range for overlap detection.
- The Booking model contains:
  - table *ForeignKey Table Model
  - name *ForeignKey User Model
  - reference
  - allergies
  - party_size
  - start_time
  - time_range
  - status

#### Wireframes

<details><summary>Show wireframes</summary>
<img src='/readmefiles/wireframes-ss.jpg'>
</details>
- **Wireframes:** Built with Mockflow (PDF Download): <a href='/readmefiles/pdf/Wireframes-gregorys.pdf'>Wireframes PDF</a>

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
- Staff can edit, cancel and delete bookings as required.

### Validation & Business Rules
- Bookings cannot be made outside opening hours.
- Bookings cannot be made in the past.
- Double bookings are prevented at both application and database level.
- The smallest suitable available table is assigned automatically.

### CRUD functions
- Both Staff and User can create bookings by their repective boooking pages when logged in.
- Both Staff and Users can edit or cancel bookings. Users from the booking page and staff from the reservations page.
- Staff can Acknowledge and delete cancelled bookings from the cancellations page when logged in.

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
- [Postgres](https://www.postgresql.org/)
  - Uses range fields and exclusion constraints to prevent overlapping bookings.

### Frontend
- [Bootstrap v5.2](https://getbootstrap.com/)
  - Responsive layout and styling.

### Version Management and Repository
- [GitHub](https://github.com/)

### Fonts
- [Google Fonts](https://fonts.google.com/)

### Wireframes
- [Mockflow](https://mockflow.com/)

### Media Storage
- [Cloudinary](https://cloudinary.com/)
  - Used for image storage and delivery.

### Deployment
- [Heroku Platform](https://id.heroku.com/login)
  - Hosts the live application with integrated PostgreSQL and Cloudinary services.

### Validation
  - [WC3 Validator](https://validator.w3.org/)
  - [Jigsaw W3 Validator](https://jigsaw.w3.org/css-validator/)
  - [JShint](https://jshint.com/)
  - [Pycodestyle(PEP8)](https://pypi.org/project/pycodestyle/)
  - [Lighthouse](https://developers.google.com/web/tools/lighthouse/)
  - [Wave Validator](https://wave.webaim.org/)
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
| Staff make booking | Make booking as staff | Booking created | Pass |
| Staff edit booking | Edit booking as staff | Booking updates | Pass |
| Staff cancel booking | Cancel booking as staff | Booking cancelled | Pass |
| Staff delete booking | Delete booking as staff | Booking deleted | Pass |
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

### Heroku Deployment

[Official Page](https://devcenter.heroku.com/articles/git) (Ctrl + click)

This application has been deployed from Github using Heroku. Here's how:

1. Create an account at heroku.com

2. Create an app, give it a name for such as ci-pp4-the-diplomat, and select a region

3. Under resources search for postgres, and add a Postgres database to the app

Heroku Postgres

1. Note the DATABASE_URL, this can be set as an environment variable in Heroku and your local deployment(env.py)

2. Install the plugins dj-database-url and psycopg2-binary.

3. Run pip3 freeze > requirements.txt so both are added to the requirements.txt file

4. Create a Procfile with the text: web: gunicorn the_diplomat.wsgi

5. In the settings.py ensure the connection is to the Heroku postgres database, no indentation if you are not using a seperate test database.
I store mine in env.py

6. Ensure debug is set to false in the settings.py file

7. Add localhost, and herokuapp.com to the ALLOWED_HOSTS variable in settings.py

8. Run "python3 manage.py showmigrations" to check the status of the migrations

9. Run "python3 manage.py migrate" to migrate the database

10. Run "python3 manage.py createsuperuser" to create a super/admin user

11. Run "python3 manage.py loaddata categories.json" on the categories file in products/fixtures to create the categories

12. Run "python3 manage.py loaddata products.json" on the products file in products/fixtures to create the products

13. Install gunicorn and add it to the requirements.txt file using the command pip3 freeze > requirements.txt

14. Disable collectstatic in Heroku before any code is pushed using the command heroku config:set DISABLE_COLLECTSTATIC=1 -a ci-pp4-the-diplomat

15. Ensure the following environment variables are set in Heroku

16. Connect the app to GitHub, and enable automatic deploys from main if you wish

17. Click deploy to deploy your application to Heroku for the first time

18. Click on the link provided to access the application

19. If you encounter any issues accessing the build logs is a good way to troubleshoot the issue
<hr>

### Fork Repository
To fork the repository by following these steps:
1. Go to the GitHub repository
2. Click on Fork button in upper right hand corner
<hr>

### Clone Repository
You can clone the repository by following these steps:
1. Go to the GitHub repository 
2. Locate the Code button above the list of files and click it 
3. Select if you prefere to clone using HTTPS, SSH, or Github CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash
5. Change the current working directory to the one where you want the cloned directory
6. Type git clone and paste the URL from the clipboard ($ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY)
7.Press Enter to create your local clone.

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