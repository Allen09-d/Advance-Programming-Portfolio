from tkinter import *
from tkinter import messagebox, simpledialog, ttk

FILENAME = "studentMarks.txt"

# Load data from file
def load_data():
    students = []
    try:
        with open(FILENAME, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    code, name = parts[0], parts[1]
                    marks = list(map(int, parts[2:]))
                    students.append({'code': code, 'name': name, 'marks': marks})
    except FileNotFoundError:  # File doesn't exist yet
        pass
    return students

# Save student data to file
def save_data(students):
    with open(FILENAME, 'w') as f:
        for s in students:
            line = f"{s['code']},{s['name']}," + ",".join(map(str, s['marks']))
            f.write(line + "\n")

# Calculate coursework, exam, percentage, grade
def calc_stats(s):
    cw, exam = sum(s['marks'][:-1]), s['marks'][-1]  # Sum of coursework, last mark = exam
    pct = round((cw + exam) / 160 * 100, 2)          # Convert to percentage
    # Determine grade based on percentage
    grade = next(g for g, r in [('A',70),('B',60),('C',50),('D',40),('F',0)] if pct >= r)
    return cw, exam, pct, grade

# Refresh Treeview table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for i, s in enumerate(students):
        cw, exam, pct, grade = calc_stats(s)
        tag = 'even' if i % 2 == 0 else 'odd'  # Alternate row colors
        tree.insert('', 'end', values=(s['name'], s['code'], cw, exam, pct, grade), tags=(tag,))
    # Update status bar with student count and average %
    avg = round(sum(calc_stats(s)[2] for s in students) / len(students), 2) if students else 0
    status.set(f"Students: {len(students)} | Avg %: {avg}")

# View individual student
def view_individual():
    choice = simpledialog.askstring("Select Student", "Enter name or code:")
    for s in students:
        if choice in (s['name'], s['code']):
            cw, exam, pct, grade = calc_stats(s)
            messagebox.showinfo("Student Record",
                f"Name: {s['name']}\nCode: {s['code']}\nCoursework: {cw}\nExam: {exam}\n%: {pct}\nGrade: {grade}")
            return
    messagebox.showerror("Not Found", "Student not found.")

# Show highest or lowest scorer
def show_extreme(high=True):
    if not students: return
    key = lambda s: calc_stats(s)[2]  # Compare based on percentage
    s = max(students, key=key) if high else min(students, key=key)
    cw, exam, pct, grade = calc_stats(s)
    title = "Highest" if high else "Lowest"
    messagebox.showinfo(f"{title} Scorer",
        f"Name: {s['name']}\nCode: {s['code']}\nCoursework: {cw}\nExam: {exam}\n%: {pct}\nGrade: {grade}")

# Sort students ascending/descending
def sort_records():
    order = simpledialog.askstring("Sort", "asc or desc?")
    rev = order == 'desc'
    students.sort(key=lambda s: calc_stats(s)[2], reverse=rev)
    refresh_table()

# Add new student
def add_student():
    code = simpledialog.askstring("Add", "Student code:")
    name = simpledialog.askstring("Add", "Student name:")
    marks = simpledialog.askstring("Add", "Marks (comma-separated):")
    try:
        mark_list = list(map(int, marks.split(',')))
        students.append({'code': code, 'name': name, 'marks': mark_list})
        save_data(students)
        refresh_table()
    except:
        messagebox.showerror("Error", "Invalid marks.")

# Delete student
def delete_student():
    ident = simpledialog.askstring("Delete", "Enter name/code:")
    for i, s in enumerate(students):
        if ident in (s['name'], s['code']):
            del students[i]
            save_data(students)
            refresh_table()
            return
    messagebox.showerror("Not Found", "Student not found.")

# Update existing student
def update_student():
    ident = simpledialog.askstring("Update", "Enter name/code:")
    for s in students:
        if ident in (s['name'], s['code']):
            new_name = simpledialog.askstring("Update", "New name (blank to skip):")
            new_marks = simpledialog.askstring("Update", "New marks (blank to skip):")
            if new_name: s['name'] = new_name
            if new_marks:
                try: s['marks'] = list(map(int, new_marks.split(',')))
                except: messagebox.showerror("Error", "Invalid marks.")
            save_data(students)
            refresh_table()
            return
    messagebox.showerror("Not Found", "Student not found.")

# Main GUI 
root = Tk()
root.title("Student Manager")
root.configure(bg="#f0f4fc")

# Style for Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#dbe9f4")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.map("Treeview", background=[('selected', '#cce5ff')])
style.configure("TButton", font=("Segoe UI", 10), padding=5)

# Status label
status = StringVar()

# Treeview table setup
tree = ttk.Treeview(root, columns=('Name','Code','CW','Exam','%','Grade'), show='headings')
for col in tree['columns']:
    tree.heading(col, text=col)
tree.tag_configure('even', background='#f9f9f9')
tree.tag_configure('odd', background='#e0f7fa')
tree.pack(fill='both', expand=True, padx=10, pady=10)

# Buttons for actions
btn_frame = Frame(root, bg="#f0f4fc")
btn_frame.pack(fill='x', padx=10)
for txt, cmd in [
    ("View All", refresh_table),
    ("View Individual", view_individual),
    ("Highest Scorer", lambda: show_extreme(True)),
    ("Lowest Scorer", lambda: show_extreme(False)),
    ("Sort Records", sort_records),
    ("Add Student", add_student),
    ("Delete Student", delete_student),
    ("Update Student", update_student),
]:
    Button(btn_frame, text=txt, command=cmd, bg="#d0eaff", fg="#003366", relief="raised").pack(side='left', padx=5, pady=5)

# Status bar
Label(root, textvariable=status, font=("Segoe UI", 10), bg="#f0f4fc").pack(pady=5)

# Load initial data and populate table
students = load_data()
refresh_table()

root.mainloop()
