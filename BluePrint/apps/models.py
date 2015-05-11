# -*- coding:utf-8 -*-
from apps import db

class User(db.Model):
	id = db.Column(db.String(255), primary_key=True)
	password = db.Column(db.String(255))
	date = db.Column(db.DateTime(), default=db.func.now())
	# 회원가입 당 시, 정보 입력(청소년,신입생,복학생,취준생,직장인)
	user_category=db.Column(db.String(255),default="신입생")
	input_jobs=db.Column(db.String(255),default="0")


class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('jobs', cascade='all, delete-orphan'))
	write_date = db.Column(db.DateTime(), default=db.func.now())
	
	# 분과
	department=db.Column(db.String(255))
	# 전공
	major=db.Column(db.String(255),default=u"없음")
	# 닉네임
	nic_name=db.Column(db.String(255),default=u"진로켓 유저")
	# 진로
	job=db.Column(db.String(255),default=u"없음")
	# 학과 한 줄평
	major_comment=db.Column(db.String(255),default=u"좋습니다.")
	# 학과 이야기
	major_story=db.Column(db.Text(65535),default=u"학과 분위기와 진로등 모두 만족합니다.")
	# 학과 만족도
	major_like=db.Column(db.String(255))
	# 복수전공 유무(y/n)
	check_double_major=db.Column(db.String(255))
	# 복수전공 과목
	double_major=db.Column(db.String(255),default=u"없음")
	# 진로를 선택하게 된 이유
	job_reason=db.Column(db.Text(65535),default=u"일반적으로 가는 진로라서 선택하였습니다.")

	
	# 진로와의 상관관계 점수(전공/자격증/복수전공/대외활동/독서)
	
	# 전공 공부
	point_major=db.Column(db.String(255))
	# 자격증
	point_licence=db.Column(db.String(255))
	# 복수전공
	point_double_major=db.Column(db.String(255))
	# 독서
	point_reading=db.Column(db.String(255))
	# 대외활동
	point_extra=db.Column(db.String(255))

	# 추가 사항(1~2) 우선 해당 내용 추가 안함. 오픈베타 시작 후 ajax이용해서 비동기식 
	point_ex_1=db.Column(db.String(255))
	point_ex_2=db.Column(db.String(255))

	def json_dump(self):
		return dict(job=self.job, count=0)



