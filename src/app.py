from flask import Flask, request
import sys
from calculations import Calculate


app = Flask(__name__)


class AppContents(object):
    def __init__(self):
        with open('html/index.html') as f:
            self.index_contents = f.read()
        with open('html/result.html') as f:
            self.result = f.read()
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


@app.route("/result")
def result():
    calculate = Calculate(
        float(request.values['shovi_dira']),
        float(request.values['hon_atzmi']),
        float(request.values['schar_dira']),
        float(request.values['years']),
        float(request.values['ribit_mashkanta']),
        float(request.values['tsua'])
    )
    calculate.calculate()
    result_html = app_contents.result
    result_html = result_html.replace('###1', '{:,}'.format(int(calculate.mortgage_payment)))
    result_html = result_html.replace('###2', '{:,}'.format(int(calculate.total_cost_of_apartment)))
    if calculate.rent_smaller_than_mortgage:
        result_html = result_html.replace('###3', app_contents.lines[0])
        result_html = result_html.replace('###4', '')
    else:
        result_html = result_html.replace('###3', app_contents.lines[1])
        result_html = result_html.replace('###4', app_contents.lines[2] + '\n' + '{:,}'.format(int(calculate.total_saving_if_buy)))
    result_html = result_html.replace('###5', '{:,}'.format(int(calculate.total_if_buy)))
    result_html = result_html.replace('###6', '{:,}'.format(int(calculate.total_saving_if_rent)))
    if calculate.total_if_buy > calculate.total_saving_if_rent:
        result_html = result_html.replace('###7', app_contents.lines[3])
    elif calculate.total_if_buy < calculate.total_saving_if_rent:
        result_html = result_html.replace('###7', app_contents.lines[4])
    else:
        result_html = result_html.replace('###7', app_contents.lines[5])

    return result_html


if __name__ == "__main__":
    app.run()

