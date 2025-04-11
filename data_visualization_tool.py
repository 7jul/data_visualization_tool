import sys
import json
import os
import numpy as np
import pandas as pd
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QLabel, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, 
                            QTextEdit, QPushButton, QComboBox, QFileDialog, QMessageBox,QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataVisualizationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据可视化工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置默认字体
        default_font = QFont("Microsoft YaHei")
        default_font.setPointSize(12)
        self.setFont(default_font)
        
        # 创建主选项卡
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 创建两个选项卡页面
        self.tab_data_input = QWidget()
        self.tab_chart_display = QWidget()
        
        # 添加选项卡
        self.tabs.addTab(self.tab_data_input, "数据输入")
        self.tabs.addTab(self.tab_chart_display, "图表展示")
        
        # 初始化各选项卡内容
        self.init_data_input_tab()
        self.init_chart_display_tab()
        
        # 存储数据
        self.data = None
        self.chart_type = "bar"
        
    def init_data_input_tab(self):
        """初始化数据输入选项卡"""
        layout = QVBoxLayout()
        
        # 数据输入方式选择
        input_method_group = QGroupBox("数据输入方式")
        input_method_layout = QHBoxLayout()
        
        self.manual_input_btn = QPushButton("手动输入")
        self.manual_input_btn.clicked.connect(self.show_manual_input_dialog)
        
        self.file_input_btn = QPushButton("从文件导入")
        self.file_input_btn.clicked.connect(self.import_from_file)
        
        input_method_layout.addWidget(self.manual_input_btn)
        input_method_layout.addWidget(self.file_input_btn)
        input_method_group.setLayout(input_method_layout)
        
        # 数据预览区域
        self.data_preview = QTextEdit()
        self.data_preview.setReadOnly(True)
        self.data_preview.setPlaceholderText("数据将显示在这里...")
        self.data_preview.setFont(QFont("Microsoft YaHei", 12))
        
        layout.addWidget(input_method_group)
        layout.addWidget(QLabel("数据预览:"))
        layout.addWidget(self.data_preview)
        
        # 图表类型选择
        chart_type_group = QGroupBox("图表类型")
        chart_type_layout = QHBoxLayout()
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["柱状图", "折线图", "饼图", "散点图", "面积图"])
        self.chart_type_combo.currentTextChanged.connect(self.update_chart_type)
        
        chart_type_layout.addWidget(QLabel("选择图表类型:"))
        chart_type_layout.addWidget(self.chart_type_combo)
        chart_type_layout.addStretch()
        chart_type_group.setLayout(chart_type_layout)
        
        # 图表标题和样式设置
        chart_style_group = QGroupBox("图表样式")
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("输入图表标题")
        
        self.x_label_input = QLineEdit()
        self.x_label_input.setPlaceholderText("输入X轴标签")
        
        self.y_label_input = QLineEdit()
        self.y_label_input.setPlaceholderText("输入Y轴标签")
        
        form_layout.addRow("标题:", self.title_input)
        form_layout.addRow("X轴标签:", self.x_label_input)
        form_layout.addRow("Y轴标签:", self.y_label_input)
        chart_style_group.setLayout(form_layout)
        
        # 生成图表按钮
        self.generate_chart_btn = QPushButton("生成图表")
        self.generate_chart_btn.clicked.connect(self.generate_chart)
        
        layout.addWidget(chart_type_group)
        layout.addWidget(chart_style_group)
        layout.addWidget(self.generate_chart_btn)
        
        # 添加版权信息
        copyright_label = QLabel("@天津市南开区南开小学-7jul")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(copyright_label)
        
        self.tab_data_input.setLayout(layout)
    

    
    def init_chart_display_tab(self):
        """初始化图表展示选项卡"""
        layout = QVBoxLayout()
        
        # 主垂直布局，图表区域占75%
        main_layout = QVBoxLayout()
        
        # Matplotlib图表区域
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # 保存按钮
        self.save_btn = QPushButton("保存图表")
        self.save_btn.clicked.connect(self.save_chart)
        
        # AI分析区域
        ai_group = QGroupBox("AI分析")
        ai_layout = QVBoxLayout()
        
        self.ai_analyze_btn = QPushButton("AI分析")
        self.ai_analyze_btn.clicked.connect(self.analyze_with_ai)
        self.ai_result = QTextEdit()
        self.ai_result.setReadOnly(True)
        self.ai_result.setPlaceholderText("AI分析结果将显示在这里...")
        
        ai_layout.addWidget(self.ai_analyze_btn)
        ai_layout.addWidget(self.ai_result)
        ai_group.setLayout(ai_layout)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(ai_group)
        
        # 设置布局比例
        main_layout.addWidget(self.canvas, stretch=3)
        main_layout.addLayout(btn_layout, stretch=1)
        
        layout.addLayout(main_layout)
        
        # 添加版权信息
        copyright_label = QLabel("@天津市南开区南开小学-7jul")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(copyright_label)
        
        self.tab_chart_display.setLayout(layout)
    
    def show_manual_input_dialog(self):
        """显示手动输入数据对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("手动输入数据")
        dialog.setMinimumWidth(800)
        dialog.setMinimumHeight(600)
        
        layout = QVBoxLayout()
        
        # 数据输入区域
        self.data_input = QTextEdit()
        self.data_input.setPlaceholderText("""请输入数据，格式如下：
