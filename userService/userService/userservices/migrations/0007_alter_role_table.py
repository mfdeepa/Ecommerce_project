# Generated by Django 5.1.1 on 2024-11-14 02:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userservices", "0006_alter_role_name_alter_role_table"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="role",
            table="roles",
        ),
    ]