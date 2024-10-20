import sqlite3
from datetime import datetime

conn = sqlite3.connect('airport_management.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Flights (
                        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT NOT NULL UNIQUE,
                        origin TEXT NOT NULL,
                        destination TEXT NOT NULL,
                        departure_time TEXT NOT NULL,
                        arrival_time TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Passengers (
                        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        passport_number TEXT NOT NULL UNIQUE,
                        nationality TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_id INTEGER,
                        passenger_id INTEGER,
                        booking_date TEXT NOT NULL,
                        FOREIGN KEY(flight_id) REFERENCES Flights(flight_id),
                        FOREIGN KEY(passenger_id) REFERENCES Passengers(passenger_id)
                    )''')
    conn.commit()

def add_flight():
    flight_number = input("Enter flight number: ")
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")
    departure_time = input("Enter departure time (YYYY-MM-DD HH:MM): ")
    arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
    
    try:
        cursor.execute('''INSERT INTO Flights (flight_number, origin, destination, departure_time, arrival_time)
                          VALUES (?, ?, ?, ?, ?)''', 
                          (flight_number, origin, destination, departure_time, arrival_time))
        conn.commit()
        print("Flight added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Flight number already exists.")

def add_passenger():
    name = input("Enter passenger name: ")
    passport_number = input("Enter passport number: ")
    nationality = input("Enter nationality: ")
    
    try:
        cursor.execute('''INSERT INTO Passengers (name, passport_number, nationality)
                          VALUES (?, ?, ?)''', 
                          (name, passport_number, nationality))
        conn.commit()
        print("Passenger added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Passport number already exists.")

def book_flight():
    flight_id = input("Enter flight ID: ")
    passenger_id = input("Enter passenger ID: ")
    
    booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute('''INSERT INTO Bookings (flight_id, passenger_id, booking_date)
                          VALUES (?, ?, ?)''', 
                          (flight_id, passenger_id, booking_date))
        conn.commit()
        print("Flight booked successfully!")
    except sqlite3.IntegrityError:
        print("Error: Invalid flight ID or passenger ID.")

def view_flights():
    cursor.execute('SELECT * FROM Flights')
    flights = cursor.fetchall()
    if flights:
        print("\n--- Flights ---")
        for flight in flights:
            print(f"ID: {flight[0]}, Number: {flight[1]}, From: {flight[2]} To: {flight[3]}, Departure: {flight[4]}, Arrival: {flight[5]}")
    else:
        print("No flights available.")

def view_passengers():
    cursor.execute('SELECT * FROM Passengers')
    passengers = cursor.fetchall()
    if passengers:
        print("\n--- Passengers ---")
        for passenger in passengers:
            print(f"ID: {passenger[0]}, Name: {passenger[1]}, Passport: {passenger[2]}, Nationality: {passenger[3]}")
    else:
        print("No passengers available.")

def view_bookings():
    cursor.execute('''SELECT b.booking_id, f.flight_number, p.name, b.booking_date 
                      FROM Bookings b
                      JOIN Flights f ON b.flight_id = f.flight_id
                      JOIN Passengers p ON b.passenger_id = p.passenger_id''')
    bookings = cursor.fetchall()
    if bookings:
        print("\n--- Bookings ---")
        for booking in bookings:
            print(f"Booking ID: {booking[0]}, Flight: {booking[1]}, Passenger: {booking[2]}, Date: {booking[3]}")
    else:
        print("No bookings available.")

def search_flight():
    flight_number = input("Enter flight number to search: ")
    cursor.execute('SELECT * FROM Flights WHERE flight_number = ?', (flight_number,))
    flight = cursor.fetchone()
    if flight:
        print(f"\nFlight found - ID: {flight[0]}, Number: {flight[1]}, From: {flight[2]} To: {flight[3]}, Departure: {flight[4]}, Arrival: {flight[5]}")
    else:
        print("Flight not found.")

def delete_flight():
    flight_id = input("Enter flight ID to delete: ")
    cursor.execute('DELETE FROM Flights WHERE flight_id = ?', (flight_id,))
    conn.commit()
    if cursor.rowcount:
        print("Flight deleted successfully!")
    else:
        print("Flight not found.")

def main_menu():
    create_tables()
    
    while True:
        print("\n--- Airport Management System ---")
        print("1. Add Flight")
        print("2. Add Passenger")
        print("3. Book Flight")
        print("4. View Flights")
        print("5. View Passengers")
        print("6. View Bookings")
        print("7. Search Flight")
        print("8. Delete Flight")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_flight()
        elif choice == '2':
            add_passenger()
        elif choice == '3':
            book_flight()
        elif choice == '4':
            view_flights()
        elif choice == '5':
            view_passengers()
        elif choice == '6':
            view_bookings()
        elif choice == '7':
            search_flight()
        elif choice == '8':
            delete_flight()
        elif choice == '9':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()

conn.close()
