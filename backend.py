import os
import main_test as m
from flask import Flask, request, render_template, send_from_directory
import classifier as c
import sad as s
import mine as f
import  CataractDetection as yeah


__author__ = 'siva'

app = Flask(__name__)
app.config['UPLOAD_CONFIG'] = './experiments/VesselNet/test/test_images/uploaded'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")
    


@app.route("/upload", methods=["POST" ])
def upload():
    
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, './experiments/VesselNet/test/test_images/uploaded')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".tif"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        fuck=c.prediction()
        menace=c.pred()
        
        # m.main_test()
        s.main_test()
        f.main_test()
        
        
    
    return render_template("dummy.html", fucks=fuck,nice=menace)
@app.route("/menacee", methods=["POST" ])
def menacee():
    
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, './experiments/VesselNet/test/test_images/uploaded')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for menacee in request.files.getlist("file"):
        print(menacee)
        print("{} is the file name".format(menacee.filename))
        filename = menacee.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".tif"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        menacee.save(destination)
        
        yeah.maint()
        xa=yeah.maint()
        
        
   
    return render_template("complete.html", noice=xa)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('./experiments/VesselNet/test/result/',filename)
    
@app.route('/menacee/<filename>')
def send_imag(filename):
    return send_from_directory('./experiments/VesselNet/test/sema/',filename)
    

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./experiments/VesselNet/test/result/')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

@app.route('/sema')
def get_galler():
    image_names = os.listdir('./experiments/VesselNet/test/sema/')
    print(image_names)
    return render_template("complete_display_image.html", image_names=image_names)

#ipothaan da poteann
@app.route('/results')
def get_gall():
    image_names = os.listdir(app.config['UPLOAD_CONFIG'])
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


#####################################################################################################
@app.route('/sema')
def get_sema():
    image_names = os.listdir('./experiments/VesselNet/test/sema/')
    print(image_names)
    return render_template("complete_display_image.html", image_names=image_names)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
