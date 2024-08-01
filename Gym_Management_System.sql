-- Drop the existing database if it exists
drop database if exists gym_database;

-- Create the new database
create database gym_database;

-- Use the new database
use gym_database;

-- Create the staff table
create table staff (
    staffID varchar(255) primary key,
    income decimal(10, 2) not null check (income >= 0),
    position varchar(255) not null,
    hire_date date not null,
    workers_name varchar(255) not null,
    contact_information varchar(255) not null unique,
    employment varchar(255) not null
);

-- Create the inventory_table
create table inventory_table (
    inventoryID int primary key auto_increment,
    item_name varchar(255) not null,
    status varchar(255) not null,
    quantity int not null check (quantity >= 0),
    purchase_date date not null,
    unique (item_name, purchase_date) -- Ensure no duplicate items with the same purchase date
);

-- Create the gym_equipment_table
create table gym_equipment_table (
    inventoryID int,
    status varchar(255) not null,
    last_maintenance_date date not null,
    foreign key (inventoryID) references inventory_table(inventoryID) on delete cascade on update cascade,
    check (last_maintenance_date >= '2024-01-01') -- Ensure maintenance dates are in 2024
);

-- Create the class_schedules table
create table class_schedules (
    classID varchar(255) primary key,
    staffID varchar(255),
    programID int,
    class_name varchar(255) not null,
    day_of_week varchar(50) not null check (day_of_week in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    start_time time not null,
    end_time time not null ,
    foreign key (staffID) references staff(staffID) on delete set null on update cascade
);

-- Create the training_programs table
create table training_programs (
    programID int primary key auto_increment,
    classID varchar(255),
    program_name varchar(255) not null,
    duration varchar(255) not null,
    description varchar(255) not null,
    foreign key (classID) references class_schedules(classID) on delete set null on update cascade
);

-- Create the members table
create table members (
    memberID varchar(255) primary key,
    programID int,
    last_name varchar(255) not null,
    first_name varchar(255) not null,
    mtype_price decimal(10, 2) not null check (mtype_price >= 0),
    start_date date not null,
    end_date date not null, -- Ensure end date is after start date
    contact_information varchar(255) not null unique,
    membership_type varchar(255) not null,
    foreign key (programID) references training_programs(programID) on delete set null on update cascade
);

-- Create the visitor_table
create table visitor_table (
    visitorID varchar(255) primary key,
    visitor_name varchar(255) not null,
    purpose_of_visit varchar(255) not null,
    contact_information varchar(255) not null unique
);

-- Create the attendance table
create table attendance (
    attendanceID int primary key auto_increment,
    personID varchar(255) not null,
    person_type varchar(50) not null check (person_type in ('member', 'staff', 'visitor')),
    arrival_time time not null,
    departure_time time not null, -- Ensure departure time is after arrival time
    date date not null
);

-- Create the damage table
create table damage (
    damageID int primary key auto_increment,
    personID varchar(255) not null,
    person_type varchar(50) not null check (person_type in ('member', 'staff', 'visitor')),
    inventoryID int,
    damage_type varchar(255) not null,
    cost decimal(10, 2) not null check (cost >= 0),
    damage_date date not null,
    foreign key (inventoryID) references inventory_table(inventoryID) on delete set null on update cascade
);

-- Create the feedback table
create table feedback (
    feedbackID int primary key auto_increment,
    personID varchar(255) not null,
    person_type varchar(50) not null check (person_type in ('member', 'staff', 'visitor')),
    feedback text not null,
    date date not null
);

-- Create the booking table
create table booking (
    bookingID int primary key auto_increment,
    memberID varchar(255) not null,
    staffID varchar(255) not null,
    booking_date date not null,
    duration varchar(255) not null,
    booking_time time not null,
    foreign key (memberID) references members(memberID) on delete cascade on update cascade,
    foreign key (staffID) references staff(staffID) on delete cascade on update cascade,
    unique (memberID, staffID, booking_date, booking_time) -- Ensure no duplicate bookings
);

-- Create the payment table
create table payment (
    paymentID int primary key auto_increment,
    person_ID varchar(50) not null,
    amount decimal(10, 2) not null check (amount >= 0),
    payment_date date not null,
    reason_for_payment varchar(255) not null
);

-- Create the class_attendance table
create table class_attendance (
    class_attendanceID int primary key auto_increment,
    memberID varchar(255),
    classID varchar(255) not null,
    attendance_date date not null,
    foreign key (memberID) references members(memberID) on delete cascade on update cascade,
    foreign key (classID) references class_schedules(classID) on delete cascade on update cascade
);

INSERT INTO staff (staffID, income, position, hire_date, workers_name, contact_information, employment) VALUES
('ST001', 1500.00, 'Fitness Trainer', '2023-01-15', 'Kwame Mensah', 'kwame.mensah@example.com', 'Full-Time'),
('ST002', 1200.00, 'Receptionist', '2023-03-10', 'Akosua Aidoo', 'akosua.aidoo@example.com', 'Part-Time'),
('ST003', 1700.00, 'Gym Manager', '2022-06-05', 'Abena Owusu', 'abena.owusu@example.com', 'Full-Time'),
('ST004', 1300.00, 'Personal Trainer', '2024-04-20', 'Kofi Boateng', 'kofi.boateng@example.com', 'Full-Time'),
('ST005', 1100.00, 'Cleaner', '2024-05-15', 'Gifty Asante', 'gifty.asante@example.com', 'Part-Time');

INSERT INTO inventory_table (item_name, status, quantity, purchase_date) VALUES
('Treadmill', 'Good', 5, '2024-02-10'),
('Dumbbells', 'Good', 20, '2024-01-20'),
('Yoga Mats', 'Need Repair', 15, '2024-03-12'),
('Resistance Bands', 'Good', 30, '2024-04-01'),
('Exercise Bikes', 'Good', 10, '2024-05-20');

INSERT INTO gym_equipment_table (inventoryID, status, last_maintenance_date) VALUES
(1, 'Good', '2024-06-15'),
(2, 'Good', '2024-07-20'),
(3, 'Need Repair', '2024-04-01'),
(4, 'Good', '2024-05-01'),
(5, 'Good', '2024-06-01');

INSERT INTO class_schedules (classID, staffID, programID, class_name, day_of_week, start_time, end_time) VALUES
('CL001', 'ST001', 1, 'Morning Yoga', 'Monday', '07:00:00', '08:00:00'),
('CL002', 'ST002', 2, 'Advanced Weight Training', 'Wednesday', '17:00:00', '18:00:00'),
('CL003', 'ST003', 3, 'Cardio Blast', 'Friday', '18:00:00', '19:00:00'),
('CL004', 'ST004', 4, 'Zumba Dance', 'Tuesday', '18:00:00', '19:00:00'),
('CL005', 'ST005', 5, 'Pilates', 'Thursday', '07:00:00', '08:00:00');

INSERT INTO training_programs (classID, program_name, duration, description) VALUES
('CL001', 'Yoga Basics', '1 Month', 'Introduction to basic yoga poses and breathing techniques.'),
('CL002', 'Strength Training', '2 Months', 'Intensive program focusing on muscle building and strength.'),
('CL003', 'Cardio Endurance', '1 Month', 'High-intensity cardio exercises to improve stamina.'),
('CL004', 'Dance Fitness', '1 Month', 'Fun dance routines to enhance fitness and agility.'),
('CL005', 'Core Strength', '1 Month', 'Exercises focusing on strengthening the core muscles.');


INSERT INTO members (memberID, programID, last_name, first_name, mtype_price, start_date, end_date, contact_information, membership_type) VALUES
('M001', 1, 'Doe', 'John', 100.00, '2024-01-01', '2024-12-31', 'john.doe@example.com', 'Standard'),
('M002', 2, 'Smith', 'Jane', 200.00, '2024-02-01', '2024-12-31', 'jane.smith@example.com', 'Premium'),
('M003', 3, 'Adom', 'Kwesi', 150.00, '2024-03-01', '2024-12-31', 'kwesi.adom@example.com', 'Standard'),
('M004', 4, 'Owusu', 'Nana', 120.00, '2024-04-01', '2024-12-31', 'nana.owusu@example.com', 'Standard'),
('M005', 5, 'Agyeman', 'Ama', 180.00, '2024-05-01', '2024-12-31', 'ama.agyeman@example.com', 'Premium');


INSERT INTO visitor_table (visitorID, visitor_name, purpose_of_visit, contact_information) VALUES
('V001', 'Ama Serwaa', 'Tour of Facilities', 'ama.serwaa@example.com'),
('V002', 'Kofi Nti', 'Consultation', 'kofi.ntin@example.com'),
('V003', 'Yaw Agyemang', 'Membership Inquiry', 'yaw.agyemang@example.com'),
('V004', 'Esi Asante', 'Equipment Demo', 'esi.asante@example.com'),
('V005', 'Kwabena Mensah', 'Feedback Submission', 'kwabena.mensah@example.com');

INSERT INTO attendance (personID, person_type, arrival_time, departure_time, date) VALUES
('M001', 'member', '07:00:00', '08:00:00', '2024-07-01'),
('ST002', 'staff', '17:00:00', '18:00:00', '2024-07-02'),
('M003', 'member', '18:00:00', '19:00:00', '2024-07-03'),
('V001', 'visitor', '18:00:00', '19:00:00', '2024-07-04'),
('M003', 'member', '07:00:00', '08:00:00', '2024-07-05');

INSERT INTO damage (personID, person_type, inventoryID, damage_type, cost, damage_date) VALUES
('M001', 'member', 1, 'Broken Treadmill', 500.00, '2024-07-01'),
('ST001', 'staff', 2, 'Damaged Dumbbells', 150.00, '2024-07-02'),
('M003', 'member', 3, 'Worn Yoga Mats', 100.00, '2024-07-03'),
('V004', 'visitor', 4, 'Faulty Resistance Bands', 50.00, '2024-07-04'),
('M005', 'member', 5, 'Scratched Exercise Bikes', 200.00, '2024-07-05');

INSERT INTO feedback (personID, person_type, feedback, date) VALUES
('ST001', 'staff', 'Great experience with the gym facilities!', '2024-07-01'),
('M002', 'member', 'The receptionist was very helpful.', '2024-07-02'),
('V003', 'visitor', 'The equipment demo was informative.', '2024-07-03'),
('M004', 'member', 'Enjoyed the Zumba class immensely!', '2024-07-04'),
('M005', 'member', 'Love the new Pilates program.', '2024-07-05');

INSERT INTO booking (memberID, staffID, booking_date, duration, booking_time) VALUES
('M001', 'ST001', '2024-07-01', '1 Hour', '07:00:00'),
('M002', 'ST002', '2024-07-02', '1 Hour', '17:00:00'),
('M003', 'ST003', '2024-07-03', '1 Hour', '18:00:00'),
('M004', 'ST004', '2024-07-04', '1 Hour', '18:00:00'),
('M005', 'ST005', '2024-07-05', '1 Hour', '07:00:00');

INSERT INTO payment ( person_ID, amount, payment_date, reason_for_payment) VALUES
('M001', 100.00, '2024-01-01', 'Annual Membership Fee'),
('M002', 200.00, '2024-02-01', 'Premium Membership Fee'),
('M003', 150.00, '2024-03-01', 'Standard Membership Fee'),
('ST002', 120.00, '2024-04-01', 'Equiment Damage'),
('ST003', 180.00, '2024-05-01', 'Equiment Damage');


INSERT INTO class_attendance (memberID, classID, attendance_date) VALUES
('M001',  'CL001', '2024-07-01'),
('M002',  'CL002', '2024-07-02'),
('M003',  'CL003', '2024-07-03'),
('M004',  'CL004', '2024-07-04'),
('M005',  'CL005', '2024-07-05');
