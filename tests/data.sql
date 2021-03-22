INSERT into person (id, first_name, middle_name, last_name, email, age, metadata) 
VALUES
    (0, 'first', NULL, 'last', 'first.last@email.com', 30, '{"20201003": "stringified-data")}'),
    (1, 'new_name', 'middle', 'tester', 'test@email.com', 45, '{"20201003": "''id'': 1, ''first_name'': "test", ''middle_name'': "middle", ''last_name'': "tester", ''email'': "test@email.com", ''age'': 45")}');