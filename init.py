import matplotlib
matplotlib.use('agg')
import numpy as np
import matplotlib.pyplot as plt
from flask import request
from flask import Flask, render_template
import os
import random

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/get_plot', methods = ['POST' ])
def get_plot():
    if request.method == 'POST':
        plt.clf()
        a = int(request.form['nilai_a'])
        b = int(request.form['nilai_b'])

        x = np.arange(-10, 10, 0.01)
        y = a*x + b

        x1 = -b/a
        y1 = b

        plt.plot(x,y, "r")
        plt.plot(x1, 0, "k*", label=f"Titik Potong Sumbu x ")
        plt.plot(0, y1, "c*", label=f"Titik Potong Sumbu y ")

        plt.xlim(-10, 10)
        plt.ylim(-20, 20)

        plt.title(f"$y = {a}x + {b}$")
        plt.xlabel("sumbu x")
        plt.ylabel("sumbu y")
        plt.grid()

        ax = plt.gca()
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')        
        plt.legend()
        plt.savefig(f'static/my_plot.png')
        plt.clf()
        return render_template('index.html', plot_url=f'static/my_plot.png')
    else:
        return render_template('index.html')
    
    
    
app.secret_key = 'some secret'

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
    