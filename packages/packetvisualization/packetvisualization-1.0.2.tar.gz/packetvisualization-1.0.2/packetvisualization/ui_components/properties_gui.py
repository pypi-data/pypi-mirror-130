import os
import sys
import traceback
from packetvisualization.models import filter


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtWidgets import QTreeWidget, QWidget, QPushButton, QDialog
from PyQt5.QtGui import QIntValidator, QValidator, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QWidget, QPushButton, QTreeWidgetItem, QInputDialog

from packetvisualization.backend_components import json_parser
from packetvisualization.backend_components.controller import Controller
from packetvisualization.models.analysis import Analysis
from packetvisualization.models.dataset import Dataset
from packetvisualization.models.workspace import Workspace
import plotly.express as px
import plotly.offline as po

from packetvisualization.ui_components import filter_options_window

class properties_window(QWidget):
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # app = QtWidgets.QApplication(sys.argv)
    # filter_window = QtWidgets.QMainWindow()

    def __init__(self, jsonString, obj, db, workspace):

        self.cursorObj = jsonString
        self.controller = Controller()
        self.obj = obj
        self.db = db
        self.workspace = workspace

        self.filters = {}

        super().__init__()
        self.setWindowTitle("Select Properties")
        # form_layout = QFormLayout()
        # self.setLayout(form_layout)
        self.layout = QtWidgets.QGridLayout()

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        self.listWidget.setGeometry(QtCore.QRect(10, 10, 211, 291))
        items = json_parser.parser(jsonString)
        properties = items[0]
        pktIds = items[1]
        self.propMap = dict(items[2])
        prop = self.propMap.keys()

        for i in prop: # properties:
            item = QtWidgets.QListWidgetItem(i)
            propRow = list(self.propMap[i])
            if propRow[1] == "False":
                item.setForeground(Qt.red)
            elif propRow[2] == "False":
                item.setBackground(QColor.fromRgb(220, 220, 220))
            # item.setFlags(Qt.ItemIsEnabled)
            self.listWidget.addItem(item)
        self.clusterLabel = QtWidgets.QLabel()
        self.clusterLabel.setText("Select Properties for Analysis")
        self.layout.addWidget(self.clusterLabel, 0, 2)

        self.layout.addWidget(self.listWidget, 1, 0, 1, 6)

        # self.listWidget2 = QtWidgets.QListWidget()
        #
        # self.listWidget2.setGeometry(QtCore.QRect(10, 10, 211, 291))
        # self.listWidget2 = QtWidgets.QListWidget()
        #
        # self.listWidget2.setGeometry(QtCore.QRect(10, 10, 422, 291))

        filter_options = {"Add", "AddCluster", "AddExpression", "AddID", "AddNoise", "AddUserFields", "AddValues",
                        "CartesianProduct", "Center", "ChangeDateFormat", "ClassAssigner", "ClusterMembership",
                        "Copy", "DataToNumeric", "Discretize", "FirstOrder", "FixedDictionaryStringToWordVector",
                        "InterquartileRange", "KernelFilter", "MakeIndicator", "MathExpression",
                        "MergeInfrequentNominalValues", "MergeManyValues", "MergeTwoValues", "NominalToBinary",
                        "NominalToString", "Normalize", "NumericCleaner", "NumbericToBinary", "NumericToDate",
                        "NumericToNominal", "NumericTransform", "Obfuscate", "OrdinalToNumeric",
                        "PartitionedMultiFilter", "PKIDiscretize", "PrincipalComponents", "RandomSubset", "Remove",
                        "RemoveByName", "RemoveType", "RemoveUseless", "RenameAttribute", "RenameNominalValues",
                        "Reorder", "ReplaceMissingValues", "ReplaceMissingWithUserConstant", "ReplaceWithMissingValue",
                        "SortLabels", "SortLabels", "Standardize", "StringToNominal", "StringToWordVector",
                        "SwapValues", "TimeSeriesDelta", "TimeSeriesTranslate", "Transpose"}


        self.pktIdsAsList = []
        for i in range(len(pktIds)):
            string = str(pktIds[i])
            self.pktIdsAsList.append(string)
            # item = QtWidgets.QListWidgetItem(string)
            # item.setFlags(Qt.ItemIsEnabled)
            # self.listWidget2.addItem(item)

        pktIdLength = len(self.pktIdsAsList)
        self.clusterLabel = QtWidgets.QLabel()
        self.clusterLabel.setText(f"Packet IDs ({pktIdLength})")
        self.layout.addWidget(self.clusterLabel, 0, 0)

        #self.layout.addWidget(self.listWidget2, 1, 0, 1, 2)

        self.button = QtWidgets.QPushButton("Analyze", clicked=lambda: self.analyze())
        self.layout.addWidget(self.button, 3, 2, 1, 2)

        self.button2 = QtWidgets.QPushButton("Filters", clicked=lambda: self.filter(filter_options))
        # self.button2 = QtWidgets.QPushButton("Filters")
        self.layout.addWidget(self.button2, 3, 4, 1, 2)

        self.clusterLabel = QtWidgets.QLabel()
        self.clusterLabel.setText("Cluster Value")
        self.layout.addWidget(self.clusterLabel, 3, 0)

        self.cluster = QtWidgets.QLineEdit(self)
        self.cluster.setObjectName("cluster")
        self.layout.addWidget(self.cluster, 3, 1, 1, 1)

        self.errorMsg = QtWidgets.QLabel()
        self.layout.addWidget(self.errorMsg, 4, 0, 1, 4)

        self.setLayout(self.layout)

    def filter(self, filter_options):
        print("in filter options")

        try:
            self.ui = filter_options_window.filter_options_window(filter_options)
            self.ui.setAttribute(Qt.WA_DeleteOnClose)
            loop = QEventLoop()
            self.ui.destroyed.connect(loop.quit)
            loop.exec()
            print(filter.filters)
            # self.ui.show()
            # print(self.ui)
        except Exception:
            print(traceback.format_exc())

    def analyze(self):
        items = self.listWidget.selectedItems()
        selected_properties = []

        for i in range(len(items)):
            property = str(self.listWidget.selectedItems()[i].text())
            actualProperty = list(self.propMap[property])
            print(actualProperty)
            selected_properties.append(actualProperty[0])
            # selected_properties.append(str(self.listWidget.selectedItems()[i].text()))

        if not len(selected_properties) != 0:

            print("Properties not selected")
            self.errorMsg.setText("Properties not selected.")
            return

        elif self.cluster.text() == "":

            self.errorMsg.setText("Must enter cluster value.")
            return

        elif not self.cluster.text().isnumeric():

            self.errorMsg.setText("Cluster value must be numeric.")
            return

        elif not int(self.cluster.text()) <= len(self.pktIdsAsList):

            print("Cluster value must not be higher than number of packets.")
            self.errorMsg.setText("Cluster value must not be higher than number of packets")
            return

        df, features = self.controller.create_analysis(self.pktIdsAsList,
                                                       selected_properties,
                                                       int(self.cluster.text()),
                                                       self.obj,
                                                       self.db)

        fig = px.scatter(df, x="cluster", y="instance_number",
                         color='cluster', color_continuous_scale=px.colors.sequential.Bluered_r,
                         hover_data=df.columns.values[:len(features)])

        def selection_fn(trace, points, selector):
            fig.data[0].cells.values = [df.loc[points.point_inds][col] for col in
                                      ['ID', 'Classification', 'Driveline', 'Hybrid']]

        # fig[0].on_selection(selection_fn)

        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
        raw_html += '<body>'
        raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
        raw_html += '</body></html>'

        self.workspace.classifier_plot_view.setHtml(raw_html)

        # Creating Analysis Item
        # Creating Analysis Item
        analysis_item_name = QInputDialog.getText(self, "Analysis Item Name Entry", "Enter Analysis Item Name:")[0]
        if analysis_item_name != "" and not self.workspace.project_tree.findItems(analysis_item_name, Qt.MatchRecursive,
                                                                                  0):
            tree = self.workspace.project_tree
            head, tail = os.path.split(self.obj.path)
            project_name = os.path.basename(head)
            project_item = tree.findItems(project_name, Qt.MatchRecursive, 0)[0]
            analysis_item = QTreeWidgetItem()
            analysis_item.setText(0, analysis_item_name)
            analysis_object = Analysis(analysis_item_name, df, features, project_item.data(0, Qt.UserRole).path,
                                       self.obj.name)
            analysis_item.setData(0, Qt.UserRole, analysis_object)
            analysis_item.setIcon(0, QIcon(":document-text.svg"))
            project_item.data(0, Qt.UserRole).add_analysis(analysis_object)
            project_item.addChild(analysis_item)

        self.workspace.classifier_window.show()
        self.close()
