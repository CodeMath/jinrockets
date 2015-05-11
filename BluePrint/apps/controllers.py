# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, render_template, session, jsonify, request,flash
from apps import app, db, facebook
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,Job
from sqlalchemy import desc,func
from forms import JoinForm

# main page
@app.route('/')
def index():
	
	main_on="y"
	# count to class Job
	job_count=Job.query.count()

	major_list={}
	major_list['major_lists']= Job.query.order_by(desc(Job.write_date)).all()

	# 로그인 후, 유저의 등록하기 정보가 입력되었는지 체크/ 그리고 마스터인지 아닌지 / 20이 마스터 아이디 / 10이 일반 유저	
	if "session_user_email" in session:
		user_log=User.query.get(session['session_user_email'])
		if user_log.input_jobs == "0" :
			off1="y"	
			return render_template("main.html",major_list=major_list,job_count=job_count,main_on=main_on,off1=off1)	

		elif user_log.input_jobs =="10" :
			off="y"	
			return render_template("main.html",major_list=major_list,job_count=job_count,main_on=main_on,off=off)	


	return render_template("main.html",major_list=major_list,job_count=job_count,main_on=main_on)




@app.route('/list_view')
def list_view():
	rader_count=Job.query.count()
	content={}
	content['major_job'] = Job.query.order_by(desc(Job.write_date)).all()
	list_on="y"
	off1="y"
	# 로그인 상태
	if "session_user_email" in session:
		user_log=User.query.get(session['session_user_email'])
		if user_log.input_jobs=="10" :
			off="y"	
			return render_template("list_view.html", content=content,rader_count=rader_count,list_on=list_on,off=off)
		# 마스터 권한 부여 (db 삭제)
		if user_log.input_jobs=="20" :
			off="y"	
			master="y"
			return render_template("list_view.html", content=content,rader_count=rader_count,list_on=list_on,off=off,master=master)
	# 비로그인
	return render_template("list_view.html", content=content,rader_count=rader_count,list_on=list_on,off1=off1)




# 검색어 입력
@app.route('/list_view/search', methods=['GET','POST'])
def search_text():
	list_on="y"
	off="y"
	off1="y"
	text_search=request.form['search_text']
	rader_count=Job.query.count()
	content={}
	content['major_job']=Job.query.order_by(desc(Job.write_date)).filter_by(major=text_search).all()
	# 로그인 유저
	if "session_user_email" in session:
		user_log=User.query.get(session['session_user_email'])
		# 양식 입력
		if user_log.input_jobs == "10" :
			return render_template("list_view.html",content=content,rader_count=rader_count,list_on=list_on,off=off)
		# 양식 미 입력
		if user_log.input_jobs == "0" :
			return render_template("list_view.html",content=content,rader_count=rader_count,list_on=list_on,off1=off1)
	return render_template("list_view.html",content=content,rader_count=rader_count,list_on=list_on)
	
	
		




@app.route('/list_view/<cate>')
def department(cate):
	off1="y"
	list_on="y"
	off="y"	
	rader_count=Job.query.count()
	content={}
	content['major_job']=Job.query.order_by(desc(Job.write_date)).filter_by(department=cate).all()
	# 로그인 유저
	if "session_user_email" in session:
		user_log=User.query.get(session['session_user_email'])
		# 양식 작성  
		if user_log.input_jobs == "10" :
			return render_template("list_view.html",content=content,rader_count=rader_count,list_on=list_on,off=off)
		# 양식 미작성
		if user_log.input_jobs == "0" :
			return render_template("list_view.html",content=content,rader_count=rader_count,list_on=list_on,off1=off1)
	return render_template("list_view.html", content=content,list_on=list_on)	



