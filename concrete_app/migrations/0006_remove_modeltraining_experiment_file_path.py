# Generated by Django 5.0.1 on 2024-01-12 04:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("concrete_app", "0005_alter_modeltraining_accuracy_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="modeltraining",
            name="experiment_file_path",
        ),
    ]
