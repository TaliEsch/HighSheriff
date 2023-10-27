import os
import sqlite3

from flask import Flask, render_template, request, redirect, send_from_directory, session, escape, Markup, flash

#Database file
DATABASE = 'HighSheriff.db'

app = Flask(__name__)
app.secret_key = 'supahsecretkey007'

#Create upload directory
UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'avi', 'mkv', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Custom functions
#Checks for allowed files for video
def allowed_file(filename):
  """
  Taken from https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
  Accessed [30/11/2021]
  """
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Gets the directory where the video files are stored
def get_video_files():
  return os.listdir(os.getcwd() + "/instance/uploads")

#Checks the usertype (admin/customer/nothing)
def user_check(page):
  session.pop('_flashes', None)
  usertype = "null"
  if 'usertype' in session:
    usertype = escape(session['usertype'])
  if usertype == "Admin":
    return page
  else:
    message = Markup("<h1> ERROR: USER NOT AUTHORISED TO ACCESS THIS AREA </h1>")
    flash(message)
    page = 'home.html'
    return page


#Routes go here
@app.route("/")
def home():
  return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
  if request.method == "GET":
    #Get location names from location table
    locations = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT locationName, latitude, longitude FROM Locations;")
      locations = cur.fetchall()
      print(locations)
    except Exception as e:
      print('There was an error: ', e)
      locations = []
    finally:
      conn.close()
    #Get charity name from applications
    charities = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT answer1 FROM Applications WHERE status = 'Accepted';")
      charities = cur.fetchall()
      print(charities)
    except Exception as e:
      print('There was an error: ', e)
      charities = []
    finally:
      conn.close()
    #Get location from applications
    charitylocations = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT answer4 FROM Applications WHERE status = 'Accepted';")
      charitylocations = cur.fetchall()
      print(charitylocations)
    except Exception as e:
      print('There was an error: ', e)
      charitylocations = []
    finally:
      conn.close()
    #Get description from applications
    descriptions = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT answer2 FROM Applications WHERE status = 'Accepted';")
      descriptions = cur.fetchall()
      print(descriptions)
    except Exception as e:
      print('There was an error: ', e)
      descriptions = []
    finally:
      conn.close()
  return render_template('about.html', locations=locations, charities=charities, charitylocations=charitylocations, descriptions=descriptions)

@app.route('/about/funding', methods=['GET'])
def about_funding_graph():
  if request.method == "GET":
    funding_data = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
        "SELECT locationName, fundingAmount FROM Locations LEFT JOIN Funding ON Locations.locationid = Funding.locationid;"
      )
      funding_data = cur.fetchall()
      print(funding_data)
    except Exception as e:
      print('There was an error: ', e)
    finally:
      conn.close()
    return dict(funding_data)

@app.route('/donations', methods=['GET', 'POST'])
def donations():
  if request.method == "GET":
    charities = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
        "SELECT * FROM Applications WHERE status = 'Accepted';"
      )
      charities = cur.fetchall()
      print(charities)
    except Exception as e:
      print('There was an error: ', e)
    finally:
      conn.close()
    return render_template('donations.html', charities=charities)

@app.route('/applications', methods=['GET', 'POST'])
def applications():
  if request.method == "GET":
      #Get location names from location table
      locations = []
      try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT locationName FROM Locations;")
        locations = cur.fetchall()
        print(locations)
      except Exception as e:
        print('There was an error: ', e)
        locations = []
      finally:
        conn.close()
      return render_template('applications.html', locations=locations)
  elif request.method == "POST":
    firstName = request.form['firstName']
    surname = request.form['surname']
    email = request.form['email']
    question1 = request.form['question1']
    question2 = request.form['question2']
    question3 = request.form['question3']
    question4 = request.form['question4']
    question5 = request.form['question5']
    print("Info received:")
    print([firstName, surname, email, question1, question2, question3, question4, question5])

    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
        "INSERT INTO Applicants (name, surname, email) VALUES (?, ?, ?);",
        (firstName, surname, email)
      )
      cur.execute(
        "SELECT applicant_id FROM Applicants WHERE email=?;",
        [email]
      )
      app_id = cur.fetchone()[0]
      cur.execute(
        "INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5) VALUES (?, ?, ?, ?, ?, ?);",
        (app_id, question1, question2, question3, question4, question5)
      )
      conn.commit()
      result = "Submitted!"
    except Exception as e:
      print('There was an error: ', e)
      conn.rollback()
      result = "Error!"
    finally:
      conn.close()

    return result

