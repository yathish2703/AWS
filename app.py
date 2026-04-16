from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from config import Config
import json
import os
from datetime import datetime, timedelta
import uuid
import markdown2

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Utility Functions
def load_json_file(filepath):
    """Load JSON file and return data"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def render_markdown(text):
    """Convert markdown to HTML"""
    if not text:
        return ""
    # Convert markdown with extras for better formatting
    html = markdown2.markdown(text, extras=[
        "fenced-code-blocks",
        "tables",
        "break-on-newline",
        "code-friendly"
    ])
    return html

def save_json_file(filepath, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_id():
    """Get or create user ID from session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def load_user_progress(user_id):
    """Load user progress data"""
    filepath = os.path.join(app.config['USERS_DIR'], f'user-{user_id}.json')
    data = load_json_file(filepath)

    if not data:
        # Create new user
        data = {
            'userId': user_id,
            'name': 'Guest User',
            'createdAt': datetime.now().isoformat(),
            'lastActive': datetime.now().isoformat(),
            'level': 1,
            'totalPoints': 0,
            'streak': 0,
            'lastLoginDate': datetime.now().date().isoformat(),
            'completedLessons': [],
            'lessonsProgress': {},
            'quizResults': {},
            'badges': [],
            'challenges': {}
        }
        save_user_progress(user_id, data)

    return data

def save_user_progress(user_id, data):
    """Save user progress data"""
    data['lastActive'] = datetime.now().isoformat()
    filepath = os.path.join(app.config['USERS_DIR'], f'user-{user_id}.json')
    save_json_file(filepath, data)

