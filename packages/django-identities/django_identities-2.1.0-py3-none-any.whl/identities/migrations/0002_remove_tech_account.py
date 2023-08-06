from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("identities", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalprofile",
            name="is_tech_account",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="is_tech_account",
        ),
    ]
