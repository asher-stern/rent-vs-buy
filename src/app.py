"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DON'T FORGET TO SET THE PYTHONPATH
(Both locally and in Heroku)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from flask import Flask, request
from calculations import Calculate


app = Flask(__name__)


class AppContents(object):
    def __init__(self):
        with open('html/index.html') as f:
            self.index_contents = f.read()
        with open('html/result.html') as f:
            self.result = f.read()
        with open('html/notes.html') as f:
            self.notes_contents = f.read()
        with open('html/tlb.html') as f:
            self.tlb_contents = f.read()

        self.lines = list()
        with open('html/lines.txt') as f:
            while True:
                line = f.readline().strip()
                if line is None or len(line) == 0:
                    break
                self.lines.append(line)


app_contents = AppContents()


@app.route("/")
def index():
    return app_contents.index_contents


@app.route("/result", methods=['GET', 'POST'])
def result():
    calculate = Calculate(
        float(request.values['shovi_dira']),
        float(request.values['hon_atzmi']),
        float(request.values['schar_dira']),
        float(request.values['years']),
        float(request.values['ribit_mashkanta']),
        float(request.values['tsua']),
        float(request.values['apartment_increase']),
        float(request.values['building']),
        float(request.values['depreciation']),
        float(request.values['rent_increase'])
    )
    calculate.calculate()
    result_html = app_contents.result
    result_html = result_html.replace('###1', '{:,}'.format(int(calculate.mortgage_payment)))
    result_html = result_html.replace('###2', '{:,}'.format(int(calculate.total_cost_of_apartment)))

    if calculate.first_month_buy_saving is not None:
        if calculate.first_month_buy_saving == 0:
            result_html = result_html.replace('###3', app_contents.lines[1])
            result_html = result_html.replace('###B', '')
        else:
            result_html = result_html.replace('###3', app_contents.lines[2])
            result_html = result_html.replace('###B', app_contents.lines[3] + ' ' + str(1 + calculate.first_month_buy_saving) + ' ' + app_contents.lines[4] + ' <br/>')
        result_html = result_html.replace('###4', app_contents.lines[5] + ' ' + '{:,}'.format(int(calculate.total_saving_if_buy)) + '<br/>')
    else:
        result_html = result_html.replace('###3', app_contents.lines[0])
        result_html = result_html.replace('###B', '')
        result_html = result_html.replace('###4', '')
    result_html = result_html.replace('###5', '{:,}'.format(int(calculate.total_if_buy)))
    result_html = result_html.replace('###6', '{:,}'.format(int(calculate.total_saving_if_rent)))

    result_html = result_html.replace('###8', '{:,}'.format(int(calculate.immediate_payment)))
    if calculate.first_month_rent_no_saving is None:
        result_html = result_html.replace('###9', app_contents.lines[6] + ' ' + app_contents.lines[7] + '<br/>')
    else:
        if calculate.first_month_rent_no_saving == 0:
            result_html = result_html.replace('###9', '')
        else:
            result_html = result_html.replace('###9', app_contents.lines[6] + ' ' + app_contents.lines[8] + ' ' + str(1 + calculate.first_month_rent_no_saving) + ' ' + app_contents.lines[9] + '<br/>')
    result_html = result_html.replace('###A', f'{calculate.saving_rate:.2f}%')

    if calculate.total_if_buy > calculate.total_saving_if_rent:
        result_html = result_html.replace('###7', app_contents.lines[10])
    elif calculate.total_if_buy < calculate.total_saving_if_rent:
        result_html = result_html.replace('###7', app_contents.lines[11])
    else:
        result_html = result_html.replace('###7', app_contents.lines[12])

    return result_html


@app.route("/notes")
def notes():
    return app_contents.notes_contents


@app.route("/tlb")
def tlb():
    return app_contents.tlb_contents


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # app.run()

