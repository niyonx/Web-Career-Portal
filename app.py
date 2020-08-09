#!/usr/bin/env python
from flask import Flask, url_for, render_template, request, redirect, flash, session
from datetime import date
import dbfunctions
import jinja2.exceptions
import secrets
import os

app = Flask(__name__)

import auth
os.environ['PORT'] = '5000'


@app.route('/index')
def index():
    if session['role'] == "Seeker":
        print("Job seeker signed in")
        userID = session["ID"]

        header1 = "Active job postings"
        numHeader1 = dbfunctions.countActiveJobs()

        header2 = "Monthly fee"
        numHeader2 = dbfunctions.getMonthlyCharge(userID)


        return render_template('index.html', header1 = header1,numHeader1=numHeader1,header2=header2,numHeader2 = numHeader2,header3=header3,numHeader3=numHeader3,percentageHeader3=percentageHeader3 )
    elif session['role'] == "Employer":
        print("Employer signed in")
    elif session['role'] == "Admin":
        print("Admin signed in")
    else:
        print("Error: Cannot identify role")
    return render_template('index.html')

@app.route('/viewUsers')
def viewUsers():
    field_names, results = dbfunctions.getUsers()
    return render_template('viewUsers.html', users = results, usersHeaders = field_names)
    
@app.route('/viewJobs')
def viewJobs():
    field_names, results = dbfunctions.getJobs()
    return render_template('viewJobs.html', jobs = results, jobsHeaders = field_names)

@app.route('/postJobs', methods=['POST'])
def postJob():
    if(request.form is not None):
        job_title = request.form['jobTitle']
        dbfunctions.postJob(job_title)
        return render_template('postJobs.html',message="Success, job has been created!")
    return render_template('postJobs.html')

@app.route('/applyJob', methods=['POST'])
def applyJob():
    if(request.form is not None):
        jobSeekerID = request.form['jobSeekerID']
        jobID = request.form['jobID']
        appliedDate = date.today().strftime("%Y-%m-%d")
        coverLetter = 'coverletter path'
        resume = 'resume path'
    dbfunctions.applyJob(jobSeekerID, jobID, appliedDate, coverLetter, resume)
    flash('Job applied successfully!')
    return redirect(url_for('viewJobs'))

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/<pagename>')
def admin(pagename):
    return render_template(pagename+'.html')

if __name__ == '__main__':
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    port = int(os.environ['PORT'])
    app.run(debug=True, host='0.0.0.0', port = port)