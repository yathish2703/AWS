import os

class Config:
    """Configuration settings for the AWS Learning Platform"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5001))
    HOST = os.environ.get('HOST', '0.0.0.0')

    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LESSONS_DIR = os.path.join(DATA_DIR, 'lessons')
    QUIZZES_DIR = os.path.join(DATA_DIR, 'quizzes')
    CHALLENGES_DIR = os.path.join(DATA_DIR, 'challenges')
    USERS_DIR = os.path.join(DATA_DIR, 'users')
    BADGES_FILE = os.path.join(DATA_DIR, 'badges.json')

    # Gamification settings
    POINTS_PER_LESSON = int(os.environ.get('POINTS_PER_LESSON', 100))
    POINTS_PER_QUIZ_QUESTION = int(os.environ.get('POINTS_PER_QUIZ_QUESTION', 10))
    POINTS_PER_CHALLENGE = int(os.environ.get('POINTS_PER_CHALLENGE', 150))
    POINTS_PER_LEVEL = int(os.environ.get('POINTS_PER_LEVEL', 500))
    STREAK_BONUS_MULTIPLIER = float(os.environ.get('STREAK_BONUS_MULTIPLIER', 0.1))
    MAX_STREAK_BONUS = float(os.environ.get('MAX_STREAK_BONUS', 1.5))

    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 86400))  # 24 hours

