# Generated by Django 5.0.4 on 2024-05-03 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_groupe_tarif'),
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payé',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planning',
            name='apc',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='apcc', to='planning.apc'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='medecin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='med_RDV', to='account.medecin'),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pat_RDV', to='account.user'),
        ),
    ]
