# Generated by Django 4.2 on 2023-04-27 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0007_alter_buttonlinkmessagequestion_q_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalBtnLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_link', models.CharField(default='https://ecargo.com.bd/', help_text='Enter Target Page Link Here To Redirect. this can be diffrent from the above link.', max_length=800, null=True)),
                ('button_name', models.CharField(default='Visit Now', help_text='Button show this text on it', max_length=800, null=True)),
                ('q_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chatbot_app.buttonlinkmessage')),
            ],
        ),
    ]
