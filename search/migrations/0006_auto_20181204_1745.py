# Generated by Django 2.1.2 on 2018-12-04 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20181109_1739'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskservicesimilarityscore',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='taskservicesimilarityscore',
            name='service',
        ),
        migrations.DeleteModel(
            name='TaskSimilarityScore',
        ),
        migrations.DeleteModel(
            name='TaskServiceSimilarityScore',
        ),
    ]