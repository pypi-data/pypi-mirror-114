=====
Mad Notifications
=====

Mad Notifications app for django to send notifications to the user

Quick start
-----------

1. Add "mad_notifications" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mad_notifications',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('notifications/', include('mad_notifications.api.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
