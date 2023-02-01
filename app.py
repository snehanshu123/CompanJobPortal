from flask import Flask, request,jsonify
from flask_cors import CORS
from config import db,SECRET_KEY
from os import path,getcwd,environ
from dotenv import load_dotenv
from models.addDetailsUser import AddDetailsUser
from models.applyInternships import ApplyInternships
from models.postInternships import PostInternships
from models.user import User
from models.applicants import Applicants
from models.jobappliedbyuser import Jobappliedbyuser
from models.postedjobs import Postedjobs
from models.availablejobs import Availablejobs

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_ECHO']=False
    app.secret_key = SECRET_KEY
    
    db.init_app(app)
    print("DB Initialized successfully..")
    with app.app_context():
        @app.route("/signup",methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)
            new_user = User(
                username=data['username']
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(msg="user added successfully..")


        @app.route("/add_user_details",methods=['POST'])
        def add_user_details():
            data=request.get_json()
            username = request.args.get('username')
            user=User.query.filter_by(username=username).first()
            user_details=AddDetailsUser(
                name=data['name'],
                email_id=data['email_id'],
                resume_url=data['resume_url'],
                skills = data['skills'],
                age_group = data['age_group'],
                jobs_applied=data['jobs_applied'],
                user_id=user.id
            )
            db.session.add(user_details)
            db.session.commit()
            return jsonify(msg="user details added..")

            
        
        @app.route('/posted_jobs',methods=['POST'])
        def posted_jobs():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            data = request.get_json()
            new_posted_jobs=Postedjobs(
                job_id=data['job_id'],
                company_name=data['company_name'],
                role=data['role'],
                job_desc=data['job_desc'],
                salary=data['salary'],
                location=data['location'],
                skills_required=data['skills_required'],
                user_id=user.id
            )
            db.session.add(new_posted_jobs)
            db.session.commit()
            return jsonify(msg='jobs_posted..')
        
        @app.route('/apply_for_job',methods=['POST'])
        def apply_for_job():
            recv_username=request.args.get('username')
            user=User.query.filter_by(username=recv_username).first()
            data=request.get_json()
            new_applicant=Applicants(
                job_id=data['job_id'],
                applicant_name=data['applicant_name'],
                applicantion_id=data['application_id'],
                applicant_email=data['applicant_email'],
                applicant_resume=data['applicant_resume'],  
                user_id=user.id
            )
            db.session.add(new_applicant)
            db.session.commit()
            return jsonify(msg="applied successfully..")
        @app.route('/get_job_applied_by_user',methods=['GET'])
        def get_job_applied_by_user():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            
            job_applied_by_user=Applicants.query.filter_by(user_id=user.id)
            job_applied=[]
            for jobs in job_applied_by_user:
                job_applied.append({
                    "job_id":jobs.job_id,
                    "applicant_name":jobs.applicant_name,
                    "applicantion_id":jobs.applicantion_id,
                    "applicant_email":jobs.applicant_email,
                    "applicant_resume":jobs.applicant_resume
                })
            return jsonify(jobs_applied_by_user=job_applied)
        
        
        @app.route('/get_jobs_posted_by_user',methods=['GET'])
        def get_jobs_posted_by_user():
            recv_username=request.args.get('username')
            user=User.query.filter_by(username=recv_username).first()
            job_posted_by_user=Postedjobs.query.filter_by(user_id=user.id)
            jobs_posted=[]
            for jobs in job_posted_by_user:
                jobs_posted.append({
                    "job_id":jobs.job_id,
                    "company_name":jobs.company_name,
                    "role":jobs.role,
                    "job_desc":jobs.job_desc,
                    "salary":jobs.salary,
                    "location":jobs.location,
                    "skills_required":jobs.skills_required
                })  
            return jsonify(jobs_posted_by_user=jobs_posted) 
        @app.route('/jobs_by_company',methods=['POST'])
        def jobs_by_company():
            recv_username=request.args.get('username')
            user=User.query.filter_by(username=recv_username).first()
            data=request.get_json()
            # for jobs in data['data']:
            company_jobs=Availablejobs(
                job_id=data['job_id'],
                company_name=data['company_name'],
                role=data['role'],
                job_desc=data['job_desc'],
                salary=data['salary'],
                location=data['location'],
                skills_required=data['skills_required'],
                user_id=user.id
            )
            db.session.add(company_jobs)
            db.session.commit()
            return jsonify(msg="jobs posted..")
        @app.route('/get_companyPostedjobs_details',methods=['GET'])
        def get_companyPostedjobs_details():
            recv_username=request.args.get('username')
            user=User.query.filter_by(username=recv_username).first()
            data=Availablejobs.query.filter_by(user_id=user.id)
            jobs=[]
            for job in data:
                jobs.append({
                    "job_id":job.job_id,
                    "company_name":job.company_name,
                    "role":job.role,
                    "job_desc":job.job_desc,
                    "salary":job.salary,
                    "location":job.location,
                    "skills_required":job.skills_required
                })
            return jsonify(msg=jobs)
        @app.route('/applied_jobs_by_user',methods=['POST'])
        def applied_jobs_by_user():
            recv_username=request.args.get('username')
            user=User.query.filter_by(username=recv_username).first()
            data=request.get_json()
            # for jobs in data['data']:
            applied_jobs=Jobappliedbyuser(
                job_id=data['job_id'],
                company_name=data['company_name'],
                job_desc=data['job_desc'],
                user_id=user.id
                )
            db.session.add(applied_jobs)
            db.session.commit()
            return jsonify(msg="jobs applied successfully..")


        @app.route('/post_internships',methods=['POST'])
        def post_internships():
            data=request.get_json()
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            user_details=PostInternships(
                company_name=data['company_name'],
                intern_type=data['intern_type'],
                location=data['location'],
                resume_url=data['resume_url'],
                skills=data['skills'],
                role=data['role'],
                salary_expected=data['salary_expected'],
                user_id=user.id
            )
            db.session.add(user_details)
            db.session.commit()
            return jsonify(msg="internships posted..")

        @app.route("/apply_internships",methods=['POST'])
        def apply_internships():
            data=request.get_json()
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            user_details=ApplyInternships(
                name=data['name'],
                company=data['company'],
                resume_url=data['resume_url'],
                skills=data['skills'],
                role=data['role'],
                internduration=data['internduration'],
                user_id=user.id
            )
            db.session.add(user_details)
            db.session.commit()
            return jsonify(data='internship applied successfully..')

        

        
            
        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app
    
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
