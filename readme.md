## WIP
This program is a work in progress. All code is currently in main.py which will be changed in the future so that it is... actually readable.
## Description
This is my Capstone project for my Computer Science Degree at Cornell College. GCAP stands for Graphical Code Architecture Project. It is built to be a GUI XMI editor and code translator allowing for drag-and-drop design.
## Paper
### Abstract

In software engineering redundancy in class and function definitions often happen between the steps of design and programming. In this paper I discuss the Graphical Code Architecture Program (GCAP) that creates Unified Modeling Language (UML) diagrams stored in XML Metadata Interchange (XMI) files from a GUI that the user can interact with and then parse XMI files into a code skeleton for the project in the Python Programming Language. This project consists of three parts, the GUI, the GUI to XMI parser, and the XMI to code parser. While the XMI to code parser is not yet implemented as of the time of this paper it is to be implemented in the near future.


### Introduction

When building software there are seven major stages: brainstorming, business analysis, design, programming, integration, quality assurance, and release. Each of these steps are crucial when producing software and the software development process relies upon each stage flowing into the next quickly and efficiently[1]. Within the design stage structures like classes, functions, and files are defined in both their components and their interactions. To transition to the next stage of software development, programming, the structures then must be redefined in code. Graphical Code Architecture Program (GCAP), aims to eventually solve the redundancy of redefining structures by allowing the information defined in GCAP's design stage, to be translated into its code counterpart for the Python programming language.
In it’s current state Graphical Code Architecture Program (GCAP) is built for Python developers in or before the design stage of a project. GCAP aims to help these developers bridge the design programming bridge through three main components UI, UI to XMI, and the not yet implemented XMI to Python. The UI is interactive allowing you to pick from the selection bar which component type you wish to add to your design. This component can then be moved to the second part of the UI, the diagram view, via drag and drop functionality. This component can then be altered by accessing the editing window. The editing window allows for the user to define parts of the component, for example, the methods in a class. Once the changes to the component through the editing windows are finished, and the product saved, the next component comes into play. UI to XMI allows for the information input by the user to the UI to then be translated to the XMI standard as defined by the Object Management Group (OMG). XMI is a subset of XML in a form to define structures, but not the logic or state of the components input. This makes it an ideal candidate to translate as an intermediary between the UI and code. Finally as part of the not yet released component GCAP plans to be able to compile Python from XMI. This should not be overly difficult due to the lack of logic and state in the XMI standard.

### Related Work


This section conducts a comprehensive survey of related work, exploring existing programs that address the visual display and translation of UML diagrams into code. Through an examination of tools such as  Lucidchart, Astah, and Enterprise Architect, the I aim to discern the similarities and differences of each work compared to GCAP.

### Lucid Charts

Lucidcharts is a web-based diagramming tool with a particular emphasis on software design. This tool provides an interface for creating various types of diagrams, including UML diagrams and flowcharts[2]. These visual representations play a crucial role in software engineering, offering developers a means to conceptualize and plan the design of their projects.
GCAP and Lucidchart share a common goal in leveraging visual diagrams for software design. Lucidchart allows for translating UML diagrams into executable code while GCAP plans to in the future, streamlining the transition from the design phase to the implementation phase. Despite this shared objective, there are notable differences between the two projects.
One prominent distinction lies in the deployment model. While Lucidchart operates as a web-based tool, this proposed project is designed to be locally run. This choice has implications such as data privacy, offline accessibility, and potentially the performance of the tool. Users of GCAP would have the advantage of keeping their design and code generation process entirely within their local environment.
Additionally, the comparison can extend to the specific features and functionalities offered by both projects. Lucidchart, being a web-based tool, emphasizes collaboration and real-time editing features, allowing multiple users to work on the same diagram simultaneously. Any real-time collaboration feature is beyond the scope of GCAP.

### Astah

Astah is a dedicated UML modeling tool with a primary focus on providing an interface for creating various UML diagrams mainly for software design[3]. Astah extends its functionality to support code generation in multiple programming languages directly from these diagrams, a feature that aligns closely with the goals of this proposed project.
The parallels between Astah and GCAP are their shared abilities of local diagramming and code generation. Both tools translate visual representations of software design into executable code, facilitating a smoother transition from the design phase to the implementation phase.
However, while the overarching objectives are similar, there may be nuances in the specific features and capabilities offered by Astah and GCAP. Astah has had years of development to refine its software. This proposed software is not planned to be as polished or feature-rich as Astah in its completed form. GCAP also is not planned to support any file type other than XMI, unlike Astah.

