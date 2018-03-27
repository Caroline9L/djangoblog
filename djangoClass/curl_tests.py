"""
Bash only -- doesn't work in powershell


curl -X POST -d "username=Fake&password=123admin" http://127.0.0.1:8000/api/auth/token/

token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6IkZha2UiLCJleHAiOjE1MjIxNTExMTgsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.IED3iZzidzlv6fTF9IwU8moLD9P7OOVHMCJ-ZF9hKE4"

curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6IkZha2UiLCJleHAiOjE1MjIxNTExMTgsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.IED3iZzidzlv6fTF9IwU8moLD9P7OOVHMCJ-ZF9hKE4" http://127.0.0.1:8000/api/comments/

curl -X POST -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6IkZha2UiLCJleHAiOjE1MjIxNTIxMjcsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.EvjWjGxQGtp9o8qDZs4rxaC5mWARYEVjW81bMd3DHiU" -H "Content-Type: application/json" -d '{"content":"A brand new reply right here"}' 'http://127.0.0.1:8000/api/comments/create/?slug=a-post-2&type=post&parent_id=10'

curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/



curl -X POST -d "username=Fake1&password=123admin" http://127.0.0.1:8000/api/auth/token/

curl -X POST -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6IkZha2UxIiwiZXhwIjoxNTIyMTUyNDc1LCJlbWFpbCI6InRlc3QxQHRlc3QuY29tIn0.5lvrjhZSCGl_hMsq1ft6Sbrr3yc8ETsAXr3f6b6e80w" -H "Content-Type: application/json" -d '{"content":"Yet another reply"}' 'http://127.0.0.1:8000/api/comments/create/?slug=a-post-2&type=post&parent_id=10'



http://getblimp.github.io/django-rest-framework-jwt/
"""