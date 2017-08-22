# PerfectCRM 客户管理系统

## 需求分析：
	* 销售顾问：
		+ 对有效客户信息进行存储
		+ 客户跟进记录
		+ 办理报名手续
		+ 各种维度查询、过滤客户信息
	* 讲师：
		+ 点名
		+ 批作业
		+ 创建上课记录
		+ 查看班级成绩
		+ 课时申报
		+ 问卷调查
	* 学生：
		+ 交作业
		+ 查成绩
		+ 请假
		+ 我的合同
		+ 我的推荐
		+ 投诉建议
	* 老板任务：
		+ 销售报表分析
		+ 教学质量报表
## 架构分析：
	* 用户：面对企业内部职员使用，在安全、界面可以放宽条件
	* 用户量：小，主要内容管理，选择django很合适
	* 业务场景：满足内容需求，要求快速开发上线，周期短。
	* 综上所述，架构简单，django能满足。

## 组件选择：
	* django
	* bootstrap 
	* jquery

## 设计表结构
	* 设计表结构的重要性：前端与后端的交互都是在与数据库进行交互，如果表结构设计不好，代码编写到一定量的时候，发现表结构有问题，会带来开发的难度，甚至导致后期开发不断出现问题。所以做好表结构设计，可以使得开发过程避免走弯路。
	
	
	