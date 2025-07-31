import os
from flask import Flask,render_template,abort,send_file
import datetime as dt
from werkzeug.utils import safe_join

app=Flask(__name__)

baseFolderPath = r'C:\Books'

def getTimeStrampString(tSec:float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj,"%Y-%m-%d %H:%M:%S")
    return tStr

def getReadableByteSize(num,suffix='B') -> str:
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num,unit,suffix)
        num /=1024.0
    return "%.1f%s%s" % (num,'Y',suffix)
@app.route("/Books/")
def home():
    return "Hello World!!!"

@app.route('/',defaults={'reqPath':''})
@app.route("/<path:reqPath>")
def index(reqPath):
    absPath = safe_join(baseFolderPath,reqPath)
    if not os.path.exists(absPath):
        return abort(404)
    if os.path.isfile(absPath):
        return send_file(absPath)
    def fObjFromScan(x):
        fIcon = 'bi bi-dolder-fill' if os.path.isdir(x.path) else 'bi bi-file-earmark'
        fileStat = x.stat()
        fBytes = getReadableByteSize(fileStat.st_size)
        fTime = getTimeStrampString(fileStat.st_mtime)
        return {'name': x.name ,
                'size': fBytes,
                'mTime': fTime,
                'fIcon': fIcon,
                'fLink' :  os.path.relpath(x.path,baseFolderPath)
                }
    fName=[fObjFromScan(x) for x in os.scandir(baseFolderPath)]
    return render_template('index.html.j2',files=fName)

#run the server
app.run(host="0.0.0.0",port=10100)