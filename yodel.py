def getNeighboringPoints(xy):
	p = set()
	for x in xrange(xy[0]-1, xy[0]+1):
		for y in xrange(xy[1]-1, xy[1]+1):
			p.add((x, y))
	p.remove(xy)
	return p

def textToLines(text):
	return filter(None, text.strip("\n").split("\n"))

class Polygon(object):
	def __init__(self):
		self.points = self.lines = self.world = self.polys = None
		self.textLines = None
		self.width = self.height = 0
	
	def readText(self, lines):
		if not isinstance(lines, list):
			lines = textToLines(lines)
		self.textLines = lines
			
		world = {}
		points = set()
		width = height = 0

		for y, line in enumerate(lines):
			for x, c in enumerate(line):
				if c != " ":
					world[x,y] = c
				if c == "#":
					points.add((x,y))
					width = max(x, width)
					height = max(y, height)
					
		wg = lambda x,y: world.get((x,y))
		def follow(xy, dx, dy, cc):
			x, y = xy
			seen = set()
			hopPointAllow = "#."+cc
			while True:
				x += dx
				y += dy
				seen.add((x,y))
				c = wg(x, y)
				if c == "#":
					return (x,y)
				elif c == ".": # Deal with hop points.
					f = False
					for nxy in getNeighboringPoints((x,y)):
						nc = wg(nxy[0], nxy[1])
						if nc in hopPointAllow and (nxy not in seen):
							if nc == "#":
								return nxy
							else:
								x, y = nxy
								f = True
								break
					if f:
						continue
				elif c != cc:
					return None
				
		#print points.keys()
		lines = set()
		def addLine(p0, p1):
			if p0 != p1:
				line = tuple(sorted((p0, p1)))
				#print "adding line %r"%(line,)
				lines.add(line)
	
		ttab = [
			( 1,  0, "-"),
			(-1,  0, "-"),
			( 0, -1, "|"),
			( 0,  1, "|"),
			(-1, -1, "\\"),	#up-left
			( 1,  1, "\\"),	#dn-right
			( 1, -1, "/"),	#up-right
			(-1,  1, "/"),	#dn-left
		]
		
		for xy in sorted(points):
			for nxy in getNeighboringPoints(xy):
				if nxy in points:
					addLine(xy, nxy)
			for dx,dy,c in ttab:
				f = follow(xy, dx, dy, c)
				if f:
					addLine(xy, f)
					
		self.width = width
		self.height = height
		self.points = points
		self.lines = sorted(lines)
		self.world = world
		
	def linesToPolys(self):
		if not self.lines:
			raise ValueError("No lines to polygonize.")
		lines = list(self.lines)
		polys = []
		
		while lines:
			l = lines.pop(0)
			poly = []
			polys.append(poly)
			while True:
				c, n = l
				poly.append(c)
				for l in lines:
					if l[0] == n:
						lines.remove(l)
						break
					elif l[1] == n:
						lines.remove(l)
						l = l[::-1]
						break
				else:
					poly.append(n)
					break
		self.polys = polys
		
	@classmethod
	def fromText(cls, text, polygonize = True):
		poly = cls()
		poly.readText(text)
		if polygonize:
			poly.linesToPolys()
		return poly
