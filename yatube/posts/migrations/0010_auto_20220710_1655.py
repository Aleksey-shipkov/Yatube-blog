# Generated by Django 2.2.16 on 2022-07-10 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20220710_1652'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='prevent_self_follow',
        ),
    ]
