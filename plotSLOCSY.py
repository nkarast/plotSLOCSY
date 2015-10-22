#################################################################################
#
#   author: Nikos Karastathis < nkarast .at. cern .dot. ch >
#
#   Read  and plot environmental parameters
#
#################################################################################


##########################################################################################################
#
#       DO YOU WANT ME TO DO SOME SETUP FOR YOU?
#       I hope you have ROOT and ROOTSYS set...
#       I also have some modules for you, if you want....
#       just change the do_setup to True......
#
do_setup = False
if do_setup:
    from mysetup import *
    exportLocalModules()
    linkPyROOT()


##########################################################################################################
#
#       LET ME IMPORT MY LIBRARY....
#       and then let's do some stuff...
#       you dont have to touch anything here... go to line 47
#
from mylib import *

# initialise the logger
init_logger()

# get the input files
inputfile = getInputFiles()
info('using files...\n \t\t\t%s' %inputfile )

# get the dictionary with the data
# dictionary is in the form of :
# {'key type 1' : [ dates 1, values 1 ], 'key type 2' : [ dates 2, values 2 ],  ....}
datadict = getdata(getInputFiles())




##########################################################################################################
#
#          YO! Welcome!
#          We have read all the environmental variables by now... Oh you haven't noticed? :)
#          I have already merged all files that correspond to the same sensors for you
#
#
#          If you want to do some date cuts... You would have to add something below.
#          You would have to make some dates yourself and pass it to the lowDate, highDate
#          variables below...
#
#          Let me show you how to make a date...
#          Copy and paste the lines that follow.
#          Change the values and the name of the <my_date> as you like.
#
#   year        =  2015
#   month       =  7
#   day         =  3
#   hour        =  12
#   minute      =  30
#   second      =  20
#   millisecond =  250
#
#   my_date = makeDateTime(year, month, day, hour, minute, second, millisecond)


##########################################################################################################
#
#          This is where we make plots
#
#
#


do_DHT_Temperature      = False
do_BMP_Temperature      = False
do_Temperatures         = False
do_BMP_Pressure         = False
do_DHT_Humidity         = False
do_2YAxis               = False
do_plotAll              = True

do_xkcd                 = True

if do_xkcd == False:

    if do_DHT_Temperature:
        figname='fig_DHT_temperature.png'
        key = 'DHT22 Temperature'
        ylabel=r"Temperature ($^{\circ}$C)"
        xlabel=r"Date (d/m-H:M)"
        lw=2.
        plotStyle='-'
        color='r'
        vary_axis=5.
        legend="DHT Temperature"
        cutDate=False
        lowDate=None
        highDate=None
        plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)




    if do_BMP_Temperature:
        figname='fig_BMP_temperature.png'
        key = 'BMP085 Temperature'
        ylabel=r"Temperature ($^{\circ}$C)"
        xlabel=r"Date (d/m-H:M)"
        lw=2.
        plotStyle='-'
        color='g'
        vary_axis=5.
        legend="BMP Temperature"
        cutDate=False
        lowDate=None
        highDate=None
        plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)




    if do_Temperatures:
        figname='fig_temperatures.png'
        key = ['DHT22 Temperature', 'BMP085 Temperature']
        ylabel=r"Temperature ($^{\circ}$C)"
        xlabel=r"Date (d/m-H:M)"
        lw=[2.,2.]
        plotStyle=['-','-']
        color=['r','g']
        vary_axis=5.
        legend=["DHT22 Temperature","BMP Temperature"]
        cutDate=False
        lowDate=None
        highDate=None

        plotTwoLinesSameY(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)





    if do_BMP_Pressure:
        figname='fig_BMP_pressure.png'
        key = 'BMP085 Pressure'
        ylabel=r"Pressure (mbar)"
        xlabel=r"Date (d/m-H:M)"
        lw=2.
        plotStyle='-'
        color='m'
        vary_axis=5.
        legend="BMP Pressure"
        cutDate=False
        lowDate=None
        highDate=None
        plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)


    if do_DHT_Humidity:
        figname='fig_DHT_humidity.png'
        key = 'BMP085 Pressure'
        ylabel=r"Pressure (mbar)"
        xlabel=r"Date (d/m-H:M)"
        lw=2.
        plotStyle='-'
        color='b'
        vary_axis=5.
        legend="BMP Pressure"
        cutDate=False
        lowDate=None
        highDate=None
        plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)


    if do_2YAxis:
        figname='fig_DHT_temperature_BMP_pressure.png'
        key = ['DHT22 Temperature', 'BMP085 Pressure']
        ylabel=[r"Temperature ($^{\circ}$C)",r"Pressure (mbar)"]
        xlabel=r"Date (d/m-H:M)"
        lw=[2.,2.]
        plotStyle=['-','-']
        color=['r','m']
        vary_axis=[5.,5.]
        legend=["DHT22 Temperature","BMP Pressure"]
        cutDate=False
        lowDate=None
        highDate=None
    
        plotTwoLinesDifferentY(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)


    if do_plotAll:
        figname='fig_Env_all.png'
        cutDate=False
        lowDate=None
        highDate=None

        plotAll(datadict, m_figname=figname, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)