### Enterprise Architect

Enterprise Architect is a design tool tailored for software architecture for the creation of large-scale software development projects. With support for various modeling languages, including[4] UML, and the ability to generate code in multiple programming languages, Enterprise Architect aligns with the core objectives of this proposed project, which focuses on local UML diagram creation and code generation.
The parallel goals of both Enterprise Architect and GCAP are that Both tools provide a means to translate visual representations of software architecture into executable code.
However, a key difference emerges in the accessibility and licensing model. While GCAP is an open-source locally run tool, Enterprise Architect is a closed-source commercial product, involving licensing fees. This distinction raises considerations related to cost, user accessibility, and the potential impact on the tool's adoption within different development communities.

### Design

This section will discuss the three main components of GCAP: UI, UI to XMI, and XMI to Python. This will include both the current and planned feature set for each component.

### UI


The user interface serves as the nexus for users to create and visualize UML diagrams. It provides an interactive environment with features for adding and modifying design elements. Users of GCAP should be able to seamlessly navigate through the UI, change parameters, and establish interactions. The proposed features of the UI are:

   - Drag-and-Drop Functionality: Users can add design elements to the canvas by dragging and dropping from a palette of available elements. The palette is available on the left of the screen, It, in its current state, only consists of one element: the class.The function and file elements are planed future features.

   - Interactive Element Modification: Design elements can be selected and modified directly on the canvas, allowing for real-time adjustments to names, arguments, parameters, etc. This is done by right clicking on the element and selecting the edit option. This then opens the editing window to allow direct access to the element’s structure.

   - Hierarchy Visualization: The GUI visually represents inheritance and relationships between elements, enhancing the understanding of the software architecture. This is not yet implemented but will be implemented by use of arrows. Arrows will show the interaction between two elements the same way the edge of a graph would for two nodes.



### UI to XMI

UI-to-XMI is the process of translating the UI-created design into an XMI file for standardization. The UI-to-XMI feature includes:

   - Export to XMI: The UI allows users to export their design as an XMI file, conforming to UML standards. This is done automatically currently to a file named xmi.xml but a future feature currently planned is the save as option. This would allow for more easy saving in UI to files not to be overwritten.

    - Import XMI: Users can save or import their design projects locally in XMI file format, enabling the continuation of work at a later time. Currently importing from XMI to the UI is not implemented. This is also planned for a future version.

### XMI to Python


The XMI-to-Python feature parses the XMI file generated in the previous step and translates it into Python code. This component is not yet implemented but is planned to be the next feature added. Key functionalities include:

   - Parsing XMI Objects: The tool parses each object in the XMI file, capturing the relationships and interactions defined in the design stage.

   - Code Representation: Translates each object into its intended code in the intended spot for the Python programming language.

### Conclusion

In this paper I presented GCAP, a locally run UML diagram creation and code generation software tool. GCAP aims to help developers during the transition from the design stage to the programming stage by providing UI, XML Metadata Interchange (XMI), and Python code generation. Two out of three of these components have been implemented leaving just python code generation from XMI left to implement. Once the major components of GCAP are all completed it will stand as a useful tool for Python developers for both building the design and transitioning from the design stage to the programming stage.


[1] R. Thampy, “7 stages of SDLC: 7 phases of SDLC Software De-
velopment Life cycle,” BETSOL, https://www.betsol.com/blog/7-stages-
of-sdlc-how-to-keep-development-teams-running/ (accessed Nov. 18,
2023).
[2] Lucidchart, “Online diagram software visual solution — Lucidchart,”
Lucidchart, 2023. https://www.lucidchart.com/pages/
[3] “Premier Diagramming, Modeling Software Tools,” Astah.
https://astah.net/
[4] “Full Lifecycle Modeling for Business, Software and
Systems — Sparx Systems,” Sparxsystems.com, 2019.
https://sparxsystems.com/products/ea/index.html
