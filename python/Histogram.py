#!/usr/bin/env python
from numpy import amax, histogram2d
from matplotlib import pyplot
import logging, matplotlib

logger = logging.getLogger(__name__)

class Histogram2D:
	def __init__(self, a, xlabel='length: l', ylabel='start: s',
			title='s/l distribution'):
		self.a = a
		logger.debug("a: %s" % self.a)
		self.xmax, self.ymax = amax(self.a.T, axis=0)
		logger.debug("xmax: %s, ymax: %s" % (self.xmax, self.ymax))
		if self.xmax == 0.:
			self.xmax = 1.
		if self.ymax == 0.:
			self.ymax = 1.
		self.histogram, self.xedges, self.yedges = histogram2d(a[0], a[1],
				normed = True,
			bins=[self.xmax, self.ymax])
		self.extent = [self.yedges[0], self.yedges[-1], self.xedges[-1],
				self.xedges[0]]
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.title = title
	@property
	def plot(self):
		im = pyplot.imshow(self.histogram, extent=self.extent,
				norm=matplotlib.colors.Normalize(vmin=0.,vmax=1.),
				interpolation='bicubic'
		)
		im.axes.set_ylabel(self.ylabel)
		im.axes.set_xlabel(self.xlabel)
		im.axes.set_title(self.title)
		im.colorbar = pyplot.colorbar()
		return im

