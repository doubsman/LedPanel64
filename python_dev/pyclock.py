# analogclock: an analog clock for the python clock application
# 02-Feb-16: Robin Verdier, for the Belmont programming courses
# This version switches between arrow and arc hands, and creates a postscript file.
# Status: May not run on python 2.3.5
# 27-Sep-16: Robin Verdier, for the Belmont programming courses

import sys # for Python version
pv3 = sys.version_info[0] > 2 # True for Python version 3, else 2
if pv3:
  import tkinter as tk
  from tkinter import ttk # for the Combobox
  import tkinter.messagebox as messagebox
else:
  import Tkinter as tk
  import ttk
  import tkMessageBox as messagebox
root = tk.Tk()
import math, os, time
from threading import Timer, currentThread

root.title("Analog Clock")

# sizes (sizewh may change on resize event):
sizewh = [400, 400] # canvas size, width and height, pixels
border = 30
framewidth = 20
bpf = border + framewidth
center = (0.5 * sizewh[0], 0.5 * sizewh[1])

# variables
arcdims = []
archands = 2
arrowdims = []
arrowhands = 1
nohands = 0
clocktype = arrowhands
debugprints = 0
digitalhands = 0
face = (bpf, bpf, sizewh[0] - bpf, sizewh[1] - bpf)
frame = (border, border, sizewh[0]-border, sizewh[1]-border)
handnames = ('Arrow hands', 'Arc hands  ')
handtype = arrowhands
holdsecs = 1.0 # seconds between time displays
init = True
now = ()

canvas = tk.Canvas(root, width=sizewh[0], height=sizewh[1], borderwidth=0,
  highlightthickness=0, bg='black')

def cmp(a, b):
    return (a > b) - (a < b)

def changehandtype(event):
  # Switch the handtype between arrow and arc
  global handtype
  typebutton.configure(text = handnames[handtype-1])
  handtype = 3 - handtype

def drawface(canvas, sizewh=[], border=30, framewidth=20, colors=('brown', 'white')):
  # Draw the clock frame and face
  frame = (border, border, sizewh[0]-border, sizewh[1]-border)
  framewidth = 20
  bpf = border + framewidth
  face = (bpf, bpf, sizewh[0] - bpf, sizewh[1] - bpf)
  canvas.create_oval (frame, fill = 'brown')
  canvas.create_oval (face, fill = 'white')
  return

def drawhands (canvas, handtype=1, hand=0, dims=[], refl=0, color='red'):
  # Draw a hand at the current local hour, minute, and second in 12-hour format set by timeinfo
  hour12, minute, second = now[0], now[1], now[2]
  minute = minute + second / 60.
  hour12 = hour12 + minute / 60.
  circ = 2 * math.pi
  div = (12. / circ, 60. / circ, 60. / circ)
  angles = (hour12 / div[0], minute / div[1], second / div[2])
  angle = math.pi - angles[hand]
  center = [0.5 * sizewh[0], 0.5 * sizewh[1]]
  #print 'draw hands, type', handtype, ', angle=', angle*180./math.pi, ', ', len(dims), 'dims'
  global debugprints
  if debugprints > 100: # *
    print('hand, refl. angle, dims =', hand, refl, angle, dims)
    debugprints -= 1
  # Rotate, scale, and translate the model dimensions
  d = border + framewidth
  xmax, ymax = 0.5 * sizewh[0] - d, 0.5 * sizewh[1] - d
  if handtype == arrowhands:
    anglesc = (math.sin(angle), math.cos(angle))
    scaleref = ((2 * refl - 1.) * xmax, ymax)
    handcolors = (('gold','yellow'), ('blue', 'cyan'), ('red', 'maroon'))
    # The seconds arrow hand has the largest radius and so must be drawn last.
    drawrotatedandscaledshape (canvas, type='arrow', 
      design=handdims(handtype=handtype, hand=hand),
      scale=scaleref, anglesc=anglesc, center=center, color=handcolors[hand][refl])
  if handtype == archands:
    handcolors = ('red', 'blue', 'gold')
    col = (handcolors[hand], 'white')[refl]
    # The seconds arc hand has the largest radius and so must be drawn first.
    drawrotatedandscaledshape (canvas, type='arc',
      design=handdims(handtype=handtype, hand=hand)[refl],
      scale=(xmax, -ymax), anglesc=[angles[2-hand] * 180. / math.pi, 0],
      center=center, color=col)

def drawnumerals(canvas, center=[100., 100.], scale=[100., 100.], color='gold'):
  # Draw 12 numerals around the clock face
  numerals = 12
  scale = 0.5 * (sizewh[0] - border), 0.5 * (sizewh[1] - border)
  fontsize = int(min(scale[0], scale[1]) / 8.) #radius / 8)
  x, y = 0, -1
  xn, yn = x, y
  delang = -2. * math.pi / numerals
  sind, cosd = math.sin(delang), math.cos(delang)
  for n in range(numerals):
    nshow = n
    if n == 0: nshow = 12
    xn, yn = x * scale[0] + center[0], y * scale[1] + center[1]
    canvas.create_text(xn, yn, text=str(nshow), fill=color,
      font=('Lucida Handwriting', fontsize, 'bold'))
    xn, yn = x, y
    x, y = xn * cosd + yn * sind, yn * cosd - xn * sind

