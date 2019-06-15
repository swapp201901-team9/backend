# Generated by Django 2.2.1 on 2019-06-15 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_auto_20190615_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='design',
            old_name='banding',
            new_name='detail_banding',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='body',
            new_name='detail_body',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='button',
            new_name='detail_buttons',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='sleeve',
            new_name='detail_sleeve',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='stripe',
            new_name='detail_stripes',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='fill',
            new_name='font_family',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='fontFamily',
            new_name='font_fill',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='fontSize',
            new_name='font_size',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='fontStyle',
            new_name='font_style',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='textvalue',
            new_name='text_value',
        ),
        migrations.RemoveField(
            model_name='design',
            name='back_image_url',
        ),
        migrations.RemoveField(
            model_name='design',
            name='front_image_url',
        ),
        migrations.RemoveField(
            model_name='text',
            name='left',
        ),
        migrations.RemoveField(
            model_name='text',
            name='stroke',
        ),
        migrations.RemoveField(
            model_name='text',
            name='strokewidth',
        ),
        migrations.RemoveField(
            model_name='text',
            name='top',
        ),
        migrations.AddField(
            model_name='design',
            name='left_arm_text',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_arm', to='homepage.Text'),
        ),
    ]
