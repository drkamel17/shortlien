from flask import Flask, render_template, request, jsonify, redirect
import string
import random
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://yhhaebfwtogxvndhzile.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InloaGFlYmZ3dG9neHZuZGh6aWxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYwNzkxNDUsImV4cCI6MjA5MTY1NTE0NX0.uOFGVYtVQOFFjsKxOWFz73vdoP6w6eWhGbbKOXZCmU0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    short_code = generate_short_code()
    
    while True:
        existing = supabase.table('urls').select('*').eq('short_code', short_code).execute()
        if not existing.data:
            break
        short_code = generate_short_code()
    
    result = supabase.table('urls').insert({
        'original_url': original_url,
        'short_code': short_code
    }).execute()
    
    return jsonify({
        'short_url': f"{request.host_url}{short_code}",
        'short_code': short_code
    })

@app.route('/<short_code>')
def redirect_to_url(short_code):
    result = supabase.table('urls').select('original_url').eq('short_code', short_code).execute()
    
    if result.data:
        return redirect(result.data[0]['original_url'])
    return "URL not found", 404

app = app  # For Vercel

if __name__ == '__main__':
    app.run(debug=True)