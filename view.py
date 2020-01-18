from flask import Flask, render_template, request
import testing
app = Flask(__name__)

@app.route('/')
def student():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        #print(result)
        resi = str(result)
        input = resi[33:-4]
        #resi = result
        output = testing.test1('250/250.sav', resi)
        #print(output)
        #result = test1.test1('250/250.sav', result)
        return render_template("result.html", result_out = output, result_in = input )

if __name__ == '__main__':
    app.run(debug = True)



"""
In testing module, after classNameMap loading and before returning do this,
pred_prob = model.predict_proba(featureVector)
proba_list = []
for i in range(0, len(classNameMap)):
	proba_list.append(str(pred_prob[0][i]) + " " + str(classNameMap[i]))
for i in proba_list:
	print(i)
"""