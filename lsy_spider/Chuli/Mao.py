# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def draw_pie(labels,quants):
    # make a square figure

    plt.figure(1, figsize=(18,6))
    plt.subplot(131)
    # For China, make the piece explode a
    expl = [0,0.1,0,0,0,0,0,0,0,0]   #第二块即China离开圆心0.1
    # Colors used. Recycle if not enough.
    colors  = ["blue","red","coral","green","yellow","orange"]  #设置颜色（循环显示）
    # Pie Plot
    # autopct: format of "percent" string;百分数格式
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
    plt.title('Top 10 GDP Countries', bbox={'facecolor':'0.8', 'pad':5})
    plt.show()
    plt.savefig("pie.jpg")
    plt.close()



# quants: GDP

# labels: country name

labels   = ['USA', 'China', 'India', 'Japan', 'Germany', 'Russia', 'Brazil', 'UK', 'France', 'Italy']

quants   = [15094025.0, 11299967.0, 4457784.0, 4440376.0, 3099080.0, 2383402.0, 2293954.0, 2260803.0, 2217900.0, 1846950.0]

draw_pie(labels,quants)