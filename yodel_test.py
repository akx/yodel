import cairo, math, yodel

def testCairoGetCtx(surf, w, h):
	ctx = cairo.Context(surf)
	ctx.set_source_rgb(1,1,1)
	ctx.paint()
	scl = (760.0 / float(max(w, h)))
	mtrx = cairo.Matrix(scl, 0, 0, scl, 20, 20)
	ctx.set_matrix(mtrx)
	for y in xrange(0, h + 1):
		for x in xrange(0, w + 1):
			ctx.new_path()
			ctx.set_source_rgba(0,0,0, .3)
			ctx.arc(x, y, 0.05, 0, 2*math.pi)
			ctx.fill()
	return ctx

def ttpCairoTest(text, surf):
	poly = yodel.Polygon.fromText(text, False)
	ctx = testCairoGetCtx(surf, poly.width, poly.height)
		
	for l in poly.lines:
		(x0, y0), (x1, y1) = l
		
		ctx.new_path()
		ctx.set_line_width(0.1)
		ctx.set_source_rgb(0,0,0)
		ctx.move_to(x0, y0)
		ctx.line_to(x1, y1)
		ctx.stroke()
		
	for xy in poly.points:
		x, y = xy
		ctx.new_path()
		ctx.set_line_width(0.2)
		ctx.arc(x, y, .2, 0, 2*math.pi)
		ctx.set_source_rgba(1,0,0,.5)
		ctx.fill()	
	
	ctx.set_source_rgba(0,0,1,1)
	ctx.identity_matrix()
	ctx.select_font_face("Courier New")
	ctx.set_font_size(20)
	for y, l in enumerate(poly.textLines):
		ctx.move_to(800, 20 + y*25)
		ctx.show_text(l)

def ttpCairoPNG(text, outfile):
	surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 800)
	ttpCairoTest(text, surf)
	surf.write_to_png(outfile)

def ttpCairoPDF(text, outfile):
	surf = cairo.PDFSurface(outfile, 1200, 800)
	ttpCairoTest(text, surf)
	
def ttpolyCairoPNG(text, outfile):
	poly = yodel.Polygon.fromText(text, True)
	surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 800)
	ctx = testCairoGetCtx(surf, poly.width, poly.height)
	for poly in poly.polys:
		ctx.new_path()
		ctx.set_line_width(0.1)
		
		for idx, p in enumerate(poly):
			if idx == 0:
				ctx.move_to(*p)
			else:
				ctx.line_to(*p)
		ctx.close_path()
		ctx.set_source_rgba(1,0,0,0.5)
		ctx.fill_preserve()
		ctx.set_source_rgb(0,0,0)
		ctx.stroke()
		
	surf.write_to_png(outfile)
	

c1="""
#----#-----#
|          |
|   #--#---#
|   .
|  / 
#-# 
"""

c2="""
 #----#
#      #
|  #--#
| #
|  #--#
#      #
 #----#
"""
ttpolyCairoPNG(c2, "yodel_poly.png")
ttpCairoPNG(c2, "yodel_tmp.png")
