import ast
with open('app.py', 'r', encoding='utf-8') as f:
    try:
        ast.parse(f.read())
        print('SUCCESS: app.py has valid Python syntax')
    except SyntaxError as e:
        print('ERROR: app.py has syntax error:', e)
        print(f'  Line {e.lineno}: {e.text}')
        print(f'  Problem: {e.msg}')
