
GENRES_MAPPING = {
         1 : "Action", 2 : "Adventure", 3 : "Comedy", 
         4 :  "Crime/Mystery", 5 : "Fantasy", 6 : "Historical",
         7 : "Horror", 8 :  "Romance", 9 : "Satire", 10 :  "Sci-Fi",
        11 : "Speculative", 12 : "Thriller", 13 : "Isekai"
    }
GENRES = ("\nGenres: 1. Action, 2. Adventure, 3. Comedy, 4. Crime/Mystery, 5. Fantasy, 6. Historical," + 
              "\n7. Horror, 8. Romance, 9. Satire, 10. Sci-Fi, 11. Speculative, 12. Thriller, 13. Isekai\n")
class Book :
    def __init__(self, title, genre, rating=0) :
        self.title = title
        self.genre = genre
        self.rating = rating
    
class BookTracker:
    def __init__(self):
        #self.books = []
        self.books = {}

    def add_book(self, book):
        #self.books.append(book)
        self.books[book.title.lower()] = book
    
    def remove(self, title) :
       for key, value in self.books.items() :
           if title == key :
            del self.books[title]
            print("Removed:{}".format(title))
            return
       print("{} not found in collection".format(title))
           
    def update_book(self, title) :
            print("1. change title")
            print("2. change genre")
            print("3. change rating")
            try :
                selection = int(input("Enter selection: "))
            except : selection = -1
            if selection == 1 :
                new_title = input("Enter the new title: ")
                self.books[title].title = new_title
                self.books[new_title] = self.books[title]
                del self.books[title]
                print("Updated title.")
            elif selection == 2:
                print(GENRES)
                new_genre = GENRES_MAPPING[int(input("Enter genre: "))]
                self.books[title].genre = new_genre
                print("Updated genre.")
            elif selection == 3 :
                new_rating = int(input("Enter new rating 1-10: "))
                self.books[title].rating = new_rating
                print("Updated rating.")
            else :
                print("Invalid selection.")
            
    
    def list_books(self) :
            for key, value in self.books.items() :
                print("Book: {}, genre: {}, rating: {} ".format(self.books[key].title, 
                                                    self.books[key].genre, self.books[key].rating))

    def list_books_by_genre(self, genre) :
            print("All books with the genre: {}".format(genre))
            for key, value in self.books.items() :
                if(self.books[key].genre == genre) :
                  print("Book: {}, genre: {}, rating: {} ".format(self.books[key].title, 
                                             self.books[key].genre, self.books[key].rating))
    def sort_by_rating() :
           


def main() :
    tacker = BookTracker()
    while True:
        print("\nBook Tracker")
        print("1. Add book")
        print("2. List books")
        print("3. Find books by genre")
        print("4. Delete book")
        print("5. Update book")
        print("6. Exit")
        try :    
            choice = int(input("Enter your choice: "))
        except :
            choice = -1

        if choice == 1:
         title = input("Enter the title: ")
         print("="*88)
         print(GENRES)
         print("="*88)
         genre = int(input("Enter the genre: ")) # check for int input later
         rating = int(input("Enter book rating 1-10: "))
         tacker.add_book(Book(title, GENRES_MAPPING[genre], rating))
         print("Added {} to list of books.".format(title))

        elif choice == 2:
            print()
            print("="*50)
            tacker.list_books()
            print("="*50)

        elif choice == 3:
            print(GENRES)
            genre = int(input("Enter genre: ")) # check for int input later
            tacker.list_books_by_genre(GENRES_MAPPING[genre])

        elif choice == 4:
           print("="*50)
           tacker.list_books()
           print("="*50)
           title = input("Enter book title to remove: ").lower()
           
           tacker.remove(title)

        elif choice == 5:
            title = input("Enter book title you would like to alter: ").lower()
            tacker.update_book(title)            
        else:
            print("Invalid Selection.")
            
main()    