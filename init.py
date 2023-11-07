import matplotlib
matplotlib.use('agg')
import numpy as np
import matplotlib.pyplot as plt
from flask import request
from flask import Flask, render_template
import cmath

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/blog/linear')
def blogLinear():
    return render_template('bloglinear.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/linear', methods = ['GET','POST'])
def linear():
    if request.method == 'POST':
        plt.clf()
        a = int(request.form['nilai_a'])
        b = int(request.form['nilai_b'])

        x = np.arange(-10, 10, 0.01)
        y = a*x + b

        x1 = -b/a
        y1 = b

        data = [x1, y1]

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
        return render_template('linear.html', plot_url=f'static/my_plot.png', data = data)
    else:
        return render_template('linear.html')

@app.route('/kuadrat', methods = ['GET','POST'])
def kuadrat():
    if request.method == 'POST':
        plt.clf()
        a = float(request.form['nilai_a'])
        b = float(request.form['nilai_b'])
        c = float(request.form['nilai_c'])

        def nilaiDeskriman(a, b, c): # <- menghitung nilai deskriminan
            deskriminan = b**2 - 4*a*c
            return deskriminan

        D = nilaiDeskriman(a, b, c)

        def nilaiFaktorX(a,b): # <- mencari titik potong pada sumbu x
            x1 = (-b + np.sqrt(D))/(2*a)
            x2 = (-b - np.sqrt(D))/(2*a)
            return x1, x2

        def titikMaxMin(a,b): # <- mencari titik maksimum atau minimum
            xm = -b/2*a
            ym = -D/4*a
            return xm, ym

        def titikPotongY(c): #<- mencari titik potong pada sumbu y
            ty = c
            return ty

        x1, x2 = nilaiFaktorX(a,b)
        ty = titikPotongY(c)
        xm, ym = titikMaxMin(a,b)
        # program menghitung fungsi kubik end

        x = np.arange(-10, 10, 0.001)
        y = a*x**2 + b*x + c
        y0 = 0
        y1 = 0

        data = [x1,x2,ty,xm,ym]

        plt.plot(x,y, "r")
        plt.plot([x1, x2], [y0, y1], "k*", label="Titik Potong Sumbu x")
        plt.plot(0, ty, "c*", label="Titik Potong Sumbu y")
        plt.plot(xm, ym, "b*", label="Titik Maximum/Minimun")

        plt.xlim(-10, 10)
        plt.ylim(-20, 20)

        plt.xticks(np.arange(-10, 10, 1))
        plt.title(f"$y = {a}x^2 + {b}x + {c}$")
        plt.xlabel("sumbu x")
        plt.ylabel("sumbu y")
        plt.grid()

        ax = plt.gca()
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')        
        plt.legend()
        plt.savefig('static/kuadrat.png')
        plt.clf()
        return render_template('kuadrat.html', plot_url='static/kuadrat.png', data = data)
    else:
        return render_template('kuadrat.html')


@app.route('/kubik', methods = ['GET','POST'])
def kubik():
    if request.method == 'POST':
        plt.clf()
        a = float(request.form['nilai_a'])
        b = float(request.form['nilai_b'])
        c = float(request.form['nilai_c'])
        d = float(request.form['nilai_d'])

        def solve_cubic(a, b, c, d):
            D = 18 * a * b * c * d - 4 * b**3 * d + b**2 * c**2 - 4 * a * c**3 - 27 * a**2 * d**2
            
            # Hitung koefisien p dan q
            p = (3 * a * c - b**2) / (3 * a**2)
            q = (2 * b**3 - 9 * a * b * c + 27 * a**2 * d) / (27 * a**3)
            
            # Hitung akar-akar persamaan kuadrat
            discriminant = cmath.sqrt(q**2 / 4 + p**3 / 27)
            u1 = -q / 2 + discriminant
            u2 = -q / 2 - discriminant
            
            # Hitung akar-akar kubik
            cube_root_u1 = u1**(1/3)
            cube_root_u2 = u2**(1/3)
            
            # Hitung akar-akar persamaan kubik
            x1 = cube_root_u1 + cube_root_u2 - b / (3 * a)
            x2 = -(cube_root_u1 + cube_root_u2) / 2 - b / (3 * a) + 1j * cmath.sqrt(3) * (cube_root_u1 - cube_root_u2) / 2
            x3 = -(cube_root_u1 + cube_root_u2) / 2 - b / (3 * a) - 1j * cmath.sqrt(3) * (cube_root_u1 - cube_root_u2) / 2

            y1 = d
            
            return x1, x2, x3, y1

        akar1, akar2, akar3, y1 = solve_cubic(a, b, c, d)
        print("Akar pertama:", akar1)
        print("Akar kedua:", akar2)
        print("Akar ketiga:", akar3)

        data = [akar1, akar2, akar3, y1]

        x = np.arange(-10, 10, 0.01)
        y = a*x**3 + b*x**2 + c*x + d

        plt.plot(x, y)
        plt.plot(akar1, 0, "k*", label=f"Titik Potong Sumbu x ")
        plt.plot(akar2, 0, "k*",)
        plt.plot(akar3, 0, "k*",)
        plt.plot(0, y1, "g*", label="Titik Potong Sumbu y")
        plt.plot()

        plt.xlabel("sumbu x")
        plt.ylabel("sumbu y")
        plt.title(f"$y = {a}x^3 + {b}x^2 + {c}x + {d}$")
        plt.xlim(-10, 10)
        plt.ylim(-20, 20)
        plt.grid()

        ax = plt.gca()
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')        
        plt.legend()

        plt.savefig('static/kubik.png')
        plt.clf()
        return render_template('kubik.html', plot_url='static/kubik.png', data = data)
    else:
        return render_template('kubik.html')
    
app.secret_key = 'some secret'

if __name__ == "__main__":
    app.run('localhost', 5000, debug=True)
    