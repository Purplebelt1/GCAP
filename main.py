from abc import abstractmethod
import sys
from PySide6.QtCore import Qt, QPointF, QRectF, QSize, QMimeData, QPoint
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsProxyWidget, QGraphicsRectItem, QComboBox, QApplication, QCheckBox, QTextEdit, QGraphicsTextItem, QMenu, QMainWindow, QGraphicsView, QGraphicsScene, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QWidget, QLineEdit, QScrollArea, QLabel, QGroupBox, QFrame, QSizePolicy, QSplitter
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QDrag
from PySide6.QtGui import QAccessibleInterface
import xml.etree.ElementTree as ET
from datetime import datetime
import copy
import xml.dom.minidom


import qdarktheme


class LeftBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setStyleSheet("background-color: lightblue;")
        layout = QVBoxLayout(self)
        
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the images
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_widget.setMinimumWidth(200)  # Set a minimum width

        # Align the layout to the top
        image_layout.setAlignment(Qt.AlignTop)
        
        window_width = self.getMainWindow().width()
        scaling_factor = min(1.0, window_width / 300.0)

        # Create an instance of ComponentButtonClass
        component_button = ComponentButtonClass(50)

        component_button.setFixedSize(QSize(150, 150))

        # Add the instance to the layout
        image_layout.addWidget(component_button)

        # Set the widget containing images as the widget for the scroll area
        scroll_area.setWidget(image_widget)

        # Add the scroll area to the layout
        layout.addWidget(scroll_area)

        # Center the component button in the layout
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def getMainWindow(self):
        parent_widget = self.parent()
        while parent_widget:
            if isinstance(parent_widget, MainWindow):
                return parent_widget
            parent_widget = parent_widget.parent()


class ComponentButtonClass(QWidget):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.image = QPixmap("button_class.png")  # Load the SVG image
        self.resize(size,size)
        self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def getMainWindow(self):
        parent_widget = self.parent()
        while parent_widget:
            if isinstance(parent_widget, MainWindow):
                return parent_widget
            parent_widget = parent_widget.parent()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            
            # Calculate the position of the drag pixmap to center it
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            dragOffset = QPoint(pixmap.width() / 2, pixmap.height() / 2)
            drag.setHotSpot(dragOffset)  # Set the hotspot to center
            
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Check if the mouse is released in the RightBox
            main_window = self.getMainWindow()
            if main_window:
                right_box = main_window.right_box
                # Map the position from LeftBox to RightBox's coordinates
                scene_pos = self.mapTo(main_window, event.pos())
                scene_pos = right_box.mapFrom(main_window, scene_pos)
                if right_box.sceneRect().contains(scene_pos):
                    self.drawComponent(scene_pos)

    def drawComponent(self, scene_pos):
        main_window = self.getMainWindow()
        right_box = main_window.right_box
        scene = right_box.scene
        scene.newClass(scene_pos)

