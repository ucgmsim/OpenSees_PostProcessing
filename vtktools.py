#!/usr/bin/python
import xml.dom.minidom

class VTUWriter:
    """

    """
    def __init__(self,fileName):
        self.fileName = fileName
        self.fileNames = []
        self.doc = xml.dom.minidom.Document()
        root_element = self.doc.createElementNS("VTK", "VTKFile")
        root_element.setAttribute("type", "UnstructuredGrid")
        root_element.setAttribute("version", "0.1")
        root_element.setAttribute("byte_order", "LittleEndian")
        unstructuredGrid = self.doc.createElementNS("VTK", "UnstructuredGrid")
        root_element.appendChild(unstructuredGrid)
        self.doc.appendChild(root_element)



    def arrayToString(self, a):
        if type(a) == str:
            return a
        if hasattr(a, "__len__"):
            return ' '.join(str(x) for x in a)
        return str(a)


    def createDataArrayElement(self,name,components=0,data=[],type="Float32"):
        dataArray = self.doc.createElementNS("VTK", "DataArray")
        dataArray.setAttribute("Name", name)
        if components > 0:
            dataArray.setAttribute("NumberOfComponents", str(components))
        dataArray.setAttribute("type", type)
        dataArray.setAttribute("format", "ascii")
        print data
        string = ""
        for line in data:
            string += "{0}\n".format(self.arrayToString(line))

        internalData = self.doc.createTextNode(string)
        dataArray.appendChild(internalData)

        return dataArray

    def addPointData(self):
        return 0


    def insertCellData(self):
        return 0

    def writeVTU(self):
        outFile = open(self.fileName, 'w')
        self.doc.writexml(outFile,  addindent="  ",newl='\n')
        outFile.close()
        self.fileNames.append(self.fileName)

