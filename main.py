"""
Room Reservation System
By Nnamdi Nwaso

"""

import heapq
import uuid



class Reservation:
    def __init__(self, res_id, name, student_id, email, priority, room):
        self.res_id = res_id
        self.name = name
        self.student_id = student_id
        self.email = email
        self.priority = priority
        self.room = room

    def __str__(self):
        return f"""
Reservation ID: {self.res_id}
Name: {self.name}
Student ID: {self.student_id}
Email: {self.email}
Room: {self.room + 1 if self.room is not None else "Waitlist"}
Priority: {self.priority}
"""



# Globals

rooms = [None] * 40  # Dynamic array for rooms
reservations = {}    # Hash table for fast lookup
waitlist = []        # Priority queue
counter = 0          # Tie-breaker for heap



#Functions to generate reservation_id and display rooms


def generate_reservation_id():
    return "R" + str(uuid.uuid4())[:5]




def display_rooms():
    print("\nRoom Layout (5 x 8 Grid):\n")

    for i in range(5):
        row = rooms[i * 8:(i + 1) * 8]

        for j, room in enumerate(row):
            room_number = i * 8 + j + 1  # Convert index → room number (1–40)

            if room is None:
                print(f"[{room_number}]", end=" ")
            else:
                print(f"[{room_number}✅]", end=" ")

        print()
    print()

def get_priority_from_reason(reason):
    reason = reason.lower()


    if any(word in reason for word in [
        "accessibility", "disability", "medical", "accommodation"
    ]):
        return 1

    elif any(word in reason for word in [
        "group", "project", "team", "assignment"
    ]):
        return 2

    # Priority 3 → General Study (default)
    else:
        return 3

# Booking Function


def book_room(name, student_id, email, priority):
    global counter

    for i in range(len(rooms)):
        if rooms[i] is None:
            res_id = generate_reservation_id()
            reservation = Reservation(res_id, name, student_id, email, priority, i)

            rooms[i] = reservation
            reservations[res_id] = reservation

            print(f"\n✅ Room {i + 1} booked successfully!")
            print(f"Reservation ID: {res_id}")
            return

    # If full , add to waitlist
    res_id = generate_reservation_id()
    reservation = Reservation(res_id, name, student_id, email, priority, None)

    heapq.heappush(waitlist, (priority, counter, reservation))
    counter += 1

    print("\n⚠️ All rooms are full.")
    print(f"Added to waitlist with Reservation ID: {res_id}")



# Reservation cancellation


def cancel_reservation(res_id):
    if res_id not in reservations:
        print("\n❌ Invalid Reservation ID")
        return

    reservation = reservations[res_id]
    room_index = reservation.room

    rooms[room_index] = None
    del reservations[res_id]

    print(f"\n✅ Reservation cancelled for Room {room_index + 1}")

    assign_from_waitlist(room_index)


# -------------------------------
# Assign from Waitlist
# -------------------------------

def assign_from_waitlist(room_index):
    if waitlist:
        _, _, reservation = heapq.heappop(waitlist)

        reservation.room = room_index
        rooms[room_index] = reservation
        reservations[reservation.res_id] = reservation

        print(f"🎉 Room {room_index + 1} assigned to {reservation.name} (Priority {reservation.priority})")


# -------------------------------
# Modify Reservation
# -------------------------------

def modify_reservation(res_id):
    if res_id not in reservations:
        print("\nOOPS!!! Reservation not found")
        return

    reservation = reservations[res_id]

    print("\n1. Change Room")
    print("2. Change Reason for Booking")
    choice = input("Select option: ")

    if choice == "1":
        try:
            new_room = int(input("Enter new room number: ")) - 1

            if new_room < 0 or new_room >= len(rooms):
                print("Invalid room number")
                return

            if rooms[new_room] is None:
                rooms[reservation.room] = None
                rooms[new_room] = reservation
                reservation.room = new_room
                print("✅ Room updated successfully")
            else:
                print("❌ Room already occupied")

        except ValueError:
            print("Invalid input")

    elif choice == "2":
        try:
            reason = input("Reason for booking: ")
            new_priority = get_priority_from_reason(reason)


            if new_priority not in [1, 2, 3]:
                print("Invalid priority")
                return

            reservation.priority = new_priority
            print("✅ Reason for Booking has been updated")

        except ValueError:
            print("Invalid input")



# Searching For Reservation


def search_reservation(res_id):
    if res_id in reservations:
        print(reservations[res_id])
    else:
        print("\n❌ Reservation not found")



# Expand Rooms


def expand_rooms():
    global rooms
    rooms.extend([None] * 10)
    print(f"\n📈 Capacity expanded! Total rooms: {len(rooms)}")



# Main Menu


def menu():
    while True:
        print("""
========= ROOM RESERVATION SYSTEM =========
1. Display Rooms
2. Book Room
3. Cancel Reservation
4. Modify Reservation
5. Search Reservation
6. Expand Rooms
7. Exit
==========================================
""")

        choice = input("Enter choice: ")

        if choice == "1":
            display_rooms()

        elif choice == "2":
            name = input("Full Name: ")
            student_id = input("Student ID: ")
            email = input("Email: ")

            try:
                reason = input("Reason for booking: ")
                priority = get_priority_from_reason(reason)

                # print(f"Assigned Priority Level: {priority}")
                if priority not in [1, 2, 3]:
                    print("Invalid priority")
                    continue
            except ValueError:
                print("Invalid input")
                continue

            book_room(name, student_id, email, priority)

        elif choice == "3":
            res_id = input("Enter Reservation ID: ")
            cancel_reservation(res_id)

        elif choice == "4":
            res_id = input("Enter Reservation ID: ")
            modify_reservation(res_id)

        elif choice == "5":
            res_id = input("Enter Reservation ID: ")
            search_reservation(res_id)

        elif choice == "6":
            expand_rooms()

        elif choice == "7":
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")





if __name__ == "__main__":
    menu()