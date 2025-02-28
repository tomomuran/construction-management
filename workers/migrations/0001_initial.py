# Generated by Django 5.1.5 on 2025-01-25 08:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='氏名')),
                ('employee_number', models.CharField(max_length=50, unique=True, verbose_name='社員番号')),
                ('phone_number', models.CharField(max_length=20, verbose_name='電話番号')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='メールアドレス')),
                ('address', models.TextField(verbose_name='住所')),
                ('employment_status', models.CharField(choices=[('full_time', '正社員'), ('contract', '契約社員'), ('part_time', 'パート'), ('temporary', '派遣')], max_length=20, verbose_name='雇用形態')),
                ('join_date', models.DateField(verbose_name='入社日')),
                ('leave_date', models.DateField(blank=True, null=True, verbose_name='退社日')),
                ('notes', models.TextField(blank=True, verbose_name='備考')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '作業員',
                'verbose_name_plural': '作業員',
                'ordering': ['employee_number'],
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='資格名')),
                ('qualification_number', models.CharField(max_length=100, verbose_name='資格番号')),
                ('issue_date', models.DateField(verbose_name='取得日')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='有効期限')),
                ('notes', models.TextField(blank=True, verbose_name='備考')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='workers.worker', verbose_name='作業員')),
            ],
            options={
                'verbose_name': '資格',
                'verbose_name_plural': '資格',
                'ordering': ['worker', '-issue_date'],
            },
        ),
        migrations.CreateModel(
            name='WorkRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(verbose_name='作業日')),
                ('start_time', models.TimeField(verbose_name='開始時間')),
                ('end_time', models.TimeField(verbose_name='終了時間')),
                ('break_time', models.PositiveIntegerField(default=60, validators=[django.core.validators.MinValueValidator(0)], verbose_name='休憩時間（分）')),
                ('work_description', models.TextField(verbose_name='作業内容')),
                ('notes', models.TextField(blank=True, verbose_name='備考')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='work_records', to='projects.project', verbose_name='プロジェクト')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='work_records', to='workers.worker', verbose_name='作業員')),
            ],
            options={
                'verbose_name': '作業記録',
                'verbose_name_plural': '作業記録',
                'ordering': ['-work_date', '-start_time'],
            },
        ),
    ]
