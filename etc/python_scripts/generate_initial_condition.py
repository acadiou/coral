import numpy as np


def read_coral_parameters():
   file1 = open('coral.parameters.in', 'r')
   Lines = file1.readlines()
   nx = int(Lines[1][:Lines[1].find(' ')])
   ny = int(Lines[2][:Lines[2].find(' ')])
   nz = int(Lines[3][:Lines[3].find(' ')])
   lx  = float(Lines [5][:Lines [5].find(' ')].replace('d','e',1).replace('D','e',1))
   ly  = float(Lines [6][:Lines [6].find(' ')].replace('d','e',1).replace('D','e',1))
   gap = float(Lines [7][:Lines [7].find(' ')].replace('d','e',1).replace('D','e',1))
   ctr = float(Lines [8][:Lines [8].find(' ')].replace('d','e',1).replace('D','e',1))
   dtm = float(Lines[10][:Lines[10].find(' ')].replace('d','e',1).replace('D','e',1))
   
   return nx*3//2, ny*3//2, nz*3//2, lx, ly, gap, ctr, dtm

# parameters
NX, NY, NZ, Lx, Ly, gap, center, dtMax = read_coral_parameters()

# Fourier and Chebyshev grids
grid_x = np.linspace(0,Lx, num=NX, endpoint=False)
grid_y = np.linspace(0,Ly, num=NY, endpoint=False)
grid_z = center + gap/2.*np.cos( (2.*np.arange(NZ) + 1.)  *np.pi / 2./NZ)
X,Y,Z = np.meshgrid(grid_y, grid_x, grid_z)
# define zero:
zeroField = np.zeros((NX,NY,NZ), dtype=np.float_)

np.array([dtMax, 0.], dtype=np.float_).tofile('./Restart/dt.sav')

####################################################
#                                                  #
#        Fluctuations (non-zero [kx,ky])           #
#                                                  #
####################################################

######## Define a new variable
temperature_fluctuations = Z**2*(Z-1.)**2*(
              np.cos(X*2*np.pi/Lx*4) + 
              np.cos(X*2*np.pi/Lx*4*0.5 + Y*2*np.pi/Ly*4) + 
              np.cos(X*2*np.pi/Lx*4*0.5 - Y*2*np.pi/Ly*4)
                                           )

######## Export to disk
# variables that are initialised to zero need to be exported as well
zeroField.tofile('./Restart/QuickSave.kxky.sys001.var001.rolling1')
zeroField.tofile('./Restart/QuickSave.kxky.sys001.var002.rolling1')
zeroField.tofile('./Restart/QuickSave.kxky.sys001.var003.rolling1')
zeroField.tofile('./Restart/QuickSave.kxky.sys001.var004.rolling1')
zeroField.tofile('./Restart/QuickSave.kxky.sys001.var006.rolling1')
# export temperature
temperature_fluctuations.tofile('./Restart/QuickSave.kxky.sys001.var005.rolling1')




####################################################
#                                                  #
#        Horizontally-averaged fields              #
#                                                  #
####################################################

######## Define a new variable
temperature_mean = grid_z - 0.5 - 4.* (grid_z-0.5)**3
horizontal_shear = 4.*np.cos(grid_z*np.pi)


######## Export to disk
# variables that are initialised to zero need to be exported as well
zeroField.tofile('./Restart/QuickSave.zero.sys001.var001.rolling1')
# export temperature
horizontal_shear.tofile('./Restart/QuickSave.zero.sys002.var001.rolling1')
temperature_mean.tofile('./Restart/QuickSave.zero.sys003.var001.rolling1')


