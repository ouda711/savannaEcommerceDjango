# Generated by Django 5.1.5 on 2025-02-01 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=120)),
                ('file_path', models.CharField(max_length=250)),
                ('original_name', models.CharField(max_length=120)),
                ('file_length', models.IntegerField()),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('fileupload_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fileuploads.fileupload')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fileuploads.fileupload',),
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('fileupload_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fileuploads.fileupload')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fileuploads.fileupload',),
        ),
        migrations.CreateModel(
            name='TagImage',
            fields=[
                ('fileupload_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fileuploads.fileupload')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fileuploads.fileupload',),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('fileupload_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fileuploads.fileupload')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='categories.category')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fileuploads.fileupload',),
        ),
    ]
