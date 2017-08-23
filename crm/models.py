from django.db import models
from celery.worker.strategy import default
from django.contrib.auth.models import  User

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
    status_choices = ((0, '已报名'),
                      (1, '未报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=1)
    # 入学后对应的账户表
    consultant = models.ForeignKey('UserProfile')
    # 做备忘录，添加一下备注
    memo = models.TextField(blank=True, null=True)
    # 咨询的日期
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.qq
    
    class Meta:
        verbose_name = '客户表'
        verbose_name_plural = '客户表'


class Tag(models.Model):
    '''标签'''
    # 根据Customer客户信息表的字段进行补充的
    # 标签的名字，唯一
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
    
    
class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    # 根据哪个客户，外键关联用户信息表
    customer = models.ForeignKey('Customer')
    # 怎么跟进的，对跟进内容做详细记录
    content = models.TextField(verbose_name='跟进内容')
    # 销售顾问跟进用户的详细信息记录，外键关联账号表
    consultant = models.ForeignKey('UserProfile')
    # 跟进判断客户意向
    intention_choices = ((0, '2周内报名'),
                         (1, '1个月报名'),
                         (2, '近期无表名计划'),
                         (3, '已在其它机构报名'),
                         (4, '已报名'),
                         (5, '已拉黑'),
                         )
    intention = models.SmallIntegerField(choices=intention_choices)
    # 跟进日期
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '<%s : %s>'%(self.customer.qq, self.intention)    
    
    class Meta:
        verbose_name = '客户跟进表'
        verbose_name_plural = '客户跟进记录'


class Course(models.Model):
    '''课程表'''
    # 课程的名字
    name = models.CharField(max_length=64, unique=True)
    # 课程的价格
    price = models.PositiveSmallIntegerField()
    # 课程周期
    period = models.PositiveSmallIntegerField(verbose_name='周期（月）')
    # 课程大纲
    outline = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'


# 补充：分校表，后期业务发展起来，没考虑到这点，会很麻烦
class Branch(models.Model):
    '''校区表'''
    # 分校名称
    name = models.CharField(max_length=128, unique=True)
    # 分校地址
    addr = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '分校'
        verbose_name_plural = '分校'
    

class ClassList(models.Model):
    '''班级表'''
    # 班级所在校区，外键关联校区表
    branch = models.ForeignKey('Branch', verbose_name='分校')
    # 班级所授课程，外键关联课程表
    course = models.ForeignKey('Course')
    # 班级的类型
    class_type_choices = ((0, '面授（脱产）'),
                          (1, '面试（周末）'),
                          (2, '网络班'),
                          )
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name='班级类型')
    # 开班期数
    semester = models.PositiveIntegerField(verbose_name='学期')
    # 班级上课的老师，多对多
    teachers = models.ManyToManyField('UserProfile')
    # 开班日期必须有，不能为空
    start_date = models.DateField(verbose_name='开班日期')
    # 结业日期不重要，所以可以为空
    end_date = models.DateTimeField(verbose_name='结业日期', blank=True, null=True)
    
    def __str__(self):
        return "%s %s %s"%(self.branch, self.course, self.semester)
    
    # 通过多个字段保持唯一性
    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name = '班级'
        verbose_name_plural = '班级'


class CourseRecord(models.Model):
    '''上课记录'''
    from_class = models.ForeignKey('ClassList', verbose_name='班级')
    day_num = models.PositiveSmallIntegerField(verbose_name='第几天（天）')
    # 上课的老师是一对多
    teacher = models.ForeignKey('UserProfile')
    # 是否有作业，默认有
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name='本节课课程大纲')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s %s'%(self.from_class, self.day_num)
    
    class Meta:
        unique_together = ('from_class', 'day_num')
        verbose_name = '上课记录'
        verbose_name_plural = '上课记录'
        
        
class StudyRecord(models.Model):
    '''学习记录'''
    # 学生，外键关联报名表
    student = models.ForeignKey('Enrollment')
    # 上课记录，外键关联上课记录表
    course_record = models.ForeignKey('CourseRecord')
    # 出勤类型
    attendance_choices = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '早退'),
                          )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    # 分数，-50,-100罚款, 0考虑肯能中途入班，前面分数为0的情况
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (85, 'B'),
                     (75, 'B-'),
                     (70, 'C+'),
                     (60, 'C'),
                     (40, 'C-'),
                     (-50, 'D'),
                     (-100, 'COPY'),
                     (0, 'N/A'),
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    # 备注
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s %s %s'%(self.student, self.course, self.score)
    
    class Meta:
        verbose_name = '学习记录'
        verbose_name_plural = '学习记录'


class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer')
    enrolled_class = models.ForeignKey('ClassList', verbose_name='所报班级')
    # 课程顾问
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问') 
    contract_agreed = models.BooleanField(default=False, verbose_name='学员已同意合同')
    contract_approved =models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s %s'%(self.customer, self.enrolled_class)
    
    # 使用多外键唯一
    class meta:
        unique_torgether = ('customer', 'enrolled_class')
        verbose_name = '报名表'
        verbose_name_plural = '报名表'


# 补充：缴费表
class Payment(models.Model):
    '''缴费记录'''
    customer = models.ForeignKey('Customer')
    course = models.ForeignKey('Course', verbose_name='所报课程')
    # 默认定金500
    amount = models.PositiveIntegerField(verbose_name='数额', default=500)
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return '%s %s'%(self.customer, self.amount)
    
    class Meta:
        verbose_name = '缴费记录'
        verbose_name_plural = '缴费记录'

class UserProfile(models.Model):
    '''账号表'''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', blank=True, null=True)

    def __str__(self):
        return self.name

class  Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'
        

class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name