字段1: 数值1, 字段2: 数值2, 字段3: 数值3
---------或者---------
A:10, B:20, C:30
---------或者---------
A:10
B:20
C:30
程序会自动转换为标准JSON格式""")
        
        # 按钮
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(lambda: self.process_manual_input(dialog))
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addWidget(self.data_input)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def process_manual_input(self, dialog):
        """处理手动输入的数据"""
        try:
            data_text = self.data_input.toPlainText().strip()
            if not data_text:
                QMessageBox.warning(self, "输入错误", "请输入有效数据！")
                return
                
            # 处理简化格式
            if ':' in data_text and ('{' not in data_text or '[' not in data_text):
                # 替换中文标点为英文标点
                data_text = data_text.replace('：', ':').replace('，', ',')
                 # 转换为JSON数组格式，保留换行符
                items = []
                for line in data_text.splitlines():
                    line_items = [item.strip() for item in line.split(',') if item.strip()]
                    items.extend(line_items)
                data_list = []
                for item in items:
                    if ':' in item:
                        key, value = item.split(':', 1)
                        data_list.append({
                            'label': key.strip(),
                            'value': float(value.strip()) if value.strip().replace('.','',1).isdigit() else value.strip()
                        })
                self.data = {"labels": [item['label'] for item in data_list], 
                             "values": [item['value'] for item in data_list]}
            else:
                # 处理标准JSON格式
                self.data = json.loads(data_text.encode('utf-8').decode('unicode_escape'))
                
            # 确保中文能正确显示，调整数组内不换行
            self.data_preview.setPlainText(json.dumps(self.data, indent=4, ensure_ascii=False, separators=(',', ': ')))
            dialog.accept()
        except (json.JSONDecodeError, ValueError) as e:
            QMessageBox.critical(self, "格式错误", f"数据格式不正确: {str(e)}，请检查输入！")
    
    def import_from_file(self):
        """从文件导入数据"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", 
                                                 "JSON文件 (*.json);;Excel文件 (*.xlsx);;CSV文件 (*.csv);;所有文件 (*.*)")
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    self.data = df.to_dict(orient='records')
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                    self.data = df.to_dict(orient='records')
                else:
                    QMessageBox.warning(self, "文件类型错误", "不支持的文件类型！")
                    return
                
                # 确保中文能正确显示
                self.data_preview.setPlainText(json.dumps(self.data, indent=4, ensure_ascii=False))
            except Exception as e:
                QMessageBox.critical(self, "导入错误", f"导入文件时出错: {str(e)}")
    
    def update_chart_type(self, text):
        """更新图表类型"""
        chart_types = {"柱状图": "bar", "折线图": "line", "饼图": "pie", 
                      "散点图": "scatter", "面积图": "area"}
        self.chart_type = chart_types.get(text, "bar")
    
    def generate_chart(self):
        """生成图表"""
        if self.data is None:
            QMessageBox.warning(self, "数据错误", "请先输入数据！")
            return
            
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            title = self.title_input.text().strip()
            x_label = self.x_label_input.text().strip()
            y_label = self.y_label_input.text().strip()
            
            if isinstance(self.data, list) and all(isinstance(item, dict) for item in self.data):
                # 处理字典列表数据
                df = pd.DataFrame(self.data)
                if self.chart_type == "bar":
                    df.plot.bar(x=df.columns[0], y=df.columns[1:], ax=ax)
                elif self.chart_type == "line":
                    df.plot.line(x=df.columns[0], y=df.columns[1:], ax=ax)
                elif self.chart_type == "scatter":
                    df.plot.scatter(x=df.columns[0], y=df.columns[1:], ax=ax)
                elif self.chart_type == "area":
                    df.plot.area(x=df.columns[0], y=df.columns[1:], ax=ax)
            elif isinstance(self.data, dict) and "labels" in self.data and "values" in self.data:
                # 处理标签-值数据
                if isinstance(self.data["values"][0], list):
                    # 多组数据情况
                    colors = plt.cm.tab10(np.linspace(0, 1, len(self.data["values"])))
                    for i, values in enumerate(self.data["values"]):
                        if self.chart_type == "bar":
                            bars = ax.bar(self.data["labels"], values, color=colors[i], alpha=0.7, label=f'系列{i+1}')
                            for bar in bars:
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                        f'{height:.1f}',
                                        ha='center', va='bottom')
                        elif self.chart_type == "line":
                            line = ax.plot(self.data["labels"], values, color=colors[i], marker='o', label=f'系列{i+1}')
                            for x, y in zip(self.data["labels"], values):
                                ax.text(x, y, f'{y:.1f}', ha='center', va='bottom')
                    ax.legend(loc='upper right')
                else:
                    # 单组数据情况
                    if self.chart_type == "bar":
                        bars = ax.bar(self.data["labels"], self.data["values"])
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{height:.1f}',
                                    ha='center', va='bottom')
                    elif self.chart_type == "line":
                        line = ax.plot(self.data["labels"], self.data["values"], marker='o')
                        for x, y in zip(self.data["labels"], self.data["values"]):
                            ax.text(x, y, f'{y:.1f}', ha='center', va='bottom')
                    elif self.chart_type == "pie":
                        ax.pie(self.data["values"], labels=self.data["labels"], autopct='%1.1f%%')

            
            if title:
                ax.set_title(title)
            if x_label:
                ax.set_xlabel(x_label)
            if y_label:
                ax.set_ylabel(y_label)
            
            # 添加网格线
            ax.grid(True)
            
            self.canvas.draw()
            self.tabs.setCurrentIndex(2)  # 切换到图表展示选项卡
        except Exception as e:
            QMessageBox.critical(self, "图表生成错误", f"生成图表时出错: {str(e)}")
    
    def save_chart(self):
        """保存图表"""
        if not hasattr(self, 'figure') or len(self.figure.get_axes()) == 0:
            QMessageBox.warning(self, "保存错误", "没有可保存的图表！")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图表", "", 
                                                  "PNG文件 (*.png);;JPEG文件 (*.jpg);;PDF文件 (*.pdf);;SVG文件 (*.svg)")
        if file_path:
            try:
                self.figure.savefig(file_path)
                QMessageBox.information(self, "保存成功", f"图表已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "保存错误", f"保存图表时出错: {str(e)}")
                
    def analyze_with_ai(self):
        """使用DeepSeek API分析数据"""
        if self.data is None:
            QMessageBox.warning(self, "数据错误", "请先输入数据！")
            return
            
        try:
            # 读取API配置
            current_dir = os.path.dirname(os.path.abspath(__file__))
            api_key_path = os.path.join(current_dir, "api.key")
            
            if not os.path.exists(api_key_path):
                QMessageBox.warning(self, "配置错误", "请先在统计图工具目录下创建api.key文件并配置DeepSeek API信息！")
                return
                
            with open(api_key_path, "r") as f:
                settings = json.load(f)
                url = settings.get("url", "https://api.deepseek.com/v1/chat/completions")
                api_key = settings.get("api_key", "")
                model = settings.get("model", "deepseek-chat")
                
            if not api_key:
                QMessageBox.warning(self, "配置错误", "请在api.key文件中配置有效的API Key！")
                return
                
            # 构造提示词
            prompt = f"""请分析以下数据，用简单易懂的语言概括数据的基本特点和趋势走向，字数不超过200字：
            {json.dumps(self.data, indent=2, ensure_ascii=False)}
            """
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "你是一个数据分析专家，能够用简洁明了的语言解释数据特点和趋势。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 400
            }
            
            # 显示正在分析的提示
            self.ai_result.setPlainText("正在分析数据，请稍候...")
            
            # 发送请求
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            
            # 显示结果
            self.ai_result.setPlainText(analysis)
            
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "API错误", f"调用DeepSeek API时出错: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "分析错误", f"分析数据时出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataVisualizationTool()
    window.show()
    sys.exit(app.exec())