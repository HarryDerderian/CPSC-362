class Task:

    def __init__(self, title, description, id):
        self.title = title
        self.description = description
        self.status = "To Do"
        self.id = id
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def update_status(self, new_status):
        self.status = new_status

    def display(self):
        print(f"Title: {self.title}\nDescription: {self.description}\nStatus: {self.status}\nComments: {self.comments},\nID:{self.id} \n")

class AgileTaskTracker:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)

    def update_task_status(self, id, new_status):
        for task in self.tasks:
            if task.id == id:
                task.update_status(new_status)

    def add_comment_to_task(self, id, comment):
        for task in self.tasks:
            if task.id == id:
                task.add_comment(comment)

    def view_tasks(self, status=None):
        for task in self.tasks:
            if status:
                if task.status == status:
                    task.display()
            else:
                task.display()

if __name__ == "__main__":
    tracker = AgileTaskTracker()

    while True:
        print("\nAgile Task Tracker")
        print("1. Add Task")
        print("2. Update Task Status")
        print("3. Add Comment to Task")
        print("4. View Tasks")
        print("5. Exit")
        try :    
            choice = int(input("Enter your choice: "))
        except :
            choice = -1

        if choice == 1:
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            task_id = 0
            task = Task(title, description, 0)
            tracker.add_task(task)
            task_id = tracker.tasks.index(task) + 1
            task.id = task_id
            print("Task '{}' added with ID: {}".format(title, str(task_id)))

        elif choice == 2:
            id = int(input("Enter task ID to update: "))
            status = input("Enter new status (To Do, In Progress, Done): ")
            tracker.update_task_status(id, status)

        elif choice == 3:
            id = input("Enter task ID to comment on: ")
            comment = input("Enter your comment: ")
            tracker.add_comment_to_task(id, comment)

        elif choice == 4:
            status_filter = input("Filter by status (leave empty for all tasks): ")
            if status_filter:
                tracker.view_tasks(status_filter)
            else:
                tracker.view_tasks()

        elif choice == 5:
            print("Thank you for using Agile Task Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")