class EditingClassWindow(QWidget):
    def __init__(self, scene, component):
        super().__init__()

        # Initialize the window with provided scene and component
        self.scene = scene
        self.component = component
        self.attributes = []
        self.methods = []

        # Set window title
        self.setWindowTitle("GCAP: Component Editor")

        # Create layout for the window
        layout = QVBoxLayout()

        # Add label for the window
        self.label = QLabel("Editing Window")
        layout.addWidget(self.label)

        # Set minimum size for the window
        self.setMinimumSize(700, 600)

        # Add label for class name
        self.name_label = QLabel("Class Name:")
        layout.addWidget(self.name_label)

        # Add text box for class name with default value
        self.name_textbox = QLineEdit("Class Name")
        layout.addWidget(self.name_textbox)

        # Add combo box for class inheritance
        self.class_inheritence_combobox = QComboBox()
        for i in self.scene.components.values():
            if isinstance(i, DiagramClassComponent):
                self.class_inheritence_combobox.addItem(i.name)
        layout.addWidget(self.class_inheritence_combobox)

        # Add methods section
        self.methods_tabwidget = QTabWidget()
        layout.addWidget(self.methods_tabwidget)
        self.setupMethodsSection()

        # Add button to add new method
        self.addMethod_button = QPushButton("Add Method")
        self.addMethod_button.clicked.connect(self.addMethod)
        layout.addWidget(self.addMethod_button)

        # Add attributes section
        self.attributes_groupbox = QGroupBox("Attributes")
        self.attributes_layout = QVBoxLayout()
        self.setup_attributes_section()
        self.attributes_groupbox.setLayout(self.attributes_layout)

        # Add a scroll area for attributes
        attribute_scroll_area = QScrollArea()
        attribute_scroll_area.setWidgetResizable(True)
        attribute_scroll_widget = QWidget()
        attribute_scroll_widget.setLayout(self.attributes_layout)
        attribute_scroll_area.setWidget(attribute_scroll_widget)
        layout.addWidget(self.attributes_groupbox)
        layout.addWidget(attribute_scroll_area)

        # Add button to add new attribute
        self.add_attribute_button = QPushButton("Add Attribute")
        self.add_attribute_button.clicked.connect(lambda: self.addAttribute())
        layout.addWidget(self.add_attribute_button)

        # Add save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.update)
        layout.addWidget(self.save_button)

        # Set layout for the window
        self.setLayout(layout)

    def setup_attributes_section(self):
        # Setup attributes section with existing attributes of the component
        for attribute in self.component.attributes:
            self.addAttribute(attribute)

    def createAttributeLayout(self, attribute):
        # Create layout for an attribute
        attribute_name_label = QLabel("Attribute Name:")
        attribute_type_label = QLabel("Attribute Type:")
        attribute_name_textbox = QLineEdit(attribute.name)
        attribute_type_textbox = QLineEdit(attribute.type)
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.removeAttribute(attribute_layout))
        attribute_layout = QHBoxLayout()
        attribute_layout.addWidget(attribute_name_label)
        attribute_layout.addWidget(attribute_name_textbox)
        attribute_layout.addWidget(attribute_type_label)
        attribute_layout.addWidget(attribute_type_textbox)
        attribute_layout.addWidget(remove_button)
        return attribute_layout

    def addAttribute(self, attribute=None):
        # Add an attribute to the attributes section
        if attribute:
            new_atr = attribute
        else:
            new_atr = AttributeComponent("", self.component, type="")

        attribute_layout = self.createAttributeLayout(new_atr)

        # Add the container widget to the attributes layout
        self.attributes_layout.addLayout(attribute_layout)

        self.attributes.append((new_atr, attribute_layout))




    def removeAttribute(self, attribute_layout):
        # Remove an attribute from the attributes section
        index = self.attributes_layout.indexOf(attribute_layout)
        self.attributes.pop(index)
        item = self.attributes_layout.takeAt(index)
        if item:
            for i in range(item.count()):
                widget = item.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

    def setupMethodsSection(self):
        # Setup methods section with existing methods of the component
        for method in self.component.operations:
            self.addMethod(method)

    def createMethodTab(self, method):
        # Create a tab for a method
        method_tab = QWidget()
        method_tab_layout = QVBoxLayout()
        method_name_label = QLabel("Method Name:")
        method_name_textbox = QLineEdit(method.name)
        method_tab_layout.addWidget(method_name_label)
        method_tab_layout.addWidget(method_name_textbox)
        
        addParameter_button = QPushButton("Add Parameter")
        parameter_scroll_area = QScrollArea()
        parameter_scroll_area.setWidgetResizable(True)
        
        # Create a widget to contain the parameters
        parameter_widget = QWidget()
        parameter_scroll_area.setWidget(parameter_widget)
        
        # Set up layout for parameters
        parameter_layout = QVBoxLayout()
        parameter_widget.setLayout(parameter_layout)
        
        addParameter_button.clicked.connect(lambda: self.addParameter(parameter_layout, method))
        method_tab_layout.addWidget(addParameter_button)
        method_tab_layout.addWidget(parameter_scroll_area)
        #for i in range(method_tab_layout.count()):
        #    print(method_tab_layout.itemAt(i).widget())
        method_tab.setLayout(method_tab_layout)
        
        # Connect textChanged signal to update tab name
        method_name_textbox.textChanged.connect(lambda text: self.updateTabName(method_tab, text))
        
        return method_tab


    def updateTabName(self, method_tab, new_name):
        # Update the name of the tab
        index = self.methods_tabwidget.indexOf(method_tab)
        if index != -1:
            self.methods_tabwidget.setTabText(index, new_name)

    def addMethod(self, method=None):
        # Add a method to the methods section
        if method:
            new_method = method
        else:
            new_method = OperationComponent(parent=self.component, name="")

        method_tab = self.createMethodTab(new_method)

        self.methods.append((new_method, method_tab,[]))
        for i in new_method.parameters:
            self.addParameter(method_tab.layout(),new_method,i)

        if new_method.name == "":
            self.methods_tabwidget.addTab(method_tab, "New Method")
        else:
            self.methods_tabwidget.addTab(method_tab, new_method.name)

    def addParameter(self, method_tab_layout, method, parameter=None):
        # Add a parameter to a method
        if parameter:
            new_parameter = parameter
        else:
            new_parameter = ParameterComponent(name="", parent=self.component)

        for i in range(len(self.methods)):
            print("self.methods")
            print(self.methods[i][0])
            print("Method")
            print(method)
            if self.methods[i] == method:
                self.methods[i][2].append(new_parameter)
                print("HUH")
                break
        parameter_layout = QHBoxLayout()
        parameter_name_label = QLabel("Parameter Name:")
        parameter_type_label = QLabel("Parameter Type:")
        parameter_optional_label = QLabel("Optional")
        name_textbox = QLineEdit(new_parameter.name)
        type_textbox = QLineEdit(new_parameter.type)
        optional_checkbox = QCheckBox()
        optional_checkbox.setCheckState(Qt.CheckState.Checked if new_parameter.optional else Qt.CheckState.Unchecked)
        parameter_layout.addWidget(parameter_name_label)
        parameter_layout.addWidget(name_textbox)
        parameter_layout.addWidget(parameter_type_label)
        parameter_layout.addWidget(type_textbox)
        parameter_layout.addWidget(parameter_optional_label)
        parameter_layout.addWidget(optional_checkbox)
        method_tab_layout.addLayout(parameter_layout)
        method_index = -1
        for i, (_, method_tab, _) in enumerate(self.methods):
            if method_tab.layout() == method_tab_layout:
                method_index = i
                break
        if method_index != -1:
            self.methods[method_index][2].append(new_parameter)
        return parameter_layout

    def update(self):
        # Update component details based on user input
        self.component.name = self.name_textbox.text()
        self.component.draw()
        # Update attributes
        for index, (attribute, layout) in enumerate(self.attributes):
            attribute_name_textbox = layout.itemAt(1).widget()
            attribute_type_textbox = layout.itemAt(3).widget()
            attribute.name = attribute_name_textbox.text()
            attribute.type = attribute_type_textbox.text()
            self.attributes[index] = (attribute, layout)
        # Remove attributes that were deleted
        for i in self.component.attributes:
            if i.id not in [attribute.id for attribute, layout in self.attributes]:
                self.scene.components.pop(i.id)
                self.component.attributes = [j for j in self.component.attributes if j.id != i.id]
        # Update or add new attributes
        for i, layout in self.attributes:
            if i.name != "":
                if i.id not in [j.id for j in self.component.attributes]:
                    i.id = self.scene.setNewId(i)
                    self.component.attributes.append(i)
                    self.scene.xmi.addComponent(i)
                self.scene.components[i.id].name = i.name
                self.scene.components[i.id].type = i.type
        # Update methods
        for index, (method, method_tab, parameters) in enumerate(self.methods):
            method_name_textbox = method_tab.layout().itemAt(1).widget()
            method.name = method_name_textbox.text()
            parameter_scroll_area = method_tab.layout().itemAt(3).widget()
            print(parameter_scroll_area.widget().layout().count())
            print(parameters)
            for i in range(parameter_scroll_area.widget().layout().count()):
                print("!")
                print(i)
                parameter_layout = parameter_scroll_area.widget().layout().itemAt(i)
                name_textbox = parameter_layout.itemAt(1).widget()
                type_textbox = parameter_layout.itemAt(3).widget()
                optional_checkbox = parameter_layout.itemAt(5).widget()
                #parameters[i].name = name_textbox.text()
                #parameters[i].type = type_textbox.text()
                #parameters[i].optional = optional_checkbox.isChecked
                print(name_textbox.text())
            self.methods[index] = (method, method_tab, parameters)
        # Remove methods that were deleted
        for i in self.component.operations:
            if i.id not in [method.id for method, method_tab, parameters in self.methods]:
                self.scene.components.pop(i.id)
                self.component.operations = [j for j in self.component.operations if j.id != i.id]
        # Update or add new methods
        for i, method_tab, parameters in self.methods:
            if i.id not in [j.id for j in self.component.operations]:
                i.id = self.scene.setNewId(i)
                self.component.operations.append(i)
                self.scene.xmi.addComponent(i)
            else:
                self.scene.components[i.id].name = i.name
        for (method, method_tab, parameters) in self.methods:
            for i in self.scene.components.get(method.id).parameters:
                if i.id not in [j.id for j in parameters]:
                    self.scene.components.pop(i.id)
                    self.scene.components.get(method.id).parameters = [j for j in self.scene.components.get(method.id).parameters if j.id != i.id]
            for i in parameters:
                if i.id not in [j.id for j in self.scene.components.get(method.id).parameters]:
                    i.parent = method
                    i.id = self.scene.setNewId(i)
                    self.scene.components.get(method.id).parameters.append(i)
                    self.scene.xmi.addComponent(i)
                else:
                    self.scene.components[i.id].name = i.name
                    self.scene.components[i.id].type = i.type
                    self.scene.components[i.id].optional = i.optional

        inheritence_parent = None
        for i in self.scene.components.values():
            if isinstance(i, DiagramClassComponent):
                #print(self.class_inheritence_combobox.currentText())
                if i.name == self.class_inheritence_combobox.currentText():

                    inheritence_parent = self.scene.components.get(i.id)
        
        if self.component.inheritence_component.parent == None:
            if inheritence_parent != None:
                self.component.inheritence_component.parent = inheritence_parent
                self.scene.xmi.addComponent(self.component.inheritence_component)
        elif inheritence_parent != self.component.inheritence_component.parent:
            self.component.inheritence_component.parent = inheritence_parent

        self.component.draw()
        self.scene.xmi.updateComponent(self.component)
        self.close()


