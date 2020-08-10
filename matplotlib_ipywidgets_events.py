#!jupyter-lab
# coding: utf-8
'''
For use in a jupyter-lab session:
    import matplot_widget_events as mwe
    mwe.App()
'''

## imports
get_ipython().run_line_magic('load_ext', 'Cython')
get_ipython().run_line_magic('matplotlib', 'widget')
import ipywidgets as widgets
from ipywidgets import Layout
import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event
from ipympl.backend_nbagg import Toolbar
import numpy as np
np.set_printoptions(precision=3) 

## print helper
def joinArgs(*args,**kwargs):
    string = ', '.join(['{}']*len(args)).format(*args)
    string+= ', ' if len(args)>0 else ''
    for k,v in kwargs.items():
        string+= '%s=%s, '%(k,v)
    if len(kwargs)>0:
        string=string[:-1]
    return string

def printLog(textWidget, *args, **kwargs):
    string= joinArgs(*args,**kwargs)
    print(string, end=';')
    textWidget.value= string+';\n'+textWidget.value[:500]

def getAxesSizePx(fig, ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = int(bbox.width*fig.dpi), int(bbox.height*fig.dpi)
    return width, height

## mandel fun
#get_ipython().run_cell_magic('cython', '', 'cpdef Mandelbrot(int[:,::1] Z, float xl, float xr, float yd, float yu, int Rx, int Ry, int maxIter ) : #except *:\n    cdef int y, x, n\n    cdef complex z, c\n    cdef float dx=Rx/(xr-xl)\n    cdef float dy=Ry/(yu-yd)\n    for y in range(Ry):\n        for x in range(Rx):\n            c = xl + x / dx + 1j*(yu - y / dy)\n            z = 0\n            for n in range(maxIter):\n                if z.real**2 + z.imag**2 >= 4:\n                    break\n                z = z*z + c\n            Z[y, x] = n')

## layout helper
def make_box_layout():
     return widgets.Layout(
        border='solid 1px black',
        margin='0px 0px 0px 0px',
        padding='1px 1px 1px 1px'
     )

## register new events
def register_new_events():
    '''
    ~View Code for Event
    Check for events registered at ipympl.backend_nbagg.Toolbar, not all are registered by ipympl
    Here's the complete list https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.NavigationToolbar2 
    '''    
    # 'home': 'home',
    home = Toolbar.home
    def new_home(self, *args, **kwargs):
        s = 'home_event'
        event = Event(s, self)
        event.foo = 1
        self.canvas.callbacks.process(s, event)
        home(self, *args, **kwargs)
    Toolbar.home = new_home

    # 'back': 'arrow-left',
    back = Toolbar.back
    def new_back(self, *args, **kwargs):
        s = 'back_event'
        event = Event(s, self)
        event.foo = 2
        self.canvas.callbacks.process(s, event)
        back(self, *args, **kwargs)
    Toolbar.back = new_back
    
    # 'forward': 'arrow-right',
    forward = Toolbar.forward
    def new_forward(self, *args, **kwargs):
        s = 'forward_event'
        event = Event(s, self)
        event.foo = 3
        self.canvas.callbacks.process(s, event)
        forward(self, *args, **kwargs)
    Toolbar.forward = new_forward

    # ZOOM
    #'zoom_to_rect': 'square-o',
    zoom = Toolbar.zoom
    def new_zoom(self, *args, **kwargs):
        s = 'zoom_event'
        event = Event(s, self)
        event.foo = 4
        self.canvas.callbacks.process(s, event)
        zoom(self, *args, **kwargs)
    Toolbar.zoom = new_zoom
    
    #'release_pan': 'arrows',
    release_pan = Toolbar.release_pan
    def new_release_pan(self, *args, **kwargs):
        s = 'release_pan_event'
        event = Event(s, self)
        event.foo = 5
        self.canvas.callbacks.process(s, event)
        release_pan(self, *args, **kwargs)
    Toolbar.release_pan = new_release_pan
    
    #'release_zoom': 'floppy-o',
    release_zoom = Toolbar.release_zoom
    def new_release_zoom(self, *args, **kwargs):
        s = 'release_zoom_event'
        event = Event(s, self)
        event.foo = 6
        self.canvas.callbacks.process(s, event)
        release_zoom(self, *args, **kwargs)
    Toolbar.release_zoom = new_release_zoom

    # listed but not working
    #'export': 'file-picture-o'
    #export = Toolbar.export
    #def new_export(self, *args, **kwargs):
    #    s = 'export_event'
    #    event = Event(s, self)
    #    event.foo = 7
    #    self.canvas.callbacks.process(s, event)
    #    export(self, *args, **kwargs)
    #Toolbar.export = new_export
    
    return Toolbar

## App
class App1(widgets.HBox):

    register_new_events()

    ## Event Handlers
    def handle_home(self, change):
        ''' home to default '''
        logginHere='home '
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    def handle_back(self,evt):
        ''' back to default '''
        logginHere='back '
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    def handle_forward(self,evt):
        ''' forward to default '''
        logginHere='forward '
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    def handle_release_zoom(self,evt):
        ''' release_zoom '''
        x='(%.3f,%.3f)'%self.ax.get_xlim()
        y='(%.3f,%.3f)'%self.ax.get_ylim()
        logginHere='release_zoom %s %s'%( x, y)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]    
        
    def handle_release_pan(self,evt):
        ''' release_pan '''
        x='(%.3f,%.3f)'%self.ax.get_xlim()
        y='(%.3f,%.3f)'%self.ax.get_ylim()
        logginHere='release_pan %s %s'%( x, y)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]   
        
    def handle_draw(self,evt):
        ''' draw '''
        x='(%.3f,%.3f)'%self.ax.get_xlim()
        y='(%.3f,%.3f)'%self.ax.get_ylim()
        logginHere='handle_draw %s %s'%( x, y)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]   
        
    def onclick(self, event):
        ''' onbutton '''
        logginHere='onclick %s %s %d %d %.3f %.3f'%(event.button, event.name, event.x, event.y, event.xdata, event.ydata)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500] 
    
    #def handle_export(self,evt):
    #    ''' export '''
    #    logginHere='export %s'%time.time()
    #    print(logginHere, end=', ')
    #    self.textArea.value=logginHere+',\n'+self.textArea.value[:500]   

    def update(self, change):
        """Draw line in plot"""
        logginHere='update slider %s->%s'%(change.old,change.new)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
        # changing the frequency here!
        self.line.set_ydata(np.sin(change.new * self.x))
        self.fig.canvas.draw()
        
    def button_reset_pressed(self, change):
        ''' slider to default '''
        logginHere='reset button %s->%s'%(self.intSlider.value,self.initial_freak)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'#+self.textArea.value[:500]
        self.intSlider.value=self.initial_freak
        self.line.set_ydata(np.sin(self.initial_freak * self.x))

    def init_plot(self):
        self.output = widgets.Output()
        with self.output:
            self.fig, self.ax = plt.subplots()
        self.initial_color = '#FF00DD'
        self.initial_freak = 2
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.line, = self.ax.plot(self.x, np.sin(self.x), self.initial_color)
        self.fig.canvas.toolbar_position = 'left'
        self.ax.grid(True)
        plt.text(0.35, 0.5, 'Hello plt.text!', dict(size=30))

    def create_widgets(self):
        self.intSlider = widgets.IntSlider( value=self.initial_freak, min=0, max=10, step=1, description='Wave freq.')
        self.resetButton = widgets.Button( description='Reset values!')
        self.titleText = widgets.Label( value='Hello Title!', layout=Layout( align_self='center') )
        self.textArea = widgets.Textarea(   placeholder='Hello TextArea! \n kinda loggin console', disabled=False,
                                            layout=Layout( height='400px') ) 
    def layout_widgets(self):
        controls = widgets.VBox([ self.titleText, self.intSlider, self.resetButton, self.textArea]) #, layout=Layout( width='100%')
        controls.layout = make_box_layout()
        out_box = widgets.Box([self.output],layout=Layout( width='100%'))
        out_box.layout = make_box_layout()
        return [controls, out_box]
        
    def plug(self):
        # observe
        self.intSlider.observe(self.update, 'value')
        self.resetButton.on_click(self.button_reset_pressed)
        # mplconnect
        self.fig.canvas.mpl_connect('home_event', self.handle_home)
        self.fig.canvas.mpl_connect('back_event', self.handle_back)
        self.fig.canvas.mpl_connect('forward_event', self.handle_forward)
        self.fig.canvas.mpl_connect('release_zoom_event', self.handle_release_zoom)
        self.fig.canvas.mpl_connect('release_pan_event', self.handle_release_pan)
        self.fig.canvas.mpl_connect('draw_event', self.handle_draw)
        #self.fig.canvas.mpl_connect('export_event', self.handle_export)      
        self.fig.canvas.mpl_connect('button_press_event'  , self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onclick)
        # this connects & prints to log console, idk y
        #self.fig.canvas.mpl_connect('pick_event', lambda f: None)

    ## Init
    def __init__(self):
        super().__init__()

        ## Init the figure
        self.init_plot()

        ## Create widgets
        self.create_widgets()

        ## Plug widgets & events
        self.plug()
        
        ## 'return a list to plug into an Horizontal Box' ~ add to children inheritance
        self.children = self.layout_widgets()

    def destroyFigure(self):
        self.fig.clf()
    
            
