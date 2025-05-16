-- SQL script to create the reports table for the stray animal app

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    image TEXT,
    status TEXT DEFAULT 'pending',
    notices INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ngo_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    ngo_username TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports (id)
);
