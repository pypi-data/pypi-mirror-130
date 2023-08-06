import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt
import matplotlib.colors as c
import matplotlib as mpl
import scipy.sparse.linalg as slinalg
import time as time
import cv2

# Default arguments:
# delta_x       Numpy array of length 3 containing the size of the grid
# dx:           Numpy array of length 3 containing the difference of coordinates between grid points
# N:            Numpy array of length 3 containing the number of grid points
# x0:           Numpy array of length 3 containing the minimum value of each coordinate
# c:            The speed of light
# mu0:          The permeability of free space
# boundaries:   The boundary conditions, it is a 3 long list, one element for each coordinate
#               each element can either be "periodic" or a 2 long list with the boundary conditions
#               in the negative and the positive direction. These can either be "open", "flat", "closed" or a matrix for a custom boundary condition

# Default vector arguments:
# grad:         Function to calculate gradient of scalar field
# div:          Function to calculate divergence of vector field
# curl:         Function to calculate curl of vector field
# lapl:         Matrix to calculate laplacian
# c:            The speed of light
# mu0:          The permeability of free space

# Function to get the vector indices for the 1 dimensional vector given the indices for the 3 dimensional vector:
# Returns a numpy array or number with the shape n.shape[1:] with the indices for the 1 dimensional vector
#
# N is default argument
# n:            A numpy numpy array with the indices for the 3 dimensional vector, 
#               more than one point can be specified but the first axis must be the indices for one point
def get_vector_index(n, N):
    Factor = np.array([1, N[0], N[0] * N[1]]).reshape((3,) + (1,) * (len(n.shape) - 1))
    return np.array(np.sum(n * Factor, axis = 0), dtype = int)


# Turns a 3 dimensional array of numbers into the vector representation
#
# N is a default argument
# Array:        The array to convert into a vector
def to_vector(Array, N):
    # Find the indices for each position
    n0, n1, n2 = np.arange(N[0]), np.arange(N[1]), np.arange(N[2])
    
    # Meshgrid together
    m0, m1, m2 = np.meshgrid(n0, n1, n2, indexing = "ij")
    
    # append together
    Shape = (1,) + m0.shape
    n = np.append(m0.reshape(Shape), np.append(m1.reshape(Shape), m2.reshape(Shape), axis = 0), axis = 0)
    
    # Get the vector index
    vn = get_vector_index(n, N)

    # Create the vector
    Vector = np.empty((np.prod(N),) + Array.shape[3:])

    Vector[vn] = Array[:]
    
    return Vector
    

# Turns a vector into the 3 dimensional array representation
#
# N is a default argument
# Vector:       The vector to turn into a array
def to_array(Vector, N):
    # Find the indices for each position
    n0, n1, n2 = np.arange(N[0]), np.arange(N[1]), np.arange(N[2])
    
    # Meshgrid together
    m0, m1, m2 = np.meshgrid(n0, n1, n2, indexing = "ij")
    
    # append together
    Shape = (1,) + m0.shape
    n = np.append(m0.reshape(Shape), np.append(m1.reshape(Shape), m2.reshape(Shape), axis = 0), axis = 0)
    
    # Get the vector index
    vn = get_vector_index(n, N)

    # Create the array
    Array = np.empty(tuple(N) + Vector.shape[1:])
    Array[:] = Vector[vn]
    
    return Array


# Calculates the total weights for each of the 8 corners in the interpolation
# Returns an array with the shape (8,) + W.shape[1:] containing the weights for the 8 corners
# for each point. For (x,y,z)  the points are sorted as (-, -, -), (-, -, +), (-, +, -), (-, +, +),
# (+, -, -), (+, -, +), (+, +, -), (+, +, +)
#
# W:    The weights for each point, the shape can be any length but the first axis
#       should be of length 3 and contain the weights for each of the coordinates,
#       where 0 is for the - corner and 1 is for +
def total_weight(W):
    # Initialise the total weight array
    Result = np.ones((8,) + W.shape[1:])
    
    # Go through all of the coordinates
    for i in range(3):
        # Go through and multiply the weights v=1-w or w in the pattern:
        #       | | | | | | | | |
        # i = 0: v v v v w w w w
        # i = 1: v v w w v v w w
        # i = 2: v w v w v w v w
        for j in range(int(2 ** i)):
            # Do the v's
            Result[int(j * 2 ** (3 - i)):int((j + 1 / 2) * 2 ** (3 - i))] *= (1 - W[i]).reshape((1,) + W.shape[1:])
            # Do the w's
            Result[int((j + 1 / 2) * 2 ** (3 - i)):int((j + 1) * 2 ** (3 - i))] *= W[i].reshape((1,) + W.shape[1:])
            
    # Return the result
    return Result


# A function to interpolate the values of 8 corners in the middle 
#
# W:        The weights for each point for the different directions,
#           the first axis should be length 3 and contain the weights for the same point
# Values:   The values at the corners, the first axis defines the corner sorted by
#           (-, -, -), (-, -, +), (-, +, -), (-, +, +), (+, -, -), (+, -, +), (+, +, -), (+, +, +)
#           The shape of Values and W should be the same except for the first axis
def interpolation(W, Values):
    # Get the total weights
    TotalW = total_weight(W)
    TotalW = TotalW.reshape(TotalW.shape + (1,) * (len(Values.shape) - len(W.shape)))

    # Calculate the lerp
    return np.sum(TotalW * Values, axis = 0)


# Samples values at specific points from a field, interpolate to get smooth values from field
# Return the values in the shape Points.shape[1:]
#
# dx, N and x0 are default arguments
# Field:        The field to sample values from in vector from, this can also be a vector field
# Points:       An array with the x,y,z coordinates in the first axis
def sample_values(Field, Points, dx, N, x0):
    # Find the new shape of dx and x0
    ShapeX = (3,) + (1,) * len(Points.shape)
    ShapeP = (3, 1) + Points.shape[1:]
    
    # Find the indices for the corners
    CornerIndex = np.repeat(np.array(np.floor((Points.reshape(ShapeP) - x0.reshape(ShapeX)) / dx.reshape(ShapeX)), dtype = int), 8, axis = 1)

    # Go through all of the coordinates
    for i in range(3):
        # Go through and multiply the weights v=1-w or w in the pattern:
        #       | | | | | | | | |
        # i = 0: - - - - + + + +
        # i = 1: - - + + - - + +
        # i = 2: - + - + - + - +
        for j in range(int(2 ** i)):
            # Add to the coordinates
            CornerIndex[i, int((j + 1 / 2) * 2 ** (3 - i)):int((j + 1) * 2 ** (3 - i))] += 1
            
    # Mod the values to be within the correct range
    ShapeMod = (3,) + (1,) * (len(CornerIndex.shape) - 1)
    CornerIndex = np.mod(CornerIndex, N.reshape(ShapeMod))
            
    # Get the vector index for each point
    CornerVectorIndex = get_vector_index(CornerIndex, N)

    # Get values from field
    FieldValues = Field[CornerVectorIndex]

    # Find new shapes
    ShapeX = (3,) + (1,) * (len(Points.shape) - 1)
    
    # Find weights
    Weights = np.mod((Points - x0.reshape(ShapeX)) / dx.reshape(ShapeX), 1)

    # Interpolate
    return interpolation(Weights, FieldValues)


# Samples vectors at specific points from a field projected onto a 2D plane, interpolate to get smooth values from field
# Return the values in the shape Points.shape[1:]
#
# dx, N and x0 are default arguments
# Field:        The field to sample values from in vector from, this has to be a vector field
# Points:       An array with the x,y,z coordinates in the first axis
# hat:          An array defining the directions of the hat vectors, it should have a shape of type 
#               (SomeShape, 3, N) where (SomeShape can be any shape with len(SomeShape) <= len(Points.shape))
#               if it is < then it will be changed to shape (SomeShape, 1, 1...) until it is long enough.
#               N is the number of hat vectors, it can also have shape (SomeShape, 3) but then you should set single = True
# single:       Set to True if you have no N dimension on the hat array
def sample_vectors(Field, Points, hat, dx, N, x0, single = False):
    # Get the 3D vectors
    FieldValues = sample_values(Field, Points, dx, N, x0)
    
    # Change hat if single is True
    if single is True:
        hat = hat.reshape(hat.shape + (1,))
    
    # Find the x and y axis components
    v = np.sum(FieldValues.reshape(FieldValues.shape + (1,)) * hat.reshape((1,) * (len(FieldValues.shape) - len(hat.shape) + 1) + hat.shape), axis = -2)

    # Reshape back if singe is True
    if single is True:
        v = v.reshape(v.shape[:-1])

    return v


# A default scale used in the scalar plotter
# Returns a numpy array filled with the values in x scaled
# 
# x:    This is a numpy array of floating points
def default_scale(x):
    return x


