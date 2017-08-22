from django.db import models

# Create your models here.
class Customer(models.Model):
    '''客户信息表'''
    # 客户姓名，客户有可能不告知名字，可以为空
    name = models.CharField(max_length=32, blank=True, null=True)
    # qq唯一，必须有，主要招生来源
    qq = models.CharField(max_length=64, unique=True)
    # qq名，可以为空
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    # 手机不是必须的，有些qq客户咨询可能不会告知手机号码
    phone = models.CharField(max_length=64, blank=True, null=True)
    # 客户来源
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '市场推广'))
    source = models.SmallIntegerField(choices=source_choices)
    # 转介绍人的qq，将来可以扩展积分商城
    referral_from = models.CharField(verbose_name='转介绍人QQ', max_length=64, blank=True, null=True)
    # 客户咨询的课程
    consult_course = models.ForeignKey('Course', verbose_name='咨询课程')
    # 客户咨询的详情内容
    content = models.TextField(verbose_name='咨询详情')
    # 给客户打上标签，后期可以用来统计客户
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    # 入学后对应的账户表
    consultant = models.ForeignKey('UserProfile')
    # 做备忘录，添加一下备注
    memo = models.TextField(blank=True, null=True)
    # 咨询的日期
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.qq

class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    pass


class Course(models.Model):
    '''课程表'''
    pass


class ClassList(models.Model):
    '''班级表'''
    pass


class CourseRecord(models.Model):
    '''上课记录'''
    pass


class StudyRecord(models.Model):
    '''学习记录'''
    pass


class Enrollment(models.Model):
    '''报名表'''
    pass


class UserProfile(models.Model):
    '''账号表'''
    pass


class  Role(models.Model):
    '''角色表'''
    pass
