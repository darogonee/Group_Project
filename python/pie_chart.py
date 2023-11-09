import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

def generate_pie_chart(percentages: list, labels: list, colours: list, image_name: str):
    y = np.array(percentages)
    plt.pie(y, labels=labels, autopct='%.1f%%', colors=colours)
    plt.savefig(f'web/images/generated/{image_name}.png')

def generate_slider(label: str):
    slider = Slider(label=label)
    