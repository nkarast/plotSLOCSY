#################################################################################
#
#   author: Nikos Karastathis < nkarast .at. cern .dot. ch >
#
#   Read  and plot environmental parameters
#
#################################################################################

##########################################################################################################
#
#       GLOBALS     -- DONT TOUCH THES!!
#
useROOT = False
makeNtuple = False
trees = []
ntupleName = "readEnvironmental.root"


##########################################################################################################
#
#       DEFINE SOME FUNCTIONS FOR MANUAL USAGE
#


def usage():
    """
        Prints usage information.
        Input : None
        Output : None
        """
    
    s=("""
        ======================================================================================
        Read and Plot Environmental Parameters from RD-51 WinCC SLOCSY Project
        ======================================================================================
        
        -- author : Nikos Karastathis  ( nkarast <at> cern <dot> ch )
        -- version: 0.1.0
        
        \033[1mNAME:\033[0m
        plotSLOCSY
        
        
        \033[1mSYNOPSIS:\033[0m
        python [-i] plotSLOCSY.py [-h] [--help] [-f \033[4margument\033[0m] [--folder=\033[4margument\033[0m]
                                         [-i \033[4m/path/to/file1.dat,/path/to/file2.dat,...\033[0m] [--input=\033[4m/path/to/file1.dat,/path/to/file2.dat,...\033[0m]
                                         [-r] [--useROOT] [-n] [--ntupleName=\033[4margument\033[0m]
        
        
        \033[1mDEPENDENCIES:\033[0m
        Python v2 (preferably) and the modules: numpy, matplotlib, [ ROOT, root_numpy ]
        To install the modules needed please do:
        \033[92mpip install numpy --upgrade && pip install matplotlib --upgrade && pip install root_numpy --upgrade\033[0m
        For ROOT bindings please read : \033[36mhttps://root.cern.ch/drupal/content/pyroot\033[0m
        
        
        \033[1mDESCRIPTION:\033[0m
        This is a code to read the files taken from the export panel of the Environmental Parameters of the
        RD-51 WinCC SLOCSY. The script reads the input files and makes multiple plots and a summary one.
        The input to the script can be given either as comma separated values, or as a folder that contains
        all the input files. If no input is specified the script goes into debug mode with the hardcoded values
        as input files. To change these look at the <sensors> class in the code.
        The format of the input file is assumed to be "YYYY MM DD HH mm ss msms value", where all columns,
        apart from 'value' are taken as integers.
        
        
        \033[1mCOMMAND LINE OPTIONS:\033[0m
        -h, --help
                    Prints the usage for the script.. You kinda found it if you're reading this :)
        
        -f \033[4margument/\033[0m , --foler=\033[4margument/\033[0m
                    Read all files under folder \033[4margument/\033[0m
        
        -i \033[4m[argument1,argument2,...]\033[0m , --input=\033[4m[argument1,argument2,...]\033[0m
                    Read only the files specified in \033[4m[argument1,argument2,...]\033[0m. \033[4m[argument1,argument2,...]\033[0m is comma separated values, without blank spaces.

        -r , --useROOT
                    Use ROOT flag.
        
        -n \033[4margument\033[0m , --ntupleName=\033[4margument\033[0m
                    Make a ROOT Ntuple to store values, with file name to be \033[4margument\033[0m. Default filename [readEnvironmental.root]
        
        
        \033[1mEXAMPLES:\033[0m
        
        1) Run PlotSLOCSY with four input dat files. And make some plots
            a) Open plotSLOCSY.py and change whatever plot flags you want.
        
            b) Run the command:
        python plotSLOCSY.py -i BMP085.Pressure1_03_07.dat,DHT22.Humidity1_03_07.dat,BMP085.Temperature1_03_07.dat,DHT22.Temperature1_03_07.dat
        
        
        2) Repeat <example 1> but now also write a ROOT file which contains trees for each. The ROOT file is names "out.root"
            a) Open plotSLOCSY.py and change whatever plot flags you want.
        
            b) Run the command:
        python plotSLOCSY.py -n out.root -i BMP085.Pressure1_03_07.dat,DHT22.Humidity1_03_07.dat,BMP085.Temperature1_03_07.dat,DHT22.Temperature1_03_07.dat
        
        
        3) Run PlotSLOCSY over a whole folder of files and make some plots. The files are assumed to be named:
        BMP085.Pressure1*
        DHT22.Humidity1*
        BMP085.Temperature1*
        DHT22.Temperature1*
        
        where * is the wildcard character. Then also write a ROOT ntuple named "out.root" .
            a) Open plotSLOCSY.py and change whatever plot flags you want.
        
            b) Run the command:
        python plotSLOCSY.py -n out.root -f input/
        
        """)
    print(s)


