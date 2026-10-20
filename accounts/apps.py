from django.contrib.auth import get_user_model
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.models.signals import m2m_changed

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(setup_roles, sender=self)
        m2m_changed.connect(administrator_group_changed, sender=get_user_model().groups.through)

def setup_roles(sender, **kwargs):
    Group = kwargs["apps"].get_model("auth", "Group")
    Permission = kwargs["apps"].get_model("auth", "Permission")
    roles = ["Customer", "Booking Staff", "Fleet Manager", "Administrator"]
    
    for role in roles:
        Group.objects.using(kwargs["using"]).get_or_create(name=role)

    booking_staff = Group.objects.using(kwargs["using"]).get(name="Booking Staff")
    
    booking_permissions = Permission.objects.using(kwargs["using"]).filter(        
        content_type__app_label="bookings",
        content_type__model="booking",
        codename__in=["view_booking", "change_booking"]
    )
    
    booking_staff.permissions.add(*booking_permissions)

    fleet_manager = Group.objects.using(kwargs["using"]).get(name="Fleet Manager")

    vehicle_permissions = Permission.objects.using(kwargs["using"]).filter(
        content_type__app_label="fleet",
        content_type__model="vehicle",
        codename__in=[
            "add_vehicle",
            "change_vehicle",
            "delete_vehicle",
            "view_vehicle"
        ]
    )

    fleet_manager.permissions.add(*vehicle_permissions)

    route_permissions = Permission.objects.using(kwargs["using"]).filter(
        content_type__app_label="fleet",
        content_type__model="drivingroute",
        codename__in=[
            "add_drivingroute",
            "change_drivingroute",
            "delete_drivingroute",
            "view_drivingroute"
        ]
    )

    fleet_manager.permissions.add(*route_permissions)

    administrator = Group.objects.using(kwargs["using"]).get(name="Administrator")

    admin_permissions = Permission.objects.using(kwargs["using"]).filter(
        content_type__app_label__in=["bookings", "fleet"]
    )

    administrator.permissions.add(*admin_permissions)

def administrator_group_changed(sender, instance, action, reverse, pk_set, **kwargs):
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    User = get_user_model()
    Group = User.groups.field.remote_field.model

    if reverse:
        if instance.name != "Administrator":
            return

        if action == "post_clear":
            return

        for user in User.objects.filter(pk__in=pk_set):
            if action == "post_add":
                user.is_staff = True
            else:
                user.is_staff = user.is_superuser
            user.save(update_fields=["is_staff"])
        return

    if action == "post_add":
        if Group.objects.filter(
            pk__in=pk_set, name="Administrator"
        ).exists():
            instance.is_staff = True
            instance.save(update_fields=["is_staff"])

    elif action in ["post_remove", "post_clear"]:
        instance.is_staff = (
            instance.is_superuser
            or instance.groups.filter(name="Administrator").exists()
        )
        instance.save(update_fields=["is_staff"])