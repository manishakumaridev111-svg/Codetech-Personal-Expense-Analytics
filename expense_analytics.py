"""
Personal Expense Analytics - CodTech Internship Task 3
A PyQt6-based GUI application for tracking and analyzing personal expenses.
Features: Add/track expenses, Category-wise breakdown, Monthly summary,
          Charts/graphs, Budget alerts
"""

import sys
import csv
import os
import json
from datetime import datetime, date
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidget,
    QTableWidgetItem, QTabWidget, QFrame, QScrollArea, QDialog,
    QDialogButtonBox, QFormLayout, QMessageBox, QProgressBar,
    QHeaderView, QSplitter, QSpinBox, QDoubleSpinBox, QGridLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QColor, QFont, QPainter, QPen, QBrush, QLinearGradient,
    QPalette, QIcon, QPixmap
)
from PyQt6.QtCharts import (
    QChart, QChartView, QPieSeries, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QLineSeries, QDateTimeAxis
)

# ─── Constants ───────────────────────────────────────────────────────────────

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budgets.json"

CATEGORIES = [
    "🍔 Food & Dining", "🚗 Transport", "🛍️ Shopping", "🏠 Housing",
    "💊 Health", "🎬 Entertainment", "📚 Education", "💡 Utilities",
    "✈️ Travel", "📱 Subscriptions", "🎁 Gifts", "📦 Others"
]

CAT_COLORS = {
    "🍔 Food & Dining": "#FF6B6B",
    "🚗 Transport":     "#4ECDC4",
    "🛍️ Shopping":      "#45B7D1",
    "🏠 Housing":       "#96CEB4",
    "💊 Health":        "#FFEAA7",
    "🎬 Entertainment": "#DDA0DD",
    "📚 Education":     "#98D8C8",
    "💡 Utilities":     "#F7DC6F",
    "✈️ Travel":        "#85C1E9",
    "📱 Subscriptions": "#F0B27A",
    "🎁 Gifts":         "#D7BDE2",
    "📦 Others":        "#AEB6BF"
}

STYLESHEET = """
QMainWindow {
    background-color: #0F1117;
}
QWidget {
    background-color: #0F1117;
    color: #E8EAF0;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QTabWidget::pane {
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    background: #161B2E;
}
QTabBar::tab {
    background: #1E2235;
    color: #8B8FA8;
    padding: 12px 24px;
    border-radius: 8px;
    margin: 4px 2px;
    font-size: 13px;
    font-weight: 500;
}
QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C3AED, stop:1 #4F46E5);
    color: white;
}
QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox {
    background: #1E2235;
    border: 1.5px solid #2A2D3E;
    border-radius: 8px;
    padding: 10px 14px;
    color: #E8EAF0;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1.5px solid #7C3AED;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #7C3AED;
    margin-right: 8px;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C3AED, stop:1 #4F46E5);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 11px 24px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8B5CF6, stop:1 #6366F1);
}
QPushButton:pressed {
    background: #5B21B6;
}
QPushButton#danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #EF4444, stop:1 #DC2626);
}
QPushButton#secondary {
    background: #1E2235;
    border: 1.5px solid #2A2D3E;
    color: #8B8FA8;
}
QPushButton#secondary:hover {
    border-color: #7C3AED;
    color: #E8EAF0;
}
QTableWidget {
    background: #161B2E;
    border: none;
    border-radius: 10px;
    gridline-color: #1E2235;
    font-size: 13px;
}
QTableWidget::item {
    padding: 10px 12px;
    border-bottom: 1px solid #1E2235;
}
QTableWidget::item:selected {
    background: #2A2D3E;
    color: white;
}
QHeaderView::section {
    background: #1E2235;
    color: #8B8FA8;
    padding: 12px;
    border: none;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QScrollBar:vertical {
    background: #1E2235;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #7C3AED;
    border-radius: 3px;
}
QProgressBar {
    background: #1E2235;
    border-radius: 6px;
    height: 10px;
    text-align: center;
    font-size: 11px;
}
QProgressBar::chunk {
    border-radius: 6px;
}
QFrame#card {
    background: #161B2E;
    border: 1px solid #2A2D3E;
    border-radius: 14px;
}
QLabel#title {
    font-size: 22px;
    font-weight: 700;
    color: #E8EAF0;
}
QLabel#subtitle {
    font-size: 13px;
    color: #8B8FA8;
}
QLabel#stat_value {
    font-size: 28px;
    font-weight: 800;
    color: #E8EAF0;
}
QLabel#stat_label {
    font-size: 12px;
    color: #8B8FA8;
    font-weight: 500;
}
QLabel#alert_warn {
    background: #2D1F1F;
    border: 1px solid #EF4444;
    border-radius: 8px;
    color: #FCA5A5;
    padding: 10px 14px;
    font-size: 13px;
}
QLabel#alert_ok {
    background: #1A2D1A;
    border: 1px solid #22C55E;
    border-radius: 8px;
    color: #86EFAC;
    padding: 10px 14px;
    font-size: 13px;
}
"""