## App
class App2(widgets.HBox):

    register_new_events()

    def handle_home(self,event):
        ''' home to default '''
        self.intSlider.value = self.A
        self.intSlider2.value = self.B
        logginHere='home reset!'
        print(logginHere, end=', ')
        self.textArea.value=logginHere
        
    def on_pick(self, event):
        line = event.artist 
        xdata, ydata = line.get_data() 
        ind = event.ind 
        logginHere='on pick point: (%f, %f)'%(xdata[ind], ydata[ind])
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]

    def handle_slider(self, change):
        self.ax.cla()
        a=self.intSlider.value
        b=self.intSlider2.value
        self.ax.plot(np.random.random([a,b]), 'o', picker=5) # 5 points tolerance
        logginHere='slider %s->%s'%(change.old, change.new)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]

    def plug(self):
        # observe
        self.intSlider.observe(self.handle_slider, 'value')
        self.intSlider2.observe(self.handle_slider, 'value')
        # mplconnect
        self.fig.canvas.mpl_connect('home_event', self.handle_home)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)

    def create_widgets(self):
        self.intSlider = widgets.IntSlider( value=100, min=1, max=150, step=5, description='~Points')
        self.intSlider2 = widgets.IntSlider( value=2, min=1, max=100, step=1, description='Series')
        self.titleText = widgets.Label( value='El título es', layout=Layout( align_self='center') )
        self.textArea = widgets.Textarea(  placeholder='Hello world!...',  disabled=False )
        
    def init_plot(self):
        self.output = widgets.Output()
        with self.output:
            self.fig, self.ax = plt.subplots()
        self.A, self.B = 100,2
        self.ax.plot(np.random.random([self.A, self.B]), 'o', picker=5) # 5 points tolerance
        self.fig.canvas.toolbar_position = 'left'
        self.ax.grid(True)

    def layout_widgets(self):
        controls = widgets.VBox([ self.titleText, self.intSlider, self.intSlider2, self.textArea])
        controls.layout = make_box_layout()
        out_box = widgets.Box([self.output],layout=Layout( width='100%'))
        out_box.layout = make_box_layout()
        self.children = [controls, out_box]

    def __init__(self):
        super().__init__()

        ## Init the figure
        self.init_plot()

        ## Create widgets
        self.create_widgets()

        ## Plug widgets & events
        self.plug()
        
        ## 'return a list to plug into an Horizontal Box' ~ add to children inheritance
        self.layout_widgets()

    def destroyFigure(self):
        self.fig.clf()

