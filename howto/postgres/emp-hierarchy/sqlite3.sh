#!/bin/bash


rm -f employees.db

cat <<'EOF' | sqlite3 employees.db
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    emp_name TEXT NOT NULL,
    manager_id INTEGER
);
INSERT INTO employees (emp_id, emp_name, manager_id)
VALUES
    (7, 'john', NULL),
    (1, 'jack', 7),
    (6, 'jill', 7),
    (5, 'mary', 7),
    (4, 'mo', 5),
    (2, 'jane', 6),
    (3, 'mike', 6);

WITH RECURSIVE top_manager AS (
    SELECT emp_id, emp_name
    FROM employees
    WHERE manager_id IS NULL
    LIMIT 1
),
employee_paths AS (
    SELECT emp_id, emp_name, CAST(emp_name AS TEXT) AS employee_path
    FROM employees
    WHERE emp_id = (SELECT emp_id FROM top_manager)
    
    UNION ALL
    
    SELECT e.emp_id, e.emp_name, ep.employee_path || '/' || e.emp_name
    FROM employees AS e
    JOIN employee_paths AS ep ON e.manager_id = ep.emp_id
)
SELECT employee_path
FROM employee_paths
ORDER BY employee_path;
EOF

rm -f employees.db