else:
    with plt.xkcd():
    
        if do_DHT_Temperature:
            figname='fig_DHT_temperature.png'
            key = 'DHT22 Temperature'
            ylabel=r"Temperature ($^{\circ}$C)"
            xlabel=r"Date (d/m-H:M)"
            lw=2.
            plotStyle='-'
            color='r'
            vary_axis=5.
            legend="DHT Temperature"
            cutDate=False
            lowDate=None
            highDate=None
            plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)
    
    
    
    
        if do_BMP_Temperature:
            figname='fig_BMP_temperature.png'
            key = 'BMP085 Temperature'
            ylabel=r"Temperature ($^{\circ}$C)"
            xlabel=r"Date (d/m-H:M)"
            lw=2.
            plotStyle='-'
            color='g'
            vary_axis=5.
            legend="BMP Temperature"
            cutDate=False
            lowDate=None
            highDate=None
            plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)




        if do_Temperatures:
            figname='fig_temperatures.png'
            key = ['DHT22 Temperature', 'BMP085 Temperature']
            ylabel=r"Temperature ($^{\circ}$C)"
            xlabel=r"Date (d/m-H:M)"
            lw=[2.,2.]
            plotStyle=['-','-']
            color=['r','g']
            vary_axis=5.
            legend=["DHT22 Temperature","BMP Temperature"]
            cutDate=False
            lowDate=None
            highDate=None
        
            plotTwoLinesSameY(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)





        if do_BMP_Pressure:
            figname='fig_BMP_pressure.png'
            key = 'BMP085 Pressure'
            ylabel=r"Pressure (mbar)"
            xlabel=r"Date (d/m-H:M)"
            lw=2.
            plotStyle='-'
            color='m'
            vary_axis=5.
            legend="BMP Pressure"
            cutDate=False
            lowDate=None
            highDate=None
            plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)
    
    
        if do_DHT_Humidity:
            figname='fig_DHT_humidity.png'
            key = 'BMP085 Pressure'
            ylabel=r"Pressure (mbar)"
            xlabel=r"Date (d/m-H:M)"
            lw=2.
            plotStyle='-'
            color='b'
            vary_axis=5.
            legend="BMP Pressure"
            cutDate=False
            lowDate=None
            highDate=None
            plotOneLine(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)


        if do_2YAxis:
            figname='fig_DHT_temperature_BMP_pressure.png'
            key = ['DHT22 Temperature', 'BMP085 Pressure']
            ylabel=[r"Temperature ($^{\circ}$C)",r"Pressure (mbar)"]
            xlabel=r"Date (d/m-H:M)"
            lw=[2.,2.]
            plotStyle=['-','-']
            color=['r','m']
            vary_axis=[5.,5.]
            legend=["DHT22 Temperature","BMP Pressure"]
            cutDate=False
            lowDate=None
            highDate=None
        
            plotTwoLinesDifferentY(datadict, m_key=key, m_figname=figname, m_ylabel=ylabel, m_xlabel=xlabel, m_lw=lw, m_plotStyle=plotStyle, m_color=color, m_vary_axis=vary_axis, m_legend=legend, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)


        if do_plotAll:
            figname='fig_Env_all.png'
            cutDate=False
            lowDate=None
            highDate=None
        
            plotAll(datadict, m_figname=figname, m_cutDate=cutDate, m_lowDate=lowDate, m_highDate=highDate)