## App
class AppMandelbrot(widgets.HBox):

    register_new_events()

    # Event Handlers
    def handle_home(self, event):
        ''' home to default '''
        printLog(self.textArea,'casa',event.name)
        #logginHere='home %s'%event.name
        #print(logginHere, end=', ')
        #self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    #def handle_back(self,event):
    #    ''' back to default '''
    #    logginHere='back '
    #    print(logginHere, end=', ')
    #    self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    #def handle_forward(self,event):
    #    ''' forward to default '''
    #    logginHere='forward '
    #    print(logginHere, end=', ')
    #    self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
    
    def handle_release_zoom(self,event):
        ''' release_zoom '''
        x='(%.3f,%.3f)'%self.ax.get_xlim()
        y='(%.3f,%.3f)'%self.ax.get_ylim()
        logginHere='%s %s %s'%(event.name, x, y)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]    
        self.releaseZoomPendingReDraw = True
        
    #def handle_release_pan(self,event):
    #    ''' release_pan '''
    #    x='(%.3f,%.3f)'%self.ax.get_xlim()
    #    y='(%.3f,%.3f)'%self.ax.get_ylim()
    #    logginHere='release_pan %s %s'%( x, y)
    #    print(logginHere, end=', ')
    #    self.textArea.value=logginHere+',\n'+self.textArea.value[:500]   
        
    def handle_draw(self,event):
        ''' Draw event, AutoZoom '''
        if self.releaseZoomPendingReDraw and self.bpx != None and self.bpy!=None and self.brx!=None and self.bry!=None:
            # check box boundaries logic
            if self.bpx>self.brx:
                self.xl, self.xr = self.brx, self.bpx
            else:
                self.xl, self.xr = self.bpx, self.brx
            if self.bpy>self.bry:
                self.yd, self.yu = self.bry, self.bpy
            else:
                self.yd, self.yu = self.bpy, self.bry
            # update pickers value & bounds
            self.xrange_picker.unobserve_all()
            self.yrange_picker.unobserve_all()
            self.xrange_picker.value=(self.xl,self.xr)
            self.yrange_picker.value=(self.yd,self.yu)
            xdif=abs(self.xr-self.xl)
            ydif=abs(self.yu-self.yd)
            self.xrange_picker.step=xdif/20
            self.yrange_picker.step=ydif/20
            self.xrange_picker.min=max(self.xl-xdif, self.init_xl)
            self.xrange_picker.max=min(self.xr+xdif, self.init_xr)
            self.yrange_picker.min=max(self.yd-ydif, self.init_yd)
            self.yrange_picker.max=min(self.yu+ydif, self.init_yu)
            self.xrange_picker.observe(self.update, 'value')
            self.yrange_picker.observe(self.update, 'value')
            # redraw
            self.title_Text.value = self.redraw()
            # finish
            self.releaseZoomPendingReDraw = False
            printLog(self.textArea,'AutoZoomRedraw',event.name, self.xl, self.xr, self.yd, self.yu)
        else:
            printLog(self.textArea,'Handle Draw Event',event.name)
        
    def onclick(self, event):
        ''' Event on button click: Check if it's release or press and store them on object variables '''
        if event.name=='button_release_event':
            self.brx, self.bry = event.xdata, event.ydata
        if event.name=='button_press_event':
            self.bpx, self.bpy = event.xdata, event.ydata
        printLog(self.textArea, 'onclick', event.button, event.name, event.x, event.y, event.xdata, event.ydata)
    
    def update(self, change):
        self.xl, self.xr = self.xrange_picker.value
        self.yd, self.yu = self.yrange_picker.value
        self.Rx, self.Ry = self.Rx_picker.value, self.Ry_picker.value
        self.maxIter= self.maxIter_picker.value
        self.title_Text.value = self.redraw()

        logginHere='update %s value %s->%s'%(change.name,change.old,change.new)
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'+self.textArea.value[:500]
        
    def button_reset_clicked(self, change):
        ''' slider to default '''
        logginHere='reset button!'
        print(logginHere, end=', ')
        self.textArea.value=logginHere+',\n'#+self.textArea.value[:500]

    def init_plot(self):
        self.output = widgets.Output()
        with self.output:
            self.fig, self.ax = plt.subplots(figsize=(8,8))
        #ax = fig.add_subplot(111)
        self.fig.canvas.toolbar_position = 'right'
        self.fig.canvas.header_visible = False
        self.fig.canvas.capture_scroll = False
        self.fig.canvas.footer_visible = False
        self.ax.grid(False)
        self.ax.set_xlabel('Real numbers')
        self.ax.set_ylabel('Imaginary numbers')
        plt.tight_layout()
        self.title_Text.value = self.redraw()

    def redraw(self):
        with self.output:
            Z=np.zeros((self.Ry,self.Rx), dtype=np.int32)
            Mandelbrot(Z, self.xl, self.xr, self.yd, self.yu, self.Rx, self.Ry, self.maxIter)
            xoffset= (self.xr-self.xl)/(2*self.Rx)
            yoffset= (self.yu-self.yd)/(2*self.Ry)
            # CLEAR AXES
            #self.ax.cla()
            im = self.ax.imshow(Z, interpolation='none', aspect='equal',
                           origin='upper',
                           extent=[self.xl+xoffset, self.xr+xoffset, self.yd+yoffset, self.yu+yoffset] )
                            # check https://matplotlib.org/3.2.1/tutorials/intermediate/imshow_extent.html#
            self.ax.set_xlabel('Real numbers')
            self.ax.set_ylabel('Imaginary numbers')
            return "MandelPlot "+"{:,}".format(Z.shape[0]*Z.shape[1])+" pixels calculated"

    def handle_resize(self, event):
        if self.ResizeSetsGrid.value:
            w,h=getAxesSizePx(self.fig, self.ax)
            self.Rx_picker.unobserve_all()
            self.Ry_picker.unobserve_all()
            self.Rx_picker.value=w
            self.Ry_picker.value=h
            self.xrange_picker.observe(self.update, 'value')
            self.yrange_picker.observe(self.update, 'value')
            printLog(self.textArea,'Handled', event.name, w=w, h=h, fig_height=event.height, fig_width=event.width)
        else:
            printLog(self.textArea,'Handled', event.name, 'setting disabled!')

    def create_widgets(self):
        self.xrange_picker = widgets.FloatRangeSlider(value=(self.init_xl,self.init_xr), min=-2.0, max=2.0, step=0.001, readout_format='.4f', #, description='real' 
                                                      continuous_update=False, orientation='horizontal') #, layout=Layout( width='110%')
                                                      #continuous_update=False, orientation='vertical', layout=Layout( height='90%', width='110%'))
        self.yrange_picker = widgets.FloatRangeSlider(value=(self.init_yd,self.init_yu), min=-1.8, max=1.8, step=0.001, readout_format='.4f', #, description='imaginary' 
                                                      continuous_update=False, orientation='horizontal') #, layout=Layout( width='110%')
                                                      #continuous_update=False, orientation='vertical', layout=Layout( height='90%', width='110%'))
        self.Rx_picker = widgets.IntText(value=self.init_Rx, min=2, max=10002, step=50, description='Real     ', continuous_update=False, layout=Layout( width='80%', align_self='flex-end'))
        self.Ry_picker = widgets.IntText(value=self.init_Ry, min=2, max=10002, step=50, description='Imaginary', continuous_update=False, layout=Layout( width='80%', align_self='flex-end'))
        self.maxIter_picker = widgets.IntText(value=self.init_maxIter, min=1, max=1000, step=50, description='Max. Iterations', continuous_update=False, layout=Layout( width='80%', align_self='flex-end'))
        self.reset_button = widgets.Button(description='Reset values!', continuous_update=False)
        self.title_Text = widgets.Label("MandelPlot ",layout=Layout( align_self='center' ))
        self.textArea = widgets.Textarea(   placeholder='Hello TextArea! \n kinda loggin console', disabled=False,
                                            layout=Layout( height='300px') ) #width='100%', 
        self.RL = widgets.Label("Real axis adjustment")
        self.IL = widgets.Label("Imaginary axis adjustment")
        self.GL = widgets.Label("Grid precision", layout=Layout( width='30%'))
        self.ResizeSetsGrid = widgets.Checkbox( value=True, description='Resize updates grid', disabled=False , layout=Layout(margin='0px 0px 0px 1px',width='80%'))

    def layout_widgets(self):
        controls = widgets.VBox([ self.title_Text, 
                                    self.RL, self.xrange_picker, 
                                    self.IL, self.yrange_picker,
                                    widgets.HBox([self.GL, self.ResizeSetsGrid]),
                                    self.Rx_picker, self.Ry_picker, self.maxIter_picker,
                                    self.textArea,
                                    self.reset_button ])
        controls.layout = make_box_layout()
        out_box = widgets.Box([self.output],layout=Layout( width='100%'))
        out_box.layout = make_box_layout()
        self.children = [out_box, controls]
        
    def plug(self):
        # observe
        self.xrange_picker.observe(self.update, 'value')
        self.yrange_picker.observe(self.update, 'value')
        self.Rx_picker.observe(self.update, 'value')
        self.Ry_picker.observe(self.update, 'value')
        self.maxIter_picker.observe(self.update, 'value')
        self.reset_button.on_click(self.button_reset_clicked)
        # mplconnect
        self.fig.canvas.mpl_connect('home_event', self.handle_home)
        #self.fig.canvas.mpl_connect('back_event', self.handle_back)
        #self.fig.canvas.mpl_connect('forward_event', self.handle_forward)
        self.fig.canvas.mpl_connect('release_zoom_event', self.handle_release_zoom)
        #self.fig.canvas.mpl_connect('release_pan_event', self.handle_release_pan)
        self.fig.canvas.mpl_connect('draw_event', self.handle_draw)
        #self.fig.canvas.mpl_connect('export_event', self.handle_export)      
        self.fig.canvas.mpl_connect('button_press_event'  , self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onclick)
        # this connects & prints to log console, idk y
        #self.fig.canvas.mpl_connect('pick_event', lambda f: None)
        self.fig.canvas.mpl_connect('resize_event', self.handle_resize)

    ## Init
    def __init__(self):
        super().__init__()

        # intial data
        self.init_xl, self.init_xr = -2.0, 0.66
        self.init_yd, self.init_yu = -1.4, 1.4
        self.init_Rx, self.init_Ry = 502, 502
        self.init_maxIter = 200

        self.xl, self.xr = self.init_xl, self.init_xr
        self.yd, self.yu = self.init_yd, self.init_yu
        self.Rx, self.Ry = self.init_Rx, self.init_Ry
        self.maxIter = self.init_maxIter

        self.bpx, self.bpy = None, None
        self.brx, self.bry = None, None
        self.releaseZoomPendingReDraw = False

        ## Create widgets
        self.create_widgets()

        ## Init the figure
        self.init_plot()

        ## Plug widgets & events
        self.plug()
        
        ## 'return a list to plug into an Horizontal Box' ~ add to children inheritance
        self.layout_widgets()

    def destroyFigure(self):
        self.fig.clf()

#evt=Event('home')
#def handlers(change):
#    if evt=='home':
#        print(change)
#Toolbar.observe(evt, handlers(evt))
#
# TODO
# mandelbrot auto zoom:
#   event: on click mouse pressed
#        get event.xdata, event.ydata
#   event: on on click mouse released 
#        get event.xdata, event.ydata
#   event: release_zoom 
#        calculate mandelbrot set
#        redraw
#
