# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-18 18:26
from django.db import migrations

def create_or_update_config_record(apps, schema_editor):
    """Create or update the ElasticsearchBoostConfig record."""

    # Get the model from the versioned app registry to ensure the correct version is used, as described in
    # https://docs.djangoproject.com/en/1.8/ref/migration-operations/#runpython
    ElasticsearchBoostConfig = apps.get_model('edx_haystack_extensions', 'ElasticsearchBoostConfig')
    ElasticsearchBoostConfig.objects.update_or_create(
        # The `solo` library uses 1 for the PrimaryKey to create/lookup the singleton record
        # See https://github.com/lazybird/django-solo/blob/1.1.2/solo/models.py
        pk=1,

        # These values were taken from production on January 20, 2017.
        defaults={
            'function_score': {
                'boost_mode': 'sum',
                'boost': 1.0,
                'score_mode': 'sum',
                'functions': [
                    {'filter': {'term': {'pacing_type_exact': 'self_paced'}}, 'weight': 1.0},
                    {'filter': {'term': {'type_exact': 'MicroMasters'}}, 'weight': 1.0},
                    {'linear': {'start': {'origin': 'now', 'decay': 0.95, 'scale': '1d'}}, 'weight': 5.0}
                ]
            }
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('edx_haystack_extensions', '0001_squashed_0002_auto_20160826_1750'),
    ]

    operations = [
        migrations.RunPython(create_or_update_config_record, reverse_code=migrations.RunPython.noop)
    ]
