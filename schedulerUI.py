from datetime import datetime, time
from pandas._config.config import options
import streamlit as st
import random
import pandas as pd
from traitlets.traitlets import default
from scheduler import Scheduler
from utils import hours
import plotly_express as px

st.set_page_config(layout="wide")

# Static data definition
color_map = {'NAVY': '#001f3f', 'BLUE': '#0074D9',
             'AQUA': '#7FDBFF', 'TEAL': '#39CCCC',
             'PURPLE': '#B10DC9',
             'FUCHSIA': '#F012BE',
             'MAROON': '#85144b',
             'RED': '#DB7093',
             'ORANGE': '#FF851B',
             'YELLOW': '#FFDC00',
             'GREEN': '#2ECC40',
             'LIME': '#01FF70'}

color_setup_matrix = {'NAVY': {'NAVY': 0,
                               'BLUE': 5,
                               'AQUA': 4,
                               'TEAL': 4,
                               'PURPLE': 6,
                               'FUCHSIA': 7,
                               'MAROON': 4,
                               'RED': 4,
                               'ORANGE': 6,
                               'YELLOW': 8,
                               'GREEN': 5,
                               'LIME': 5},
                      'BLUE': {'NAVY': 3,
                               'BLUE': 0,
                               'AQUA': 6,
                               'TEAL': 8,
                               'PURPLE': 6,
                               'FUCHSIA': 5,
                               'MAROON': 4,
                               'RED': 4,
                               'ORANGE': 8,
                               'YELLOW': 4,
                               'GREEN': 5,
                               'LIME': 4},
                      'AQUA': {'NAVY': 5,
                               'BLUE': 8,
                               'AQUA': 0,
                               'TEAL': 3,
                               'PURPLE': 4,
                               'FUCHSIA': 6,
                               'MAROON': 7,
                               'RED': 5,
                               'ORANGE': 4,
                               'YELLOW': 5,
                               'GREEN': 7,
                               'LIME': 6},
                      'TEAL': {'NAVY': 4,
                               'BLUE': 8,
                               'AQUA': 3,
                               'TEAL': 0,
                               'PURPLE': 3,
                               'FUCHSIA': 7,
                               'MAROON': 4,
                               'RED': 6,
                               'ORANGE': 3,
                               'YELLOW': 8,
                               'GREEN': 8,
                               'LIME': 5},
                      'PURPLE': {'NAVY': 5,
                                 'BLUE': 8,
                                 'AQUA': 6,
                                 'TEAL': 3,
                                 'PURPLE': 0,
                                 'FUCHSIA': 8,
                                 'MAROON': 5,
                                 'RED': 7,
                                 'ORANGE': 3,
                                 'YELLOW': 4,
                                 'GREEN': 3,
                                 'LIME': 7},
                      'FUCHSIA': {'NAVY': 5,
                                  'BLUE': 4,
                                  'AQUA': 4,
                                  'TEAL': 5,
                                  'PURPLE': 5,
                                  'FUCHSIA': 0,
                                  'MAROON': 4,
                                  'RED': 5,
                                  'ORANGE': 7,
                                  'YELLOW': 7,
                                  'GREEN': 6,
                                  'LIME': 7},
                      'MAROON': {'NAVY': 7,
                                 'BLUE': 5,
                                 'AQUA': 4,
                                 'TEAL': 7,
                                 'PURPLE': 8,
                                 'FUCHSIA': 3,
                                 'MAROON': 0,
                                 'RED': 4,
                                 'ORANGE': 8,
                                 'YELLOW': 4,
                                 'GREEN': 7,
                                 'LIME': 8},
                      'RED': {'NAVY': 7,
                              'BLUE': 4,
                              'AQUA': 4,
                              'TEAL': 4,
                              'PURPLE': 7,
                              'FUCHSIA': 6,
                              'MAROON': 8,
                              'RED': 0,
                              'ORANGE': 4,
                              'YELLOW': 4,
                              'GREEN': 3,
                              'LIME': 4},
                      'ORANGE': {'NAVY': 4,
                                 'BLUE': 4,
                                 'AQUA': 7,
                                 'TEAL': 3,
                                 'PURPLE': 7,
                                 'FUCHSIA': 6,
                                 'MAROON': 6,
                                 'RED': 4,
                                 'ORANGE': 0,
                                 'YELLOW': 5,
                                 'GREEN': 6,
                                 'LIME': 6},
                      'YELLOW': {'NAVY': 6,
                                 'BLUE': 8,
                                 'AQUA': 7,
                                 'TEAL': 7,
                                 'PURPLE': 7,
                                 'FUCHSIA': 4,
                                 'MAROON': 6,
                                 'RED': 5,
                                 'ORANGE': 4,
                                 'YELLOW': 0,
                                 'GREEN': 3,
                                 'LIME': 6},
                      'GREEN': {'NAVY': 4,
                                'BLUE': 3,
                                'AQUA': 7,
                                'TEAL': 7,
                                'PURPLE': 7,
                                'FUCHSIA': 4,
                                'MAROON': 3,
                                'RED': 3,
                                'ORANGE': 5,
                                'YELLOW': 3,
                                'GREEN': 0,
                                'LIME': 6},
                      'LIME': {'NAVY': 5,
                               'BLUE': 3,
                               'AQUA': 5,
                               'TEAL': 3,
                               'PURPLE': 4,
                               'FUCHSIA': 3,
                               'MAROON': 4,
                               'RED': 6,
                               'ORANGE': 3,
                               'YELLOW': 4,
                               'GREEN': 7,
                               'LIME': 0}}

