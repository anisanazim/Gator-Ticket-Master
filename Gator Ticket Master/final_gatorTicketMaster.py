import sys
from datetime import datetime
import time

class Node:
    def __init__(self, user_id, seat_id):
        self.user_id = user_id
        self.seat_id = seat_id
        self.color = 1  # 1 for red, 0 for black
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, None)
        self.NIL.color = 0
        self.root = self.NIL

    def insert(self, user_id, seat_id):
        node = Node(user_id, seat_id)
        node.left = self.NIL
        node.right = self.NIL

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.user_id < x.user_id:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.user_id < y.user_id:
            y.left = node
        else:
            y.right = node

        node.color = 1
        self._fix_insert(node)

    def _fix_insert(self, k):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, user_id):
        z = self.search(user_id)
        if z:
            y = z
            y_original_color = y.color
            if z.left == self.NIL:
                x = z.right
                self._transplant(z, z.right)
            elif z.right == self.NIL:
                x = z.left
                self._transplant(z, z.left)
            else:
                y = self._minimum(z.right)
                y_original_color = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    self._transplant(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self._transplant(z, y)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
            if y_original_color == 0:
                self._fix_delete(x)
            return z.seat_id
        return None

    def _fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.right.color == 0:
                        w.left.color = 0
                        w.color = 1
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.right.color = 0
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.left.color == 0:
                        w.right.color = 0
                        w.color = 1
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def search(self, user_id):
        return self._search_helper(self.root, user_id)

    def _search_helper(self, node, user_id):
        if node == self.NIL or user_id == node.user_id:
            return node
        if user_id < node.user_id:
            return self._search_helper(node.left, user_id)
        return self._search_helper(node.right, user_id)

    def inorder_traversal(self):
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append((node.seat_id, node.user_id))
            self._inorder_helper(node.right, result)

class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_item

    def _heapify_up(self, i):
        parent = self.parent(i)
        if i > 0 and self._compare(self.heap[i], self.heap[parent]) < 0:
            self.swap(i, parent)
            self._heapify_up(parent)

    def _heapify_down(self, i):
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        if left < len(self.heap) and self._compare(self.heap[left], self.heap[min_index]) < 0:
            min_index = left
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[min_index]) < 0:
            min_index = right
        if min_index != i:
            self.swap(i, min_index)
            self._heapify_down(min_index)

    def _compare(self, item1, item2):
        # For waitlist: item = (-priority, timestamp, user_id)
        # For available seats: item = (seat_id, seat_id)
        if isinstance(item1[0], int) and isinstance(item2[0], int):
            # This is for available seats
            return item1[0] - item2[0]
        else:
            # This is for waitlist
            if item1[0] != item2[0]:
                return item1[0] - item2[0]  # Higher priority (more negative) first
            else:
                return item1[1] - item2[1]  # Earlier timestamp first

