# ModDrive

ModDrive is a Django web application for browsing professionally modified vehicles, selecting curated Texas driving routes, saving Favorites, and submitting staff-reviewed booking requests.

## Local setup

```bash
cd ~/Desktop/Moddrive
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_moddrive
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Main pages

- `/` homepage
- `/fleet/` fleet and filters
- `/fleet/routes/` curated routes
- `/fleet/favorites/` customer Favorites
- `/accounts/register/` registration
- `/accounts/login/` login
- `/bookings/mine/` customer booking history
- `/bookings/staff/` protected staff dashboard
- `/admin/` Django administration

Staff access requires a user with `is_staff` enabled. Use the Django admin site to grant staff access.
