# Generated by Django 3.1.8 on 2021-04-25 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_adverse_event', '0005_auto_20210120_0005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aeclassification',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'), 'get_latest_by': 'modified', 'ordering': ['display_index', 'display_name']},
        ),
        migrations.AlterModelOptions(
            name='causeofdeath',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'), 'get_latest_by': 'modified', 'ordering': ['display_index', 'display_name']},
        ),
    ]
