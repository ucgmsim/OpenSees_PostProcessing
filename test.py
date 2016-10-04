#!/usr/bin/python


from vtktools import VTUWriter

writer = VTUWriter("empty.vtu")
writer.addData("Points",data=[[0,0,0],[1,0,0],[0,1,0],[1,1,0]],components=3)
writer.addData("Cells","connectivity",data=[[0,1,2,3]],type="Int32")
writer.addData("Cells","offsets",data=[4],type="Int32")
writer.addData("Cells","types",data=[8],type="UInt8")
writer.addData("PointData","test",data=[1,2,3,4],type="Float32")
writer.addData("PointData","test2",data=[[1,2,0],[3,4,0],[5,6,0],[7,8,0]],type="Float32",components=3)
writer.addData("CellData","test3",data=[1.5],type="Float32")
writer.writeVTU()