@app.route('/infor/<name>')
def infor(name):
	
	if not 'session_user_email' in session:
		flash(u"로그인 되어있지 않음")
		return redirect(url_for('signin'))
	

	user_log=User.query.get(session['session_user_email'])
	# 마스터 아이디 
	if user_log.input_jobs == "20" :
		infors={}
		infors['major_jobs_label']=Job.query.order_by(desc(Job.write_date)).filter_by(major=name).all()
	
		# take job and distinct job's number
		major_filter=Job.query.filter_by(major=name).add_columns(func.count(Job.job)).group_by(Job.job).all()
		infors['major_jobs_count'] = []
		for each in major_filter:
			select = each[0].json_dump()
			select['count'] = each[1]
			infors['major_jobs_count'].append( select )

		# 최근 3개 보내주기
		rows=Job.query.filter_by(major=name).count()
		rows=rows-3
		infors['comment_list']=Job.query.order_by(desc(Job.write_date)).filter_by(major=name).filter(Job.id>rows)

		# average major's score
		zeros=0
		for each in infors['major_jobs_label']:
			zeros+=int(each.major_like)
		zeros=zeros/len(infors['major_jobs_label'])
		return render_template("infor.html", infors=infors,name=name,zeros=zeros)

	# 일반 유저 
	if user_log.input_jobs != "10" :
		flash(u"정보를 입력하세요 ^^")
		return redirect(url_for('write'))
	# off
	off="y"
	# take major query all
	infors={}
	infors['major_jobs_label']=Job.query.order_by(desc(Job.write_date)).filter_by(major=name).all()
	
	# take job and distinct job's number
	major_filter=Job.query.filter_by(major=name).add_columns(func.count(Job.job)).group_by(Job.job).all()
	infors['major_jobs_count'] = []
	for each in major_filter:
		select = each[0].json_dump()
		select['count'] = each[1]
		infors['major_jobs_count'].append( select )
	# 최근 3개 보내주기
	rows=Job.query.filter_by(major=name).count()
	rows=rows-3
	infors['comment_list']=Job.query.order_by(desc(Job.write_date)).filter_by(major=name).filter(Job.id>rows)	

	# average major's score
	zeros=0
	for each in infors['major_jobs_label']:
		zeros+=int(each.major_like)
	zeros=zeros/len(infors['major_jobs_label'])
	return render_template("infor.html", infors=infors,name=name,zeros=zeros,off=off)
		

	

# 1단계 정보 입력
@app.route('/write', methods=['GET','POST'])
def write():
	write_on="y"
	off1="y"
	# 새로운 유저의 정보 입력
	if request.method=='GET':
		return render_template("write.html",write_on=write_on,off1=off1)

	# 정보 입력 db
	major_jobss=Job(
		department=request.form['department'],
		nic_name=request.form['nic_name'],
		major=request.form['major'],
		major_comment=request.form['major_comment'],
		major_story=request.form['major_story'],
		major_like=request.form['major_like'],
		job=request.form['my_job'],
		job_reason=request.form['job_reason'],
		point_major=request.form['point_major'],
		point_licence=request.form['point_licence'],
		point_reading=request.form['point_reading'],
		point_double_major=request.form['point_double_major'],
		point_extra=request.form['point_extra'],
		check_double_major=request.form['check_double_major'],
		double_major=request.form['double_major'],
		user_id=session['session_user_email']
		)
# 추가 예
	# point_ex_1=request.form['point_ex_1'],
	# point_ex_2=request.form['point_ex_2'],
	# 사용자 신분 확인
	
	# 세션 쿼리
	input_user_data=User.query.get(session['session_user_email'])
	# 마스터 아이디 확인
	if input_user_data.input_jobs =="20":
		input_user_data.input_jobs ="20"
		input_user_data.user_category=request.form['user_category']
	else:
		input_user_data.input_jobs="10"
		input_user_data.user_category=request.form['user_category']
	
	
	db.session.add(input_user_data)
	db.session.add(major_jobss)
	db.session.commit()
	
	return redirect(url_for('index'))


# 마이페이지 보기
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
	user_log=User.query.get(session['session_user_email'])
	# 마스터 아이디 마이페이지
	if user_log.input_jobs == "20" :
		off="y"
		mypage_on="y"
		job_list=Job.query.order_by(desc(Job.write_date)).filter_by(user_id=session['session_user_email']).all()
		mypage_user=session['session_user_email']
		return render_template("mypage.html", job_list=job_list,mypage_user=mypage_user,off=off,mypage_on=mypage_on)
	
	# 일반유저 마이페이지 불러오기
	if user_log.input_jobs=="10" :
		off="y"
		mypage_on="y"
		job_list=Job.query.order_by(desc(Job.write_date)).filter_by(user_id=session['session_user_email']).all()
		mypage_user=session['session_user_email']
		return render_template("mypage.html", job_list=job_list,mypage_user=mypage_user,off=off,mypage_on=mypage_on)