@app.route('/applications/upload', methods=['GET', 'POST'])
def applications_upload():
  if request.method == 'POST':
    if 'uploadAppFile' not in request.files:
      return "No file provided."
    firstName = request.form['uploadFirstName']
    surname = request.form['uploadSurname']
    email = request.form['uploadEmail']
    file = request.files['uploadAppFile']
    user_id = None

    if file.filename == '':
      return "No file name was found."
    if not allowed_file(file.filename):
      return f"That file type is not allowed. We accept {', '.join(ALLOWED_EXTENSIONS)}."
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT applicant_id FROM Applicants WHERE email = ?", [email])
      user_id = cur.fetchone()
      if not user_id:
        cur.execute(
          "INSERT INTO Applicants (name, surname, email) VALUES (?, ?, ?)",
          (firstName, surname, email)
        )
        conn.commit()
        cur.execute("SELECT applicant_id FROM Applicants WHERE email = ?", [email])
        user_id = cur.fetchone()[0]
        cur.execute(
          "INSERT INTO VideoApplications (applicant_id, video_name) VALUES (?, ?)",
          (user_id, f"{firstName}{surname}-{user_id}.mp4")
        )
        conn.commit()
    except Exception as e:
      print('There was an error: ', e)
      conn.rollback()
    finally:
      conn.close()

    if firstName and surname and file and user_id:
      file.filename = f"{firstName}{surname}-{user_id}"
      file_type = file.content_type.rsplit('/', 1)[1].lower()
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{file.filename}.{file_type}"))
      print(f"{file.filename}.{file_type} saved.")
      return f"Thanks {firstName}, your video has been submitted!"
    return "There was incorrect or missing information."

@app.route('/admin', methods=['GET'])
def admin():
  #Base application table
  applications = []
  video_applications = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'open';")
    applications = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'open';")
    video_applications = cur.fetchall()
    print(applications, video_applications)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  if request.method == "GET":
    page = 'admin.html'
    page = user_check(page)
    return render_template(page, applications=applications, videos=video_applications)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template('login.html')
  elif request.method == "POST":
    try:
      username = request.form.get('username')
      password = request.form.get('password')
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT userType from Admin WHERE username = ?  AND password = ? ;", (username, password))
      try:
        userType = cur.fetchone()[0]
        if userType == 'Admin':
          session['usertype'] = 'Admin'
          return render_template('admin.html')
        else:
          msg = Markup(f"<h1> {username} successfully logged in </h1>")
          flash(msg)
          session['usertype'] = 'Customer'
          return render_template('home.html')
      except:
        message = Markup("<h1> ERROR: INCORRECT USERNAME/PASSWORD </h1>")
        flash(message)
        return render_template('login.html')
      finally:
        pass
    except Exception as e:
      print('There was an error: ', e)
      conn.close()
    finally:
      conn.close()

    msg = Markup("<h1> An error occurred in the login system, please contact a site administrator </h1>")
    flash(msg)
    return render_template('home.html')

@app.route("/display/<path:video_link>", methods=['GET'])
def get_videos(video_link):
  if request.method == "GET":
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               video_link, as_attachment=True)

@app.route('/userReg', methods=['GET', 'POST'])
def userReg():
  session.pop('_flashes', None)
  if request.method == "GET":
    return render_template('userReg.html')
  # Form handling to register users
  elif request.method == "POST":
    try:
      username = request.form.get(str('username'))
      password = request.form.get(str('password'))
      print(username, password)
      # Validation for username and password
      if username == "" or password == "":
        msg = Markup("<h1> ERROR USERNAME/PASSWORD FIELD EMPTY </h1>")
        flash(msg)
        return render_template('userReg.html')
      # Further validation
      elif " " in username or " " in password:
        msg = Markup("<h1> Username/Password includes disallowed characters </h1>")
        flash(msg)
        return render_template('userReg.html')
      # If the entered strings meet validation requirements it goes on to this:
      else:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT userType from Admin WHERE username = ? ; ", [username])
        try:
          # Result = The first result from the above query, if there are already any usernames
          # that are the same as the entered username the code below this will run. However if there aren't
          # it will cause an error which will run the exception code *
          result = cur.fetchone()[0]
          print(result)
          # Msg appears at the top of the screen below the navbar
          msg = Markup("<h1> Error username already taken </h1>")
          flash(msg)
          return render_template('userReg.html')
        # *
        except Exception as e:
          print(e)
          conn = sqlite3.connect(DATABASE)
          cur = conn.cursor()
          # This inserts the new users information and sets them as a customer
          cur.execute(
            "INSERT INTO Admin (username, password, userType) VALUES (?, ?, ?);",
            (username, password, 'Customer')
          )
          conn.commit()
          msg = Markup(f"<h1> Welcome {username} ! </h1>")
          flash(msg)
          return render_template('home.html')
    # If the main code has an error this is run
    except Exception as e:
      print('ERROR:', e)
      msg = Markup("<h1> Error detected with the login system please contact a site admin")
      flash(msg)
      return render_template('userReg.html')
    finally:
      pass