# - * - * - * - * - * - * - * - * - * - * - * - * - * - *


def short_usage():
    s=("""
        python [-i] plotSLOCSY.py [-h] [--help] [-f \033[4margument\033[0m] [--folder=\033[4margument\033[0m]
        [-i \033[4m/path/to/file1.dat,/path/to/file2.dat,...\033[0m]
        [--input=\033[4m/path/to/file1.dat,/path/to/file2.dat,...\033[0m]
        
        Try python plotSLOCSY.py -h
        """)
    print(s)

# - * - * - * - * - * - * - * - * - * - * - * - * - * - *


def dependencies():
    s=("""
        \033[1mDEPENDENCIES:\033[0m
        Python v2 (preferably) and the modules: numpy, matplotlib, [ ROOT, root_numpy ]
        To install the modules needed please do:
        \033[92mpip install numpy --upgrade && pip install matplotlib --upgrade && pip install root_numpy --upgrade\033[0m
        For ROOT bindings please read : \033[36mhttps://root.cern.ch/drupal/content/pyroot\033[0m
        
        """)
    print(s)

# - * - * - * - * - * - * - * - * - * - * - * - * - * - *



##########################################################################################################
#
#       IMPORT MODULES & CHECK IF THERE ARE THERE...
#

# this is to use logging
from logging import *

# this is to use "datetime" class
from datetime import datetime

# this is to merge input files
import fileinput

# import sys to get command line arguments
import sys, getopt, os, glob

# use the numpy module for fast array handling
try:
    import numpy as np
except ImportError:
    print(""" \033[91m[FATAL] Missing numpy module.\033[0m
        \033[93mPlease install numpy module, by doing in your command line:
        pip install numpy --upgrade\033[0m""")
    short_usage()
    dependencies()
    sys.exit(2)

# use matplotlib for plotting stuff
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import *
except ImportError:
    print(""" [FATAL] Missing matplotlib module.
        \033[93mPlease install matplolib module, by doing in your command line:
        pip install matplolib --upgrade\033[0m""")
    short_usage()
    dependencies()
    sys.exit(2)

## use ROOT for plotting
try:
    import ROOT as rt
except ImportError:
    print("[FATAL] Missing ROOT binding.\n\033[93mPlease install ROOT.\nMake sure that you have configured it with --enable-python or --all arguments.\nAlso make sure that ROOT is in your $PYTHONPATH\nCheck: https://root.cern.ch/drupal/content/pyroot\033[0m")
    short_usage()
    dependencies()
    sys.exit(2)

## use root_numpy for filling tree
#try:
#    from root_numpy import array2tree
#except ImportError:
#    print(""" [FATAL] Missing root_numpy module.
#        \033[93mPlease install root_numpy module, by doing in your command line:
#        pip install root_numpy --upgrade\033[0m""")
#
#    short_usage()
#    dependencies()
#    sys.exit(2)

##########################################################################################################
#
#       DEFINE THE SENSORS CLASS FOR BOOK KEEPING
#

class sensors:
    #
    # constructor of class
    #
    def __init__(self):
        # names of sensor files
        self.bmp_pres_name = 'BMP085.Pressure1'
        self.bmp_temp_name = 'BMP085.Temperature1'
        self.dht_temp_name = 'DHT22.Temperature1'
        self.dht_hum_name  = 'DHT22.Humidity1'
    
        # list that holds files for each type
        self.bmp_pres_list = []
        self.bmp_temp_list = []
        self.dht_temp_list = []
        self.dht_hum_list  = []

        # list of lists  # i do it so detailed to improve readability of the code
        self.listoflists = [self.bmp_pres_list, self.bmp_temp_list, self.dht_temp_list, self.dht_hum_list]
    
        # list of names  # i do it so detailed to improve readability of the code
        self.listofnames = [self.bmp_pres_name, self.bmp_temp_name, self.dht_temp_name, self.dht_hum_name]

    # give a list to fill_list_of_lists(), then it'll fill the list of lists
    def filllistoflists(self, files):
        for file in files:
            if self.bmp_pres_name in file : self.bmp_pres_list.append(file)
            if self.bmp_temp_name in file : self.bmp_temp_list.append(file)
            if self.dht_temp_name in file : self.dht_temp_list.append(file)
            if self.dht_hum_name  in file : self.dht_hum_list.append(file)
   
   # return the list of lists for this instance
    def getlistoflist(self): return self.listoflists

    # return a dictionary in the format {'name1':[list1], 'name2':[list2] }
    def getdict(self):
        listoflegends = [(legend.replace("."," ").replace("1","")) for legend in self.listofnames]
        return dict(zip(listoflegends,self.listoflists))

