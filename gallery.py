from flask import Flask, send_from_directory, abort
import os, glob
import urllib.parse

app = Flask(__name__)

# @app.route("/")
# def index():
    # images = glob.glob("*.jpg")
    # html = ""
    # for i in images:
        # html += "<img style='max-width:1500px' src='{}'>".format(i)
    # return html

@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def gallery(path):
    # decode url first
    path = urllib.parse.unquote(path)
    #print(path)
    
    # if path indicate image 
    ext = path.split('.')[-1]
    exts = ["jpg", "jpeg", "png", "webp"]
    if(ext.lower() in exts):
        return send_from_directory('.', path)
    # if path indicate directory
    '''else:
        path_array = path.split("/")
        if len(path_array) > 1:
            if path_array[-1]:
                filename = path_array[-1]
            else:
                filename = path_array[-2] #route("/path/")
                del path_array[-1]
        else:
            filename = path_array[0] #route("/")
            
    ext = filename.split(".")
    if len(ext) > 1:
        abort(404)'''
        
    # get all path
    #dirs = filter(os.path.isdir, glob.glob(os.path.join(path, "*")))
    #images = filter(lambda filenames: filenames.split(".")[-1] in exts, glob.glob(os.path.join(path, "*")))
    dirs = next(os.walk(os.path.join(".", path)))[1]
    images = filter(lambda filenames: filenames.split(".")[-1].lower() in exts, next(os.walk(os.path.join(".", path)))[2])
    
    html = '\
    <!DOCTYPE html>\
    <html>\
    <head>\
      <meta charset="UTF-8">\
      <meta name="viewport" content="width=device-width, initial-scale=1">\
      <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\
    </head>\
    <body class="w3-dark-grey">\
      <div class="w3-row">\
        <!-- Left Column -->\
        <div class="w3-col m2">\
          <div class="w3-container w3-dark-grey">\
            <h3>Directories</h3>\
          </div>\
          <div class="w3-container">\
            <ul class="w3-ul w3-dark-grey">'

    # redirect to parent dir
    path_array = path.split("/")
    del path_array[-1]
    html += "<li><a href=\"/{}\">..</a></li>".format("/".join(path_array))

    for d in dirs:
        dirPath = "/{}/{}".format(path, d) if path else "/{}".format(d)
        html += "<li><a href=\"{}\">{}</a></li>\n".format(dirPath, d)
        
    html += '\
            </ul>\
            </div>\
          </div>\
          \
          <!-- Right Column -->\
          <div class="w3-col m10">'
    for i in images:
        imgPath = "/{}/{}".format(path, i) if path else "/{}".format(i)
        html += "<img class=\"w3-image\" src='{}'>".format(imgPath)
        
    html += '\
          </div>\
        </div>\
      </body>\
      </html>'
    return html

if __name__ == '__main__':
    app.run(debug=True)
