from __future__ import division
from numpy import arange, pi, cos, sin, tan

from traits.api import HasTraits, Range, Bool, Button, Instance, \
        on_trait_change
from traitsui.api import View, Item, Group
from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, \
                MlabSceneModel

from mayavi import mlab
import numpy as np
import colorsys

########## Modify things in this section: ##########
def f(z):
    return sin(z) # Examples: sin(z),  np.absolute(z), np.exp(1/z), np.exp(-1*np.power(z,2)), 


resolution = 400 # Number of values of phi (and of theta) plotted. 400 is fast, 1000 is pretty

polarPlane = False # When True plane is drawn with more pixels closer to 0; when False, pixels are evenly distributed with cartesian coordinates.
trimMag = 5 # Disc extends to |z| = trimMag, or square to Re(z), Im(z) = +/-trimMag if polarPlane is False

def contourfunc(x):
    return lin_contourfunc(x) # Pick one of the functions defined below, or a product such as lin_contourfunc(x)*log_contourfunc(x) to overlay multiple

def lin_contourfunc(x):
    # Parameters:
    T=1       # interval between contours
    b=0.00    # mark when b+|f(z)|/T is within ~0.06 of an integer. E.g. b=-0.07 marks the biggest region around zeroes, b=0.07 doesn't mark zeroes. (Estimates are for t~5, increase |b| if you increase t)
    t=10      # thickness of contours (0-100) (~5 is usually good, 50 is quite thick)
    return 1/(1 + np.power(10, t-500*((cos((2*pi*abs(x)/T)+(1+b)*pi)+1)/2)))

def log_contourfunc(x):
    # Parameters:
    T=np.e    # log base, use np.e for natural log
    b=0.00    # mark when b+|f(z)|/T is within ~0.06 of an integer. E.g. b=-0.07 marks the biggest region around zeroes, b=0.07 doesn't mark zeroes. (Estimates are for t~5, increase |b| if you increase t)
    t=10      # thickness of contours (0-100) (~5 is usually good, 50 is quite thick)
    return 1/(1 + np.power(10, t-500*((cos((2*pi*np.log(abs(x))/np.log(T))+(1+b)*pi)+1)/2)))

########## Don't modify things below this line (unless you want to) ##########

phi, theta = np.mgrid[0:pi:(resolution+1)*1j, -pi:pi:(resolution+1)*1j] #complex step number just makes it inclusive

# Do stereographic projection. Theta is measured counter-clockwise from the negative real direction (-pi), phi down from the Northern half of the vertical axis (so pi/2 is the equator, pi the S pole)
z = 2*tan(0.5*(pi-phi))*np.exp(1j*theta)

# Define cartesian cordinates for spherical plots
cartX = sin(phi) * cos(theta)
cartY = sin(phi) * sin(theta)
cartZ = cos(phi)+1

# Define coordinates for planar plots
if polarPlane:
    # Define section of the polar grid to project onto planar plots
    trimPhi = np.arctan(trimMag/2)*(-2)+pi
    trimmedZ = z[int(len(z) * trimPhi/pi):]
    trimmedZeros = np.zeros_like(np.real(trimmedZ))
    trimmedTheta = theta[int(len(theta) * trimPhi/pi):]
else:
    reZ, imZ = np.mgrid[-trimMag:trimMag:(resolution+1)*1j, -trimMag:trimMag:(resolution+1)*1j] #complex step number just makes it inclusive
    trimmedZ = reZ + 1j*imZ
    trimmedZeros = np.zeros_like(np.real(trimmedZ))
    trimmedTheta = np.angle(trimmedZ)

    
# Define color look up table for contours
magLut = np.zeros((256,4), dtype='uint8')
magLut[:, 3] = np.linspace(255, 0, 256) # set alpha channel
#white contours:
#for i in range(3):
#    magLut[:,i] = np.linspace(255, 255, 256)

# Define color look up table for argument
argLut = np.zeros((256,4), dtype='uint8')
# set alpha channel to 255
argLut[:, 3] = np.linspace(255, 255, 256)
# color by hue: red - green - blue - not green (adj for angles from -pi to pi)
for i in range(128,192):
    rgb = colorsys.hls_to_rgb((i-128)/64/3, 0.5, 1.0)
    for j in range(3):
        argLut[i,j] = int(rgb[j]*255)
for i in range(192,256):
    rgb = colorsys.hls_to_rgb((1/3) + (1/3)*(i-192)/64, 0.5, 1.0)
    for j in range(3):
        argLut[i,j] = int(rgb[j]*255)
for i in range(0,64):
    rgb = colorsys.hls_to_rgb((2/3) + (1/6)*(i-0)/64, 0.5, 1.0)
    for j in range(3):
        argLut[i,j] = int(rgb[j]*255)
