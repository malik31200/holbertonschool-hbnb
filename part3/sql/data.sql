INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$U9r2LEgXhX9wqV5U9.4DjeH2Ho5SclSRnq72FwK8KJ1Sp8tL7TxDq',
    TRUE
);

INSERT INTO amenities (id, name)
VALUES
    ('4f1c31e2-67c4-4de1-b218-8b44a4fdbb8d', 'WiFi'),
    ('a8db6cb9-b6a5-4c26-8a34-f38b7a5c9e11', 'Swimming Pool'),
    ('b9c8e5a7-cc5b-47ac-b2b9-1e62a932a8c0', 'Air Conditioning');

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
  '1a2b3c4d-5678-90ab-cdef-1234567890ab',
  'Test Place',
  'Une belle maison test',
  100.0,
  48.8566,
  2.3522,
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);