##########################################################################################################
#
#       DEFINE THE COLOR CLASS FOR BOOK KEEPING OF FORMAT STUFF  -- Not used anywhere...
#
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


##########################################################################################################
#
#       DEFINE SOME FUNCTIONS TO PLAY IT SMART
#

def init_logger(logfile="",loglevel="debug"):
    """
        Initialize the format and log level and even the file of the logger
        Inputs logfile (default=""), loglevel (default="debug")
        """
    m_level = ""
    if loglevel=="debug" : m_level = DEBUG
    elif loglevel=="info" : m_level = INFO
    elif loglevel=="warning" : m_level = WARNING
    elif loglevel=="error" : m_level = ERROR
    elif loglevel=="critical" : m_level = loggin.CRITICAL
    FORMAT = '%(asctime)s %(levelname)s : %(message)s'
    basicConfig(format=FORMAT, filename=logfile, level=m_level)
    info('(init_logger) logger initialized with format : %s , file = %s , at level %s ' % (FORMAT, logfile, loglevel) )



def getInputFiles():
    """
    Description: Reads if there are files in the prompt arguments and returns a list with the filenames
    Input: None
    Output: A dictionary with the format of { 'sensor label 1' : [list of files for sensorl label 1] , 'sensor label 2' : [list of files for sensorl label 2],  ... }

    """
    global useROOT
    global makeNtuple
    global ntupleName
    
    if len(sys.argv)>1:
        try:
            # return a two list of tuples
            # the opts one has tuples with ('-option', 'argument') that is passed after readEnvironmental.py
            opts, args = getopt.getopt(sys.argv[1:], "hrf:i:n:", ["help", "useROOT", "folder=", "input=", "ntupleName="])
        except getopt.GetoptError as err:
            print(err); short_usage(); sys.exit(2);

        for option, argument in opts:
            if option in ('-h', '--help'):
                usage()
                sys.exit()
            elif option in ('-r', '--useROOT'):
                info("using ROOT...")
                useROOT = True
                        
            elif option in ('-n', '--ntupleName'):
                info("using ROOT to make ntuple...")
                useROOT = True
                makeNtuple = True
                ntupleName=argument

            elif option in ('-f','--folder'):
                # create an instance of the sensors class
                sens_obj = sensors()
                
                # get all files under the folder passed as argument, and return the dictionary
                files = glob.glob(argument+"/*")
                sens_obj.filllistoflists(files)
                return sens_obj.getdict()   #getlistoflist()  # return this list of lists

            elif option in ('-i', '--input'):
                # the argument is comma separated. So split them
            
                # create an instance of the sensors class
                sens_obj = sensors()
            
                files = argument.split(',')
                sens_obj.filllistoflists(files)
                return sens_obj.getdict()
                    
    # This is for debug mode, when no arguments are passed for fast checking
    else :
        info("running debug mode with hardcoded inputs...")
        return {'BMP085 Pressure':["input/BMP085.Pressure1_03_07.dat"], 'BMP085 Temperature':["input/BMP085.Temperature1_03_07.dat"], 'DHT22 Temperature':["input/DHT22.Temperature1_03_07.dat"], 'DHT22 Humidity':["input/DHT22.Humidity1_03_07.dat"]}



# - * - * - * - * - * - * - * - * - * - * - * - * - * - *

