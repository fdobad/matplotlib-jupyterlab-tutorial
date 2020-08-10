---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
# this is for using jupytext, just ignore it
%autosave 0 
```

Matplotlib tutorial topics:  

    - Pyplot [Exploring_pyplot](Exploring_pyplot.ipynb)  
    - Manipulate plot  
    
        - widgets  
        - mpl_interactions  
        
    - Backends [Tk, Widgets, qt5]  
    - Events  
    - Animations  
    - Transformations  
    - Paths, contours, collections  
    - Mandelbrot example


# Pyplot : The basics
Mainly for interactive plotting so choose an interactive backend like widget, qt5 or tk
Typical steps:
1. Choose backend
2. Create a figure and the plot area (or axes)
3. Each Axes can have several axis or plotted objects

Keep learning pyplot options here [Exploring_pyplot](Exploring_pyplot.ipynb):

```python
%matplotlib tk
import matplotlib.pyplot as plt
```

```python
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=3)
ax1.plot([1,2],[3,5], 'g--.')
ax1.plot([2,3],[3,5], 'y-')
```

```python
ax2.scatter([1,2],[3,5])
ax2.set_xlim(0,4)
ax2.set_ylim(2,6)
```

```python
import numpy as np
rg = np.random.default_rng([69,420]) # execute next to the random generator to get the same results
nrows, ncols, rgba = 5, 4, 4         # (M, N, 4): an image with RGBA
rgba_image = rg.integers(1,256,size=(nrows, ncols, rgba))
ax3.imshow(rgb_image)
```

```python
fig.canvas.toolbar_visible = False
fig.canvas.header_visible = False
fig.canvas.footer_visible = False
fig.canvas.resizable = False
fig.canvas.capture_scroll = True
```

```python
# Force close
ax2.cla() # clear this axis
fig.cla() # clear all axes 
fig.clf() # clear figure
plt.close() # close all
```

# Manipulate plot


## ipywidgets

```python
# When using the `widget` backend from ipympl,
# fig.canvas is a proper Jupyter interactive widget, which can be embedded in
# an ipywidgets layout. See https://ipywidgets.readthedocs.io/en/stable/examples/Layout%20Templates.html

# One can bound figure attributes to other widget values.
%matplotlib widget
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import AppLayout, FloatSlider
```

```python
#plt.close()
plt.ioff() # ipykernel plots it by default, avoid it because we're embedding
slider = FloatSlider(
    orientation='horizontal',
    description='Factor:',
    value=1.0,
    min=0.02,
    max=2.0
)

slider.layout.margin = '0px 30% 0px 30%'
slider.layout.width = '40%'

fig = plt.figure()
fig.canvas.header_visible = False
fig.canvas.layout.min_height = '400px'
plt.title('Plotting: y=sin({} * x)'.format(slider.value))

x = np.linspace(0, 20, 500)

lines = plt.plot(x, np.sin(slider.value * x))

def update_lines(change):
    plt.title('Plotting: y=sin({} * x)'.format(change.new))
    lines[0].set_data(x, np.sin(change.new * x))
    fig.canvas.draw()
    fig.canvas.flush_events()

slider.observe(update_lines, names='value')

AppLayout(
    center=fig.canvas,
    footer=slider,
    pane_heights=[0, 6, 1]
)
```

# Manipulate plot
Like the Mathematica interface, but simpler!  

Canned interaction with mpl_interactions, great for 2D ploting and heatmap, exploring.  

See [mpl_interactions.ipynb](mpl_interactions.ipynb)

For the widgets backend, from https://github.com/ianhi/mpl-interactions/


# Backends
The first interactive command should be the backend choosing, because not all of them are interchangeable without restarting the kernel.  
List them:  

```python
%matplotlib -l
```

There are native widgets on matplotlib.widgets; so backend mainly connect to them and their events.  

| backend | features |
| --- | --- |
| __widget__ | Interaction wrappers for jupyter-widgets, sliders, textboxes, layouts... |
|   | Built on top of ipympl & nbagg |
| __tk__ | Python default, faster |
| __qt5__ | Multiplatform ? |
| __osx__ | pending ... |

## Hacking a toolbar

```python
%matplotlib widget
import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event
from ipympl.backend_nbagg import Toolbar

home = Toolbar.home

def new_home(self, *args, **kwargs):
    s = 'home_event'
    event = Event(s, self)
    event.foo = 420
    self.canvas.callbacks.process(s, event)
    home(self, *args, **kwargs)

Toolbar.home = new_home

fig, ax = plt.subplots(1, 1)
t=ax.text(x=0.6,y=0.9,s='place holder')

def handle_home(change):
    ''' home to default '''
    print('hello foo ', change.foo, end=', ')
    t.set_text('hello foo %s'%change.foo)
    fig.canvas.flush_events()

#connectionId = fig.canvas.mpl_connect('home_event',handle_home)
fig.canvas.mpl_connect('home_event',handle_home)
```

```python
# keep the connection id on class o non-interactive
fig.canvas.mpl_disconnect(connectionId)
```

```python
# Force redraw depending on the backend are needed
fig.canvas.flush_events()
fig.canvas.draw()
plt.show()
```

# Events


# References  
https://matplotlib.org/3.1.1/api/index.html  
https://github.com/matplotlib/jupyter-matplotlib  

## Thanks to  
https://github.com/ianhi/mpl-interactions/  

https://github.com/rougier/matplotlib-tutorial

```python

```
