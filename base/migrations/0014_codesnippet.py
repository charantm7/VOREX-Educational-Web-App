# Generated by Django 5.2 on 2025-04-20 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_room_tags'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSnippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('c', 'C'), ('cpp', 'C++'), ('java', 'Java'), ('html', 'HTML'), ('css', 'CSS'), ('sql', 'SQL'), ('php', 'PHP'), ('ruby', 'Ruby'), ('swift', 'Swift'), ('kotlin', 'Kotlin'), ('go', 'Go'), ('rust', 'Rust'), ('typescript', 'TypeScript'), ('c#', 'C#')], max_length=50)),
                ('code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_snippets', to='base.room')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