# ─── Data Manager ─────────────────────────────────────────────────────────────

class DataManager:
    def __init__(self):
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "date", "category", "description", "amount"])

        if not os.path.exists(BUDGET_FILE):
            budgets = {cat: 0 for cat in CATEGORIES}
            with open(BUDGET_FILE, "w") as f:
                json.dump(budgets, f)

    def load_expenses(self):
        expenses = []
        try:
            with open(DATA_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["amount"] = float(row["amount"])
                    expenses.append(row)
        except Exception:
            pass
        return expenses

    def add_expense(self, date_str, category, description, amount):
        expenses = self.load_expenses()
        new_id = str(len(expenses) + 1)
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([new_id, date_str, category, description, amount])

    def delete_expense(self, expense_id):
        expenses = self.load_expenses()
        expenses = [e for e in expenses if e["id"] != expense_id]
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "category", "description", "amount"])
            for e in expenses:
                writer.writerow([e["id"], e["date"], e["category"], e["description"], e["amount"]])

    def load_budgets(self):
        try:
            with open(BUDGET_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {cat: 0 for cat in CATEGORIES}

    def save_budgets(self, budgets):
        with open(BUDGET_FILE, "w") as f:
            json.dump(budgets, f)

# ─── Stat Card ────────────────────────────────────────────────────────────────

class StatCard(QFrame):
    def __init__(self, label, value, accent="#7C3AED"):
        super().__init__()
        self.setObjectName("card")
        self.accent = accent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        self.val_label = QLabel(value)
        self.val_label.setObjectName("stat_value")
        self.val_label.setStyleSheet(f"color: {accent}; font-size: 26px; font-weight: 800;")

        self.lbl_label = QLabel(label)
        self.lbl_label.setObjectName("stat_label")

        layout.addWidget(self.val_label)
        layout.addWidget(self.lbl_label)

    def update_value(self, value):
        self.val_label.setText(value)

# ─── Add Expense Tab ──────────────────────────────────────────────────────────

class AddExpenseTab(QWidget):
    expense_added = pyqtSignal()

    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 30, 30, 30)
        outer.setSpacing(20)

        # Header
        hdr = QLabel("Add New Expense")
        hdr.setObjectName("title")
        outer.addWidget(hdr)

        sub = QLabel("Track where your money is going")
        sub.setObjectName("subtitle")
        outer.addWidget(sub)

        # Form card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(16)

        # Row 1: Date + Category
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        date_col = QVBoxLayout()
        date_col.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd MMM yyyy")
        date_col.addWidget(self.date_edit)

        cat_col = QVBoxLayout()
        cat_col.addWidget(QLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(CATEGORIES)
        cat_col.addWidget(self.cat_combo)

        row1.addLayout(date_col)
        row1.addLayout(cat_col)
        card_layout.addLayout(row1)

        # Row 2: Description + Amount
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        desc_col = QVBoxLayout()
        desc_col.addWidget(QLabel("Description"))
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("e.g. Lunch at Cafe Coffee Day")
        desc_col.addWidget(self.desc_edit)

        amt_col = QVBoxLayout()
        amt_col.addWidget(QLabel("Amount (₹)"))
        self.amt_edit = QDoubleSpinBox()
        self.amt_edit.setRange(0.01, 9999999)
        self.amt_edit.setDecimals(2)
        self.amt_edit.setPrefix("₹ ")
        amt_col.addWidget(self.amt_edit)

        row2.addLayout(desc_col, 2)
        row2.addLayout(amt_col, 1)
        card_layout.addLayout(row2)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch()

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondary")
        clear_btn.setFixedWidth(100)
        clear_btn.clicked.connect(self._clear)

        add_btn = QPushButton("➕  Add Expense")
        add_btn.setFixedWidth(160)
        add_btn.clicked.connect(self._add_expense)

        btn_row.addWidget(clear_btn)
        btn_row.addWidget(add_btn)
        card_layout.addLayout(btn_row)

        outer.addWidget(card)

        # Quick summary
        self.summary_label = QLabel("")
        self.summary_label.setObjectName("subtitle")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(self.summary_label)

        outer.addStretch()

    def _clear(self):
        self.date_edit.setDate(QDate.currentDate())
        self.cat_combo.setCurrentIndex(0)
        self.desc_edit.clear()
        self.amt_edit.setValue(0)
        self.summary_label.setText("")

    def _add_expense(self):
        desc = self.desc_edit.text().strip()
        amount = self.amt_edit.value()

        if not desc:
            QMessageBox.warning(self, "Missing Info", "Please enter a description.")
            return
        if amount <= 0:
            QMessageBox.warning(self, "Missing Info", "Please enter a valid amount.")
            return

        date_str = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.cat_combo.currentText()

        self.dm.add_expense(date_str, category, desc, amount)
        self.summary_label.setText(f"✅ Added: {category} — ₹{amount:,.2f} ({desc})")
        self._clear()
        self.expense_added.emit()

# ─── Expense List Tab ─────────────────────────────────────────────────────────

class ExpenseListTab(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Header row
        hdr_row = QHBoxLayout()
        title = QLabel("All Expenses")
        title.setObjectName("title")
        hdr_row.addWidget(title)
        hdr_row.addStretch()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search...")
        self.search_edit.setFixedWidth(220)
        self.search_edit.textChanged.connect(self._filter)
        hdr_row.addWidget(self.search_edit)

        self.filter_cat = QComboBox()
        self.filter_cat.addItem("All Categories")
        self.filter_cat.addItems(CATEGORIES)
        self.filter_cat.currentIndexChanged.connect(self._filter)
        hdr_row.addWidget(self.filter_cat)

        layout.addLayout(hdr_row)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["#", "Date", "Category", "Description", "Amount", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

        # Total row
        total_row = QHBoxLayout()
        total_row.addStretch()
        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #7C3AED;")
        total_row.addWidget(self.total_label)
        layout.addLayout(total_row)

        self.all_expenses = []
        self.refresh()

    def refresh(self):
        self.all_expenses = self.dm.load_expenses()
        self._filter()

    def _filter(self):
        search = self.search_edit.text().lower()
        cat_filter = self.filter_cat.currentText()

        filtered = self.all_expenses
        if search:
            filtered = [e for e in filtered if search in e["description"].lower() or search in e["category"].lower()]
        if cat_filter != "All Categories":
            filtered = [e for e in filtered if e["category"] == cat_filter]

        self._populate(filtered)

    def _populate(self, expenses):
        self.table.setRowCount(len(expenses))
        total = 0
        for row, exp in enumerate(expenses):
            total += exp["amount"]
            items = [
                QTableWidgetItem(exp["id"]),
                QTableWidgetItem(exp["date"]),
                QTableWidgetItem(exp["category"]),
                QTableWidgetItem(exp["description"]),
                QTableWidgetItem(f"₹ {exp['amount']:,.2f}"),
            ]
            color = CAT_COLORS.get(exp["category"], "#AEB6BF")
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col == 2:
                    item.setForeground(QColor(color))
                if col == 4:
                    item.setForeground(QColor("#22C55E"))
                self.table.setItem(row, col, item)

            del_btn = QPushButton("🗑")
            del_btn.setObjectName("danger")
            del_btn.setFixedSize(34, 34)
            del_btn.setStyleSheet("font-size:16px; padding:0; border-radius:6px; background:#2D1F1F;")
            del_btn.clicked.connect(lambda _, eid=exp["id"]: self._delete(eid))
            self.table.setCellWidget(row, 5, del_btn)
            self.table.setRowHeight(row, 46)

        self.total_label.setText(f"Total: ₹{total:,.2f}")

    def _delete(self, expense_id):
        reply = QMessageBox.question(self, "Delete?", "Remove this expense?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.dm.delete_expense(expense_id)
            self.refresh()
            self.data_changed.emit()

# ─── Charts Tab ───────────────────────────────────────────────────────────────

class ChartsTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Analytics & Charts")
        title.setObjectName("title")
        layout.addWidget(title)

        # Month filter
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Month:"))
        self.month_combo = QComboBox()
        months = ["All Time"] + [date(2024, m, 1).strftime("%B %Y") for m in range(1, 13)]
        # Build dynamic month list from data
        self.month_combo.addItem("All Time")
        self.month_combo.setFixedWidth(160)
        self.month_combo.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.month_combo)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Charts row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        self.pie_view = QChartView()
        self.pie_view.setMinimumHeight(320)
        self.pie_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.bar_view = QChartView()
        self.bar_view.setMinimumHeight(320)
        self.bar_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        charts_row.addWidget(self.pie_view)
        charts_row.addWidget(self.bar_view)
        layout.addLayout(charts_row)

        self.refresh()

    def refresh(self):
        expenses = self.dm.load_expenses()

        # Update month combo
        months_set = sorted({e["date"][:7] for e in expenses}, reverse=True)
        current = self.month_combo.currentText()
        self.month_combo.blockSignals(True)
        self.month_combo.clear()
        self.month_combo.addItem("All Time")
        for m in months_set:
            dt = datetime.strptime(m, "%Y-%m")
            self.month_combo.addItem(dt.strftime("%B %Y"))
        idx = self.month_combo.findText(current)
        self.month_combo.setCurrentIndex(max(idx, 0))
        self.month_combo.blockSignals(False)

        selected = self.month_combo.currentText()
        if selected != "All Time":
            dt = datetime.strptime(selected, "%B %Y")
            expenses = [e for e in expenses if e["date"].startswith(dt.strftime("%Y-%m"))]

        self._build_pie(expenses)
        self._build_bar(expenses)

    def _build_pie(self, expenses):
        cat_totals = defaultdict(float)
        for e in expenses:
            cat_totals[e["category"]] += e["amount"]

        series = QPieSeries()
        for cat, total in sorted(cat_totals.items(), key=lambda x: -x[1]):
            sl = series.append(f"{cat}  ₹{total:,.0f}", total)
            color = CAT_COLORS.get(cat, "#AEB6BF")
            sl.setColor(QColor(color))
            sl.setLabelColor(QColor("#E8EAF0"))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Spending by Category")
        chart.setTitleFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        chart.setTitleBrush(QBrush(QColor("#E8EAF0")))
        chart.setBackgroundBrush(QBrush(QColor("#161B2E")))
        chart.legend().setVisible(True)
        chart.legend().setLabelColor(QColor("#8B8FA8"))
        chart.legend().setBackgroundVisible(False)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.pie_view.setChart(chart)
        self.pie_view.setBackgroundBrush(QBrush(QColor("#161B2E")))

    def _build_bar(self, expenses):
        monthly = defaultdict(float)
        for e in expenses:
            month = e["date"][:7]
            monthly[month] += e["amount"]

        sorted_months = sorted(monthly.keys())[-6:]
        bar_set = QBarSet("Monthly Spending")
        bar_set.setColor(QColor("#7C3AED"))

        labels = []
        for m in sorted_months:
            dt = datetime.strptime(m, "%Y-%m")
            labels.append(dt.strftime("%b '%y"))
            bar_set.append(monthly[m])

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Monthly Spending Trend")
        chart.setTitleFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        chart.setTitleBrush(QBrush(QColor("#E8EAF0")))
        chart.setBackgroundBrush(QBrush(QColor("#161B2E")))

        ax = QBarCategoryAxis()
        ax.append(labels if labels else ["No data"])
        ax.setLabelsColor(QColor("#8B8FA8"))
        chart.addAxis(ax, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(ax)

        ay = QValueAxis()
        ay.setLabelsColor(QColor("#8B8FA8"))
        ay.setGridLineColor(QColor("#2A2D3E"))
        chart.addAxis(ay, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(ay)

        chart.legend().setVisible(False)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.bar_view.setChart(chart)
        self.bar_view.setBackgroundBrush(QBrush(QColor("#161B2E")))

# ─── Budget Tab ───────────────────────────────────────────────────────────────

class BudgetTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        hdr_row = QHBoxLayout()
        title = QLabel("Budget & Alerts")
        title.setObjectName("title")
        hdr_row.addWidget(title)
        hdr_row.addStretch()

        month_lbl = QLabel(datetime.now().strftime("📅 %B %Y"))
        month_lbl.setStyleSheet("color: #8B8FA8; font-size: 13px;")
        hdr_row.addWidget(month_lbl)
        layout.addLayout(hdr_row)

        sub = QLabel("Set monthly budgets per category. Get alerts when you exceed them.")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)

        # Scroll area for budget rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.budget_layout = QVBoxLayout(container)
        self.budget_layout.setSpacing(10)
        self.budget_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Save btn
        save_btn = QPushButton("💾  Save Budgets")
        save_btn.setFixedWidth(180)
        save_btn.clicked.connect(self._save)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.spin_map = {}
        self.refresh()

    def refresh(self):
        # Clear old rows
        while self.budget_layout.count():
            child = self.budget_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        budgets = self.dm.load_budgets()
        expenses = self.dm.load_expenses()

        # This month spending
        this_month = datetime.now().strftime("%Y-%m")
        month_spending = defaultdict(float)
        for e in expenses:
            if e["date"].startswith(this_month):
                month_spending[e["category"]] += e["amount"]

        self.spin_map = {}

        for cat in CATEGORIES:
            budget = budgets.get(cat, 0)
            spent = month_spending.get(cat, 0)
            color = CAT_COLORS.get(cat, "#AEB6BF")

            card = QFrame()
            card.setObjectName("card")
            card.setFixedHeight(90)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(6)

            row1 = QHBoxLayout()
            cat_lbl = QLabel(cat)
            cat_lbl.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 13px;")
            row1.addWidget(cat_lbl)
            row1.addStretch()

            spent_lbl = QLabel(f"₹{spent:,.0f} / ")
            spent_lbl.setStyleSheet("color: #8B8FA8; font-size: 12px;")
            row1.addWidget(spent_lbl)

            spin = QDoubleSpinBox()
            spin.setRange(0, 999999)
            spin.setValue(budget)
            spin.setPrefix("₹")
            spin.setDecimals(0)
            spin.setFixedWidth(110)
            spin.setFixedHeight(30)
            row1.addWidget(spin)
            self.spin_map[cat] = spin

            card_layout.addLayout(row1)

            # Progress bar
            pct = int((spent / budget * 100)) if budget > 0 else 0
            pct_clamped = min(pct, 100)
            prog = QProgressBar()
            prog.setValue(pct_clamped)

            if pct >= 100:
                prog.setStyleSheet(f"QProgressBar::chunk {{ background: #EF4444; }}")
                prog.setFormat(f"⚠️ OVER BUDGET! {pct}%")
            elif pct >= 80:
                prog.setStyleSheet(f"QProgressBar::chunk {{ background: #F59E0B; }}")
                prog.setFormat(f"⚡ {pct}% used")
            else:
                prog.setStyleSheet(f"QProgressBar::chunk {{ background: {color}; }}")
                prog.setFormat(f"{pct}% used")

            prog.setTextVisible(True)
            card_layout.addWidget(prog)
            self.budget_layout.addWidget(card)

        self.budget_layout.addStretch()

    def _save(self):
        budgets = {cat: self.spin_map[cat].value() for cat in CATEGORIES}
        self.dm.save_budgets(budgets)
        QMessageBox.information(self, "Saved", "✅ Budgets saved successfully!")
        self.refresh()

# ─── Summary Tab ──────────────────────────────────────────────────────────────

class SummaryTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Monthly Summary")
        title.setObjectName("title")
        layout.addWidget(title)

        # Stat cards row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        self.total_card  = StatCard("Total Spent This Month", "₹0", "#7C3AED")
        self.avg_card    = StatCard("Daily Average", "₹0", "#4ECDC4")
        self.top_card    = StatCard("Top Category", "—", "#FF6B6B")
        self.count_card  = StatCard("Transactions", "0", "#F59E0B")

        for c in [self.total_card, self.avg_card, self.top_card, self.count_card]:
            stats_row.addWidget(c)

        layout.addLayout(stats_row)

        # Month-by-month table
        month_title = QLabel("Month-by-Month Breakdown")
        month_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #E8EAF0; margin-top: 8px;")
        layout.addWidget(month_title)

        self.month_table = QTableWidget()
        self.month_table.setColumnCount(4)
        self.month_table.setHorizontalHeaderLabels(["Month", "Transactions", "Total Spent", "Top Category"])
        self.month_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.month_table.verticalHeader().setVisible(False)
        self.month_table.setShowGrid(False)
        self.month_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.month_table)

        self.refresh()

    def refresh(self):
        expenses = self.dm.load_expenses()
        this_month = datetime.now().strftime("%Y-%m")

        # This month stats
        this_month_exp = [e for e in expenses if e["date"].startswith(this_month)]
        total = sum(e["amount"] for e in this_month_exp)
        count = len(this_month_exp)

        days_in_month = datetime.now().day
        avg = total / days_in_month if days_in_month else 0

        cat_totals = defaultdict(float)
        for e in this_month_exp:
            cat_totals[e["category"]] += e["amount"]
        top_cat = max(cat_totals, key=cat_totals.get) if cat_totals else "—"

        self.total_card.update_value(f"₹{total:,.0f}")
        self.avg_card.update_value(f"₹{avg:,.0f}")
        self.top_card.update_value(top_cat[:16] if top_cat != "—" else "—")
        self.count_card.update_value(str(count))

        # Monthly table
        monthly = defaultdict(list)
        for e in expenses:
            monthly[e["date"][:7]].append(e)

        sorted_months = sorted(monthly.keys(), reverse=True)
        self.month_table.setRowCount(len(sorted_months))

        for row, month in enumerate(sorted_months):
            exps = monthly[month]
            m_total = sum(e["amount"] for e in exps)
            m_cats = defaultdict(float)
            for e in exps:
                m_cats[e["category"]] += e["amount"]
            m_top = max(m_cats, key=m_cats.get) if m_cats else "—"

            dt = datetime.strptime(month, "%Y-%m")
            items = [
                QTableWidgetItem(dt.strftime("%B %Y")),
                QTableWidgetItem(str(len(exps))),
                QTableWidgetItem(f"₹ {m_total:,.2f}"),
                QTableWidgetItem(m_top),
            ]
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col == 2:
                    item.setForeground(QColor("#22C55E"))
                self.month_table.setItem(row, col, item)
            self.month_table.setRowHeight(row, 44)

# ─── Main Window ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dm = DataManager()
        self.setWindowTitle("💰 Personal Expense Analytics")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
        top_bar = QFrame()
        top_bar.setFixedHeight(64)
        top_bar.setStyleSheet("background: #161B2E; border-bottom: 1px solid #2A2D3E;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 0, 30, 0)

        logo = QLabel("💰 Expense Analytics")
        logo.setStyleSheet("font-size: 18px; font-weight: 800; color: #E8EAF0;")
        top_layout.addWidget(logo)
        top_layout.addStretch()

        self.header_total = QLabel("Loading...")
        self.header_total.setStyleSheet("font-size: 14px; color: #7C3AED; font-weight: 600;")
        top_layout.addWidget(self.header_total)

        main_layout.addWidget(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.add_tab     = AddExpenseTab(self.dm)
        self.list_tab    = ExpenseListTab(self.dm)
        self.charts_tab  = ChartsTab(self.dm)
        self.budget_tab  = BudgetTab(self.dm)
        self.summary_tab = SummaryTab(self.dm)

        self.tabs.addTab(self.add_tab,     "➕  Add Expense")
        self.tabs.addTab(self.list_tab,    "📋  All Expenses")
        self.tabs.addTab(self.charts_tab,  "📊  Charts")
        self.tabs.addTab(self.budget_tab,  "🎯  Budgets")
        self.tabs.addTab(self.summary_tab, "📈  Summary")

        main_layout.addWidget(self.tabs)

        # Connect signals
        self.add_tab.expense_added.connect(self._on_data_changed)
        self.list_tab.data_changed.connect(self._on_data_changed)

        self._refresh_header()

    def _on_data_changed(self):
        self.list_tab.refresh()
        self.charts_tab.refresh()
        self.budget_tab.refresh()
        self.summary_tab.refresh()
        self._refresh_header()

    def _refresh_header(self):
        expenses = self.dm.load_expenses()
        total = sum(e["amount"] for e in expenses)
        this_month = datetime.now().strftime("%Y-%m")
        month_total = sum(e["amount"] for e in expenses if e["date"].startswith(this_month))
        self.header_total.setText(
            f"This month: ₹{month_total:,.0f}   |   All time: ₹{total:,.0f}"
        )

# ─── Entry Point ─────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Personal Expense Analytics")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
