import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 파일 경로 설정
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'guestbook.db')

app = Flask(__name__, 
            static_folder=os.path.join(base_dir, 'static'), 
            template_folder=os.path.join(base_dir, 'templates'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 데이터베이스 모델 (거주지 추가)
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=True)  # 거주지 칸
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.date_posted.desc()).all()
    return render_template('index.html', 
                           entries=entries, 
                           title="충청남도의원 예비후보 전성일",
                           subtitle="우리 동네 불편한 점을 적어주세요")

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form.get('name')
    location = request.form.get('location')
    content = request.form.get('content')
    
    if name and content:
        new_entry = Entry(name=name, location=location, content=content)
        db.session.add(new_entry)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

