from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='accounts.Profile')
def create_profile_grade(instance, created, sender, **kwargs):
    from accounts.models import ProfileGrades
    if created and instance.role != sender.ROLE_USER:
        ProfileGrades.objects.get_or_create(profile=instance)


@receiver(post_save, sender='accounts.Profile')
def add_emails_subs_to_profile(instance, created, sender, **kwargs):
    if created:
        instance.email_settings.add(*instance.get_email_settings())