# 수정하는 페이지
@app.route('/modify/<int:id>', methods=['GET', 'POST'])
def modify(id):
	if not "session_user_email" in session:
		return redirect(url_for("signin"))

	this = Job.query.get(id)
	off1="y"
	off="y"
	if request.method == 'GET':
		return render_template("modify.html", this=this,off1=off1,off=off)
	# 수정사항 db보내기
	fix_job=Job(
		department=request.form['department'],
		nic_name=request.form['nic_name'],
		major=request.form['major'],
		major_comment=request.form['major_comment'],
		major_story=request.form['major_story'],
		major_like=request.form['major_like'],
		job=request.form['my_job'],
		job_reason=request.form['job_reason'],
		point_major=request.form['point_major'],
		point_licence=request.form['point_licence'],
		point_reading=request.form['point_reading'],
		point_double_major=request.form['point_double_major'],
		point_extra=request.form['point_extra'],
		check_double_major=request.form['check_double_major'],
		double_major=request.form['double_major'],
		user_id=session['session_user_email']
		)
	
	# 세션 쿼리
	input_user_data=User.query.get(session['session_user_email'])
	# 마스터 아이디 확인
	if input_user_data.input_jobs =="20":
		input_user_data.input_jobs ="20"
		input_user_data.user_category=request.form['user_category']
	else:
		input_user_data.input_jobs="10"
		input_user_data.user_category=request.form['user_category']
	
	db.session.add(input_user_data)
	db.session.add(fix_job)
	db.session.commit()
	
	return redirect(url_for("index"))


# db 삭제 마스터 아이디만 적용
@app.route('/delete/<name>', methods=['GET','POST'])
def delete(name):
	if request.method == 'GET':
		return render_template("delete.html")
	
	db_list = Job.query.get(name)
	# 정말로 삭제하겠는가
	if request.form['delete']=="yes":
		db.session.delete(db_list)
		db.session.commit()
		return redirect(url_for('list_view'))
		
	return redirect(url_for('list_view'))
		
	
	






# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	off="y"
	signup_on="y"
	# take form filed of JoinForm
	form = JoinForm()
	# check for request method POST
	if request.method=='GET':
		return render_template("signup.html",form=form,signup_on=signup_on,off=off)
	# check for validate
	if not form.validate_on_submit():
		return redirect(url_for("signup"))
	
	# +: check for user email does not include for class User
	inputs=form.email.data
	if User.query.get(inputs):
		alert="danger"
		return render_template("signup.html",form=form,alert=alert,signup_on=signup_on,off=off)

	# commit class User to user data
	user_db=User(
		id=form.email.data,
		password=generate_password_hash(form.password.data)
		)

	db.session.add(user_db)
	db.session.commit()

	return redirect(url_for('index'))


# 일반 로그인
@app.route('/signin', methods=['GET', 'POST'])
def signin():
	signin_on="y"
	off="y"
	# 이메일 로그인 
	if request.method=='GET':
		return render_template("signin.html",signin_on=signin_on,off=off)
	# 페이스북 로그인
	if session.get('oauth_token'):
		return redirect('index')
	
	# get input data
	user_email=request.form['user_email']
	user_password=request.form['user_password']


	# 이메일 주소가 db에 없을 때,
	if not User.query.get(user_email):
		alert="danger"
		return render_template("signin.html",signin_on=signin_on,alert=alert)
	
	# get query user_email
	user_db_session=User.query.get(user_email)
	
	#check for password of hash data for DB
	if not check_password_hash(user_db_session.password, user_password):
		alert1="danger"
		return render_template("signin.html",signin=signin,alert1=alert1)

	#input sessions and redirect 
	session['session_user_email']=user_db_session.id

	return redirect(url_for('index'))


# 로그아웃
@app.route('/logout')
def logout():
	if "session_user_email" in session:
		session.clear()
	
	else:
		flash(u"로그인 하시길 바랍니다.")
	return redirect(url_for('index'))	




# 페이스북 로그인
@app.route('/login')
def login():
	return facebook.authorize(callback=url_for('facebook_authorized',next=request.args.get('next') or request.referrer or None, _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	if resp is None:
		flash('Access denied: reason=%s error=%s' % ( request.args['error_reason'], request.args['error_description'] ))
		return redirect(url_for('index'))

	session['oauth_token']=(resp['access_token'],'')
	me=facebook.get('/me')
	session['session_user_email']=me.data['email']

	user = User.query.get( session['session_user_email'] )
	
	if user == None: # 회원가입 안되있
		user_db=User(
		id=session['session_user_email'],
		password="faceook_login"
		)

		db.session.add(user_db)
		db.session.commit()

		flash(u"페북으로 회원가입됨")

	else:
		flash(u"페북으로 로그인됨")

	return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('oauth_token')



