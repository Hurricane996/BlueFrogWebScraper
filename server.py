from bottle import route,run,request

@route("/",method='POST')
def index():
    for l in request.body:
       print l
    return "i"

run(host='localhost',port=8080)