@app.route('/export/<id>', methods=['GET', 'POST'])
def export(id):
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
      "SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE application_id = ?",
      [id])
    application = cur.fetchall()
    print(application)
  except Exception as e:
    print('There was an error: ', e)
    application = []
  finally:
    conn.close()
  return render_template('exportApplication.html',
                          name=application[0][1],
                          surname=application[0][2],
                          email=application[0][3],
                          answer1=application[0][6],
                          answer2=application[0][7],
                          answer3=application[0][8],
                          answer4=application[0][9],
                          answer5=application[0][10])

@app.route('/invite/<id>', methods=['GET', 'POST'])
def invite(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE Applications SET status = 'Invited' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Invited"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/invite/video/<id>', methods=['GET', 'POST'])
def invite_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Invited' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Invited"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/accept/<id>', methods=['GET', 'POST'])
def accept(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # Change status
    cur.execute("UPDATE Applications SET status = 'Accepted' WHERE application_id = ?", [id])
    conn.commit()
    # Updating funding
    cur.execute("SELECT answer4 FROM Applications WHERE application_id = ?", [id])
    location_name = cur.fetchone()[0]
    print(location_name)
    cur.execute("SELECT locationid FROM Locations WHERE locationName = ?", [location_name])
    location_id = cur.fetchone()[0]
    print(location_id)
    cur.execute("SELECT fundingAmount FROM Funding WHERE locationid = ?", [location_id])
    amount = cur.fetchone()[0]
    new_amount = float(amount) + 5000
    cur.execute("UPDATE Funding SET fundingAmount = (?) WHERE locationid = (?)", (new_amount, location_id))
    conn.commit()
    status = "Accepted"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/accept/video/<id>', methods=['GET', 'POST'])
def accept_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Accepted' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Accepted"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/decline/<id>', methods=['GET', 'POST'])
def decline(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE Applications SET status = 'Declined' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Declined"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/decline/video/<id>', methods=['GET', 'POST'])
def decline_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Declined' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Declined"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/hold/<id>', methods=['GET', 'POST'])
def hold(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE Applications SET status = 'Holding' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Holding"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/hold/video/<id>', methods=['GET', 'POST'])
def hold_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Holding' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Holding"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/shortlist/<id>', methods=['GET', 'POST'])
def shortlist(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE Applications SET status = 'Shortlisted' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Shortlisted"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/shortlist/video/<id>', methods=['GET', 'POST'])
def shortlist_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Shortlisted' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Shortlisted"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/close/<id>', methods=['GET', 'POST'])
def close(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE Applications SET status = 'Closed' WHERE application_id = ?''', [id])
    conn.commit()
    # Updating funding
    cur.execute("SELECT answer4 FROM Applications WHERE application_id = ?", [id])
    location_name = cur.fetchone()[0]
    print(location_name)
    cur.execute("SELECT locationid FROM Locations WHERE locationName = ?", [location_name])
    location_id = cur.fetchone()[0]
    print(location_id)
    cur.execute("SELECT fundingAmount FROM Funding WHERE locationid = ?", [location_id])
    amount = cur.fetchone()[0]
    if amount >= 5000:
      new_amount = float(amount) - 5000
    else:
      new_amount = 0
    cur.execute("UPDATE Funding SET fundingAmount = (?) WHERE locationid = (?)", (new_amount, location_id))
    conn.commit()
    status = "Closed"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

@app.route('/close/video/<id>', methods=['GET', 'POST'])
def close_video(id):
  try:
    print("The id is: " + id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE VideoApplications SET status = 'Closed' WHERE application_id = ?''', [id])
    conn.commit()
    status = "Closed"
    print("The status is now: " + status)
  except Exception as e:
    print('There was an error: ', e)
    status = "error"
  finally:
    conn.close()
    print("The status has been updated to: " + status)
  return redirect("/admin")

