from flask import Flask,render_template,request,jsonify
import numpy as np
import pickle
from feature import FeatureExtraction

app = Flask(__name__)
#Load model
model = pickle.load(open('web_phishing_model.bin','rb'))


@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =model.predict(x)[0]
        print(y_pred)
        #1 is safe       
        #-1 is unsafe

        y_pro_phishing = model.predict_proba(x)[0,0]
        y_pro_non_phishing = model.predict_proba(x)[0,1]
        if y_pro_phishing>y_pro_non_phishing:
            print(y_pro_phishing,'pro')
            ans = y_pro_phishing
        else:
            print(y_pro_non_phishing,'non-pro')
            ans = y_pro_non_phishing
        # if(y_pred ==1 ):
        #     pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx =round(ans,2),url=url )
    return render_template("index.html", xx =-1)

if __name__ == "__main__":
    app.run(debug=True)