# Generated by Django 2.2.1 on 2019-06-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_auto_20190615_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='design',
            old_name='detail_banding',
            new_name='banding',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='detail_body',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='detail_buttons',
            new_name='button',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='detail_sleeve',
            new_name='sleeve',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='detail_stripes',
            new_name='stripe',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='font_family',
            new_name='fill',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='font_fill',
            new_name='fontFamily',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='font_size',
            new_name='fontSize',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='font_style',
            new_name='fontStyle',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='text_value',
            new_name='textvalue',
        ),
        migrations.RemoveField(
            model_name='design',
            name='left_arm_text',
        ),
        migrations.AddField(
            model_name='design',
            name='back_image_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='design',
            name='front_image_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='left',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='text',
            name='stroke',
            field=models.CharField(default='#fcfcfc', max_length=7),
        ),
        migrations.AddField(
            model_name='text',
            name='strokewidth',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='text',
            name='top',
            field=models.IntegerField(default=0),
        ),
    ]
