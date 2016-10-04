#!/usr/bin/python
import xml.dom.minidom

class VTUWriter:
    """

    """
    def __init__(self,fileName):
        self.fileName = fileName
        self.fileNames = []

        # Document and root element
        self.doc = xml.dom.minidom.Document()

        # the data will go here
        self.data = {}


    def arrayToString(self, a):
        if type(a) == str:
            return a
        if hasattr(a, "__len__"):
            return ' '.join(str(x) for x in a)
        return str(a)


    def createDataArrayElement(self,name,data=[],components=0,type="Float32",format="ascii"):
        dataArray = self.doc.createElementNS("VTK", "DataArray")
        if name != "":
            dataArray.setAttribute("Name", name)
        if components > 0:
            dataArray.setAttribute("NumberOfComponents", str(components))
        dataArray.setAttribute("type", type)
        dataArray.setAttribute("format", format)
        print "Inserting into %s %i elements" %(name,len(data))
        #print data
        string = ""
        for line in data:
            string += "{0}\n".format(self.arrayToString(line))

        internalData = self.doc.createTextNode(string)
        dataArray.appendChild(internalData)

        return dataArray


    def addData(self,target, name= "",data=[],components=0,type="Float32",format="ascii"):
        # sanity check for the sections
        assert target in ["PointData", "CellData", "Points","Cells"]

        if self.data.has_key(target):
            self.data[target].append(self.createDataArrayElement(name,data,components,type,format))
        else:
            self.data[target] = [self.createDataArrayElement(name,data,components,type,format)]

        # preparing the number of points/cells for the output
        if target == "Points":
            self.numberOfPoints = len(data)
        if target == "Cells":
            if name == "connectivity":
                self.numberOfCells = len(data)


    def writeVTU(self):
        root_element = self.doc.createElementNS("VTK", "VTKFile")
        root_element.setAttribute("type", "UnstructuredGrid")
        root_element.setAttribute("version", "0.1")
        root_element.setAttribute("byte_order", "LittleEndian")
        self.doc.appendChild(root_element)

        # Unstructured grid element
        unstructuredGrid = self.doc.createElementNS("VTK", "UnstructuredGrid")
        root_element.appendChild(unstructuredGrid)

        # we will have a single piece
        piece = self.doc.createElementNS("VTK", "Piece")
        piece.setAttribute("NumberOfPoints", str(self.numberOfPoints))
        piece.setAttribute("NumberOfCells", str(self.numberOfCells))
        unstructuredGrid.appendChild(piece)

        for key in self.data.keys():
            # create points data
            element = self.doc.createElementNS("VTK", key)

            arrays = self.data[key]
            for dataArray in arrays:
                element.appendChild(dataArray)
            piece.appendChild(element)


        outFile = open(self.fileName, 'w')
        self.doc.writexml(outFile,  addindent="  ",newl='\n')
        outFile.close()
        self.fileNames.append(self.fileName)

