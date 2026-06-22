# 💰 Personal Expense Analytics
### CodTech Internship — Task 3

A sleek PyQt6-based desktop application to track, analyze, and manage your personal expenses with beautiful charts and smart budget alerts.

---

## 🚀 Features

| Feature | Description |
|---|---|
| ➕ Add Expenses | Log expenses with date, category, description, and amount |
| 📋 Expense List | View, search, filter, and delete all expenses |
| 📊 Charts | Pie chart (category breakdown) + Bar chart (monthly trend) |
| 🎯 Budget Alerts | Set monthly budgets per category with visual progress bars |
| 📈 Monthly Summary | Stats, averages, top categories, and month-wise table |

---

## 🛠️ Setup & Run

### 1. Install dependencies
```bash
pip install PyQt6 PyQt6-Charts
```

### 2. Run the app
```bash
python expense_analytics.py
```

---

## 📁 Project Structure

```
expense_analytics.py   ← Main application (single file)
expenses.csv           ← Auto-created; stores all expense records
budgets.json           ← Auto-created; stores category budgets
requirements.txt       ← Python dependencies
```

---

## 🖥️ Tech Stack

- **Python 3.10+**
- **PyQt6** — GUI framework
- **PyQt6-Charts** — Pie and bar charts
- **CSV** — Lightweight data storage
- **JSON** — Budget configuration

---

## 📸 UI Highlights

- Dark theme with purple gradient accents
- Responsive tab-based navigation
- Color-coded categories
- Real-time budget progress bars with ⚠️ over-budget alerts
- Live total in the header bar

---

*Built for CodTech Internship Task 3 — Personal Expense Analytics*