class RightBox(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = DiagramScene(self)
        self.setScene(self.scene)
        self.setSceneRect(QRectF(0, 0, 700, 500))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.accept()

        if self.scene.isOverlapping(event.pos(), 100, 100):
            return
        
        self.scene.newClass(event.pos())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:  # Check for right mouse button
            component = self.scene.isInComponent(event.pos())
            if component:
                # Create a context menu
                menu = QMenu(self)

                # Add actions to the menu
                edit_action = QAction("Edit", self)
                copy_action = QAction("Copy", self)

                # Connect actions to functions or methods
                edit_action.triggered.connect(lambda: self.scene.editAction(component))
                copy_action.triggered.connect(lambda: self.scene.copyAction(component))

                # Add actions to the menu
                menu.addAction(edit_action)
                menu.addAction(copy_action)

                # Show the menu at the mouse position
                menu.exec_(event.globalPos())

class XMIDocument():
    UML_NAMESPACE = "org.omg.xmi.namespace.UML"

    def __init__(self):
        self.xmi = ET.Element("XMI", 
                              attrib={"xmi.version": "2.1", 
                                      "xmlns:UML": self.UML_NAMESPACE, 
                                      "timestamp": datetime.utcnow().isoformat()})

        self.header = ET.SubElement(self.xmi, "XMI.header")
        self.documentation = ET.SubElement(self.header, "XMI.documentation")

        ET.SubElement(self.documentation, "XMI.exporter").text = "Graphical Code Architecture Program"
        ET.SubElement(self.documentation, "XMI.exporterVersion").text = "v0.1"

        self.content = ET.SubElement(self.xmi, "XMI.content")

        self.tree = ET.ElementTree(self.xmi)


    def addComponent(self, component):
        if isinstance(component, DiagramClassComponent):
            class_element = ET.SubElement(self.content, f"{{{self.UML_NAMESPACE}}}Class", attrib={"xmi.id": "_" + str(component.id), "name": component.name})
            for attribute in component.attributes:
                ET.SubElement(class_element, f"{{{self.UML_NAMESPACE}}}Attribute", attrib={"xmi.id": "_" + str(attribute.id), "name": attribute.name, "type": attribute.type})
            for operation in component.operations:
                operation_element = ET.SubElement(class_element, f"{{{self.UML_NAMESPACE}}}Operation", attrib={"xmi.id": "_" + str(operation.id), "name": operation.name})
                for parameter in operation.parameters:
                    self._addParameterToOperation(operation_element, parameter)
        elif isinstance(component, AttributeComponent):
            parent_id = "_" + str(component.parent.id)
            parent_element = self.content.find(f"./UML:Class[@xmi.id='{parent_id}']", namespaces={"UML": self.UML_NAMESPACE})
            if parent_element is not None:
                ET.SubElement(parent_element, f"{{{self.UML_NAMESPACE}}}Attribute", attrib={"xmi.id": "_" + str(component.id), "name": component.name, "type": component.type})
            else:
                print(f"Parent class with ID {parent_id} not found.")
        elif isinstance(component, OperationComponent):
            parent_id = "_" + str(component.parent.id)
            parent_element = self.content.find(f"./UML:Class[@xmi.id='{parent_id}']", namespaces={"UML": self.UML_NAMESPACE})
            if parent_element is not None:
                operation_element = ET.SubElement(parent_element, f"{{{self.UML_NAMESPACE}}}Operation", attrib={"xmi.id": "_" + str(component.id), "name": component.name})
                for parameter in component.parameters:
                    self._addParameterToOperation(operation_element, parameter)
            else:
                print(f"Parent class with ID {parent_id} not found.")
        elif isinstance(component, ParameterComponent):
            if isinstance(component.parent, OperationComponent):
                parent_id = "_" + str(component.parent.id)
                parent_element = self.content.find(f"./UML:Class/UML:Operation[@xmi.id='{parent_id}']", namespaces={"UML": self.UML_NAMESPACE})
                if parent_element is not None:
                    self._addParameterToOperation(parent_element, component)
                else:
                    print(f"Parent operation with ID {parent_id} not found.")
            else:
                print("Parent of parameter should be an OperationComponent.")
        elif isinstance(component, InheritenceComponent):
            parent_id = "_" + str(component.parent.id)
            child_id = "_" + str(component.child.id)
            parent_element = self.content.find(f"./UML:Class[@xmi.id='{child_id}']", namespaces={"UML": self.UML_NAMESPACE})
            if parent_element is not None:
                generalization_element = ET.SubElement(parent_element, f"{{{self.UML_NAMESPACE}}}Generalization", attrib={"xmi.id": f"{child_id}i", "parent": parent_id, "child": child_id})
            else:
                print(f"Parent class with ID {parent_id} not found.")
        self.save()


    def _addParameterToOperation(self, operation_element, parameter):
        ET.SubElement(operation_element, f"{{{self.UML_NAMESPACE}}}Parameter", attrib={"xmi.id": "_" + str(parameter.id), "name": parameter.name, "type": parameter.type, "use": "optional" if parameter.optional else "mandatory"})


    def updateComponent(self, component):
        if isinstance(component, DiagramClassComponent):
            for element in self.content.findall(".//UML:Class", namespaces={"UML": self.UML_NAMESPACE}):
                if element.attrib.get("xmi.id") == "_" + str(component.id):
                    # Update the name of the class
                    element.attrib["name"] = component.name
                    if hasattr(component, "attributes"):
                        for attribute in component.attributes:
                            for child in element.findall(".//UML:Attribute", namespaces={"UML": self.UML_NAMESPACE}):
                                if child.attrib.get("xmi.id") == "_" + str(attribute.id):
                                    # Update the name and type of the attribute
                                    child.attrib["name"] = attribute.name
                                    child.attrib["type"] = attribute.type
                                    break
                    # Update operations
                    if hasattr(component, "operations"):
                        for operation in component.operations:
                            for child in element.findall(".//UML:Operation", namespaces={"UML": self.UML_NAMESPACE}):
                                if child.attrib.get("xmi.id") == "_" + str(operation.id):
                                    # Update the name of the operation
                                    child.attrib["name"] = operation.name
                                    break
                            for parameter in operation.parameters:
                                for child in element.findall(".//UML:Parameter", namespaces={"UML": self.UML_NAMESPACE}):
                                    if child.attrib.get("xmi.id") == "_" + str(parameter.id):
                                        child.attrib["name"] = parameter.name
                                        child.attrib["type"] = parameter.type
                                        child.attrib["use"] = "optional" if parameter.optional else "mandatory"
                    break  # Exit loop after updating

            # Update inheritance
            for inheritance_element in self.content.findall(".//UML:Generalization", namespaces={"UML": self.UML_NAMESPACE}):
                if inheritance_element.attrib.get("child") == "_" + str(component.id):
                    inheritance_element.attrib["parent"] = "_" + str(component.inheritence_component.parent.id)  # Update id of inheritance
                    break

        elif isinstance(component, AttributeComponent):
            for element in self.content.findall(".//UML:Class", namespaces={"UML": self.UML_NAMESPACE}):
                if element.attrib.get("xmi.id") == "_" + str(component.parent.id):
                    ET.SubElement(element, f"{{{self.UML_NAMESPACE}}}Attribute", attrib={"xmi.id": "_" + str(component.id), "name": component.name, "type": component.type})
                    break
        self.save()




    def save(self):
        self.tree = ET.ElementTree(self.xmi)
        with open("XMI.xml", "wb") as f:
            xml_str = ET.tostring(self.xmi, encoding="utf-8")
            dom = xml.dom.minidom.parseString(xml_str)
            pretty_xml_str = dom.toprettyxml(indent="  ", encoding="utf-8")
            f.write(pretty_xml_str)

class DiagramScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.components = {}
        self.next_id = 1 
        self.xmi = XMIDocument()
    
    def newClass(self, scene_pos):

        new_class = DiagramClassComponent(scene=self, 
                                          x=scene_pos.x(), 
                                          y=scene_pos.y(), 
                                          l=100, 
                                          h=100,
                                          parent=self)
        
        new_class.id = self.setNewId(new_class)
        
        new_class.draw()
        self.xmi.addComponent(new_class)

    def setNewId(self, component):
        component_id = self.next_id
        self.next_id += 1
        self.components[component_id] = component
        return component_id

    def isInComponent(self, scene_pos):
        for component_id, component in self.components.items():
            if isinstance(component, DiagramComponent):
                if (abs(scene_pos.x() - component.x) <= component.l//2) and (abs(scene_pos.y() - component.y) <= component.h//2):
                    return component
        return None  # Return None if no component is found
    
    def isOverlapping(self, scene_pos, l, h):
        for component_id, component in self.components.items():
            if isinstance(component, DiagramComponent):
                if (abs(scene_pos.x() - component.x) < (l + component.l)/2) and (abs(scene_pos.y() - component.y) < (h + component.h)/2):
                    return component
        return None
    
    def editAction(self, component):
        if component:
            self.editing_window = EditingClassWindow(self, component)
            self.editing_window.show()

    def copyAction(self, component_id):
        component = self.components.get(component_id)
        if component:
            pass

class InheritenceComponent():
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

class AttributeComponent():
    def __init__(self, name, parent, id = None, type = None):
        self.parent = parent
        self.name = name
        self.id = id
        self.type = type

    def __str__(self):
        return(self.name + " " + self.type)

class ParameterComponent():
    def __init__(self, name, parent, id = None, type = None, optional = True):
        self.parent = parent
        self.name = name
        self.id = id
        self.type = type
        self.optional = optional

class OperationComponent():
    def __init__(self, name, parent = None, id = None, parameters = []):
        self.parent = parent
        self.name = name
        self.id = id
        self.parameters = parameters

    def __str__(self):
        return self.name + "()"


class DiagramComponent():
    @abstractmethod
    def draw(self):
        ...
    
class DiagramClassComponent(DiagramComponent):
    def __init__(self, scene:QGraphicsScene, x, y, l, h, id=None, parent=None, inheritence_component=None):
        self.scene = scene
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.id = id
        self.name = "Class Name"
        self.operations = []
        self.attributes = []
        self.inheritence_component = InheritenceComponent(inheritence_component, self)
        self.text_items = []

    def draw(self):
        # Clear existing text items
        for item in self.text_items:
            self.scene.removeItem(item)
        self.text_items.clear()

        # Draw class rectangle

        comp_count = len(self.attributes) + len(self.operations)
        comp_count = 0 if comp_count < 3 else comp_count - 2
        print(comp_count)
        rect = QGraphicsRectItem(self.x - self.l//2, self.y + (comp_count * 20)//2 - (self.h + comp_count * 20)//2, self.l, self.h + comp_count * 20)

        pen = QPen(Qt.black)
        brush = QBrush(QColor(128,128,128))
        rect.setPen(pen)
        rect.setBrush(brush)
        self.scene.addItem(rect)
        self.text_items.append(rect)

        # Draw class name
        name_text = QGraphicsTextItem(self.name)
        name_text.setPos(self.x - self.l//2 + 10, self.y - self.h//2 + 10)
        self.scene.addItem(name_text)
        self.text_items.append(name_text)

        # Add separator line between class name and attributes
        separator1 = QGraphicsLineItem(self.x - self.l//2, self.y - self.h//2 + 30,
                                      self.x + self.l//2, self.y - self.h//2 + 30)
        self.scene.addItem(separator1)
        self.text_items.append(separator1)

        # Adding attributes to the scene
        for i, attribute in enumerate(self.attributes):
            attribute_text = QGraphicsTextItem(str(attribute))
            attribute_text.setPos(self.x - self.l//2 + 10, self.y - self.h//2 + (i + 1.2) * 20)
            self.scene.addItem(attribute_text)
            self.text_items.append(attribute_text)

        # Add separator line between attributes and methods
        separator2 = QGraphicsLineItem(self.x - self.l//2, self.y - self.h//2 + (len(self.attributes) + 1.5) * 20,
                                       self.x + self.l//2, self.y - self.h//2 + (len(self.attributes) + 1.5) * 20)
        self.scene.addItem(separator2)
        self.text_items.append(separator2)

        # Adding methods to the scene
        for i, operation in enumerate(self.operations):
            operation_text = QGraphicsTextItem(str(operation))
            operation_text.setPos(self.x - self.l//2 + 10, self.y - self.h//2 + (len(self.attributes) + i + 1.2) * 20)
            self.scene.addItem(operation_text)
            self.text_items.append(operation_text)
            
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("GCAP")
        self.setMinimumSize(1000, 500)

        splitter = QSplitter(Qt.Horizontal)

        self.left_box = LeftBox(self)
        self.right_box = RightBox(self)

        splitter.addWidget(self.left_box)
        splitter.addWidget(self.right_box)

        splitter.setSizes([300, 700])

        self.setCentralWidget(splitter)

        app.setStyleSheet(qdarktheme.load_stylesheet())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())