def calculate_level(points):
    """Calculate level from total points"""
    return (points // app.config['POINTS_PER_LEVEL']) + 1

def update_streak(user_data):
    """Update user's daily streak"""
    today = datetime.now().date().isoformat()
    last_login = user_data.get('lastLoginDate', today)

    if last_login == today:
        return user_data['streak']

    yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()

    if last_login == yesterday:
        user_data['streak'] += 1
    else:
        user_data['streak'] = 1

    user_data['lastLoginDate'] = today
    return user_data['streak']

def check_badge_criteria(user_id):
    """Check if user earned new badges"""
    user_data = load_user_progress(user_id)
    badges_data = load_json_file(app.config['BADGES_FILE'])

    if not badges_data:
        return []

    earned_badges = []
    earned_badge_ids = [b['badgeId'] for b in user_data.get('badges', [])]

    for badge in badges_data.get('badges', []):
        if badge['id'] in earned_badge_ids:
            continue

        criteria = badge.get('criteria', {})
        earned = False

        # Check different badge criteria
        if 'streak' in criteria:
            if user_data.get('streak', 0) >= criteria['streak']:
                earned = True

        if 'service' in criteria:
            service = criteria['service']
            min_score = criteria.get('minScore', 0)

            lesson_progress = user_data.get('lessonsProgress', {}).get(service, {})
            quiz_result = user_data.get('quizResults', {}).get(f'{service}-quiz', {})

            if (lesson_progress.get('completed', False) and
                quiz_result.get('score', 0) >= min_score):
                earned = True

        if earned:
            earned_badges.append({
                'badgeId': badge['id'],
                'unlockedAt': datetime.now().isoformat()
            })

    return earned_badges

# Core Page Routes
@app.route('/')
def index():
    """Landing page / Dashboard"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)
    update_streak(user_data)
    save_user_progress(user_id, user_data)

    return render_template('index.html', user=user_data)

# Teacher Routes
@app.route('/teacher')
def teacher_dashboard():
    """Teacher Dashboard - Overview of all lessons"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    lessons_dir = app.config['LESSONS_DIR']
    all_lessons = []

    # Load cloud basics
    cloud_basics_dir = os.path.join(lessons_dir, '00-cloud-basics')
    if os.path.exists(cloud_basics_dir):
        for filename in sorted(os.listdir(cloud_basics_dir)):
            if filename.endswith('.json'):
                lesson_data = load_json_file(os.path.join(cloud_basics_dir, filename))
                if lesson_data:
                    lesson_data['filepath'] = f'00-cloud-basics/{filename}'
                    all_lessons.append(lesson_data)

    # Load AWS service lessons
    for filename in sorted(os.listdir(lessons_dir)):
        if filename.endswith('.json'):
            lesson_data = load_json_file(os.path.join(lessons_dir, filename))
            if lesson_data:
                lesson_data['filepath'] = filename
                all_lessons.append(lesson_data)

    return render_template('teacher_dashboard.html', lessons=all_lessons, user=user_data)

@app.route('/teacher/create', methods=['GET', 'POST'])
def teacher_create_lesson():
    """Create a new lesson"""
    if request.method == 'POST':
        data = request.json

        # Determine file path
        service_id = data.get('serviceId')
        is_cloud_basic = data.get('isCloudBasic', False)

        if is_cloud_basic:
            filepath = os.path.join(app.config['LESSONS_DIR'], '00-cloud-basics', f'{service_id}.json')
        else:
            filepath = os.path.join(app.config['LESSONS_DIR'], f'{service_id}.json')

        # Save lesson
        save_json_file(filepath, data)

        return jsonify({'success': True, 'message': 'Lesson created successfully!'})

    user_id = get_user_id()
    user_data = load_user_progress(user_id)
    return render_template('teacher_create.html', user=user_data)

@app.route('/teacher/edit/<path:filepath>')
def teacher_edit_lesson(filepath):
    """Edit existing lesson"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    # Load lesson
    full_path = os.path.join(app.config['LESSONS_DIR'], filepath)
    lesson_data = load_json_file(full_path)

    if not lesson_data:
        return "Lesson not found", 404

    return render_template('teacher_edit.html', lesson=lesson_data, filepath=filepath, user=user_data)

@app.route('/teacher/update/<path:filepath>', methods=['POST'])
def teacher_update_lesson(filepath):
    """Update existing lesson"""
    data = request.json
    full_path = os.path.join(app.config['LESSONS_DIR'], filepath)

    save_json_file(full_path, data)

    return jsonify({'success': True, 'message': 'Lesson updated successfully!'})

@app.route('/teacher/delete/<path:filepath>', methods=['POST'])
def teacher_delete_lesson(filepath):
    """Delete a lesson"""
    full_path = os.path.join(app.config['LESSONS_DIR'], filepath)

    try:
        os.remove(full_path)
        return jsonify({'success': True, 'message': 'Lesson deleted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/teacher/preview', methods=['POST'])
def teacher_preview():
    """Preview lesson markdown rendering"""
    data = request.json
    content = data.get('content', '')
    html = render_markdown(content)
    return jsonify({'html': html})

@app.route('/lesson/<service>')
def lesson(service):
    """Lesson viewer"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    return render_template('lesson.html', service=service, user=user_data)

@app.route('/quiz/<service>')
def quiz(service):
    """Quiz page"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    return render_template('quiz.html', service=service, user=user_data)

@app.route('/challenge/<service>/<challenge_id>')
def challenge(service, challenge_id):
    """Challenge page"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    return render_template('challenge.html', service=service, challenge_id=challenge_id, user=user_data)

@app.route('/profile')
def profile():
    """User profile"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    return render_template('profile.html', user=user_data)

@app.route('/leaderboard')
def leaderboard():
    """Leaderboard page"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    return render_template('leaderboard.html', user=user_data)

# API Endpoints
@app.route('/api/lessons')
def api_lessons():
    """Get all lessons"""
    lessons = []
    cloud_basics_dir = os.path.join(app.config['LESSONS_DIR'], '00-cloud-basics')

    # Load cloud basics lessons
    if os.path.exists(cloud_basics_dir):
        for filename in sorted(os.listdir(cloud_basics_dir)):
            if filename.endswith('.json'):
                filepath = os.path.join(cloud_basics_dir, filename)
                lesson_data = load_json_file(filepath)
                if lesson_data:
                    lessons.append(lesson_data)

    # Load AWS service lessons
    for filename in sorted(os.listdir(app.config['LESSONS_DIR'])):
        if filename.endswith('.json'):
            filepath = os.path.join(app.config['LESSONS_DIR'], filename)
            lesson_data = load_json_file(filepath)
            if lesson_data:
                lessons.append(lesson_data)

    return jsonify(lessons)

@app.route('/api/lesson/<service>')
def api_lesson(service):
    """Get specific lesson content"""
    # Check cloud basics first
    cloud_basics_path = os.path.join(app.config['LESSONS_DIR'], '00-cloud-basics', f'{service}.json')
    if os.path.exists(cloud_basics_path):
        lesson_data = load_json_file(cloud_basics_path)
        if lesson_data:
            return jsonify(lesson_data)

    # Check regular AWS service lessons
    filepath = os.path.join(app.config['LESSONS_DIR'], f'{service}.json')
    lesson_data = load_json_file(filepath)

    if lesson_data:
        return jsonify(lesson_data)
    return jsonify({'error': 'Lesson not found'}), 404

@app.route('/api/quiz/<service>')
def api_quiz(service):
    """Get quiz questions"""
    filepath = os.path.join(app.config['QUIZZES_DIR'], f'{service}-quiz.json')
    quiz_data = load_json_file(filepath)

    if quiz_data:
        # Remove correct answers from questions
        safe_quiz = quiz_data.copy()
        safe_quiz['questions'] = [
            {k: v for k, v in q.items() if k != 'correctAnswer'}
            for q in quiz_data.get('questions', [])
        ]
        return jsonify(safe_quiz)
    return jsonify({'error': 'Quiz not found'}), 404

@app.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    """Submit quiz answers and return score"""
    data = request.json
    service = data.get('service')
    answers = data.get('answers', {})

    filepath = os.path.join(app.config['QUIZZES_DIR'], f'{service}-quiz.json')
    quiz_data = load_json_file(filepath)

    if not quiz_data:
        return jsonify({'error': 'Quiz not found'}), 404

    # Calculate score
    correct = 0
    total = len(quiz_data['questions'])
    results = []
    total_points = 0

    for question in quiz_data['questions']:
        q_id = question['id']
        user_answer = answers.get(q_id)
        correct_answer = question['correctAnswer']
        is_correct = user_answer == correct_answer

        if is_correct:
            correct += 1
            total_points += question.get('points', app.config['POINTS_PER_QUIZ_QUESTION'])

        results.append({
            'questionId': q_id,
            'correct': is_correct,
            'correctAnswer': correct_answer,
            'userAnswer': user_answer,
            'explanation': question.get('explanation', '')
        })

    score = round((correct / total) * 100)

    # Update user progress
    user_id = get_user_id()
    user_data = load_user_progress(user_id)

    quiz_id = f'{service}-quiz'
    user_data['quizResults'][quiz_id] = {
        'score': score,
        'attempts': user_data.get('quizResults', {}).get(quiz_id, {}).get('attempts', 0) + 1,
        'completedAt': datetime.now().isoformat()
    }

    # Award points only if first attempt or better score
    if user_data['quizResults'][quiz_id]['attempts'] == 1:
        user_data['totalPoints'] += total_points
        user_data['level'] = calculate_level(user_data['totalPoints'])

    save_user_progress(user_id, user_data)

    # Check for new badges
    new_badges = check_badge_criteria(user_id)
    if new_badges:
        user_data['badges'].extend(new_badges)
        save_user_progress(user_id, user_data)

    return jsonify({
        'score': score,
        'correct': correct,
        'total': total,
        'points': total_points,
        'results': results,
        'newBadges': new_badges,
        'level': user_data['level']
    })

@app.route('/api/user/progress')
def api_user_progress():
    """Get user progress data"""
    user_id = get_user_id()
    user_data = load_user_progress(user_id)
    return jsonify(user_data)

@app.route('/api/user/progress', methods=['POST'])
def api_update_progress():
    """Update user progress"""
    user_id = get_user_id()
    data = request.json

    user_data = load_user_progress(user_id)

    # Update lesson progress
    if 'lessonId' in data:
        lesson_id = data['lessonId']
        user_data['lessonsProgress'][lesson_id] = {
            'completed': data.get('completed', False),
            'score': data.get('score', 0),
            'completedAt': datetime.now().isoformat(),
            'timeSpent': data.get('timeSpent', 0)
        }

        if data.get('completed') and lesson_id not in user_data['completedLessons']:
            user_data['completedLessons'].append(lesson_id)
            user_data['totalPoints'] += app.config['POINTS_PER_LESSON']
            user_data['level'] = calculate_level(user_data['totalPoints'])

    save_user_progress(user_id, user_data)

    # Check for new badges
    new_badges = check_badge_criteria(user_id)
    if new_badges:
        user_data['badges'].extend(new_badges)
        save_user_progress(user_id, user_data)

    return jsonify({
        'success': True,
        'newBadges': new_badges,
        'level': user_data['level'],
        'totalPoints': user_data['totalPoints']
    })

@app.route('/api/leaderboard')
def api_leaderboard():
    """Get leaderboard data"""
    users = []
    users_dir = app.config['USERS_DIR']

    if os.path.exists(users_dir):
        for filename in os.listdir(users_dir):
            if filename.startswith('user-') and filename.endswith('.json'):
                filepath = os.path.join(users_dir, filename)
                user_data = load_json_file(filepath)
                if user_data:
                    users.append({
                        'userId': user_data['userId'],
                        'name': user_data.get('name', 'Anonymous'),
                        'level': user_data.get('level', 1),
                        'totalPoints': user_data.get('totalPoints', 0),
                        'badges': len(user_data.get('badges', []))
                    })

    # Sort by points
    users.sort(key=lambda x: x['totalPoints'], reverse=True)

    # Add rank
    for i, user in enumerate(users):
        user['rank'] = i + 1

    return jsonify(users[:20])  # Top 20

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['LESSONS_DIR'], exist_ok=True)
    os.makedirs(os.path.join(app.config['LESSONS_DIR'], '00-cloud-basics'), exist_ok=True)
    os.makedirs(app.config['QUIZZES_DIR'], exist_ok=True)
    os.makedirs(app.config['CHALLENGES_DIR'], exist_ok=True)
    os.makedirs(app.config['USERS_DIR'], exist_ok=True)

    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