def getdata(filesdict):
    """
    Return a dictionary of lists in the format of { filename1 : [f1X, f1Y], filename2 : [f2X, f2Y],..., filenameN:[fNX, fNY] }, N= # of files/axes
    Input: List of filenames
    Output: Dictionary of filenames as keys and list of [X,Y] axes as values
    
    """
    
    # if you need to make an ntuple, you have to have root_numpy...
    # if you already have it, you can comment this and uncomment it on the top of imports
    if makeNtuple:
        try:
            from root_numpy import array2tree
        except ImportError:
            critical("Missing root_numpy module.\n\033[93mPlease install root_numpy module, by doing in your command line:\npip install root_numpy --upgrade\033[0m")
            short_usage()
            dependencies()
            sys.exit(2)

    
    
    axes = []
    # for every sub-list corresponding to one sensor type, merge inputs into a "file" then pass this file into numpy
    # this loops over the different types in the dictionary
    for key in filesdict.keys():
        # now for each type get all the files into "one"
        infiles = fileinput.input(filesdict[key])
        #get the data array from numpy
        data_array = np.loadtxt(infiles, dtype={'names' : ('year', 'month', 'day', 'hour', 'minute', 'second' , 'msecond', 'value'), 'formats': ('i4', 'i4','i4','i4','i4','i4','i4','float64')})
        
        if makeNtuple:
            info('filling tree %s', key)
            tree = array2tree(data_array)
            tree.SetName(key)
            trees.append(tree)


        # convert to datetime
        dates = []
        for ientry in range(len(data_array['value'])):
            dates.append(datetime(data_array['year'][ientry], data_array['month'][ientry], data_array['day'][ientry], data_array['hour'][ientry], data_array['minute'][ientry], data_array['second'][ientry], data_array['msecond'][ientry]*1000))
        dates = np.array(dates)
        #print dates
        axes.append([dates,data_array['value'] ])



    # this is to write the file -- it has to be out of for loop
    if useROOT and makeNtuple:
        info("creating ROOT file with name %s" % ntupleName)
        fout = rt.TFile(ntupleName,'recreate')
        fout.cd()
        for outree in trees:
            outree.Write()
        fout.Close()


    return dict(zip(filesdict.keys(),axes))




# - * - * - * - * - * - * - * - * - * - * - * - * - * - *


