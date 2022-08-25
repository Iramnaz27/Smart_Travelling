from flask import render_template

from project import app


visitors = 0

@app.route('/')
def loadIndex():
    global visitors
    visitors+=1
    print (visitors)
    return render_template('core/index.html')

@app.route('/about')
def loadAbout():
    return render_template('core/about.html')

@app.route('/services')
def loadServices():
    return render_template('core/services.html')

@app.route('/faq')
def loadFaq():
    return render_template('core/faq.html')

@app.route('/contact')
def loadContact():
    return render_template('core/contact.html')


