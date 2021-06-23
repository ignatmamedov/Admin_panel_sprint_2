import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Genre, Person, Filmwork, User


@receiver(pre_save, sender=Person)
def congratulatory(sender, instance, **kwargs):
    if instance.first_name == "Joe":
        print(f"У {instance.first_name} сегодня день рождения! 🥳")