def drawrotatedandscaledshape (canvas, type='poly', design=[], anglesc=[0., 1.],
  scale=(100., 100.), center=[100,100], color='red'):
  # Rotate x and y through arcsin anglesc[0], scale x for eccentricity, and add offsets
  # print 'drss dims=', design
  # tag 'hand' marks the hand to be deleted each tick
  points = []
  #print 'design=', design
  if type == 'arrow':
    sind, cosd = anglesc[0], anglesc[1]
    # Reflect about the y axis if the x-scale is negative
    reflectx = cmp(scale[0], 0)
    for c in range(len(design)):
      x, y = reflectx * design[c][0], design[c][1]
      # rotate the model
      xr, yr = x * cosd + y * sind, y * cosd - x * sind
      # Scale and translate the points
      points.append(abs(scale[0]) * xr + center[0])
      points.append(scale[1] * yr + center[1])
    canvas.create_polygon(points, fill = color, tag = 'hand')
  if type == 'arc':
    for c in range(len(design)):
      xy = c % 2
      points.append(design[c]*scale[xy] + center[xy])
    # Note angles in Tk are positive ANTI-clockwise
    canvas.create_arc(points, start=90., extent = -anglesc[0], 
      fill = color, outline = color, tag = 'hand')
  if type == 'tick':
    sind, cosd = anglesc[0], anglesc[1]
    for c in range(len(design)):
      x, y = design[c][0], design[c][1]
      # rotate the model
      xr, yr = x * cosd + y * sind, y * cosd - x * sind
      points.append(xr * scale[0] + center[0])
      points.append(yr * scale[1] + center[1])
    canvas.create_polygon(points, fill = color, tag = 'tick')
  return points

def drawticks(canvas, center=[100., 100.], radius=0.8*center[0], color='white'):
  # Draw tick marks around the frame as a set of polygons
  d = border #  + 0.5 * framewidth
  xmax, ymax = 0.5 * sizewh[0] - d, 0.5 * sizewh[1] - d
  nticks = 60
  radius = ymax
  f = xmax / ymax
  # Set dims = dimensions of tick 0 for a circle of radius ymax
  #  length, width = 0.08 * radius, 0.5 * radius * math.pi / nticks
  length, width = 0.08, 0.5 * radius * math.pi / nticks
  # nb: length should scale with phi and eccentricity
  dims = [[[-0.01, -0.92],
           [ 0.01, -0.92],     
           [ 0.01,  -1.0],     
           [-0.01,  -1.0]],
          [[-0.01, -0.92],
           [ 0.01, -0.92],     
           [ 0.01,  -1.0],     
           [-0.01,  -1.0]] \
         ]
  delang = 2. * math.pi / nticks # angle between ticks
  sind, cosd = math.sin(delang), math.cos(delang)
  sinphi, cosphi = 0., 1. # initial angle phi = 0 at x = 0, y = ymax
  for tick in range(nticks):
    idim = 0
    tickcolor = 'red'
    if tick % 5 == 0: tickcolor = 'white'
    if tick % 5 == 0: idim = 1-1 # future change to make 5-minute ticks larger
    drawrotatedandscaledshape (canvas, type='tick', design=dims[idim],
      anglesc=[sinphi, cosphi], scale=(xmax, ymax),
      center = [0.5 * sizewh[0], 0.5 * sizewh[1]], color=tickcolor)
    # Rotate to angle phi + delang
    s, c = sinphi, cosphi
    sinphi, cosphi = s * cosd + c * sind, c * cosd - s * sind
  return dims

def drawtime(now = ' ', label = []):
  # Draw the digital time
  label.config (text = now[3])

def handdims(handtype = arrowhands, hand = 0):
  # Returns model dimensions for arrow hand or arc hand
  # Any other type returns an empty list.
  dims = []
  global arcdims, arrowdims
  if handtype == arrowhands:
    # model dimensions for arrow hands:
    # An arow hand has 10 dimensions: 5 half-widths xi, 5 lengths yi:
    # x0 x1     x2             x3    x4
    # ========= O =====================
    # y0 y1     y2             y3    y4
    # e.g., y3 for the minute hand is handdims[1][3][1]
    #    x0    y0     x1     y1      x2    y2     x3    y3      x4   y4 
    if arrowdims == []:
      arrowdims = \
      [[[0.0, -0.1], [0.06, -0.09], [0.10, 0.0], [0.08, 0.72], [0.0, 0.82]], # hour
       [[0.0, -0.1], [0.05, -0.09], [0.07, 0.0], [0.07, 0.80], [0.0, 0.90]], # minute
       [[0.0, -0.1], [0.04, -0.09], [0.05, 0.0], [0.03, 0.90], [0.0, 0.98]]  # second
      ]
    dims = arrowdims[hand]
  if handtype == archands:
    # model dimensions for arc hands:
    # An arc hand has 8 dims: x0, y0, x1, y1 defining the bounding box for the outer 
    # ellipse, then the same for the inner ellipse, for second, minute, and hour hands
    if arcdims == []:
      arcdims = \
      [[[-1.00, -1.00, 1.00, 1.00], [-0.92, -0.92, 0.92, 0.92]], # second
       [[-0.90, -0.90, 0.90, 0.90], [-0.82, -0.82, 0.82, 0.82]], # minute
       [[-0.80, -0.80, 0.80, 0.80], [-0.72, -0.72, 0.72, 0.72]]  # hour
      ]
    dims = arcdims[hand]
  return dims

