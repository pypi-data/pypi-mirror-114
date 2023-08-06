# Node class is used to store unit of data or element in the list / Stack / Queue / etc.
class Node:
    data = None
    def __init__(self, **kwargs):
        self.data = kwargs.get("data", None)
        self.next = kwargs.get("next", None)
        self.previous = kwargs.get("previous", None)
        self.left = kwargs.get("left", None)
        self.right = kwargs.get("right", None)

# Declaration and definition of Singly Linked List class
class LinkedList:
    def __init__(self):
        self.__head = None

    def __len__(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to count the number of nodes
        count = 0

        while(traverser != None):
            count = count + 1
            traverser = traverser.next

        return count

    def append(self, data):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Conditions for adding elements to the list
        if(self.__head == None):
            self.__head = Node(data = data, next = None)
            self.__head.next = None

        else:
            while(traverser.next != None):
                traverser = traverser.next

            traverser.next = Node(data = data, next = None)

    def insert(self, data, index):
        if(index == 0):
            temp = Node(data = data, next = self.__head) # Temporary pointer
            self.__head = temp

        else:
            count = 1
            # Traverser is the temporary pointer used for linked list traversal
            traverser = self.__head

            temp = Node(data = data, next = None)
            while(count < index):
                traverser = traverser.next
                count = count + 1
            
            if(traverser == None):
                print("Index out of Bound!")
            else:
                temp.next = traverser.next
                traverser.next = temp

    def remove(self, element):
        # Check if list is empty
        if(self.__head == None):
            print("Cannot remove from empty list.")

        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Check if the parameter is integer or not
        if (str(type(element)) == "<class 'int'>"):
            # A counter is used to check if element index matches the node's index
            count = 0

            # Check if head is the only element in the list
            if(self.__head.next == None):
                if(count == element):
                    temp = self.__head # temporary pointer
                    self.__head = self.__head.next
                    return temp

                elif(self.__head.data != element):
                    print("Element not found.")
                    return None

            # check if head is the element to be removed
            elif(count == element):
                temp = self.__head # temporary pointer
                self.__head = self.__head.next
                return temp

            while(traverser.next != None):
                temp = traverser.next # temporary pointer
                count = count + 1
                if(count == element):
                    traverser.next = temp.next
                    return temp

                traverser = traverser.next

            # Check if the last element is the node to remove
            if(traverser.next == None):
                print("Element not found.")

        else:
            print(TypeError) # Write error definition

    def display(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        while(traverser != None):
            print(traverser.data, end=" - ")
            traverser = traverser.next

        print("NONE")

    def returnNode(self, index):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to identify index at which the node is
        count = 0

        while(traverser != None):
            if(count == index):
                return traverser

            traverser = traverser.next
            count = count + 1

        if(traverser == None):
            return None

    ## Start further coding here

# Declaration and definition of Doubly Linked List class
class DoublyLinkedList:
    def __init__(self):
        self.__head = None

    def __len__(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to count the number of nodes
        count = 0

        while(traverser != None):
            count = count + 1
            traverser = traverser.next

        return count

    def append(self, data):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # self.__node = Node(data, None)
        # Conditions for adding elements to the list
        if(self.__head == None):
            self.__head = Node(data = data, next = None, previous = None)
            self.__head.next = None
            self.__head.previous = None

        else:
            while(traverser.next != None):
                traverser = traverser.next

            traverser.next = Node(data = data, next = None, previous = None)

    def remove(self, element):
        # Check if list is empty
        if(self.__head == None):
            print("Cannot remove from empty list.")

        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head
        count = 0

        # Check if the parameter is integer
        if (str(type(element)) == "<class 'int'>"):
            # Check if head is the only element in the list
            if(self.__head.next == None):
                if(count == element):
                    temp = self.__head # temporary pointer
                    self.__head = self.__head.next
                    self.__head.previous = None
                    return temp

                elif(count != element):
                    print("Element not found.")
                    return None

            # check if head is the element to be removed
            elif(count == element):
                temp = self.__head # temporary pointer
                self.__head = self.__head.next
                self.__head.previous = None
                return temp

            while(traverser.next != None):
                temp = traverser.next # temporary pointer
                count = count + 1
                if(count == element):
                    traverser.next = temp.next # Setting next node
                    traverser = temp.next
                    traverser.previous = temp.previous # Setting previous node
                    return temp

                traverser = traverser.next

            # Check if the last element is the node to remove
            if(traverser.next == None):
                print("Element not found.")

        else:
            print(TypeError)

    def insert(self, data, index):
        if(index == 0):
            temp = Node(data = data, next = self.__head, previous = None) # Temporary pointer
            self.__head = temp

        else:
            count = 1
            # Traverser is the temporary pointer used for linked list traversal
            traverser = self.__head

            temp = Node(data = data, next = None, previous = None)
            while(count < index):
                traverser = traverser.next
                count = count + 1
            
            if(traverser == None):
                print("Index out of Bound!")
            else:
                temp.next = traverser.next
                temp.previous = traverser
                traverser.next = temp

    def display(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        while(traverser != None):
            print(traverser.data, end=" - ")
            traverser = traverser.next

        print("NONE")

    def returnNode(self, index):  
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to identify index at which the node is
        count = 0

        while(traverser != None):
            if(count == index):
                return traverser

            traverser = traverser.next
            count = count + 1  

        if(traverser == None):
            return None

# Declaration and definition of Circular Singly Linked List class
class CircularLinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def __len__(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to count the number of nodes
        if (self.__head == None):
            return 0 # There will be no element in the list.

        count = 1

        while(traverser != self.__tail):
            count = count + 1
            traverser = traverser.next

        return count

    def append(self, data):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Conditions for adding elements to the list
        if(self.__head == None):
            self.__head = self.__tail = Node(data = data, next = self.__head)

        else:
            while(traverser != self.__tail):
                traverser = traverser.next

            self.__tail = traverser.next = Node(data = data, next = self.__head)

    def insert(self, data, index):
        if(index == 0):
            self.__tail.next = temp = Node(data = data, next = self.__head) # Temporary pointer
            self.__head = temp

        elif (index == len(self)-1):
            self.__tail.next = temp = Node(data = data, next = self.__head)
            self.__tail = temp

        else:
            count = 1
            # Traverser is the temporary pointer used for linked list traversal
            traverser = self.__head

            temp = Node(data = data, next = None)
            while(count < index and count <= len(self)):
                traverser = traverser.next
                count = count + 1
            
            if(traverser == None):
                print("Index out of Bound!")
            else:
                temp.next = traverser.next
                traverser.next = temp

    def remove(self, element):
        # Check if list is empty
        if(self.__head == None):
            print("Cannot remove from empty list.")

        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Check if the parameter is integer or not
        if (str(type(element)) == "<class 'int'>"):
            # A counter is used to check if element index matches the node's index
            count = 0

            # Check if head is the only element in the list
            if(self.__head.next == None):
                if(count == element):
                    temp = self.__head # temporary pointer
                    self.__head = self.__head.next
                    return temp

                elif(self.__head.data != element):
                    print("Element not found.")
                    return None

            # check if head is the element to be removed
            elif(count == element):
                temp = self.__head # temporary pointer
                self.__head = self.__head.next
                return temp

            while(traverser.next != self.__tail):
                temp = traverser.next # temporary pointer
                count = count + 1
                if(count == element):
                    traverser.next = temp.next
                    return temp

                traverser = traverser.next

            # Check if the last element is the node to remove
            if(traverser.next == self.__tail and element == count+1):
                traverser.next = self.__head
                self.__tail = traverser
            else:
                print("Element not found.")

        else:
            print(TypeError) # Write error definition

    def display(self):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        while(traverser != self.__tail):
            print(traverser.data, end=" - ")
            traverser = traverser.next

        print(self.__tail.data)

    def returnNode(self, index):
        # Traverser is the temporary pointer used for linked list traversal
        traverser = self.__head

        # Count is used to identify index at which the node is
        count = 0

        while(traverser != self.__tail):
            if(count == index):
                return traverser

            traverser = traverser.next
            count = count + 1

        if(traverser == self.__tail and index == count):
            return traverser
        else:
            return None

# Declaration and definition of Stack class
class Stack:
    def __init__(self):
        self.__top = None
        self.__stack = LinkedList()

    def isEmpty(self):
        if (self.__top == None):
            return True
        else:
            return False

    def push(self, data):
        self.__stack.append(data)
        self.__top = self.__stack.returnNode(len(self.__stack) - 1)

    def pop(self):
        if (self.isEmpty()):
            print("Empty stack, Nothing to pop!")
            return None

        temp = self.__stack.remove(len(self.__stack) - 1)
        self.__top = self.__stack.returnNode(len(self.__stack) - 1)
        return temp

    def peek(self):
        print(self.__top.data)

    def returnTop(self):
        return self.__top

# Declaration and definition of Queue class
class Queue:
    def __init__(self):
        self.__front = None
        self.__rear = None
        self.__queue = LinkedList()

    def isEmpty(self):
        if (self.__front == self.__rear == None):
            return True
        else:
            return False

    def enqueue(self, data):
        if (self.__front == self.__rear == None):
            self.__queue.append(data)
            self.__front = self.__rear = self.__queue.returnNode(len(self.__queue) - 1)

        else:
            self.__queue.append(data)
            self.__rear = self.__queue.returnNode(len(self.__queue) - 1)

    def dequeue(self):
        if (self.isEmpty()):
            print("Empty Queue")
            return None

        elif (self.__front == self.__rear):
            self.__front = self.__queue.returnNode(1)
            self.__front = self.__rear = None
            return self.__queue.remove(0)
            
        else:
            self.__front = self.__queue.returnNode(1)
            return self.__queue.remove(0)

    def returnFront(self):
        return self.__front

    def returnRear(self):
        return self.__rear