strategies = ['Random', 'Local', 'Complete']
st.sidebar.header("Scheduling problem definition")

form = st.sidebar.form(key="input-form")
n_tasks = form.slider("Number of tasks", 1, 100, 10, 1)

duration_range = form.slider("Task duration range:",
                             value=(3, 10), min_value=2, max_value=15)

desnsity = 0  # form.slider("density", 10, 100, 10, 10)

colors = form.multiselect(
    "Task colors", color_map.keys(), default=['RED', 'YELLOW', 'BLUE', 'GREEN'])

n_resources = form.slider("Number of resources", 1, 20, 3, 1)

strategy = form.selectbox("Choose a solver", strategies, index=0)
n_repeats = form.slider("Iterations", 1, 10000, 1, 100)
showTables = form.checkbox("Show Data Tables", value=False)
showColorMatrix = form.checkbox("Show Color Matrix", value=False)


def generateProblem():
    sch = Scheduler(n_tasks, n_resources, colors,
                    color_setup_matrix, desnsity, duration_range)
    sch.createProblem()
    bestSch, result = sch.solveProblem(strategy, n_repeats)
    # [task.serialize() for task in bestSch.tasks.values()]
    tasks = bestSch['Tasks']
    # [res.serialize() for res in bestSch.resources.values()]
    resources = bestSch['Resources']
    # makespan
    makespan = bestSch['makespan']

    # Display Schedule
    st.title("Schedule length: " + str(hours(makespan)) +
             " hours (" + str(makespan) + ")")
    # resource timeline chart
    # st.header("Resource Schedule:")
    df = pd.DataFrame(tasks)
    fig = px.timeline(df,  x_start="Start", x_end="Finish",
                      y="Resource", color="Color",  color_discrete_map=color_map, title="Best Solution")  # text="Task",
    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, use_container_width=True)

    utilization, allocation = st.columns(2)
    # resource utilization chart
    # utilization.subheader("Resource Utilization")
    barFig = px.bar(resources, x='Resource', y='Utilization', color="Color",
                    color_discrete_map=color_map, title="Resource utilization")
    utilization.plotly_chart(barFig, use_container_width=True)

    # resource allocation chart
    # allocation.subheader("Resource Allocations")
    pieFig = px.pie(resources, values='Allocation', names='Resource',
                    color="Color", color_discrete_map=color_map, title="Resource allocation")
    allocation.plotly_chart(pieFig, use_container_width=True)

    # generation
    # st.subheader("Generation")
    lineFig = px.scatter(result, x='id', y='makespan',
                         title="Makespan analysis")
    # st.plotly_chart(lineFig, use_container_width=True)
    utilization.plotly_chart(lineFig, use_container_width=True)

    # st.subheader("Generation")
    pf = pd.DataFrame(result)
    lineFig2 = px.scatter(result, x='makespan', y='id',
                          title="Solution analysis")
    # st.plotly_chart(lineFig2, use_container_width=True)
    # allocation.plotly_chart(lineFig2, use_container_width=True)
    histFig = px.histogram(
        pf, x='makespan', nbins=n_repeats, title="Solution analysis")
    allocation.plotly_chart(histFig)
    # allocation.write(pf.hist('makespan', bins=n_repeats))

    # Data tables
    if(showTables or showColorMatrix):
        st.header("Data Tables")
    if(showTables):
        st.subheader("Tasks")
        # show tasks shorted by start date
        tasks.sort(key=lambda c: c['Start'])
        st.table(tasks)  # lambda c: c['Start']))

        st.subheader("Resources")
        # show resource shorted by utilization
        resources.sort(key=lambda r: r['Utilization'])
        st.table(resources)

    if(showColorMatrix):
        st.header("Color Setup Matrix")
        st.table(pd.DataFrame(color_setup_matrix))


submit = form.form_submit_button(label="Solve")

if(submit):
    generateProblem()
else:
    st.title("Task assignment problem play ground")
    st.header("Purpose")
    st.text("""We want to play with different algorithms to solve simple task assignment problems with the goal **minimize** length of a schedule.""")
    st.text("""User can create a task assignment problem by selecting few parameters (defined below), and then choose a type of solver to create a solution.""")
    st.text("""The task assignment problem generated here is a simple problem. For each task we need to assign a resource to it. 
    Each task has a color.
    For a given resource, offset between two consecutive tasks is determined by looking up the color offset matrix. 
    Goal is to assign all tasks to available resources, while minimizing the toal length of the schedule.
    Length of a schedule is defined as the time difference between earliest start time and latest end time among the tasks.
    """)
    st.markdown('1. Select number of tasks')
    st.markdown('---')
    st.markdown('**Hello**')
    st.markdown('### **Metrics**')
    st.markdown("""|First|Second|\n|---|----|\n """)
    st.text("Select duration range of tasks. Duration to tasks are assinged within this range. Durations are in hours.")
    st.text("Select set of colors for tasks. When tasks are executed on same resource, colors defines the offset between ")
    st.text("concequtive execution of tasks. Color offset matrix is predefined for the list of colors")
