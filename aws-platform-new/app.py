from flask import Flask, render_template
import json
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Mock data - structure for easy API swap later
COURSES = [
    {
        'id': 4,
        'title': 'Learn EC2',
        'instructor': 'AWS Learning Platform',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=Learn+EC2',
        'progress': 0,
        'difficulty': 'beginner',
        'duration': '2 hours',
        'locked': False,
        'lessons': 8,
        'completed_lessons': 0,
        'url': '/learn/ec2'
    },
    {
        'id': 5,
        'title': 'Learn IAM',
        'instructor': 'AWS Learning Platform',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=Learn+IAM',
        'progress': 0,
        'difficulty': 'beginner',
        'duration': '1.5 hours',
        'locked': False,
        'lessons': 6,
        'completed_lessons': 0,
        'url': '/learn/iam'
    },
    {
        'id': 6,
        'title': 'Learn Security Groups',
        'instructor': 'AWS Learning Platform',
        'thumbnail': 'https://via.placeholder.com/400x225/232F3E/FFFFFF?text=Learn+Security+Groups',
        'progress': 0,
        'difficulty': 'beginner',
        'duration': '1 hour',
        'locked': False,
        'lessons': 5,
        'completed_lessons': 0,
        'url': '/learn/security-groups'
    }
]

LESSONS = []

QUIZ_QUESTIONS = []

@app.route('/')
def dashboard():
    stats = {
        'enrolled': 3,
        'completed': 0,
        'hours': 4.5
    }
    return render_template('dashboard.html', courses=COURSES, stats=stats)

@app.route('/course/<int:course_id>')
def course(course_id):
    # Redirect to the appropriate learning page
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    if 'url' in course:
        from flask import redirect
        return redirect(course['url'])
    return "Course not found", 404

@app.route('/lesson/<int:course_id>/<int:lesson_id>')
def lesson(course_id, lesson_id):
    # Redirect to the appropriate learning page
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    if 'url' in course:
        from flask import redirect
        return redirect(course['url'])
    return "Not found", 404

@app.route('/quiz/<int:course_id>')
def quiz(course_id):
    # Redirect to the appropriate learning page
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    if 'url' in course:
        from flask import redirect
        return redirect(course['url'])
    return "Not found", 404

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