#Routes for viewing status tables
@app.route('/invite', methods=['GET'])
def inviteview():
  #Invited application table created
  invited = []
  video_invited = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'Invited';")
    invited = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'Invited';")
    video_invited = cur.fetchall()
    print(invited)
    print(video_invited)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  return render_template('invite.html', invited=invited, videos=video_invited)

@app.route('/accept', methods=['GET'])
def acceptview():
  #Accepted application table created
  accepted = []
  video_accepted = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'Accepted';")
    accepted = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'Accepted';")
    video_accepted = cur.fetchall()
    print(accepted)
    print(video_accepted)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  page = 'accept.html'
  page = user_check(page)
  return render_template(page, accepted=accepted, videos=video_accepted)

@app.route('/decline', methods=['GET'])
def declineview():
  #Declined application table created
  declined = []
  video_declined = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'Declined';")
    declined = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'Declined';")
    video_declined = cur.fetchall()
    print(declined)
    print(video_declined)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  page = 'decline.html'
  page = user_check(page)
  return render_template(page, declined=declined, videos=video_declined)


@app.route('/hold', methods=['GET'])
def heldview():
  #Declined application table created
  holded = []
  video_holded = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'Holding';")
    holded = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'Holding';")
    video_holded = cur.fetchall()
    print(holded)
    print(video_holded)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  page = 'hold.html'
  page = user_check(page)
  return render_template(page, holded=holded, videos=video_holded)


@app.route('/shortlist', methods=['GET'])
def shortview():
  #Declined application table created
  shortlisted = []
  video_shortlisted = []
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Applicants LEFT JOIN Applications ON Applicants.applicant_id = Applications.applicant_id WHERE status = 'Shortlisted';")
    shortlisted = cur.fetchall()
    cur.execute("SELECT * FROM Applicants LEFT JOIN VideoApplications ON Applicants.applicant_id = VideoApplications.applicant_id WHERE status = 'Shortlisted';")
    video_shortlisted = cur.fetchall()
    print(shortlisted)
    print(video_shortlisted)
  except Exception as e:
    print('There was an error: ', e)
  finally:
    conn.close()

  page = 'shortlist.html'
  page = user_check(page)
  return render_template(page, shortlisted=shortlisted, videos=video_shortlisted)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  #GET/POST requests for creating and storing submissons
  if request.method == "GET":
    return render_template('contactus.html')
  elif request.method == "POST":
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    print("Info recevied: " + str([name, email, message]))

  #Database integration
  try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
      "INSERT INTO Contact (name, email, message) VALUES (?, ?, ?);",
      (name, email, message)
    )
    conn.commit()
    result = "Submitted!"
  except Exception as e:
    print('There was an error: ', e)
    conn.rollback()
    result = "Error!"
  finally:
    print(str(result))
    conn.close()

  return result


@app.route('/contactadmin', methods=['GET', 'POST'])
def contactadmin():
  if request.method == "GET":
    #Contact table created
    contacted = []
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT * FROM Contact;")
      contacted = cur.fetchall()
      print(contacted)
    except Exception as e:
      print('There was an error: ', e)
      conn.close()
    finally:
      conn.close()

    page = 'contactadmin.html'
    page = user_check(page)
    return render_template(page, contacted=contacted)

@app.route('/addadmin', methods=['GET', 'POST'])
def addadmin():
  #GET/POST requests for creating and storing submissons
  if request.method == "GET":
    return render_template('addAdmin.html')
  elif request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    print("Info recevied: " + str([username, password]))

    #Database integration
    try:
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
        "INSERT INTO Admin (username, password) VALUES (?, ?);",
        (username, password)
      )
      conn.commit()
      result = "Submitted!"
    except Exception as e:
      print('There was an error: ', e)
      conn.rollback()
      result = "Error!"
    finally:
      print(str(result))
      conn.close()

    return render_template("admin.html")

if __name__ == "__main__":
  app.run(debug=True)
