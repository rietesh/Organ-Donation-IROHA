from flask import Flask, render_template, request
import iroha_sdk

app = Flask(__name__)

global data2
data2 = []
@app.route("/")
def page0():
    return render_template('index.html')

@app.route("/donors.html", methods=["GET", "POST"])

def page1():
    global data2
    if request.method == "POST":
        data = request.form.to_dict()
        iroha_sdk.create_account_donor(data['name'],data['organ'])
        hash = iroha_sdk.transfer_coin_from_src_to_dest(data['name'],data['pat_name'],data['organ'])
        return render_template('results.html',data=hash)
    if len(data2) < 5:
        return render_template('donors.html',data1=data2)
    data2 = []
    data2.append('Register')
    return render_template('donors.html', data1=data2)

@app.route("/query.html", methods=["GET", "POST"])
def page3():
    if request.method == "POST":
        data = request.form.to_dict()
        if data['opti'] == 'patient':
            return render_template('query.html')

        ans = iroha_sdk.get_account_assets(data['name'])
        return render_template('results.html',data=ans)
    return render_template('query.html')

@app.route("/patient.html", methods=["GET", "POST"])
def page2():
    if request.method == "POST":
        data = request.form.to_dict()
        global data2
        data2.append(data)
        iroha_sdk.create_asset(data['organ'])
        iroha_sdk.add_coin_to_admin(data['organ'])
        hash = iroha_sdk.create_account_donor(data['name'],data['organ'])
        return render_template('results.html',data=hash)
    return render_template('patient.html')

@app.route("/contact.html")
def page4():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