# plot one line plot
def plotOneLine(datadict, m_key='DHT22 Temperature', m_figname='fig_DHT_temp.png', m_ylabel=r"Temperature ($^{\circ}$C)", m_xlabel=r"Date (d/m-H:M)", m_lw=2., m_plotStyle='-', m_color='r', m_vary_axis=5., m_legend="DHT22 Temperature", m_cutDate=False, m_lowDate=None, m_highDate=None):

    x1 = datadict[m_key][0]
    y1 = datadict[m_key][1]


    if m_cutDate==True:
        sel_ind = np.where((x1>m_lowDate) & (x1<m_highDate) )
        x1 = x1[sel_ind]
        y1 = y1[sel_ind]
    
    
    plt.close('all')
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    formatter = mdates.DateFormatter('%d/%m-%H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=60)
    minorlocator = AutoMinorLocator()
    ax.xaxis.set_minor_locator(minorlocator)
    ax.yaxis.set_minor_locator(minorlocator)
    ax.plot(x1, y1, m_plotStyle+m_color, lw=m_lw, label=m_legend)

    ymin, ymax = ax.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis = m_vary_axis
    ax.set_ylim([ymin-(vary_axis*axis_ratio), ymax+(vary_axis*axis_ratio)])
    ax.set_ylabel(m_ylabel)
    ax.set_xlabel(m_xlabel)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.yaxis.grid(which='both')
    ax.xaxis.grid(which='both')
    fig.tight_layout()
    info("Writing file : %s" % m_figname)
    fig.savefig(m_figname)



# - * - * - * - * - * - * - * - * - * - * - * - * - * - *


# plot 2 lines sharing the same Y axis and X axis
def plotTwoLinesSameY(datadict, m_key=['DHT22 Temperature', 'BMP085 Temperature'], m_figname='fig_temp.png', m_ylabel=r"Temperature ($^{\circ}$C)", m_xlabel=r"Date (d/m-H:M)", m_lw=[2.,2.], m_plotStyle=['-','-'], m_color=['r','g'], m_vary_axis=5., m_legend=["DHT22 Temperature","BMP Temperature"], m_cutDate=False, m_lowDate=None, m_highDate=None):
    
    x1 = datadict[m_key[0]][0]
    y1 = datadict[m_key[0]][1]
    
    x2 = datadict[m_key[0]][0]
    y2 = datadict[m_key[0]][1]
    
    if m_cutDate==True:
        sel1_ind = np.where((x1>m_lowDate) & (x1<m_highDate) )
        x1 = x1[sel1_ind]
        y1 = y1[sel1_ind]

        sel2_ind = np.where((x2>m_lowDate) & (x2<m_highDate) )
        x2 = x2[sel2_ind]
        y2 = y2[sel2_ind]

    plt.close('all')
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)

    formatter = mdates.DateFormatter('%d/%m-%H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=60)
    minorlocator = AutoMinorLocator()
    ax.xaxis.set_minor_locator(minorlocator)
    ax.yaxis.set_minor_locator(minorlocator)

    ax.plot(x1,y1, m_plotStyle[0]+m_color[0], lw=m_lw[0], label=m_legend[0])
    ax.plot(x2,y2, m_plotStyle[1]+m_color[1], lw=m_lw[1], label=m_legend[1])

    vary_axis = m_vary_axis
    ymin, ymax = ax.get_ylim()
    axis_ratio = (ymin/ymax)
    ax.set_ylim([ymin-(vary_axis*axis_ratio), ymax+(vary_axis*axis_ratio)])

    ax.set_ylabel(m_ylabel)
    ax.set_xlabel(m_xlabel)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.yaxis.grid(which='both')
    ax.xaxis.grid(which='both')
    fig.tight_layout()
    info("Writing file : %s" % m_figname)
    fig.savefig(m_figname)



# - * - * - * - * - * - * - * - * - * - * - * - * - * - *

def plotTwoLinesDifferentY(datadict, m_key=['DHT22 Temperature', 'BMP085 Pressure'], m_figname='fig_temp_pres.png', m_ylabel=[r"Temperature ($^{\circ}$C)", r"Pressure (mbar)"], m_xlabel=r"Date (d/m-H:M)", m_lw=[2.,2.], m_plotStyle=['-','-'], m_color=['r','g'], m_vary_axis=[5.,5.], m_legend=["DHT22 Temperature","BMP Pressure"], m_cutDate=False, m_lowDate=None, m_highDate=None):

    x1 = datadict[m_key[0]][0]
    y1 = datadict[m_key[0]][1]
    
    x2 = datadict[m_key[1]][0]
    y2 = datadict[m_key[1]][1]
    
    if m_cutDate==True:
        sel1_ind = np.where((x1>m_lowDate) & (x1<m_highDate) )
        x1 = x1[sel1_ind]
        y1 = y1[sel1_ind]
        
        sel2_ind = np.where((x2>m_lowDate) & (x2<m_highDate) )
        x2 = x2[sel2_ind]
        y2 = y2[sel2_ind]

    plt.close('all')
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    formatter = mdates.DateFormatter('%d/%m-%H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=60)
    minorlocator = AutoMinorLocator()
    ax.xaxis.set_minor_locator(minorlocator)
    ax.yaxis.set_minor_locator(minorlocator)
    
    line1 = ax.plot(x1,y1, m_plotStyle[0]+m_color[0], lw=m_lw[0], label=m_legend[0])
    ymin, ymax = ax.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis=m_vary_axis[0]
    ax.set_ylim([ymin-(vary_axis*axis_ratio), ymax+(vary_axis*axis_ratio)])
    ax.set_ylabel(m_ylabel[0])
    ax.set_xlabel(m_xlabel)
    ax.yaxis.grid(which='both')
    ax.xaxis.grid(which='both')

    ###  ------------------   second y axis ------------
    ax2 = ax.twinx()
    line2 = ax2.plot(x2,y2, m_plotStyle[1]+m_color[1], lw=m_lw[1], label=m_legend[1])
    ymin, ymax = ax2.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis=m_vary_axis[1]
    ax2.set_ylim([ymin-(vary_axis*axis_ratio), ymax+(vary_axis*axis_ratio)])

    ax2.set_ylabel(m_ylabel[1])

    # make double legend
    lns = line1+line2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)
    ax2.yaxis.grid(which='both')

    fig.tight_layout()
    info("Writing file : %s" % m_figname)
    fig.savefig(m_figname)


# - * - * - * - * - * - * - * - * - * - * - * - * - * - *

def plotAll(datadict, m_figname='fig_Env_all.png', m_cutDate=False, m_lowDate=None, m_highDate=None):
    
    info('You are crazy...')
    
    x1= datadict['DHT22 Temperature'][0]
    y1= datadict['DHT22 Temperature'][1]

    x2= datadict['BMP085 Temperature'][0]
    y2= datadict['BMP085 Temperature'][1]
    
    x3= datadict['BMP085 Pressure'][0]
    y3= datadict['BMP085 Pressure'][1]
    
    x4= datadict['DHT22 Humidity'][0]
    y4= datadict['DHT22 Humidity'][1]
    
    if m_cutDate==True:
        sel1_ind = np.where((x1>m_lowDate) & (x1<m_highDate) )
        x1 = x1[sel1_ind]
        y1 = y1[sel1_ind]
        
        sel2_ind = np.where((x2>m_lowDate) & (x2<m_highDate) )
        x2 = x2[sel2_ind]
        y2 = y2[sel2_ind]
    
        sel3_ind = np.where((x3>m_lowDate) & (x3<m_highDate) )
        x3 = x3[sel3_ind]
        y3 = y3[sel3_ind]
        
        sel4_ind = np.where((x4>m_lowDate) & (x4<m_highDate) )
        x4 = x4[sel4_ind]
        y4 = y4[sel4_ind]


    plt.close('all')
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)

    formatter = mdates.DateFormatter('%d/%m-%H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=60)

    #minor ticks
    minorlocator = AutoMinorLocator()
    ax.xaxis.set_minor_locator(minorlocator)
    ax.yaxis.set_minor_locator(minorlocator)
    ax.yaxis.grid(which='both')
    ax.xaxis.grid(which='both')


    ax2 = ax.twinx()
    ax2.yaxis.grid(which='both', color='m')

    ax3 = ax.twinx()
    ax2.yaxis.grid(which='both', color='b')

    axes = [ax, ax2, ax3]

    fig.subplots_adjust(right=0.75)

    # Move the last y-axis spine over to the right by 20% of the width of the axes
    axes[-1].spines['right'].set_position(('axes', 1.2))
    # To make the border of the right-most axis visible, we need to turn the frame
    # on. This hides the other plots, however, so we need to turn its fill off.
    axes[-1].set_frame_on(True)
    axes[-1].patch.set_visible(False)

    line1 = ax.plot(x1, y1, 'r-', lw=2, label="DHT22 Temperature")
    line2 = ax.plot(x2, y2, 'g-', lw=2, label="BMP085 Temperature")

    ymin, ymax = ax.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis = 5.
    
    ax.set_ylim([ymin-((vary_axis/2.)*axis_ratio), ymax+(vary_axis*axis_ratio)])

    # set labels
    ax.set_ylabel(r"Temperature ($^{\circ}$C)")
    ax.set_xlabel(r"Date (d/m-H:M)")

            #         -----

    line3 = ax2.plot(x3, y3, 'm-', lw=2, label="BMP085 Pressure")

    ymin, ymax = ax2.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis=10.
    ax2.set_ylim([ymin-((vary_axis/2.)*axis_ratio), ymax+(vary_axis*axis_ratio)])

    # set labels
    ax2.set_ylabel(r"Pressure (mbar)",color='m')
    ax2.tick_params(axis='y', colors='m')

            #         -----

    line4 = ax3.plot(x4, y4, 'b-', lw=2, label="DHT22 Humidity")

    ymin, ymax = ax3.get_ylim()
    axis_ratio = (ymin/ymax)
    vary_axis=20.
    ax3.set_ylim([ymin-((vary_axis/2.)*axis_ratio), ymax+(vary_axis*axis_ratio)])

    # set labels
    ax3.set_ylabel(r"Humidity ($\%$)", color='b')
    ax3.tick_params(axis='y', colors='b', which='both')

    # make double legend
    lns = line1+line2+line3+line4
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=2)

    fig.tight_layout()
    info("Writing file : %s" % m_figname)
    fig.savefig(m_figname)



# - * - * - * - * - * - * - * - * - * - * - * - * - * - *


def makeDateTime(m_year, m_month, m_day, m_hour, m_minute, m_second, m_millisecond):
    return datetime(int(m_year), int(m_month), int(m_day), int(m_hour), int(m_minute), int(m_second), int(m_millisecond*1000))


# - * - * - * - * - * - * - * - * - * - * - * - * - * - *




