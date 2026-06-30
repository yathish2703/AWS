from flask import Flask, render_template
import json
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Mock data - structure for easy API swap later
COURSES = [
    {
        'id': 1,
        'title': 'AWS fundamentals',
        'instructor': 'Adrian Cantrill',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=AWS+Fundamentals',
        'progress': 45,
        'difficulty': 'beginner',
        'duration': '8 hours',
        'locked': False,
        'lessons': 12,
        'completed_lessons': 5
    },
    {
        'id': 2,
        'title': 'EC2 deep dive',
        'instructor': 'Stephane Maarek',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=EC2+Deep+Dive',
        'progress': 0,
        'difficulty': 'intermediate',
        'duration': '12 hours',
        'locked': False,
        'lessons': 20,
        'completed_lessons': 0
    },
    {
        'id': 3,
        'title': 'Solutions architect pro',
        'instructor': 'Adrian Cantrill',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=Solutions+Architect',
        'progress': 0,
        'difficulty': 'advanced',
        'duration': '40 hours',
        'locked': True,
        'lessons': 50,
        'completed_lessons': 0
    }
]

LESSONS = [
    {'id': 1, 'title': 'Introduction to AWS', 'duration': '8:45', 'completed': True},
    {'id': 2, 'title': 'AWS global infrastructure', 'duration': '12:30', 'completed': True},
    {'id': 3, 'title': 'IAM fundamentals', 'duration': '15:20', 'completed': True},
    {'id': 4, 'title': 'EC2 basics', 'duration': '18:15', 'completed': True},
    {'id': 5, 'title': 'Security groups', 'duration': '10:45', 'completed': True},
    {'id': 6, 'title': 'EBS volumes', 'duration': '14:30', 'completed': False},
    {'id': 7, 'title': 'EBS snapshots', 'duration': '9:20', 'completed': False},
    {'id': 8, 'title': 'AMI overview', 'duration': '11:50', 'completed': False},
]

QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': 'Which service provides virtual servers in AWS?',
        'options': ['Lambda', 'EC2', 'S3', 'RDS'],
        'correct': 1
    },
    {
        'id': 2,
        'question': 'What does IAM stand for?',
        'options': ['Internet Access Management', 'Identity and Access Management', 'Internal Authentication Module', 'Integrated Application Manager'],
        'correct': 1
    },
    {
        'id': 3,
        'question': 'Which pricing model offers up to 90% discount?',
        'options': ['On-Demand', 'Reserved Instances', 'Spot Instances', 'Dedicated Hosts'],
        'correct': 2
    }
]

@app.route('/')
def dashboard():
    stats = {
        'enrolled': 12,
        'completed': 5,
        'hours': 47
    }
    return render_template('dashboard.html', courses=COURSES, stats=stats)

@app.route('/course/<int:course_id>')
def course(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    return render_template('course.html', course=course, lessons=LESSONS)

@app.route('/lesson/<int:course_id>/<int:lesson_id>')
def lesson(course_id, lesson_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    lesson = next((l for l in LESSONS if l['id'] == lesson_id), None)
    if not course or not lesson:
        return "Not found", 404
    return render_template('lesson.html', course=course, lesson=lesson, lessons=LESSONS)

@app.route('/quiz/<int:course_id>')
def quiz(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    return render_template('quiz.html', course=course, questions=QUIZ_QUESTIONS)

@app.route('/how-cloud-works')
def how_cloud_works():
    return render_template('how-cloud-works.html')

@app.route('/category/<category_name>')
def category(category_name):
    # Filter courses by category (for demo, just show all for now)
    category_titles = {
        'compute': 'Compute Services',
        'storage': 'Storage & Databases',
        'security': 'Security & Identity',
        'networking': 'Networking'
    }
    title = category_titles.get(category_name, 'AWS Courses')
    return render_template('category.html', courses=COURSES, category_title=title, category_name=category_name)

@app.route('/learn/ec2')
def learn_ec2():
    return render_template('learn-ec2.html')

@app.route('/learn/iam')
def learn_iam():
    return render_template('learn-iam.html')

@app.route('/learn/security-groups')
def learn_security_groups():
    return render_template('learn-security-groups.html')

if __name__ == '__main__':
    # Get port from command line argument or use default 8080
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"Starting Flask app on port {port}...")
    print(f"Access at: http://localhost:{port}")
    app.run(debug=True, port=port, host='0.0.0.0')