for i in range(64,128):
    rgb = colorsys.hls_to_rgb((5/6) + (1/6)*(i-64)/64, 0.5, 1.0)
    for j in range(3):
        argLut[i,j] = int(rgb[j]*255)
        
        
class MyaviModel(HasTraits):
    # Create parts for id view:
    idScene = Instance(MlabSceneModel, ())
    idInclSphereArg = Bool(label='Include Argument on Stereographic Sphere')
    idInclSphereMag = Bool(label='Include Magnitude on Stereographic Sphere')
    idInclPlaneArg = Bool(label='Include Argument on Plane')
    idInclPlaneMag = Bool(label='Include Magnitude on Plane')
    idSphereArgPlot = Instance(PipelineBase)
    idSphereMagPlot = Instance(PipelineBase)
    idPlaneArgPlot = Instance(PipelineBase)
    idPlaneMagPlot = Instance(PipelineBase)
    syncButton = Button(label='Match function view')
    
    # Create parts for f view:
    fScene = Instance(MlabSceneModel, ())
    fInclSphereArg = Bool(label='Include Argument on Stereographic Sphere')
    fInclSphereMag = Bool(label='Include Magnitude on Stereographic Sphere')
    fInclPlaneArg = Bool(label='Include Argument on Plane')
    fInclPlaneMag = Bool(label='Include Magnitude on Plane')
    fSphereArgPlot = Instance(PipelineBase)
    fSphereMagPlot = Instance(PipelineBase)
    fPlaneArgPlot = Instance(PipelineBase)
    fPlaneMagPlot = Instance(PipelineBase)
    
    @on_trait_change('syncButton')
    def sync_cam(self):
        self.idScene.mlab.sync_camera(self.fScene.mayavi_scene, self.idScene.mayavi_scene)
        self.idScene.mlab.draw(figure=self.idScene.mayavi_scene)
    
    # When the scene is activated, or when the parameters are changed, we
    # update the plot.
    @on_trait_change('idInclSphereArg,idInclSphereMag,idInclPlaneArg,idInclPlaneMag,idScene.activated,fInclSphereArg,fInclSphereMag,fInclPlaneArg,fInclPlaneMag,fScene.activated') 
    def update_plot(self):
        #initialize the plots if unintialized
        if (self.idSphereArgPlot is None) or (self.idSphereMagPlot is None) or (self.idPlaneArgPlot is None) or (self.idPlaneMagPlot is None) or (self.fSphereArgPlot is None) or (self.fSphereMagPlot is None) or (self.fPlaneArgPlot is None) or (self.fPlaneMagPlot is None):
            # id meshes
            self.idSphereArgPlot = self.idScene.mlab.mesh(cartX, cartY, cartZ, scalars=theta, vmin=-pi, vmax=pi, figure=self.idScene.mayavi_scene)
            self.idSphereMagPlot = self.idScene.mlab.mesh(cartX, cartY, cartZ, scalars=contourfunc(z), figure=self.idScene.mayavi_scene)
            self.idPlaneArgPlot = self.idScene.mlab.mesh(np.real(trimmedZ), np.imag(trimmedZ), trimmedZeros, scalars=trimmedTheta, figure=self.idScene.mayavi_scene)
            self.idPlaneMagPlot = self.idScene.mlab.mesh(np.real(trimmedZ), np.imag(trimmedZ), trimmedZeros, scalars=contourfunc(trimmedZ), figure=self.idScene.mayavi_scene)
            # f meshes
            self.fSphereArgPlot = self.fScene.mlab.mesh(cartX, cartY, cartZ, scalars=np.angle(f(z)), vmin=-pi, vmax=pi, figure=self.fScene.mayavi_scene)
            self.fSphereMagPlot = self.fScene.mlab.mesh(cartX, cartY, cartZ, scalars=contourfunc(f(z)), figure=self.fScene.mayavi_scene)
            self.fPlaneArgPlot = self.fScene.mlab.mesh(np.real(trimmedZ), np.imag(trimmedZ), trimmedZeros, scalars=np.angle(f(trimmedZ)), figure=self.fScene.mayavi_scene)
            self.fPlaneMagPlot = self.fScene.mlab.mesh(np.real(trimmedZ), np.imag(trimmedZ), trimmedZeros, scalars=contourfunc(f(trimmedZ)), figure=self.fScene.mayavi_scene)
            
        # define lut variables for each part of the plots
        idArgSphereLut=argLut
        idMagSphereLut=magLut
        idArgPlaneLut=argLut
        idMagPlaneLut=magLut
        fArgSphereLut=argLut
        fMagSphereLut=magLut
        fArgPlaneLut=argLut
        fMagPlaneLut=magLut
        # zero the lut if the corresponding box is not checked
        if (not self.idInclSphereArg):
            idArgSphereLut=np.zeros((256,4), dtype='uint8')
            self.idSphereArgPlot.mlab_source.set(z=np.zeros_like(cartX), x=np.zeros_like(cartX), y=np.zeros_like(cartX)) #didn't work: transparent=True, opacity=0.5, figure=self.idScene.mayavi_scene, zmax=0.5
        else: #spheres need to shrink out of the way (half-baked bug fix)
            self.idSphereArgPlot.mlab_source.set(z=cartZ, x=cartX, y=cartY)
        if (not self.idInclSphereMag):
            idMagSphereLut=np.zeros((256,4), dtype='uint8')
            self.idSphereMagPlot.mlab_source.set(z=np.zeros_like(cartX), x=np.zeros_like(cartX), y=np.zeros_like(cartX)) #didn't work: transparent=True, opacity=0.5, figure=self.idScene.mayavi_scene, zmax=0.5
        else: #spheres need to shrink out of the way (half-baked bug fix)
            self.idSphereMagPlot.mlab_source.set(z=cartZ, x=cartX, y=cartY)
        if (not self.idInclPlaneArg):
            idArgPlaneLut=np.zeros((256,4), dtype='uint8')
        if (not self.idInclPlaneMag):
            idMagPlaneLut=np.zeros((256,4), dtype='uint8')
        if (not self.fInclSphereArg):
            fArgSphereLut=np.zeros((256,4), dtype='uint8')
            self.fSphereArgPlot.mlab_source.set(z=np.zeros_like(cartX), x=np.zeros_like(cartX), y=np.zeros_like(cartX)) #didn't work: transparent=True, opacity=0.5, figure=self.idScene.mayavi_scene, zmax=0.5
        else: #spheres need to shrink out of the way (half-baked bug fix)
            self.fSphereArgPlot.mlab_source.set(z=cartZ, x=cartX, y=cartY)
        if (not self.fInclSphereMag):
            fMagSphereLut=np.zeros((256,4), dtype='uint8')
            self.fSphereMagPlot.mlab_source.set(z=np.zeros_like(cartX), x=np.zeros_like(cartX), y=np.zeros_like(cartX))
        else: #spheres need to shrink out of the way (half-baked bug fix)
            self.fSphereMagPlot.mlab_source.set(z=cartZ, x=cartX, y=cartY)
        if (not self.fInclPlaneArg):
            fArgPlaneLut=np.zeros((256,4), dtype='uint8')
        if (not self.fInclPlaneMag):
            fMagPlaneLut=np.zeros((256,4), dtype='uint8')
            
        # update the luts
        self.idSphereArgPlot.module_manager.scalar_lut_manager.lut.table = idArgSphereLut #load lut into figure
        self.idSphereMagPlot.module_manager.scalar_lut_manager.lut.table = idMagSphereLut #load lut into figure
        self.idPlaneArgPlot.module_manager.scalar_lut_manager.lut.table = idArgPlaneLut #load lut into figure
        self.idPlaneMagPlot.module_manager.scalar_lut_manager.lut.table = idMagPlaneLut #load lut into figure

        self.fSphereArgPlot.module_manager.scalar_lut_manager.lut.table = fArgSphereLut #load lut into figure
        self.fSphereMagPlot.module_manager.scalar_lut_manager.lut.table = fMagSphereLut #load lut into figure
        self.fPlaneArgPlot.module_manager.scalar_lut_manager.lut.table = fArgPlaneLut #load lut into figure
        self.fPlaneMagPlot.module_manager.scalar_lut_manager.lut.table = fMagPlaneLut #load lut into figure
        
        # force a redraw of the figures
        self.fScene.mlab.draw(figure=self.fScene.mayavi_scene)
        self.idScene.mlab.draw(figure=self.idScene.mayavi_scene)

            
idView = View(Item('idScene', editor=SceneEditor(scene_class=MayaviScene),height=250, width=300, show_label=False), #, show_label=False),
            Group(
                    '_', 'idInclSphereArg', 'idInclSphereMag', 'idInclPlaneArg', 'idInclPlaneMag',
                 ),
            Item('syncButton', show_label=False),
            resizable=True, title='z - identity'
            )
fView = View(Item('fScene', editor=SceneEditor(scene_class=MayaviScene),height=250, width=300, show_label=False), #, show_label=False),
            Group(
                    '_', 'fInclSphereArg', 'fInclSphereMag', 'fInclPlaneArg', 'fInclPlaneMag',
                 ),
            resizable=True, title='f(z) - as defined under the line "def f(z):" '
            )

myaviModel = MyaviModel()
myaviModel.idInclSphereArg = True
myaviModel.idInclSphereMag = True
myaviModel.idInclPlaneArg = True
myaviModel.idInclPlaneMag = True
myaviModel.fInclSphereArg = True
myaviModel.fInclSphereMag = True
myaviModel.fInclPlaneArg = True
myaviModel.fInclPlaneMag = True
myaviModel.edit_traits(view=idView)
myaviModel.configure_traits(view=fView)
