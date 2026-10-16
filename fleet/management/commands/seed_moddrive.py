from django.core.management.base import BaseCommand

from fleet.models import DrivingRoute, Vehicle


class Command(BaseCommand):
    help = 'Create sample ModDrive vehicles and routes.'

    def handle(self, *args, **options):
        vehicles = [
            {
                'name': '1969 Ford Mustang Restomod', 'vehicle_type': 'coupe', 'transmission': 'manual',
                'daily_price': 295, 'is_featured': True,
                'description': 'Classic American style with modern handling and braking.',
                'modifications': 'Fuel-injected V8, coilover suspension, performance brakes, upgraded cooling.',
                'image_url': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=1200&q=80',
            },
            {
                'name': 'Toyota Tacoma TRD Pro', 'vehicle_type': 'truck', 'transmission': 'automatic',
                'daily_price': 245, 'is_featured': True,
                'description': 'Trail-ready truck prepared for Texas back roads.',
                'modifications': 'Lift kit, all-terrain tires, skid plates, recovery equipment.',
                'image_url': 'https://images.unsplash.com/photo-1551830820-330a71b99659?auto=format&fit=crop&w=1200&q=80',
            },
            {
                'name': 'Mazda MX-5 Track Edition', 'vehicle_type': 'coupe', 'transmission': 'manual',
                'daily_price': 210, 'is_featured': True,
                'description': 'Lightweight roadster tuned for a responsive driving experience.',
                'modifications': 'Sport suspension, performance exhaust, roll bar, upgraded tires.',
                'image_url': 'https://images.unsplash.com/photo-1504215680853-026ed2a45def?auto=format&fit=crop&w=1200&q=80',
            },
            {
                'name': 'Subaru WRX Rally Build', 'vehicle_type': 'sedan', 'transmission': 'manual',
                'daily_price': 230, 'is_featured': False,
                'description': 'All-wheel-drive sedan set up for confident all-weather driving.',
                'modifications': 'ECU tune, coilovers, intercooler, performance brakes.',
                'image_url': 'https://images.unsplash.com/photo-1619767886558-efdc259cde1a?auto=format&fit=crop&w=1200&q=80',
            },
        ]
        vehicle_objects = []
        for data in vehicles:
            vehicle, _ = Vehicle.objects.update_or_create(name=data['name'], defaults=data)
            vehicle_objects.append(vehicle)

        routes = [
            {
                'name': 'Big Bend Scenic Run', 'location': 'West Texas', 'distance_miles': 118,
                'estimated_hours': 3.5, 'additional_price': 85,
                'description': 'A scenic route with desert landscapes and long open-road sections.',
                'image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80',
            },
            {
                'name': 'Texas Hill Country Drive', 'location': 'Central Texas', 'distance_miles': 92,
                'estimated_hours': 3, 'additional_price': 60,
                'description': 'Curving roads, overlooks, and small-town stops through Hill Country.',
                'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
            },
            {
                'name': 'Gulf Coast Cruise', 'location': 'Texas Gulf Coast', 'distance_miles': 74,
                'estimated_hours': 2.5, 'additional_price': 45,
                'description': 'A relaxed coastal route designed for street-focused vehicles.',
                'image_url': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80',
            },
        ]
        for data in routes:
            route, _ = DrivingRoute.objects.update_or_create(name=data['name'], defaults=data)
            route.vehicles.set(vehicle_objects)

        self.stdout.write(self.style.SUCCESS('Sample ModDrive data is ready.'))
