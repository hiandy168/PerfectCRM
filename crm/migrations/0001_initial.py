# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('addr', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': '分校',
                'verbose_name_plural': '分校',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_type', models.SmallIntegerField(verbose_name='班级类型', choices=[(0, '面授（脱产）'), (1, '面试（周末）'), (2, '网络班')])),
                ('semester', models.PositiveIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('end_date', models.DateTimeField(verbose_name='结业日期', blank=True, null=True)),
                ('branch', models.ForeignKey(verbose_name='分校', to='crm.Branch')),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price', models.PositiveSmallIntegerField()),
                ('period', models.PositiveSmallIntegerField(verbose_name='周期（月）')),
                ('outline', models.TextField()),
            ],
            options={
                'verbose_name': '课程表',
                'verbose_name_plural': '课程表',
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='第几天（天）')),
                ('has_homework', models.BooleanField(default=True)),
                ('homework_title', models.CharField(max_length=128, blank=True, null=True)),
                ('homework_content', models.TextField(blank=True, null=True)),
                ('outline', models.TextField(verbose_name='本节课课程大纲')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_class', models.ForeignKey(verbose_name='班级', to='crm.ClassList')),
            ],
            options={
                'verbose_name': '上课记录',
                'verbose_name_plural': '上课记录',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, blank=True, null=True)),
                ('qq', models.CharField(max_length=64, unique=True)),
                ('qq_name', models.CharField(max_length=64, blank=True, null=True)),
                ('phone', models.CharField(max_length=64, blank=True, null=True)),
                ('source', models.SmallIntegerField(choices=[(0, '转介绍'), (1, 'QQ群'), (2, '官网'), (3, '百度推广'), (4, '51CTO'), (5, '知乎'), (6, '市场推广')])),
                ('referral_from', models.CharField(verbose_name='转介绍人QQ', max_length=64, blank=True, null=True)),
                ('content', models.TextField(verbose_name='咨询详情')),
                ('status', models.SmallIntegerField(default=1, choices=[(0, '已报名'), (1, '未报名')])),
                ('memo', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consult_course', models.ForeignKey(verbose_name='咨询课程', to='crm.Course')),
            ],
            options={
                'verbose_name': '客户表',
                'verbose_name_plural': '客户表',
            },
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='跟进内容')),
                ('intention', models.SmallIntegerField(choices=[(0, '2周内报名'), (1, '1个月报名'), (2, '近期无表名计划'), (3, '已在其它机构报名'), (4, '已报名'), (5, '已拉黑')])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '客户跟进表',
                'verbose_name_plural': '客户跟进记录',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('contract_agreed', models.BooleanField(verbose_name='学员已同意合同', default=False)),
                ('contract_approved', models.BooleanField(verbose_name='合同已审核', default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('url_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.PositiveIntegerField(verbose_name='数额', default=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '缴费记录',
                'verbose_name_plural': '缴费记录',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('attendance', models.SmallIntegerField(default=0, choices=[(0, '已签到'), (1, '迟到'), (2, '缺勤'), (3, '早退')])),
                ('score', models.SmallIntegerField(default=0, choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (85, 'B'), (75, 'B-'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (-100, 'COPY'), (0, 'N/A')])),
                ('memo', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course_record', models.ForeignKey(to='crm.CourseRecord')),
                ('student', models.ForeignKey(to='crm.Enrollment')),
            ],
            options={
                'verbose_name': '学习记录',
                'verbose_name_plural': '学习记录',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('roles', models.ManyToManyField(blank=True, null=True, to='crm.Role')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='consultant',
            field=models.ForeignKey(to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='course',
            field=models.ForeignKey(verbose_name='所报课程', to='crm.Course'),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(to='crm.Customer'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='consultant',
            field=models.ForeignKey(verbose_name='课程顾问', to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='customer',
            field=models.ForeignKey(to='crm.Customer'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_class',
            field=models.ForeignKey(verbose_name='所报班级', to='crm.ClassList'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='consultant',
            field=models.ForeignKey(to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(to='crm.Customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='crm.Tag'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(to='crm.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='crm.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('from_class', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('branch', 'course', 'semester')]),
        ),
    ]
