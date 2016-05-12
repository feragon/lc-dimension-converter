import ezdxf
from math import sqrt

dxf = ezdxf.readfile("input.dxf")

modelspace = dxf.modelspace()
dimensions = modelspace.query('DIMENSION')

for dimension in dimensions:
	block_name = dimension.dxf.geometry
	
	if(dimension.dxf.dimtype == 128):
		print("Adding block", block_name, "to Dimension")

		for b in dxf.blocks:
			if(b.name == block_name):
				#Add dimension points
				points = b.query('POINT')
				dimension.dxf.defpoint = dimension.dxf.text_midpoint
				dimension.dxf.defpoint2 = points[0].dxf.location
				dimension.dxf.defpoint3 = points[1].dxf.location
				dimension.dxf.angle = 0

				#Check if horizontal or vertical
				lines = b.query('LINE')
				for line in lines:
					if(line.dxf.start[1] == dimension.dxf.defpoint2[1] or
					line.dxf.end[1] == dimension.dxf.defpoint2[1] or
					line.dxf.start[1] == dimension.dxf.defpoint3[1] or
					line.dxf.end[1] == dimension.dxf.defpoint3[1]):
						dimension.dxf.angle = 90

		print("Point 1:", dimension.dxf.defpoint2)
		print("Point 2:", dimension.dxf.defpoint3)	
		print("Text pos:", dimension.dxf.text_midpoint)
		print("Angle:", dimension.dxf.angle)
		
	if(dimension.dxf.dimtype == 130):
		origin = tuple()
		point1 = tuple()
		point2 = tuple()
		
		print("Adding block", block_name, "to Dimension Angular")
		for b in dxf.blocks:
			if(b.name == block_name):
				radius = float()
				arcs = b.query('ARC')
				for arc in arcs:
					origin = arc.dxf.center
					radius = round(arc.dxf.radius, 2)
					
				lines = b.query('LINE')
				for line in lines:
					distance = round(sqrt(pow(origin[0] - line.dxf.start[0],2) + pow(origin[1] - line.dxf.start[1],2)), 2)
					if(distance == radius):
						if(point1 == tuple()):
							point1 = line.dxf.start
						else:
							point2 = line.dxf.start

		print("Origin:", origin)
		print("Point1:", point1)
		print("Point2:", point2)

		dimension.dxf.defpoint = origin
		dimension.dxf.defpoint4 = point1
		
		dimension.dxf.defpoint2 = origin
		dimension.dxf.defpoint3 = point2
		
		dimension.dxf.defpoint5 = dimension.dxf.text_midpoint

	print()

dxf.saveas("output.dxf")