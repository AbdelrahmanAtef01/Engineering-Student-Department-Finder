% ---------- GRADE MAPPING ----------
grade_value(a, 4).
grade_value(b, 3).
grade_value(c, 2).
grade_value(d, 1).
grade_value(f, 0).

% ---------- DEPARTMENT LIST ----------
department(computer).
department(electrical).
department(communication).
department(civil).
department(mechanical).
department(production).
department(architecture).
department(geometrics).

% ---------- ELIGIBILITY RULES ----------
eligible(computer) :-
    grade(differentiation, G1), grade_value(G1, V1), V1 >= 2,
    grade(physics_electricity_substances, G2), grade_value(G2, V2), V2 >= 2.

eligible(electrical) :-
    eligible(computer).

eligible(communication) :-
    eligible(computer).

eligible(civil) :-
    grade(statics, G1), grade_value(G1, V1), V1 >= 2,
    grade(engineering_drawing_2, G2), grade_value(G2, V2), V2 >= 1.

eligible(mechanical) :-
    grade(integration, G1), grade_value(G1, V1), V1 >= 2,
    grade(physics_light_heat, G2), grade_value(G2, V2), V2 >= 2.

eligible(production) :-
    eligible(mechanical).

eligible(architecture) :-
    grade(engineering_drawing_2, G1), grade_value(G1, V1), V1 >= 2.

eligible(geometrics). % Always eligible

% ---------- ACADEMIC SCORE (0 to 1 normalized) ----------
academic_score(Dep, Score) :-
    findall(V, (
        department_course(Dep, Course),
        grade(Course, G),
        grade_value(G, V)
    ), Grades),
    average(Grades, Avg),
    Score is Avg / 4.0.

% Define important subjects for academic score (optional)
department_course(computer, differentiation).
department_course(computer, physics_electricity_substances).

department_course(electrical, differentiation).
department_course(electrical, physics_electricity_substances).

department_course(communication, differentiation).
department_course(communication, physics_electricity_substances).

department_course(civil, statics).
department_course(civil, engineering_drawing_2).

department_course(mechanical, integration).
department_course(mechanical, physics_light_heat).

department_course(production, integration).
department_course(production, physics_light_heat).

department_course(architecture, engineering_drawing_2).

department_course(geometrics, engineering_drawing_1).

% ---------- INTEREST SCORES ----------
interest_score(computer, programming).
interest_score(electrical, electronics).
interest_score(communication, electronics).
interest_score(civil, drawing).
interest_score(mechanical, mechanics).
interest_score(production, mechanics).
interest_score(architecture, drawing).
interest_score(geometrics, drawing).

% ---------- TRAIT SCORES ----------
trait_score(civil, physical_work).
trait_score(mechanical, physical_work).
trait_score(production, physical_work).
trait_score(geometrics, visual_thinking).
trait_score(architecture, visual_thinking).
trait_score(computer, analytical).
trait_score(electrical, analytical).
trait_score(communication, analytical).
trait_score(architecture, creative).
trait_score(civil, team_oriented).
trait_score(production, team_oriented).

% Sum interest scores (normalized)
total_interest_score(Dep, Score) :-
    findall(V, (
        interest_score(Dep, X),
        interest(X, V)
    ), Scores),
    average(Scores, Score0),
    (number(Score0) -> Score = Score0 / 5.0 ; Score = 0.0).

% Sum trait scores (normalized)
total_trait_score(Dep, Score) :-
    findall(V, (
        trait_score(Dep, X),
        trait(X, V)
    ), Scores),
    average(Scores, Score0),
    (number(Score0) -> Score = Score0 / 5.0 ; Score = 0.0).

% ---------- FINAL SCORING ----------
department_score(Dep, Total) :-
    eligible(Dep),
    academic_score(Dep, A),
    total_interest_score(Dep, I),
    total_trait_score(Dep, T),
    Total is A * 0.5 + I * 0.3 + T * 0.2.

% ---------- RECOMMENDATION OUTPUT ----------
recommend_all(Sorted) :-
    findall((Dep, Score), department_score(Dep, Score), Pairs),
    sort(2, @>=, Pairs, Sorted).

% ---------- UTILITIES ----------
average(List, Avg) :-
    sum_list(List, Sum),
    length(List, Len),
    Len > 0,
    Avg is Sum / Len.