# Plot a scalar field
#
# Values:       The 2D array of values to plot
# extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
# scale:        Function to scale the values of the field
# ax:           The axes to draw the plot inside
# fig:          The figure to draw in, if given then ax must also be given
# figsize:      The size of the figure if ax is not given
# dpi:          The resolution of the figure if ax is not given
# cmap:         The colour map to plot the scalar field with
# clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
#               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
#               values in the field
def plot_scalar(Values, extent = [0, 1, 0, 1], scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", clim = None):
    # Calculate clim
    if clim is None:
        clim = np.array([np.min(Values), np.max(Values)], dtype = float)
    
    clim = scale(clim)
    
    # Create figure
    if ax is None:
        fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
        
    # Plot scalar field
    Plot = ax.imshow(np.transpose(scale(Values)), cmap = cmap, clim = clim, origin = "lower", extent = extent)
    
    return fig, ax, Plot


# Updates a scalar plot with some new values
#
# Plot:         The Plot element returned by plot_scalar
# Values:       The new values to plot, it will use same extent, cmap and clim
# scale:        The scale function used, this should be the same as originally used
def update_plot_scalar(Plot, Values, scale = default_scale):
    Plot.set_array(np.transpose(scale(Values)))


# Define a contour class
class contour:
    def __init__(self, ax, plot, X, Y, levels, cmap, extent, vmin, vmax, colors, linestyles, use_cmap):
        # Save all the data
        self.__ax = ax
        self.__plot = plot
        self.__X = X
        self.__Y = Y
        self.__levels = levels
        self.__cmap = cmap
        self.__extent = extent
        self.__vmin = vmin
        self.__vmax = vmax
        self.__colors = colors
        self.__linestyles = linestyles
        self.__use_cmap = use_cmap
        
    # Update the plot
    #
    # Values: The new values in the same shape as the old
    def update(self, Values):
        # Remove old contours
        for Coll in self.__plot.collections:
            Coll.remove()
        
        # Plot the contours
        if self.__use_cmap is True:
            self.__plot = self.__ax.contour(self.__X, self.__Y, Values, self.__levels, cmap = self.__cmap, extent = self.__extent, vmin = self.__vmin, vmax = self.__vmax, linestyles = self.__linestyles)
        
        else:
            self.__plot = self.__ax.contour(self.__X, self.__Y, Values, self.__levels, extent = self.__extent, colors = self.__colors, linestyles = self.__linestyles)      
            
        return self.__plot

# Plots contour lines
#
# Values:       The 2D array of values to plot
# extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
# levels:       The levels to draw contours for, if an int then they will be evenly spaced between clim[0] and clim[1].
#               Can also be a list/array of levels in increasing order
# scale:        Function to scale the values of the field
# ax:           The axes to draw the plot inside
# fig:          The figure to draw in, if given then ax must also be given
# figsize:      The size of the figure if ax is not given
# dpi:          The resolution of the figure if ax is not given
# cmap:         The colour map to plot the scalar field with, used if use_cmap is True
# clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
#               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
#               values in the field
# colors:       Matplotlib colour string or a list of colours to give each contour their own colour, only used if use_cmap is False
# use_cmap:     True if the cmap should determine the colours, false if they should be determined by color
# linestyles:   The linestyles to draw the contours with, a string if all contours should use same linestyle or a list of string for different linestyles
def plot_contour(Values, extent = [0, 1, 0, 1], levels = 10, scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", colors = "black", use_cmap = False, clim = None, linestyles = "solid"):
    # Calculate the positions of the vectors
    x = np.linspace(extent[0], extent[1], Values.shape[0] + 1)[:-1]
    y = np.linspace(extent[2], extent[3], Values.shape[1] + 1)[:-1]
    X, Y = np.meshgrid(x, y, indexing = "ij")
    
    # Calculate clim
    if clim is None:
        clim = np.array([np.min(Values), np.max(Values)], dtype = float)
    
    clim = scale(clim)
    
    # If levels is and int find the correct levels
    if isinstance(levels, int):
        levels = np.linspace(clim[0], clim[1], levels)
    
    # Create figure
    if ax is None:
        fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    # Plot the contours
    if use_cmap is True:
        Plot = ax.contour(X, Y, scale(Values), levels, cmap = cmap, extent = extent, vmin = clim[0], vmax = clim[1], linestyles = linestyles)
    
    else:
        Plot = ax.contour(X, Y, scale(Values), levels, extent = extent, colors = colors, linestyles = linestyles)        
    
    return fig, ax, contour(ax, Plot, X, Y, levels, cmap, extent, clim[0], clim[1], colors, linestyles, use_cmap)


# Updates a contour plot with some new values
#
# Plot:         The Plot element returned by plot_contour
# Values:       The new values to plot, it will use same extent, cmap and clim
# scale:        The scale function used, this should be the same as originally used
def update_plot_contour(Plot, Values, scale = default_scale):
    Plot.update(scale(Values))


# Plot the values along a line in a scalar field
#
# Values:       The 1D array of values to plot
# x:            The x values, this should be same shape as Values or None
# xlim:         The limit of x values to look at, set to None to let matplotlib do it automatically
# ylim:         The limit of y values to look at, set to None to let matplotlib do it automatically
# scale:        Function to scale the values of the field
# ax:           The axes to draw the plot inside
# fig:          The figure to draw in, if given then ax must also be given
# figsize:      The size of the figure if ax is not given
# dpi:          The resolution of the figure if ax is not given
# fmt:          The fmt used for plotting
def plot_1D(Values, x = None, xlim = None, ylim = None, scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, fmt = "-", label = ""):
    # Create figure
    if ax is None:
        fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
        
    # Plot graph with x
    if x is not None:
        Plot = ax.plot(x, Values, fmt, label = label)
        
    # Plot without x
    else:
        Plot = ax.plot(Values, fmt, label = label)
    
    # Set limits if specified
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])
    
    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])
    
    return fig, ax, Plot[0]


# Updates a normal 1D plot
#
# Plot:         The Plot element returned by plot_1D
# Values:       The new values to plot
# scale:        The scale function used, this should be the same as originally used
def update_plot_1D(Plot, Values, scale = default_scale):
    # Get the x values
    x, _ = Plot.get_data()
    
    # Set the new values
    Plot.set_data(x, scale(Values))
    