def ondismiss():
  # Shut down immediately
  os._exit(0)

def onresize(event):
  # Event handler for user window resizing resets the size to current value
  # NB: the event size information is not useful, so we use the current canvas size
  global sizewh, init 
  # Reset the canvas dimensions to fill the window
  sizewh = [canvas.winfo_width(), canvas.winfo_height()]
  init = True

def processevent(canvas):
  # Create and draw clock
  global now
  # Get the current local time
  now = timeinfo() # hour, minute, second, ascii
  #print 'now=', now[3]
  # Draw it for the digital clock
  drawtime(now, digitaltimelabel)
  global init, frame, framewidth, ww, face, center
  if init:
    canvas.delete('all')
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill='black') 
    center = (0.5 * sizewh[0], 0.5 * sizewh[1])
    # Draw the clock face and frame
    drawface(canvas, sizewh=sizewh, border=30, framewidth=20, colors=('brown', 'white'))
    # Draw tick marks
    r = max(sizewh) / 2 - 0.5 * border
    drawticks(canvas, center, radius=r)
    # Draw the numerals
    scale = center[0] - 0.5 * border, center[1] - 0.5 * border
    drawnumerals(canvas, center, scale=scale)
    init = False
  # delete and redraw hands
  canvas.delete('hand')
  # handtype = clocktype
  handcolors = (['gold', 'yellow'], ['cyan', 'green'], ['red', 'maroon'])
  for hand in range(3):
    for refl in range(2):
      if handtype == archands: dims=handdims(handtype=handtype, hand=hand)[refl]
      else: dims=handdims(handtype=handtype, hand=hand)
      drawhands(canvas, handtype=handtype, hand=hand, dims=dims, refl=refl,
        color=handcolors[hand][refl])
      global debugprints
      if debugprints > 100: # *
        print('hand, refl. dims =', hand, refl, dims)
        debugprints -= 1

def run():
  # Process event, wait holdsecs seconds, then start a new timer
  processevent(canvas)
  global timer
  timer.cancel()
  timer = Timer (holdsecs, run)
  timer.start()

def saveclicked(event):
  # Event handler for save button clicked
  file = writepostscript()
  tkMessageBox.showinfo('Note', 'Created Postscript file ' + file + '.')  
  run()

def timeinfo():
  # Returns a Tuple with 4 elements: the current local hour (in 12-hour format),
  # minute, and second, and the date and time as formatted text
  lt = time.localtime()
  hour, minute, second = lt[3], lt[4], lt[5]
  year, month, day = lt[0], lt[1], lt[2]
  hour12 = hour % 12
  if hour12 == 0: hour12 = 12
  ampm = (' AM', ' PM')[int(hour/12)]
  mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec')
  sec2d = str(second)
  if second <= 9: sec2d = '0' + sec2d
  nowtext = str(hour12) + ':' + str(minute) + ':' + sec2d + ampm
  date = mons[month-1] + str(day) + ', ' + str(year)
  # The following works only if str.format is available, Python version > 2.3.5
  # nowtext = '{0:d}:{1:02d}:{2:02d}'.format(hour12, minute, second) + ampm
  # date = '{0:s} {1:d}, {2:d}'.format(mons[month-1], day, year)
  nowtext = date + ' ' + nowtext
  return (hour12, minute, second, nowtext)

def writepostscript():
  # Create a postscript file with name including the time
  lt = time.localtime()
  hour, minute, second = lt[3], lt[4], lt[5]
  sec2d = str(second)
  if second <= 9: sec2d = '0' + sec2d
  nowtext = str(hour)+'.'+str(minute)+'.'+sec2d
  postscriptfile = 'clock@'+nowtext+'.ps'
  canvas.postscript(file=postscriptfile, colormode='color')
  return postscriptfile

# Create the timer
timer = Timer (holdsecs, run) # must be placed after run is defined

# Create the buttons and digital time label
digitaltimelabel = tk.Label(root, width = 22, height = 1, bg = 'light blue')
savebutton = tk.Button(root, text='Save as postscript file') 
typebutton = tk.Button(root, text=handnames[2-handtype])
typebutton.bind('<Button-1>', changehandtype)

root.bind("<Configure>", onresize)

# Create the layout
canvas.pack(fill='both', expand=True) # This is critical to allow resize
typebutton.pack (side='left')
digitaltimelabel.pack (side='left') #'bottom')
savebutton.pack(side = 'right')
savebutton.bind('<Button-1>', saveclicked)

root.protocol('WM_DELETE_WINDOW', ondismiss)

# Start the run loop
run()

root.mainloop()