class GatorTicketMaster:
    def __init__(self):
        self.reserved_seats = RedBlackTree()
        self.available_seats = MinHeap()
        self.waitlist = MinHeap()
        self.seat_count = 0

    def initialize(self, seat_count):
        if seat_count <= 0:
            print("Invalid input. Please provide a valid number of seats.")
            return
        self.seat_count = seat_count
        for i in range(1, seat_count + 1):
            self.available_seats.insert((i, i))
        print(f"{seat_count} Seats are made available for reservation")

    def available(self):
        available_count = len(self.available_seats.heap)
        waitlist_count = len(self.waitlist.heap)
        print(f"Total Seats Available : {available_count}, Waitlist : {waitlist_count}")

    def reserve(self, user_id, user_priority):
        if self.available_seats.heap:
            seat_id, _ = self.available_seats.extract_min()
            self.reserved_seats.insert(user_id, seat_id)
            print(f"User {user_id} reserved seat {seat_id}")
        else:
            timestamp = datetime.now().timestamp()+ time.time_ns() % 1 * 1e-9
            self.waitlist.insert((-user_priority, timestamp, user_id))
            print(f"User {user_id} is added to the waiting list")

    def cancel(self, seat_id, user_id):
        node = self.reserved_seats.search(user_id)
        if node and node.seat_id == seat_id:
            self.reserved_seats.delete(user_id)
            if self.waitlist.heap:
                _, _, next_user_id = self.waitlist.extract_min()
                self.reserved_seats.insert(next_user_id, seat_id)
                print(f"User {user_id} canceled their reservation")
                print(f"User {next_user_id} reserved seat {seat_id}")
            else:
                self.available_seats.insert((seat_id, seat_id))
                print(f"User {user_id} canceled their reservation")
        else:
            print(f"User {user_id} has no reservation for seat {seat_id} to cancel")

    def print_reservations(self):
        reservations = sorted(self.reserved_seats.inorder_traversal())
        for seat_id, user_id in reservations:
            print(f"Seat {seat_id}, User {user_id}")

    def add_seats(self, count):
        if count <= 0:
            print("Invalid input. Please provide a valid number of seats.")
            return
        new_seat_start = self.seat_count + 1
        self.seat_count += count
        print(f"Additional {count} Seats are made available for reservation")
        
        assigned_seats = []
        while count > 0 and self.waitlist.heap:
            _, timestamp, user_id = self.waitlist.extract_min()
            seat_id = new_seat_start
            new_seat_start += 1
            count -= 1
            self.reserved_seats.insert(user_id, seat_id)
            assigned_seats.append((user_id, seat_id))
        
        # Add remaining seats to available seats
        for i in range(new_seat_start, self.seat_count + 1):
            self.available_seats.insert((i, i))
        
        for user_id, seat_id in assigned_seats:
            print(f"User {user_id} reserved seat {seat_id}")
        
    def exit_waitlist(self, user_id):
        for i, (_, _, waitlist_user_id) in enumerate(self.waitlist.heap):
            if waitlist_user_id == user_id:
                self.waitlist.heap.pop(i)
                self.waitlist._heapify_down(i)
                print(f"User {user_id} is removed from the waiting list")
                return
        print(f"User {user_id} is not in waitlist")

    def update_priority(self, user_id, new_priority):
        for i, (priority, timestamp, uid) in enumerate(self.waitlist.heap):
            if uid == user_id:
                self.waitlist.heap[i] = (-new_priority, timestamp, user_id)
                self.waitlist._heapify_up(i)
                self.waitlist._heapify_down(i)
                print(f"User {user_id} priority has been updated to {new_priority}")
                return
        print(f"User {user_id} priority is not updated")
    
    def release_seats(self, user_id1, user_id2):
        if user_id1 < 0 or user_id2 < 0 or user_id2 < user_id1:
            print("Invalid input. Please provide a valid range of users.")
            return

        released_seats = []
        current = self.reserved_seats.root
        stack = []
        while current != self.reserved_seats.NIL or stack:
            while current != self.reserved_seats.NIL:
                stack.append(current)
                current = current.left
            current = stack.pop()
            if user_id1 <= current.user_id <= user_id2:
                released_seats.append((current.user_id, current.seat_id))
            current = current.right

        for user_id, seat_id in released_seats:
            self.reserved_seats.delete(user_id)
            self.available_seats.insert((seat_id, seat_id))

        # Remove users from waitlist
        self.waitlist.heap = [item for item in self.waitlist.heap if not (user_id1 <= item[2] <= user_id2)]

        print(f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released")

        # Assign seats to users in waitlist
        while self.available_seats.heap and self.waitlist.heap:
            seat_id, _ = self.available_seats.extract_min()
            _, _, user_id = self.waitlist.extract_min()
            self.reserved_seats.insert(user_id, seat_id)
            print(f"User {user_id} reserved seat {seat_id}")

def process_command(gtm, command):
    parts = command.strip().split('(')
    operation = parts[0]
    args = parts[1].rstrip(')').split(',')

    if operation == 'Initialize':
        gtm.initialize(int(args[0]))
    elif operation == 'Available':
        gtm.available()
    elif operation == 'Reserve':
        gtm.reserve(int(args[0]), int(args[1]))
    elif operation == 'Cancel':
        gtm.cancel(int(args[0]), int(args[1]))
    elif operation == 'PrintReservations':
        gtm.print_reservations()
    elif operation == 'AddSeats':
        gtm.add_seats(int(args[0]))
    elif operation == 'ExitWaitlist':
        gtm.exit_waitlist(int(args[0]))
    elif operation == 'UpdatePriority':
        gtm.update_priority(int(args[0]), int(args[1]))
    elif operation == 'ReleaseSeats':
        gtm.release_seats(int(args[0]), int(args[1]))
    elif operation == 'Quit':
        print("Program Terminated!!")
        return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gatorTicketMaster.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.split('.')[0] + "_output_file.txt"

    gtm = GatorTicketMaster()

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        sys.stdout = f_out  # Redirect stdout to the output file
        for line in f_in:
            if not process_command(gtm, line.strip()):
                break

    sys.stdout = sys.__stdout__  # Reset stdout

if __name__ == "__main__":
    main()