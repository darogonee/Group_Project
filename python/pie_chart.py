import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt # use this command to install matplotlib.pyplot:     pip3 install matplotlib
import numpy as np
from matplotlib.widgets import Slider

# creates a pie chart and saves it to a file
def generate_pie_chart(percentages: list, labels: list, colours: list, image_name: str, user: str):
    y = np.array(percentages)
    fig, ax = plt.subplots()
    ax.pie(y, labels=labels, autopct='%.1f%%', colors=colours, startangle=90, wedgeprops=dict(edgecolor='black', linewidth=2))
    fig.patch.set_facecolor('none') #transparent
    ax.set_facecolor('none')
    plt.tight_layout()
    plt.savefig(f'web/images/generated/user_charts/{user}/{image_name}') # save pie chart to specified path

# create a slider and saves it to a file
def generate_slider(label: str):
    slider = Slider(label=label)
    