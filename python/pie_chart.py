import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_pie_chart(percentages: list, labels: list, colours: list, image_name: str):
    y = np.array(percentages)
    plt.pie(y, labels=labels, autopct='%.1f%%', colors=colours)
    plt.savefig(f'web/images/generated/{image_name}.png')
