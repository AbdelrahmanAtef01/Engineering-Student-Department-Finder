# advisor_interface.py

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QGridLayout, QComboBox, QGroupBox, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt
from pyswip import Prolog
import sys
import re

class AdvisorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Department Advisor")
        self.setGeometry(100, 100, 600, 700)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Grades Input
        grade_group = QGroupBox("Enter your grades")
        grade_layout = QGridLayout()
        self.grade_inputs = {}
        subjects = [
            "engineering_drawing_1", "engineering_drawing_2", "statics", "dynamics",
            "differentiation", "integration", "computer_principles",
            "physics_light_heat", "physics_electricity_substances",
            "principles_manufacturing", "engineering_chemistry", "technical_english"
        ]
        for i, subject in enumerate(subjects):
            grade_label = QLabel(subject.replace("_", " ").title())
            grade_combo = QComboBox()
            for g in ["A", "B", "C", "D", "F"]:
                grade_combo.addItem(g)
            self.grade_inputs[subject] = grade_combo
            grade_layout.addWidget(grade_label, i, 0)
            grade_layout.addWidget(grade_combo, i, 1)
        grade_group.setLayout(grade_layout)
        layout.addWidget(grade_group)

        # Interests
        interest_labels = ["Programming", "Drawing", "Math", "Mechanics", "Electronics"]
        self.interest_spinboxes = {}
        interest_group = QGroupBox("Rank your interests (1 = Not Interested, 5 = Very Interested)")
        interest_layout = QGridLayout()
        for i, label in enumerate(interest_labels):
            spinbox = QSpinBox()
            spinbox.setRange(1, 5)
            spinbox.setValue(3)
            interest_layout.addWidget(QLabel(label), i, 0)
            interest_layout.addWidget(spinbox, i, 1)
            self.interest_spinboxes[label.lower()] = spinbox
        interest_group.setLayout(interest_layout)
        layout.addWidget(interest_group)

        # Traits
        trait_labels = ["Creative", "Analytical", "Team-Oriented", "Physical Work", "Visual Thinking"]
        self.trait_spinboxes = {}
        trait_group = QGroupBox("Rank your personality traits (1 = Not at all, 5 = Very much)")
        trait_layout = QGridLayout()
        for i, label in enumerate(trait_labels):
            spinbox = QSpinBox()
            spinbox.setRange(1, 5)
            spinbox.setValue(3)
            trait_layout.addWidget(QLabel(label), i, 0)
            trait_layout.addWidget(spinbox, i, 1)
            self.trait_spinboxes[label.lower().replace(" ", "_")] = spinbox
        trait_group.setLayout(trait_layout)
        layout.addWidget(trait_group)

        # Output box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        # Submit button
        submit_btn = QPushButton("Get Recommendation")
        submit_btn.clicked.connect(self.submit_form)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def parse_prolog_pair(self, pair_str):
        # Remove leading and trailing whitespace or commas, and match the pair format.
        pair_str = pair_str.strip().strip(',')  # Remove leading/trailing spaces and commas
        match = re.match(r'\((\w+),\s*([\d\.]+)\)', pair_str)
        if match:
            dept = match.group(1)
            score = float(match.group(2))
            return dept, score
        return None, None

    def submit_form(self):
        # Generate Prolog facts from inputs
        student_facts = []

        for subj, combo in self.grade_inputs.items():
            grade = combo.currentText().lower()
            student_facts.append(f"grade({subj}, {grade}).")

        interest_values = {k: sb.value() for k, sb in self.interest_spinboxes.items()}
        for interest, value in interest_values.items():
            student_facts.append(f"interest({interest}, {value}).")

        trait_values = {k: sb.value() for k, sb in self.trait_spinboxes.items()}
        for trait, value in trait_values.items():
            student_facts.append(f"trait({trait}, {value}).")

        # Write to temporary student file
        with open("student_temp.pl", "w") as f:
            f.write("\n".join(student_facts))

        # Query Prolog
        prolog = Prolog()
        prolog.consult("advisor.pl")
        prolog.consult("student_temp.pl")

        results = list(prolog.query("recommend_all(Sorted)."))
        print("Prolog Results:", results)

        if results:
            ranked = results[0]["Sorted"]
            output = "Ranked Department Recommendations:\n\n"
            for item in ranked:
                dept, score = self.parse_prolog_pair(item)
                print(f"Parsed: {dept}, {score}")
                if dept is not None:
                    name = dept.replace("_", " ").title()
                    output += f"- {name}: {round(score, 2)}\n"
        else:
            output = "No recommendation available."

        self.result_box.setText(output)
        print("Output Set: ", output)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdvisorApp()
    window.show()
    sys.exit(app.exec_())