# Plot a vector field
#
# vx:           The vector components along the x axis to plot
# vy:           The vector components along the y axis to plot
# extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
# scale:        Function to scale the values of the field
# fig:          The figure to draw in, if given then ax must also be given
# ax:           The axes to draw the plot inside
# figsize:      The size of the figure if ax is not given
# dpi:          The resolution of the figure if ax is not given
# cmap:         The colour map to plot the vectors with
# clim:         Array containing the (min, max) values in the colour map, these are the raw values of the vector lengths,
#               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
#               values of the lengths
# cutoff:       The percentage of the max length of a vector or clim[1] where if a vector is smaller than this, then it will not be shown
def plot_vector(vx, vy, extent = [0, 1, 0, 1], scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", clim = None, cutoff = 0):  
    # Calculate the positions of the vectors
    x = np.linspace(extent[0], extent[1], vx.shape[0])
    y = np.linspace(extent[2], extent[3], vy.shape[1])
    X, Y = np.meshgrid(x, y, indexing = "ij")
    
    # Calculate length of vectors
    vAbs = np.sqrt(vx ** 2 + vy ** 2)

    # Make cutoff
    if clim is None:
        MaxVal = np.max(vAbs)
        
    else:
        MaxVal = clim[1]
        
    vAbs[vAbs < MaxVal * cutoff] = 0

    # Calculate clim
    if clim is None:
        clim = np.array([np.min(vAbs), np.max(vAbs)], dtype = float)
        
    clim = scale(clim)

    # Make sure it can plot
    if np.all(vAbs == 0):
        vAbs[int(vAbs.shape[0] / 2), int(vAbs.shape[1] / 2)] = 1
        vy[int(vAbs.shape[0] / 2), int(vAbs.shape[1] / 2)] = 1
    
    vAbs[vAbs == 0] = np.nan
    
    # Normalize lengths
    vx = vx / vAbs
    vy = vy / vAbs
    
    # Create figure
    if ax is None:
        fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    # Plot vectors
    Plot = ax.quiver(X, Y, vx, vy, scale(vAbs), cmap = cmap, pivot = "middle", clim = clim)

    return fig, ax, Plot


# Updates a vector plot
#
# Plot:         The Plot element returned by plot_vector
# vx:           The new vector components along the x axis to plot
# vy:           The new vector components along the y axis to plot
# scale:        The scale function used, this should be the same as originally used
# cutoff:       The cutoff used in absolute values, this should be the same as originally used
def update_plot_vector(Plot, vx, vy, scale = default_scale, cutoff = 0):
    # Calculate length of vectors
    vAbs = np.sqrt(vx ** 2 + vy ** 2)

    # Make cutoff        
    vAbs[vAbs < cutoff] = 0
    
    if np.all(vAbs == 0):
        vAbs[int(vAbs.shape[0] / 2), int(vAbs.shape[1] / 2)] = 1
        vy[int(vAbs.shape[0] / 2), int(vAbs.shape[1] / 2)] = 1

    # Normalise the lengths
    vAbs[vAbs == 0] = np.nan
    
    vx = vx / vAbs
    vy = vy / vAbs
 
    # Update the plot
    Plot.set_UVC(vx, vy, scale(vAbs))


class streamplot:
    def __init__(self, ax, Plot, X, Y, norm, cmap, minlength, density):
        # Store data
        self.__ax = ax
        self.__plot = Plot
        self.__X = X
        self.__Y = Y
        self.__norm = norm
        self.__cmap = cmap
        self.__minlength = minlength
        self.__density = density
        
    # Update the plot
    def update(self, vx, vy, scale = default_scale):
        # Remove old streams
        keep = lambda x: not isinstance(x, mpl.patches.FancyArrowPatch)
        self.__ax.patches = [patch for patch in self.__ax.patches if keep(patch)]
        self.__plot.lines.remove()
        
        # Find vAbs
        vAbs = np.sqrt(vx ** 2 + vy ** 2)
        
        # Make sure it can plot
        if np.all(vAbs == 0):
            vAbs[:] = 1
            vy[:] = 1

        # Plot new streams
        self.__plot = self.__ax.streamplot(self.__X.transpose(), self.__Y.transpose(), vx.transpose(), vy.transpose(), color = scale(vAbs.transpose()), norm = self.__norm, cmap = self.__cmap, minlength = self.__minlength, density = self.__density)
        
        return self.__plot


# Plot a vector stream
#
# vx:           The vector components along the x axis to plot
# vy:           The vector components along the y axis to plot
# extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
# scale:        Function to scale the values of the field
# fig:          The figure to draw in, if given then ax must also be given
# ax:           The axes to draw the plot inside
# figsize:      The size of the figure if ax is not given
# dpi:          The resolution of the figure if ax is not given
# cmap:         The colour map to plot the vectors with
# clim:         Array containing the (min, max) values in the colour map, these are the raw values of the vector lengths,
#               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
#               values of the lengths
# density:      How many stream lines should be drawn
# length:       The minimum length of the lines (In some scaled coordinates)
def plot_streams(vx, vy, extent = [0, 1, 0, 1], scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", clim = None, density = 1, length = 1, cutoff = 0):
    # Calculate the positions of the vectors
    x = np.linspace(extent[0], extent[1], vx.shape[0])
    y = np.linspace(extent[2], extent[3], vy.shape[1])
    X, Y = np.meshgrid(x, y, indexing = "ij")

    # Calculate length of vectors
    vAbs = np.sqrt(vx ** 2 + vy ** 2)
        
    # Calculate clim
    if clim is None:
        clim = np.array([np.min(vAbs), np.max(vAbs)], dtype = float)
        
    clim = scale(clim)
    
    # Make sure it can plot
    if np.all(vAbs == 0):
        vAbs[:] = 1
        vy[:] = 1
    
    # Create the color norm
    Norm = c.Normalize(vmin = clim[0], vmax = clim[1])
    
    # Create figure
    if ax is None:
        fig, ax = plt.subplots(figsize = figsize, dpi = dpi)

    # Plot vectors
    Plot = ax.streamplot(X.transpose(), Y.transpose(), vx.transpose(), vy.transpose(), color = scale(vAbs.transpose()), norm = Norm, cmap = cmap, minlength = np.min([extent[1] - extent[0], extent[3] - extent[2]]) * length / 10, density = density)

    return fig, ax, streamplot(ax, Plot, X, Y, Norm, cmap, np.min([extent[1] - extent[0], extent[3] - extent[2]]) * length / 10, density)
    

# Updates a streams plot with some new values
#
# Plot:         The Plot element returned by plot_contour
# vx:           The vector components along the x axis to plot
# vy:           The vector components along the y axis to plot
# scale:        The scale function used, this should be the same as originally used
def update_plot_streams(Plot, vx, vy, scale = default_scale):
    return Plot.update(vx, vy, scale = scale)


# Creates an array of points sampled from a plane spanned by x_hat and y_hat and centered on x_c
# Returns the coordinates for all of the points in a 2D array form for imshow
#
# x_hat:        The direction for the x-axis
# y_hat:        The direction for the y-axis
# x_c:          The center point
# Size:         2 component array giving the width in the x_hat and y_hat direction
# Resolution:   2 component array giving the number of points in the x_hat and y_hat direction
def sample_points_plane(x_hat, y_hat, x_c, Size, Resolution):
    # Make sure x_hat and y_hat is normalised
    x_hat = x_hat / np.sqrt(np.sum(x_hat ** 2))
    y_hat = y_hat / np.sqrt(np.sum(y_hat ** 2))
    
    # Find the points in the x_hat, y_hat system
    x = np.linspace(-Size[0] / 2, Size[0] / 2, Resolution[0])
    y = np.linspace(-Size[1] / 2, Size[1] / 2, Resolution[1])
    
    # Calculate the real positions
    return x_c.reshape((3, 1, 1)) + x_hat.reshape((3, 1, 1)) * x.reshape((1, -1, 1)) + y_hat.reshape((3, 1, 1)) * y.reshape((1, 1, -1))
    

# Creates an array of points sampled from a line between x1 and x2
# Returns the coordinates for all points along a line to sample field values for in 1D plotting
#
# x1:           The starting point of the line
# x2:           The ending poing of the line
# Resolution:   The number of points to be sampled
def sample_points_line(x1, x2, Resolution):
    # Make an evenly distributed linspace between the 2 points
    return x1.reshape((3, 1)) + (x2.reshape((3, 1)) - x1.reshape((3, 1))) * np.linspace(0, 1, Resolution).reshape((1, -1))
    

# Creates a function which returns a current/charge density which is 0 everywhere
#
# dx, N, x0, c, mu0 are default arguments
def default_J(dx, N, x0, c, mu0):
    # Create current which is 0 everywhere
    J = np.zeros((np.prod(N), 4))
    
    # Create function to return J
    # t:        The time
    def GetJ(t):
        return J
    
    # Return the function
    return GetJ


# Creates a function which returns the closed boundary conditions for each boundary
#
# dx, N, x0, c, mu0 are default arguments
def default_C(dx, N, x0, c, mu0):
    # Create a closed boundary condition which is 0 everywhere, the first axis is the coordinate
    # The second axis is the direction of the boundary
    C = np.zeros((np.prod(N), 4, 3, 2), dtype = float)
       
    # Create the function to return the conditions
    # t:        The time
    def GetC(t):
        return C
    
    return GetC


# Creates open boundary matrices the first dimension is the coordinate and the second dimension is the direction (positive or negative)
#
# N is a default argument
def get_boundaries_open(N, Coordinate, Dir):
    # Calculate the position of the offdiagonal
    OffPos1 = np.prod(N[:Coordinate])
    OffPos2 = 2 * np.prod(N[:Coordinate])
    OffPos3 = 3 * np.prod(N[:Coordinate])
    OffPos4 = 4 * np.prod(N[:Coordinate])
    
    # Create a tile
    Tile = np.zeros(np.prod(N[:Coordinate + 1]))
    OffTile1 = np.zeros(np.prod(N[:Coordinate + 1]))
    OffTile2 = np.zeros(np.prod(N[:Coordinate + 1]))
    OffTile3 = np.zeros(np.prod(N[:Coordinate + 1]))
    OffTile4 = np.zeros(np.prod(N[:Coordinate + 1]))

    # Add the ones
    if Dir == 0:
        Tile[:np.prod(N[:Coordinate])] = 4#5#4
        OffTile1[:np.prod(N[:Coordinate])] = -6#-10#-6
        OffTile2[:np.prod(N[:Coordinate])] = 4#10#4
        OffTile3[:np.prod(N[:Coordinate])] = -1#-5#-1
        OffTile4[:np.prod(N[:Coordinate])] = 0#1#0

    else:
        Tile[-np.prod(N[:Coordinate]):] = 4#5#4
        OffTile1[-np.prod(N[:Coordinate]):] = -6#-10#-6
        OffTile2[-np.prod(N[:Coordinate]):] = 4#10#4
        OffTile3[-np.prod(N[:Coordinate]):] = -1#-5#-1
        OffTile4[-np.prod(N[:Coordinate]):] = 0#1#0
        OffPos1 *= -1
        OffPos2 *= -1
        OffPos3 *= -1
        OffPos4 *= -1
        
    # Create the diagonal
    Diag = np.tile(Tile, np.prod(N[Coordinate + 1:]))
    OffDiag1 = np.tile(OffTile1, np.prod(N[Coordinate + 1:]))
    OffDiag2 = np.tile(OffTile2, np.prod(N[Coordinate + 1:]))
    OffDiag3 = np.tile(OffTile3, np.prod(N[Coordinate + 1:]))
    OffDiag4 = np.tile(OffTile4, np.prod(N[Coordinate + 1:]))
    
    if Dir == 0:
        OffDiag1 = OffDiag1[:-np.prod(N[:Coordinate])]
        OffDiag2 = OffDiag2[:-2 * np.prod(N[:Coordinate])]
        OffDiag3 = OffDiag3[:-3 * np.prod(N[:Coordinate])]
        OffDiag4 = OffDiag4[:-4 * np.prod(N[:Coordinate])]
       
    else:
        OffDiag1 = OffDiag1[np.prod(N[:Coordinate]):]
        OffDiag2 = OffDiag2[2 * np.prod(N[:Coordinate]):]
        OffDiag3 = OffDiag3[3 * np.prod(N[:Coordinate]):]
        OffDiag4 = OffDiag4[4 * np.prod(N[:Coordinate]):]

    # Create the boundary
    Bound = sparse.diags([Diag, OffDiag1, OffDiag2, OffDiag3, OffDiag4], [0, OffPos1, OffPos2, OffPos3, OffPos4], format = "csr")
            
    return Bound


# Creates boundary matrices, this is matrices with ones at the diagonal at points at each of the 6 boundaries
# the first dimension is the coordinate and the second dimension is the direction (positive or negative)
#
# N is a default argument
def get_boundaries_flat(N, Coordinate, Dir):
    # Create a tile
    Tile = np.zeros(np.prod(N[:Coordinate + 1]))
    
    # Add the ones
    if Dir == 0:
        Tile[:np.prod(N[:Coordinate])] = 1
        
    else:
        Tile[-np.prod(N[:Coordinate]):] = 1
        
    # Create the diagonal
    Diag = np.tile(Tile, np.prod(N[Coordinate + 1:]))
    
    # Create the boundary
    Bound = sparse.diags([Diag], [0], format = "csr")
            
    return Bound


# Creates boundary matrices for the periodic boundary conditions
# the first dimension is the coordinate and the second dimension is the direction (positive or negative)
#
# N is a default argument
def get_boundaries_periodic(N, Coordinate, Dir):
    # Calculate the position of the offdiagonal
    OffPos = np.prod(N[:Coordinate]) * (N[Coordinate] - 1)
                  
    if Dir == 1:
        OffPos *= -1
    
    # Create a tile
    Tile = np.zeros(np.prod(N[:Coordinate + 1]))
    
    # Add the ones
    Tile[:np.prod(N[:Coordinate])] = 1
    
    # Create the diagonal
    Diag = np.tile(Tile, np.prod(N[Coordinate + 1:]))
    
    # Remove the part outside the matrix
    Diag = Diag[:Tile.shape[0] * np.prod(N[Coordinate + 1:]) - np.prod(N[:Coordinate]) * (N[Coordinate] - 1)]

    # Create the boundary
    Bound = sparse.diags([Diag], [OffPos], format = "csr")
            
    return Bound


# Creates a custom boundary matrix for some coordinate and direction, each point can either be open or closed
#
# N is a default argument
# OpenPos:          A vector with either 0 or 1 for each position in the grid, 0 for closed or not on boundary and 1 for open
# Coordinate:       The coordinate along which the boundary is (1, 2 or 3 for x, y or z)
# Dir:              0 for the negative boundary and 1 for the positive boundary
#def get_boundaries_custom(N, OpenPos, Coordinate, Dir):
    # Find the off diagonal position
#    OffPos = np.prod(N[:Coordinate])
    
    # Shorten OpenPos
#    if Dir == 0:
#        Diag = OpenPos[:-OffPos]
        
#    else:
#        Diag = OpenPos[OffPos:]
#        OffPos *= -1
        
#    # Create the matrix
#    return sparse.diags([Diag], [OffPos], format = "csr")
    

# Creates matrices for differentiating once
#
# dx, N and boundaries are default arguments
def get_ddx(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Make a list for (ddx, ddy, ddz)
    ddx = np.empty(3, dtype = sparse.csr_matrix)
        
    # Go through each coordinate
    for Coordinate in range(3):
        # Create a tile
        Tile = np.ones(np.prod(N[:Coordinate + 1]))
        
        # Add zeros at the boundaries
        Tile[-np.prod(N[:Coordinate]):] = 0
        
        # Create the diagonal
        Diag = np.tile(Tile, np.prod(N[Coordinate + 1:]))[:-np.prod(N[:Coordinate])]
        
        # Create the matrix
        ddx[Coordinate] = sparse.diags([Diag, -Diag], [np.prod(N[:Coordinate]), -np.prod(N[:Coordinate])], format = "csr")
        
        # Add the open boundaries
        if boundaries[Coordinate] == "periodic":
            ddx[Coordinate] -= get_boundaries_periodic(N, Coordinate, 0)

        elif isinstance(boundaries[Coordinate][0], sparse.csr_matrix):
            ddx[Coordinate] -= boundaries[Coordinate][0]

        elif boundaries[Coordinate][0] == "open":
            ddx[Coordinate] -= get_boundaries_open(N, Coordinate, 0)            
   
        elif boundaries[Coordinate][0] == "flat":
            ddx[Coordinate] -= get_boundaries_flat(N, Coordinate, 0)         
                    
        if boundaries[Coordinate] == "periodic":
            ddx[Coordinate] += get_boundaries_periodic(N, Coordinate, 1)

        elif isinstance(boundaries[Coordinate][1], sparse.csr_matrix):
            ddx[Coordinate] += boundaries[Coordinate][1]
            
        elif boundaries[Coordinate][1] == "open":
            ddx[Coordinate] += get_boundaries_open(N, Coordinate, 1)

        elif boundaries[Coordinate][1] == "flat":
            ddx[Coordinate] += get_boundaries_flat(N, Coordinate, 1)
                               
        # Correct the value
        ddx[Coordinate] /= (2 * dx[Coordinate])

    return ddx

    
# Creates matrices for differentiating twice, 
#
# dx, N and boundaries are default arguments
def get_ddx2(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Make a list for (ddx, ddy, ddz)
    ddx2 = np.empty(3, dtype = sparse.csr_matrix)

    # Go through each coordinate
    for Coordinate in range(3):
        # Create a tile
        Tile = np.ones(np.prod(N[:Coordinate + 1]))
        
        # Add zeros at the edges
        Tile[-np.prod(N[:Coordinate]):] = 0
        
        # Create the diagonal
        Diag = np.tile(Tile, np.prod(N[Coordinate + 1:]))[:-np.prod(N[:Coordinate])]
        
        # Create the matrix
        ddx2[Coordinate] = sparse.diags([-2 * np.ones(np.prod(N)), Diag, Diag], [0, np.prod(N[:Coordinate]), -np.prod(N[:Coordinate])], format = "csr")

        # Add open boundary conditions
        if boundaries[Coordinate] == "periodic":
            ddx2[Coordinate] += get_boundaries_periodic(N, Coordinate, 0)

        elif isinstance(boundaries[Coordinate][0], sparse.csr_matrix):
            ddx2[Coordinate] += boundaries[Coordinate][0]

        elif boundaries[Coordinate][0] == "open":
            ddx2[Coordinate] += get_boundaries_open(N, Coordinate, 0)
      
        elif boundaries[Coordinate][0] == "flat":
            ddx2[Coordinate] += get_boundaries_flat(N, Coordinate, 0)
                  
        if boundaries[Coordinate] == "periodic":
            ddx2[Coordinate] += get_boundaries_periodic(N, Coordinate, 1)

        elif isinstance(boundaries[Coordinate][1], sparse.csr_matrix):
            ddx2[Coordinate] += boundaries[Coordinate][1]

        elif boundaries[Coordinate][1] == "open":
            ddx2[Coordinate] += get_boundaries_open(N, Coordinate, 1)

        elif boundaries[Coordinate][1] == "flat":
            ddx2[Coordinate] += get_boundaries_flat(N, Coordinate, 1)

        # Correct the value
        ddx2[Coordinate] /= dx[Coordinate] ** 2

    return ddx2


# Creates a function to take the gradient in cartesian coordinates
#
# dx, N and boundaries are default arguments
def get_grad(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Get the diff matrices
    ddx = get_ddx(dx, N, boundaries = boundaries)
        
    # Calculate the gradient
    # Scalar:   A scalar field of shape (N1 * N2 * N3)
    # C:        The closed boundary conditions for some time
    def calcGrad(Scalar, C):
        # Create empty vector field
        Result = np.empty((np.prod(N), 3))

        # Calculate result
        for i in range(3):
            Result[:, i] = ddx[i].dot(Scalar) + 1 / (2 * dx[i]) * (C[:, i, 1] - C[:, i, 0])
        
        # Return result
        return Result
    
    return calcGrad


# Creates a function to take the divergence in cartesian coordinates
#
# dx, N and boundaries are default arguments
def get_div(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Get the diff matrices
    ddx = get_ddx(dx, N, boundaries = boundaries)
    
    # Calculate the divergence
    # Vector:   A vector field to take the divergence of
    # C:        The closed boundary conditions for some time
    def calcDiv(Vector, C):
        # Calculate result
        return ddx[0].dot(Vector[:, 0]) + 1 / (2 * dx[0]) * (C[:, :, 0, 1] - C[:, :, 0, 0]) + ddx[1].dot(Vector[:, 1]) + 1 / (2 * dx[1]) * (C[:, :, 1, 1] - C[:, :, 1, 0]) + ddx[2].dot(Vector[:, 2]) + 1 / (2 * dx[2]) * (C[:, :, 2, 1] - C[:, :, 2, 0])
    
    return calcDiv


# Creates a function to take the curl in cartesian coordinates
#
# dx, N and boundaries are default arguments
def get_curl(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Get diff matrices
    ddx = get_ddx(dx, N, boundaries = boundaries)
    
    # Calculate the curl
    # Vector:   A vector fied to take the curl of
    # C:        The closed boundary conditions for some time
    def calcCurl(Vector, C):
        # Create result array
        Result = np.empty((np.prod(N), 3))

        # Calculate curl
        for i in range(3):
            Result[:, i] = ddx[(i + 1) % 3].dot(Vector[:, (i + 2) % 3]) + 1 / (2 * dx[(i + 1) % 3]) * (C[:, (i + 2) % 3, (i + 1) % 3, 1] - C[:, (i + 2) % 3, (i + 1) % 3, 0]) - ddx[(i + 2) % 3].dot(Vector[:, (i + 1) % 3]) - 1 / (2 * dx[(i + 2) % 3]) * (C[:, (i + 1) % 3, (i + 2) % 3, 1] - C[:, (i + 1) % 3, (i + 2) % 3, 0])
            
        return Result
    
    return calcCurl


# Creates the laplacian matrix in cartesian coordinates
#
# dx, N and boundaries are default arguments
def get_lapl(dx, N, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
    # Get ddx2
    ddx2 = get_ddx2(dx, N, boundaries = boundaries)

    # Create laplacian
    return np.sum(ddx2)


# Finds the E-field
#
# V:            The electric potential: A[:, 0] * c
# grad:         Function to calculate gradient
# C:            The closed boundary conditions for some time
def calc_E(V, grad, C):
    return -grad(V, C)


# Finds the B-field
#
# A:            The vector potential: A[:, 1:]
# curl:         Function to calculate curl
# C:            The closed boundary conditions for some time
def calc_B(A, curl, C):
    return curl(A, C)


# Finds the Poynting vector field
#
# mu0 is a default argument
# E:            The electric field
# B:            The magnetic field
def calc_S(E, B, mu0):
    return np.cross(E, B) / mu0

# Finds the energy density
#
# mu0 and c are default arguments
# E:            The electric field
# B:            The magnetic field
def calc_u(E, B, mu0, c):
    return 1 / (2 * mu0) * (np.sum(E ** 2, axis = -1) / c ** 2 + np.sum(B ** 2, axis = -1))

# Solves non-responsive EM-statics exactly
#
# mu0 and dx are default arguments
# J:            The current/charge density
# Laplacian:    The laplacian matrix
# C:            The closed boundary conditions for some time
def solve_exact(J, lapl, C, mu0, dx):
    # Figure out what the laplacian equals
    b = -mu0 * J
    
    for Coordinate in range(3):
        b -= 1 / dx[Coordinate] ** 2 * (C[:, :, Coordinate, 0] + C[:, :, Coordinate, 1])
    
    return slinalg.spsolve(lapl, b)

# Solves non-responsive EM-statics approximately
#
# mu0 and dx are default arguments
# J:            The current/charge density
# Laplacian:    The laplacian matrix
# C:            The closed boundary conditions for some time
# A0:           The starting guess for the potential
# n:            The number of iterations for the approximation
# k:            The approximation parameter to make sure it does not diverge
# progress:     How to show how much time is remaining, False if it should be disabled
#               a number to show time remaining with a period >= progress
def solve_approx(J, lapl, C, mu0, dx, A0, n, k, progress = False):
    # Setup the starting guess
    A = A0
    
    # Get the evolution matrix
    Matrix = sparse.identity(J.shape[0], format = "csr") + k * lapl
    
    # Get the vector to add
    b = k * mu0 * J
    
    for Coordinate in range(3):
        b += k / dx[Coordinate] ** 2 * (C[:, :, Coordinate, 0] + C[:, :, Coordinate, 1])
    
    # Setup time for writing time remaining
    Time0 = time.time()
    Time1 = Time0
    
    for i in range(n):
        # Evolve one step
        A = Matrix.dot(A) + b
        
        # Write the time remaining
        Time2 = time.time()
        if progress is not False and (Time2 - Time1 >= progress):
            print(f"{(Time2 - Time0) * (n - i - 1) / (i + 1):.2g} s remaining")
            Time1 = Time2
        
    return A


# Get the next value of A in the dynamics solution
#
# dx, dt, c and mu0 are default arguments
# A:            The potential field at time t0
# dAdt:         The change per time of A at time t0
# J:            The charge and current density array at time t0 + dt/2
# lapl:         The laplacian
# C:            The closed boundary conditions
# n:            The number of approximation steps if exact = False
# exact:        Whether it should be solved exactly or approximatly, should be a boolean
def solve_dynamics(A, dAdt, J, lapl, C, dx, dt, c, mu0, n, exact = False):
    # Get R
    R = (c * dt) ** 2 / 8. * mu0 * J + dt / 2. * dAdt + A
    
    for Coordinate in range(3):
        R += (c * dt) ** 2 / (8 * dx[Coordinate] ** 2) * (C[:, :, Coordinate, 0] + C[:, :, Coordinate, 1])
    
    # Calculate matrix
    M = (c * dt) ** 2 / 8 * lapl
    
    # Calculate A(t0 + 1/2 dt)
    if exact is True:
        HalfA = slinalg.spsolve(sparse.identity(A.shape[0], format = "csr") - M, R)
        
    else:
        HalfA = A + dt / 2. * dAdt
        
        for _ in range(n):
            HalfA = M.dot(HalfA) + R
    
    # Calculate the new values for the potential
    NewA = 4 * HalfA - dt * dAdt - 3 * A
    NewdAdt = (8 / dt * (HalfA - A) - 3 * dAdt)
    return (NewA, NewdAdt)


# The simulation class, create this class to define your simulation,
# Then use it's methods to run the simulation and diagnistics/plotting
# N, delta_x, x0, c, mu0 and boundaries are default arguments
#
# Initialize:
# approx_n:     The base number of times to run the approximation algorithm, this is multiplied by Nx^2+Ny^2+Nz^2
# dyn_n:        The number of approximation steps used in the dynamics simulation
# approx_k:     The base approximation parameter to make sure it does not diverge, this is multiplied by -1 / lapl[0, 0]
# init:         If true then the potentials will initialize to be 0 everywhere
#               If it is a numpy array of the correct size then it will
#               use that as the starting condition, the shape should either be
#               (N3, N2, N1, 4) or (N1 * N2 * N3, 4) if it is another shape but
#               still size 4 * N1 * N2 * N3 then it will reshape it to (N1 * N2 * N3, 4)
#               but with no guarantee that it will format correctly 
# init_ddt:     If true then the change of potentials with time will initialize to be 0 everywhere
#               If it is a numpy array of the correct size then it will
#               use that as the starting condition, the shape should either be
#               (N3, N2, N1, 4) or (N1 * N2 * N3, 4) if it is another shape but
#               still size 4 * N1 * N2 * N3 then it will reshape it to (N1 * N2 * N3, 4)
#               but with no guarantee that it will format correctly 
# init_copy:    Only used if init is a numpy array, if true then it will copy
#               the array, if false then it will use and alter the original array
# J:            The current and charge distribution, must be a function with default
#               arguments which returns a function to give the current and charge densit at any time
# C:            The closed boundary conditions, must be a function of default arguments
#               which returns a function of time to give the boundaries at that time
# grad:         A function to return a function to calculate the gradient in the coordinate system used
# div:          A function to return a function to calculate the divergence in the coordinate system used
# curl:         A function to return a function to calculate the curl in the coordinate system used
# lapl:    A function to calculate the laplacian in the coordinate system used
class sim:
    def __init__(self, N, delta_x = np.array([1, 1, 1]), x0 = np.array([0, 0, 0]), t0 = 0, dt = 1, c = 1, mu0 = 1, approx_n = 0.1, dyn_n = 10, approx_k = 1, init = True, init_ddt = True, init_copy = False, J = default_J, C = default_C, grad = get_grad, div = get_div, curl = get_curl, lapl = get_lapl, boundaries = [["closed", "closed"], ["closed", "closed"], ["closed", "closed"]]):
        # Test for type errors
        if not isinstance(N, np.ndarray):
            raise Exception(f"N has wrong type, it is {str(type(N)):s} but it should be {str(np.ndarray):s}")
        
        if not issubclass(N.dtype.type, np.integer):
            raise Exception(f"N has wrong dtype, it is {str(N.dtype.type):s} but it should be {str(np.integer):s}")
        
        if not isinstance(delta_x, np.ndarray):
            raise Exception(f"delta_x has wrong type, it is {str(type(delta_x)):s} but it should be {str(np.ndarray):s}")
        
        if not (issubclass(delta_x.dtype.type, np.floating) or issubclass(delta_x.dtype.type, np.integer)):
            raise Exception(f"delta_x has wrong dtype, it is {str(delta_x.dtype.type):s} but it should be {str(np.integer):s} or {str(np.floating):s}")
        
        if not isinstance(x0, np.ndarray):
            raise Exception(f"x0 has wrong type, it is {str(type(x0)):s} but it should be {str(np.ndarray):s}")
        
        if not (issubclass(x0.dtype.type, np.floating) or issubclass(x0.dtype.type, np.integer)):
            raise Exception(f"x0 has wrong dtype, it is {str(x0.dtype.type):s} but it should be {str(np.integer):s} or {str(np.floating):s}")

        if not (isinstance(t0, int) or isinstance(t0, float)):
            raise Exception(f"t0 has wrong type, it is {str(type(t0)):s} but it should be {str(int):s} or {str(float):s}")

        if not (isinstance(dt, int) or isinstance(dt, float)):
            raise Exception(f"dt has wrong type, it is {str(type(dt)):s} but it should be {str(int):s} or {str(float):s}")

        if not (isinstance(c, int) or isinstance(c, float)):
            raise Exception(f"c has wrong type, it is {str(type(c)):s} but it should be {str(int):s} or {str(float):s}")

        if not (isinstance(mu0, int) or isinstance(mu0, float)):
            raise Exception(f"mu0 has wrong type, it is {str(type(mu0)):s} but it should be {str(int):s} or {str(float):s}")

        if not (isinstance(approx_n, int) or isinstance(approx_n, float)):
            raise Exception(f"approx_n has wrong type, it is {str(type(approx_n)):s} but it should be {str(int):s} or {str(float):s}")
        
        if not (isinstance(approx_k, int) or isinstance(approx_k, float)):
            raise Exception(f"approx_k has wrong type, it is {str(type(approx_k)):s} but it should be {str(int):s} or {str(float):s}")
        
        if not isinstance(dyn_n, int):
            raise Exception(f"dyn_n has wrong type, it is {str(type(dyn_n)):s} but it should be {str(int):s}")
        
        # 0 if direction is periodic, 1 if not
        self.__periodic = np.ones(3, dtype = int)
        
        for i in range(3):
            if boundaries[i] == "periodic":
                self.__periodic[i] = 0
        
        # Store basic information
        self.__delta_x = np.array(delta_x.copy(), dtype = float)
        self.__N = np.array(N.copy(), dtype = int)
        self.__dx = self.__delta_x / (self.__N - self.__periodic)
        self.__x0 = np.array(x0.copy(), dtype = float)
        self.__c = float(c)
        self.__mu0 = float(mu0)
        self.__V = np.prod(self.__N)
        self.__n = int(approx_n * np.sum(self.__N ** 2))
        self.__nDyn = dyn_n
        self.__k = float(approx_k)
        self.__t = t0
        self.__dt = dt
        
        # Setup sampler list
        self.__samplers = []
        
        # Setup data calculated fields
        self.__reset_derived()
        
        # Create starting condition for potential
        # Initialize to 0
        if init is True:
            self.__A = np.zeros((self.__V, 4))
            
        # Use given starting conditions
        elif isinstance(init, np.ndarray):
            if np.prod(np.array(init.shape)) != self.__V * 4:
                raise Exception(f"init has wrong length, it has length {np.prod(np.array(init.shape)):d} but it should be {self.__V * 4:d}")
            
            if init_copy is True:
                self.__A = init.copy().reshape((self.__V, 4))
                
            elif init_copy is False:
                self.__A = init.reshape((self.__V, 4))
                
            else:
                raise Exception(f"init_copy has wrong type, it is {str(type(init_copy)):s} but it should be {str(bool):s}")
            
        else:
            raise Exception(f"init has wrong type, it is {str(type(init)):s} but it should be {str(np.ndarray):s} or be True")
        
        if init_ddt is True:
            self.__dAdt = np.zeros((self.__V, 4))
            
        # Use given starting conditions
        elif isinstance(init_ddt, np.ndarray):
            if np.prod(np.array(init_ddt.shape)) != self.__V * 4:
                raise Exception(f"init_ddt has wrong length, it has length {np.prod(np.array(init_ddt.shape)):d} but it should be {self.__V * 4:d}")
            
            if init_copy is True:
                self.__dAdt = init_ddt.copy().reshape((self.__V, 4))
                
            elif init_copy is False:
                self.__dAdt = init.reshape((self.__V, 4))
                
            else:
                raise Exception(f"init_copy has wrong type, it is {str(type(init_copy)):s} but it should be {str(bool):s}")
            
        else:
            raise Exception(f"init_ddt has wrong type, it is {str(type(init_ddt)):s} but it should be {str(np.ndarray):s} or be True")
            
        
        # Save all the generators
        self.__genJ = J
        self.__genGrad = grad
        self.__genDiv = div
        self.__genCurl = curl
        self.__genLapl = lapl
        
        # Get the current/charge density function
        self.__J = J(self.__dx, self.__N, self.__x0, self.__c, self.__mu0)
        
        if not callable(self.__J):
            raise Exception(f"J has wrong type, it is {str(type(self.__J)):s} but it should be a function")
        
        # Get the closed boundary conditions
        self.__C = C(self.__dx, self.__N, self.__x0, self.__c, self.__mu0)
        
        if not callable(self.__C):
            raise Exception(f"C has wrong type, it is {str(type(self.__C)):s} but it should be a function")
        
        # Get vector calculus functions
        self.__grad = grad(self.__dx, self.__N, boundaries = boundaries)
            
        if not callable(self.__grad):
            raise Exception(f"grad has wrong type, it is {str(type(self.__grad)):s} but it should be a function")

        self.__div = div(self.__dx, self.__N, boundaries = boundaries)
            
        if not callable(self.__div):
            raise Exception(f"div has wrong type, it is {str(type(self.__div)):s} but it should be a function")

        self.__curl = curl(self.__dx, self.__N, boundaries = boundaries)
            
        if not callable(self.__curl):
            raise Exception(f"curl has wrong type, it is {str(type(self.__curl)):s} but it should be a function")
                
        self.__lapl = lapl(self.__dx, self.__N, boundaries = boundaries)
                
        if not isinstance(self.__lapl, sparse.csr_matrix):
            raise Exception(f"lapl has wrong type, it is {str(type(self.__lapl)):s} but it should be {str(sparse.csr_matrix):s}")
            
        # Update the value for k
        self.__k /= (2 * np.sum(1 / self.__dx ** 2))
        
    # Resets all the derived fields
    def __reset_derived(self):
        self.__E = None
        self.__B = None
        self.__S = None
        self.__u = None
                
    # Get the dx
    def get_dx(self):
        return self.__dx
        
    # Get electric potential
    def get_V(self):
        return self.__A[:, 0] * self.__c
    
    # Get vector potential
    def get_A(self):
        return self.__A[:, 1:]
    
    # Get E-field
    def get_E(self):
        if self.__E is None:
            self.__E = calc_E(self.__A[:, 0] * self.__c, self.__grad, self.__C(self.__t)[:, 0, :, :])
        
        return self.__E
    
    # Get the B-field
    def get_B(self):
        if self.__B is None:
            self.__B = calc_B(self.__A[:, 1:], self.__curl, self.__C(self.__t)[:, 1:, :, :])
        
        return self.__B
    
    # Get the Poynting vector field
    def get_S(self):
        if self.__S is None:
            self.__S = calc_S(self.get_E(), self.get_B(), self.__mu0)
        
        return self.__S

    # Get the energy density
    def get_u(self):
        if self.__u is None:
            self.__u = calc_u(self.get_E(), self.get_B(), self.__mu0, self.__c)
        
        return self.__u

    # Get the charge density
    def get_Rho(self):
        return self.__J(self.__t)[:, 0] / self.__c
    
    # Get the current density
    def get_J(self):
        return self.__J(self.__t)[:, 1:]

    # Get the time
    def get_t(self):
        return self.__t

    # Finds the electrostatics solution
    # Returns the time it took
    #
    # exact:        Whether it should be solved exactly or approximatly, should be a boolean
    # progress:     How to show how much time is remaining, False if it should be disabled
    #               a number to show time remaining with a period >= progress
    def solve(self, exact = False, progress = False):
        Time1 = time.time()
        
        # Do it exact
        if exact is True:
            self.__A = solve_exact(self.__J(self.__t), self.__lapl, self.__C(self.__t), self.__mu0, self.__dx)
            
        # Do it approximatly
        else:
            self.__A = solve_approx(self.__J(self.__t), self.__lapl, self.__C(self.__t), self.__mu0, self.__dx, self.__A, self.__n, self.__k, progress = progress)
            
        Time2 = time.time()
        
        # Run samplers
        self.run_samplers()
        
        # Reset derived values
        self.__reset_derived()
        
        return Time2 - Time1
    
    def dynamics(self, Count, SubCount, exact = False, progress = False):
        Time1 = time.time()
        Time = OriginalTime = Time1

        # Go through all of the steps
        for n in range(Count):
            # Show progress
            NewTime = time.time()
            if progress is not False and NewTime > Time + progress:
                Time = NewTime
                print("%.2g s remaining" %((Time - OriginalTime) / n * (Count - n)))

            # Do the substeps
            for _ in range(SubCount):
                self.__A, self.__dAdt = solve_dynamics(self.__A, self.__dAdt, self.__J(self.__t + self.__dt / 2), self.__lapl, self.__C(self.__t + self.__dt / 2), self.__dx, self.__dt, self.__c, self.__mu0, self.__nDyn, exact = exact)
                
                # Add to the time
                self.__t += self.__dt
                
            # Run samplers
            self.run_samplers()
            
            # Reset the fields
            self.__reset_derived()

        # Calculate ellapsed time
        Time2 = time.time()
                        
        return Time2 - Time1
    
    # Samples values at specific points from a field, interpolate to get smooth values from field
    # Return the values in the shape Points.shape[1:]
    #
    # Field:        The field to sample values from in vector from, this can also be a vector field
    # Points:       An array with the x,y,z coordinates in the first axis
    def sample_values(self, Field, Points):
        return sample_values(Field, Points, self.__dx, self.__N, self.__x0)
        
    # Samples vectors at specific points from a field projected onto a 2D plane, interpolate to get smooth values from field
    # Return the values in the shape Points.shape[1:]
    #
    # Field:        The field to sample values from in vector from, this has to be a vector field
    # Points:       An array with the x,y,z coordinates in the first axis
    # hat:          An array defining the directions of the hat vectors, it should have a shape of type 
    #               (SomeShape, 3, N) where (SomeShape can be any shape with len(SomeShape) <= len(Points.shape))
    #               if it is < then it will be changed to shape (SomeShape, 1, 1...) until it is long enough.
    #               N is the number of hat vectors, it can also have shape (SomeShape, 3) but then you should set single = True
    # single:       Set to True if you have no N dimension on the hat array
    def sample_vectors(self, Field, Points, hat, single = False):
        return sample_vectors(Field, Points, hat, self.__dx, self.__N, self.__x0, single = single)
        
    # Adds a sampler to the simulation
    #
    # Sampler:      The sampler to add, this will be run every time step/solve is run
    def add_sampler(self, sampler):
        self.__samplers.append(sampler)
    
    # Run all the samplers
    def run_samplers(self):
        for sampler in self.__samplers:
            sampler.sample()

    
# Creates a video
#
# Name:         The name of the video file to be saved
# FPS:          How many frames per second the video should have
# figsize:      The size of the figure in
# dpi:          The resolution of the figure
class video:
    def __init__(self, Name, FPS = 30, figsize = np.array([10., 10.]), dpi = 100):
        # Create hidden figure
        plt.ioff()
        self.__fig, self.__ax = plt.subplots(figsize = figsize, dpi = dpi)
        plt.ion()
        
        # Create video
        self.__v = cv2.VideoWriter(Name, cv2.VideoWriter_fourcc(*'DIVX'), FPS, tuple((figsize * dpi).astype(int)))
        self.__active = True
        
    def __del__(self):
        self.finish()
        
    # Retrieve the fig and ax
    def get_fig(self):
        return self.__fig, self.__ax
    
    # Create one frame in the video
    def update(self):
        # Convert figure to image
        # Draw figure to canvas
        self.__fig.canvas.draw()
        
        # Get shape
        Width, Height = self.__fig.canvas.get_width_height()
        
        # Convert to numpy array
        Buffer = np.fromstring(self.__fig.canvas.tostring_rgb(), dtype = np.uint8)
        
        # Convert buffer to image
        Image = Buffer.reshape((Height, Width, 3))
    
        # Convert to cv2 colours
        Image = cv2.cvtColor(Image, cv2.COLOR_RGB2BGR)
        
        # Draw to video
        self.__v.write(Image)
        
    # Finishes the video
    def finish(self):
        if self.__active is True:
            # Close figure
            plt.close(self.__fig)
            
            # Close video
            self.__v.release()
            
            self.__active = False
          
    # Plot a scalar field
    #
    # Values:       The 2D array of values to plot
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the scalar field with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    def plot_scalar(self, Values, extent = [0, 1, 0, 1], scale = default_scale, cmap = "coolwarm", clim = None):
        # Save scale
        self.__scale = scale
                
        # Plot
        _, _, self.__plot = plot_scalar(Values, extent = extent, scale = scale, fig = self.__fig, ax = self.__ax, cmap = cmap, clim = clim)
    
    # Updates a scalar field
    #
    # Values:       The 2D array of values to plot
    def update_scalar(self, Values):
        update_plot_scalar(self.__plot, Values, scale = self.__scale)
    
    # Plots contour lines
    #
    # Values:       The 2D array of values to plot
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # levels:       The levels to draw contours for, if an int then they will be evenly spaced between clim[0] and clim[1].
    #               Can also be a list/array of levels in increasing order
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the scalar field with, used if use_cmap is True
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    # colors:       Matplotlib colour string or a list of colours to give each contour their own colour, only used if use_cmap is False
    # use_cmap:     True if the cmap should determine the colours, false if they should be determined by color
    # linestyles:   The linestyles to draw the contours with, a string if all contours should use same linestyle or a list of string for different linestyles
    def plot_contour(self, Values, extent = [0, 1, 0, 1], levels = 10, scale = default_scale, cmap = "coolwarm", clim = None, colors = "black", use_cmap = False, linestyles = "solid"):
        # Save the scale
        self.__scale = scale
        
        # Plot
        _, _, self.__plot = plot_contour(Values, extent = extent, levels = levels, scale = scale, fig = self.__fig, ax = self.__ax, cmap = cmap, colors = colors, use_cmap = use_cmap, clim = clim, linestyles = linestyles)
        
    # Updates a contour plot
    #
    # Values:       The 2D array of new values to plot
    def update_contour(self, Values):
        update_plot_scalar(self.__plot, Values, scale = self.__scale)
    
    # Plots a 1D curve
    #
    # Values:       The 1D array of values to plot
    # x:            The x values, this should be same shape as Values or None
    # xlim:         The limit of x values to look at, set to None to let matplotlib do it automatically
    # ylim:         The limit of y values to look at, set to None to let matplotlib do it automatically
    # scale:        Function to scale the values of the field
    # fmt:          The fmt data of the plot, this is the colour and type of plot
    # label:        The label of the curve
    def plot_1D(self, Values, x = None, xlim = None, ylim = None, scale = default_scale, fmt = "-", label = ""):
        # Save scale
        self.__scale = scale
                
        # Plot
        _, _, self.__plot = plot_1D(Values, x = x, xlim = xlim, ylim = ylim, scale = scale, fig = self.__fig, ax = self.__ax, fmt = fmt, label = label)
    
    # Updates a 1D curve
    #
    # Values:       The 1D array of values to plot
    def update_1D(self, Values):
        update_plot_1D(self.__plot, Values, scale = self.__scale)
    
    # Plots a vector field
    #
    # vx:           The x-component of the vectors
    # vy:           The y-component of the vectors
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the scalar field with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    # cutoff:       Determines a cutoff point where if vectors are shorter than the length of the longest vector times cutoff, then it is not shown
    def plot_vector(self, vx, vy, extent = [0, 1, 0, 1], scale = default_scale, cmap = "coolwarm", clim = None, cutoff = 0):
        # Save scale
        self.__scale = scale
        
        # Find cutoff
        if clim is None:
            self.__cutoff = cutoff * np.max(vx ** 2 + vy ** 2)
            
        else:
            self.__cutoff = cutoff * clim[1]
        
        # Plot
        _, _, self.__plot = plot_vector(vx, vy, extent = extent, scale = scale, fig = self.__fig, ax = self.__ax, cmap = cmap, clim = clim, cutoff = cutoff)
        
    # Updates a vector field
    #
    # vx:           The x-component of the vectors
    # vy:           The y-component of the vectors
    def update_vector(self, vx, vy):
        update_plot_vector(self.__plot, vx, vy, scale = self.__scale, cutoff = self.__cutoff)
        
    # Plot a vector stream
    #
    # vx:           The vector components along the x axis to plot
    # vy:           The vector components along the y axis to plot
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the vectors with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the vector lengths,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values of the lengths
    # density:      How many stream lines should be drawn
    # length:       The minimum length of the lines (In some scaled coordinates)
    def plot_streams(self, vx, vy, extent = [0, 1, 0, 1], scale = default_scale, cmap = "coolwarm", clim = None, density = 1, length = 1):
        # Save scale
        self.__scale = scale
        
        # Plot
        _, _, self.__plot = plot_streams(vx, vy, extent = extent, scale = scale, fig = self.__fig, ax = self.__ax, cmap = cmap, clim = clim, density = density, length = length)
        
    # Updates a stream plot
    #
    # vx:           The x-component of the vectors
    # vy:           The y-component of the vectors
    def update_streams(self, vx, vy):
        update_plot_streams(self.__plot, vx, vy, scale = self.__scale)
        

# A class to take samples of a simulation every timestep
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
class sampler:
    def __init__(self, Sim):
        # Make sure it has gotten a simulation
        if not isinstance(Sim, sim):
            raise Exception(f"Sim has wrong type, it is {str(type(Sim)):s} but it should be {str(sim):s}")
        
        # Set the simulation
        self.sim = Sim

        # Add the sampler to the simulation
        self.sim.add_sampler(self)

        # Initialise the data
        self.data = []
        self.t = []
    
    # Take one sample
    #
    # Sim:      The simulation the sample is to be taken from
    def sample(self):
        self.t.append(self.sim.get_t())
        
    # Defines what to sample
    def sample_data(self):
        pass
    
    # Retrieves all the samples stored
    def get_samples(self):
        return self.t, self.data
    

# A sampler which samples numbers each timestep
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
class sampler_number(sampler):
    # Plots the data with t on the x-axis
    #
    # fmt:          The fmt data for the plot, this is the type of curve and colour
    # title:        The title of the plot
    # xlabel:       The xlabel of the plot
    # ylabel:       The ylabel of the plot
    # label:        The label of the curve
    # legend:       Set to True if you want a legend
    # figsize:      The figure size, if ax is given this is ignored
    # dpi:          The resolution of the plot, if ax is given this is ignored
    # ax:           The ax to plot on, if None it will create its own
    def plot(self, fmt = "-", title = "", xlabel = "", ylabel = "", label = "", legend = False, figsize = (10, 10), dpi = 100, ax = None):
        # Create the plot
        if ax is None:
            fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
        
        else:
            fig = None
        
        # Plot the data
        ax.plot(self.t, self.data, fmt, label = label)
        
        # Set labels
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Add legend
        if legend is True:
            ax.legend()
            
        # Return the figure
        return fig, ax
    
    # Take one sample
    def sample(self):
        super().sample()
        
        # Get the number
        self.data.append(self.sample_data())


# A sampler which samples a field each timestep
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# single:   True if you don't include the N-dimension in the hat vector
class sampler_field(sampler):
    def __init__(self, Sim, Points, hat = None, single = False):
        super().__init__(Sim)
        
        # Make sure points are of correct type
        if not isinstance(Points, np.ndarray):
            raise Exception(f"Points has wrong type, it is {str(type(Points)):s} but it should be {str(np.ndarray):s}")

        # Save the points
        self.points = Points

        # Make sure the hat is None or an array
        if not (isinstance(hat, np.ndarray) or hat is None):
            raise Exception(f"hat has wrong type, it is {str(type(hat)):s} but it should be {str(np.ndarray):s} or None")
            
        # Save the hat
        self.hat = hat
        
        # Make sure single is of correct type
        if not isinstance(single, bool):
            raise Exception(f"single has wrong type, it is {str(type(single)):s} but it should be {str(bool):s}")
        
        # Save the single
        self.single = single
    
    # Takes a sample from the simulation
    def sample(self):
        super().sample()

        # Sample from a scalar field
        if self.hat is None:
            self.data.append(self.sim.sample_values(self.sample_data(), self.points).copy())
            
        # Sample from a vector
        else:
            self.data.append(self.sim.sample_vectors(self.sample_data(), self.points, self.hat, single = self.single).copy())
        
        
    # Creates a video using the data it has samples
    #
    # Name:         The name of the video file to be saved
    # FPS:          How many frames per second the video should have
    # figsize:      The size of the figure in
    # dpi:          The resolution of the figure
    def make_video(self, Name, FPS = 30, figsize = np.array([10., 10.]), dpi = 100):
        # Create the video object
        self.video = video(Name, FPS = FPS, figsize = figsize, dpi = dpi)
        
        # Start the video
        self.start_video(self.t[0], self.data[0])
        self.video.update()
        
        # Create the video
        for t, data in zip(self.t[1:], self.data[1:]):
            self.update_video(t, data)
            self.video.update()
            
        # Finish the video
        self.video.finish()
                
    # Creates the first frame of a video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def start_video(self, t, Data):
        pass
    
    # Create the next frame of the video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def update_video(self, t, Data):
        pass
        

# A sampler which samples a field in 2D
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_field_scalar(sampler_field):
    def __init__(self, Sim, Points, hat = None):
        super().__init__(Sim, Points, hat = hat, single = True)
        
    # Creates a video using the data it has sampled
    #
    # Name:         The name of the video file to be saved
    # FPS:          How many frames per second the video should have
    # figsize:      The size of the figure in
    # dpi:          The resolution of the figure
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the scalar field with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    # contour_lim   A two array or tuple containing the lower and upper bounds for the contour lines
    # levels:       The levels to draw contours for, if an int then they will be evenly spaced between clim[0] and clim[1].
    #               Can also be a list/array of levels in increasing order
    # colors:       Matplotlib colour string or a list of colours to give each contour their own colour, only used if use_cmap is False
    # linestyles:   The linestyles to draw the contours with, a string if all contours should use same linestyle or a list of string for different linestyles
    # use_scalar:   True if it should plot the scalar field
    # use_contour:  True if it should plot the contours
    def make_video(self, Name, FPS = 30, figsize = np.array([10., 10.]), dpi = 100, extent = [0, 1, 0, 1], scale = default_scale, cmap = "coolwarm", clim = None, contour_lim = None, levels = 10, colors = "black", linestyles = "solid", use_scalar = True, use_contour = False):
        # Save data
        self.extent = extent
        self.scale = scale
        self.cmap = cmap
        self.clim = clim
        self.contour_lim = contour_lim
        self.levels = levels
        self.linestyles = linestyles
        self.colors = colors
        self.use_scalar = use_scalar
        self.use_contour = use_contour

        # Make the video
        super().make_video(Name, FPS = FPS, figsize = figsize, dpi = dpi)
                
    # Creates the first frame of a video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def start_video(self, t, Data):
        # Plot the scalar
        if self.use_scalar is True:
            self.video.plot_scalar(Data, extent = self.extent, scale = self.scale, cmap = self.cmap, clim = self.clim)
    
        # Plot the contours
        if self.use_contour is True:
            self.video.plot_contour(Data, extent = self.extent, levels = self.levels, scale = self.scale, colors = self.colors, use_cmap = False, linestyles = self.linestyles, clim = self.contour_lim)
    
    # Create the next frame of the video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def update_video(self, t, Data):
        # Update the scalar
        if self.use_scalar is True:
            self.video.update_scalar(Data)
        
        # Plot the contours
        if self.use_contour is True:
            self.video.update_contour(Data)
    
    # Plots the scalar field at some time
    #
    # t:            The time from which to take the data, it will find the data closest to this time
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # ax:           The axes to draw the plot inside
    # fig:          The figure to draw in, if given then ax must also be given
    # figsize:      The size of the figure if ax is not given
    # dpi:          The resolution of the figure if ax is not given
    # cmap:         The colour map to plot the scalar field with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    # contour_lim   A two array or tuple containing the lower and upper bounds for the contour lines
    # levels:       The levels to draw contours for, if an int then they will be evenly spaced between clim[0] and clim[1].
    #               Can also be a list/array of levels in increasing order
    # colors:       Matplotlib colour string or a list of colours to give each contour their own colour, only used if use_cmap is False
    # linestyles:   The linestyles to draw the contours with, a string if all contours should use same linestyle or a list of string for different linestyles
    # use_scalar:   True if it should plot the scalar field
    # use_contour:  True if it should plot the contours
    def plot(self, t, extent = [0, 1, 0, 1], scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", clim = None, contour_lim = None, levels = 10, colors = "black", linestyles = "solid", use_scalar = True, use_contour = False):
        # Find the correct data
        Dist = np.abs(np.array(self.t) - t)
        Pos = np.argmin(Dist)
        
        Data = self.data[Pos]
        Plot1 = None
        Plot2 = None
        
        # Plot the data
        if use_scalar is True:
            fig, ax, Plot1 = plot_scalar(Data, extent = extent, scale = scale, fig = fig, ax = ax, figsize = figsize, dpi = dpi, cmap = cmap, clim = clim)

        if use_contour is True:
            fig, ax, Plot2 = plot_contour(Data, extent = extent, levels = levels, fig = fig, ax = ax, figsize = figsize, dpi = dpi, clim = contour_lim, colors = colors, use_cmap = False, linestyles = linestyles)

        return fig, ax, (Plot1, Plot2)

# A sampler which samples a vector field in 2D
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_field_vector(sampler_field):
    def __init__(self, Sim, Points, x_hat, y_hat):
        # Collect the hats
        hat = np.append(x_hat.reshape(x_hat.shape + (1,)), y_hat.reshape(y_hat.shape + (1,)), axis = -1)
        
        super().__init__(Sim, Points, hat = hat, single = False)

    # Creates a video using the data it has sampled
    #
    # Name:         The name of the video file to be saved
    # FPS:          How many frames per second the video should have
    # figsize:      The size of the figure in
    # dpi:          The resolution of the figure
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # cmap:         The colour map to plot the scalar field with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the field,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values in the field
    # cutoff:       Determines a cutoff point where if vectors are shorter than the length of the longest vector times cutoff, then it is not shown
    # density:      How many stream lines should be drawn
    # length:       The minimum length of the stream lines (In some scaled coordinates)
    # use_vector:   True if it should plot the vector field
    # use_streams:  True if it should plot the streamlines
    def make_video(self, Name, FPS = 30, figsize = np.array([10., 10.]), dpi = 100, extent = [0, 1, 0, 1], scale = default_scale, cmap = "coolwarm", clim = None, cutoff = 0, density = 1, length = 1, use_vector = True, use_streams = False):
        # Save the data
        self.extent = extent
        self.scale = scale
        self.cmap = cmap
        self.clim = clim
        self.cutoff = cutoff
        self.density = density
        self.length = length
        self.use_vector = use_vector
        self.use_streams = use_streams

        # Make the video
        super().make_video(Name, FPS = FPS, figsize = figsize, dpi = dpi)
                
    # Creates the first frame of a video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def start_video(self, t, Data):
        # Plot the data
        if self.use_vector is True:
            self.video.plot_vector(Data[:, :, 0], Data[:, :, 1], extent = self.extent, scale = self.scale, cmap = self.cmap, clim = self.clim, cutoff = self.cutoff)
    
        if self.use_streams is True:
            self.video.plot_streams(Data[:, :, 0], Data[:, :, 1], extent = self.extent, scale = self.scale, cmap = self.cmap, clim = self.clim, density = self.density, length = self.length)
    
    # Create the next frame of the video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def update_video(self, t, Data):
        # Update the data
        if self.use_vector is True:
            self.video.update_vector(Data[:, :, 0], Data[:, :, 1])
            
        if self.use_streams is True:
            self.video.update_streams(Data[:, :, 0], Data[:, :, 1])
        
    # Plots a vector field
    #
    # t:            The time from which to take the data, it will find the data closest to this time
    # extent:       Used to label the axis must be given as [x_min, x_max, y_min, y_max]
    # scale:        Function to scale the values of the field
    # fig:          The figure to draw in, if given then ax must also be given
    # ax:           The axes to draw the plot inside
    # figsize:      The size of the figure if ax is not given
    # dpi:          The resolution of the figure if ax is not given
    # cmap:         The colour map to plot the vectors with
    # clim:         Array containing the (min, max) values in the colour map, these are the raw values of the vector lengths,
    #               not the scaled values, if None then it will find the scale automatially by the minimum and maximum
    #               values of the lengths
    # density:      How many stream lines should be drawn
    # length:       The minimum length of the stream lines (In some scaled coordinates)
    # use_vector:   True if it should plot the vector field
    # use_streams:  True if it should plot the streamlines
    def plot(self, t, extent = [0, 1, 0, 1], scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, cmap = "coolwarm", clim = None, cutoff = 0, density = 1, length = 1, use_vector = True, use_streams = False):
        # Find the correct data
        Dist = np.abs(np.array(self.t) - t)
        Pos = np.argmin(Dist)
        
        Data = self.data[Pos]
        Plot1 = None
        Plot2 = None
        
        # Plot the data
        if use_vector is True:
            fig, ax, Plot1 = plot_vector(Data[:, :, 0], Data[:, :, 1], extent = extent, scale = scale, fig = fig, ax = ax, figsize = figsize, dpi = dpi, cmap = cmap, clim = clim, cutoff = cutoff)
        
        if use_streams is True:
            fig, ax, Plot2 = plot_streams(Data[:, :, 0], Data[:, :, 1], extent = extent, scale = scale, fig = fig, ax = ax, figsize = figsize, dpi = dpi, cmap = cmap, clim = clim, density = density, length = length)
        
        return fig, ax, (Plot1, Plot2)


# A sampler to sample a field along a line
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_field_line(sampler_field):
    def __init__(self, Sim, Points, x = None, hat = None):
        super().__init__(Sim, Points, hat = hat, single = True)
        
        # Set x
        self.x = x

    # Creates a video using the data it has sampled
    #
    # Name:         The name of the video file to be saved
    # FPS:          How many frames per second the video should have
    # figsize:      The size of the figure in
    # dpi:          The resolution of the figure
    # xlim:         The limit of x values to look at, set to None to let matplotlib do it automatically
    # ylim:         The limit of y values to look at, set to None to let matplotlib do it automatically
    # scale:        Function to scale the values of the field
    # fmt:          The fmt data of the plot, this is the colour and type of plot
    # label:        The label of the curve
    def make_video(self, Name, FPS = 30, figsize = np.array([10., 10.]), dpi = 100, xlim = None, ylim = None, scale = default_scale, fmt = "", label = ""):
        # Save the data
        self.xlim = xlim
        self.ylim = ylim
        self.scale = scale
        self.fmt = fmt
        self.label = label

        # Make the video
        super().make_video(Name, FPS = FPS, figsize = figsize, dpi = dpi)
                
    # Creates the first frame of a video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def start_video(self, t, Data):
        # Plot the data
        self.video.plot_1D(Data, x = self.x, xlim = self.xlim, ylim = self.ylim, scale = self.scale, fmt = self.fmt, label = self.label)
    
    # Create the next frame of the video
    #
    # t:        The timestamp of the frame
    # Data:     The data for the frame
    def update_video(self, t, Data):
        # Update the data
        self.video.update_1D(Data)
        
    # Plot the data for some time
    #
    # Values:       The 1D array of values to plot
    # xlim:         The limit of x values to look at, set to None to let matplotlib do it automatically
    # ylim:         The limit of y values to look at, set to None to let matplotlib do it automatically
    # scale:        Function to scale the values of the field
    # ax:           The axes to draw the plot inside
    # fig:          The figure to draw in, if given then ax must also be given
    # figsize:      The size of the figure if ax is not given
    # dpi:          The resolution of the figure if ax is not given
    # fmt:          The fmt used for plotting
    def plot(self, t, xlim = None, ylim = None, scale = default_scale, fig = None, ax = None, figsize = np.array([10., 10.]), dpi = 100, fmt = "-", label = ""):
        # Find the correct data
        Dist = np.abs(np.array(self.t) - t)
        Pos = np.argmin(Dist)
        
        Data = self.data[Pos]
        
        # Plot the data
        return plot_1D(Data, x = self.x, xlim = xlim, ylim = ylim, scale = scale, fig = fig, ax = ax, figsize = figsize, dpi = dpi, fmt = fmt, label = label)
        

# A list of standard samplers which can be imported

# Samples from the scalar potential
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
class sampler_V_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points):
        super().__init__(Sim, Points)
            
    def sample_data(self):
        return self.sim.get_V()
    
    
# Samples from the scalar potential
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_V_line(sampler_field_line):
    def __init__(self, Sim, Points, x = None):
        super().__init__(Sim, Points, x = x)
            
    def sample_data(self):
        return self.sim.get_V()
    
    
# Samples from the vector potential
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_A_vector(sampler_field_vector):
    def __init__(self, Sim, Points, x_hat, y_hat):
        super().__init__(Sim, Points, x_hat, y_hat)
            
    def sample_data(self):
        return self.sim.get_A()


# Samples from the vector potential
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_A_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points, hat):
        super().__init__(Sim, Points, hat = hat)
            
    def sample_data(self):
        return self.sim.get_A()
    
    
# Samples from the vector potential
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_A_line(sampler_field_line):
    def __init__(self, Sim, Points, hat, x = None):
        super().__init__(Sim, Points, hat = hat, x = x)
            
    def sample_data(self):
        return self.sim.get_A()
    
    
# Samples from the E-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_E_vector(sampler_field_vector):
    def __init__(self, Sim, Points, x_hat, y_hat):
        super().__init__(Sim, Points, x_hat, y_hat)
            
    def sample_data(self):
        return self.sim.get_E()


# Samples from the E-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_E_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points, hat):
        super().__init__(Sim, Points, hat = hat)
            
    def sample_data(self):
        return self.sim.get_E()
    
    
# Samples from the E-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_E_line(sampler_field_line):
    def __init__(self, Sim, Points, hat, x = None):
        super().__init__(Sim, Points, hat = hat, x = x)
            
    def sample_data(self):
        return self.sim.get_E()
    
    
# Samples from the B-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_B_vector(sampler_field_vector):
    def __init__(self, Sim, Points, x_hat, y_hat):
        super().__init__(Sim, Points, x_hat, y_hat)
            
    def sample_data(self):
        return self.sim.get_B()


# Samples from the B-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_B_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points, hat):
        super().__init__(Sim, Points, hat = hat)
            
    def sample_data(self):
        return self.sim.get_B()
    
    
# Samples from the B-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_B_line(sampler_field_line):
    def __init__(self, Sim, Points, hat, x = None):
        super().__init__(Sim, Points, hat = hat, x = x)
            
    def sample_data(self):
        return self.sim.get_B()
    

# Samples from the S-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_S_vector(sampler_field_vector):
    def __init__(self, Sim, Points, x_hat, y_hat):
        super().__init__(Sim, Points, x_hat, y_hat)
            
    def sample_data(self):
        return self.sim.get_S()


# Samples from the S-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_S_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points, hat):
        super().__init__(Sim, Points, hat = hat)
            
    def sample_data(self):
        return self.sim.get_S()
    
    
# Samples from the S-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_S_line(sampler_field_line):
    def __init__(self, Sim, Points, hat, x = None):
        super().__init__(Sim, Points, hat = hat, x = x)
            
    def sample_data(self):
        return self.sim.get_S()


# Samples from the energy density
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
class sampler_u_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points):
        super().__init__(Sim, Points)
            
    def sample_data(self):
        return self.sim.get_u()
    
    
# Samples from the energy density
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_u_line(sampler_field_line):
    def __init__(self, Sim, Points, x = None):
        super().__init__(Sim, Points, x = x)
            
    def sample_data(self):
        return self.sim.get_u()


# Samples the total energy
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
class sampler_U_number(sampler_number):
    def sample_data(self):
        return np.sum(self.sim.get_u()) * np.prod(self.sim.get_dx())


# Samples from the J-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x_hat:    The x direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors.
# y_hat:    The y direction, should have unit norm, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors, it should be the same shape as for x_hat
class sampler_J_vector(sampler_field_vector):
    def __init__(self, Sim, Points, x_hat, y_hat):
        super().__init__(Sim, Points, x_hat, y_hat)
            
    def sample_data(self):
        return self.sim.get_J()


# Samples from the J-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
class sampler_J_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points, hat):
        super().__init__(Sim, Points, hat = hat)
            
    def sample_data(self):
        return self.sim.get_J()
    
    
# Samples from the J-field
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# hat:      An array defining the directions of the hat vector, it should have a shape of type 
#           Points.shape + (3,) or (3,) for constant vectors. Leave as None if sampling from a scalar field
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_J_line(sampler_field_line):
    def __init__(self, Sim, Points, hat, x = None):
        super().__init__(Sim, Points, x = x, hat = hat)
            
    def sample_data(self):
        return self.sim.get_J()
    

# Samples from the charge desnity
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
class sampler_Rho_scalar(sampler_field_scalar):
    def __init__(self, Sim, Points):
        super().__init__(Sim, Points)
            
    def sample_data(self):
        return self.sim.get_Rho()
    
    
# Samples from the charge desnity
#
# Sim:      The simulation to sample from, it will automatically add this sampler to the sim
# Points:   numpy array of all the points to sample from, the x,y,z-coordinates are in the first axis
# x:        The x-values for the different points, should have same shape as Points except for the coordinate axis
class sampler_Rho_line(sampler_field_line):
    def __init__(self, Sim, Points, x = None):
        super().__init__(Sim, Points, x = x)
            
    def sample_data(self):
        return self.sim.get_Rho()
