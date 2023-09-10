
# CONSTANTS
GENRES_MAPPING = {
         1 : "Action", 2 : "Adventure", 3 : "Comedy", 
         4 :  "Crime/Mystery", 5 : "Fantasy", 6 : "Historical",
         7 : "Horror", 8 :  "Romance", 9 : "Satire", 10 :  "Sci-Fi",
        11 : "Speculative", 12 : "Thriller", 13 : "Isekai"
        }
GENRES = ("Genres:\n1. Action, 2. Adventure, 3. Comedy, 4. Crime/Mystery, 5. Fantasy, 6. Historical," + 
          "\n7. Horror, 8. Romance, 9. Satire, 10. Sci-Fi, 11. Speculative, 12. Thriller, 13. Isekai")

class Book :
    def __init__(self, title, genre, rating=0) :
        self.title = title
        self.genre = genre
        self.rating = rating
        self.review = "not yet reviewed."
    
    def display(self) :
        print("\n\nTITLE: {}".format(self.title))
        print("GENRE: {}".format(self.genre))
        print("RATING: {}".format(self.rating))
        print("REVIEW: {}".format(self.review))

    # Comparison operators ==, <=, >=, <, >
    # see docs https://docs.python.org/2.7/reference/datamodel.html#object.__lt__
    def __eq__(self, other): 
        if not isinstance(other, Book):
            return NotImplemented
        return self.rating == other.rating
    def __lt__(self, other) :
        if not isinstance(other, Book):
            return NotImplemented
        return self.rating < other.rating
    
    def __le__(self, other) :
            if not isinstance(other, Book):
                return NotImplemented
            return self.rating <= other.rating
    
    def __gt__(self, other) :
            if not isinstance(other, Book): 
                return NotImplemented
            return self.rating > other.rating
    
    def __ge__(self, other) :
            if not isinstance(other, Book): 
                return NotImplemented
            return self.rating >= other.rating
    
class BookTracker:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        #self.books.append(book)
        self.books[book.title.lower()] = book
    
    def remove(self, title) :
       if title not in self.books.keys() :
            print("{} not found in collection.".format(title))
       else :
            orginal_title = self.books[title].title
            del self.books[title]
            print("Removed:{}".format(orginal_title))
       
    def update_book(self, title) :
            if title not in self.books.keys() :
                print("{} not found in collection.".format(title))
                return
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

    def list_book_titles(self) :
          
            print("\nBook Titles")
            for book in self.books.values() :
                print(book.title + ", ", end="")
            print()
    
    def list_books(self) :
            for book in self.books.values() :
                print("Book: {}, genre: {}, rating: {}, review: {}".format(book.title, 
                                                    book.genre, book.rating, book.review))

    def list_books_by_genre(self, genre) :
            print("All books with the genre: {}".format(genre))
            for book in self.books.values() :
                if(book.genre == genre) :
                  print("Book: {}, genre: {}, rating: {}, review: {}".format(book.title, 
                                             book.genre, book.rating, book.review))
    def sort_by_rating(self) :
        for book in reversed(sorted(self.books.values())) :
            print("Rating: {}, title: {}, genre: {}, review: {}"
                  .format(book.rating,book.title, book.genre, book.review))

    def total_books_by_genre(self) -> int:
        # WHY DO WE HAVE SO MANY GENRES UGHHHHHHHHHHHHHHH
        action_count = 0
        adventure_count = 0
        comedy_count = 0
        crime_mystery_count = 0
        fantasy_count = 0
        historical_count = 0
        horror_count = 0
        romance_count = 0
        satire_count = 0
        sci_fi_count = 0
        speculative_count = 0
        thriller_count = 0
        isekai_count = 0
        for book in self.books.values() :
            genre = book.genre
            if genre == GENRES_MAPPING[1]: action_count += 1
            elif genre == GENRES_MAPPING[2] : adventure_count += 1
            elif genre == GENRES_MAPPING[3] : comedy_count += 1
            elif genre == GENRES_MAPPING[4] : crime_mystery_count += 1
            elif genre == GENRES_MAPPING[5] : fantasy_count += 1
            elif genre == GENRES_MAPPING[6] : historical_count += 1
            elif genre == GENRES_MAPPING[7] : horror_count += 1
            elif genre == GENRES_MAPPING[8] : romance_count += 1
            elif genre == GENRES_MAPPING[9] : satire_count += 1
            elif genre == GENRES_MAPPING[10] : sci_fi_count += 1
            elif genre == GENRES_MAPPING[11] : speculative_count += 1
            elif genre == GENRES_MAPPING[12] : thriller_count += 1
            elif genre == GENRES_MAPPING[13] : isekai_count += 1
        print("\nBOOKS PER GENRE")
        print("total action books: {}".format(action_count))
        print("total adventure books: {}".format(adventure_count))
        print("total comedy books: {}".format(comedy_count))
        print("total crime/mystery books: {}".format(crime_mystery_count))
        print("total fantasy books: {}".format(fantasy_count))
        print("total historical books: {}".format(historical_count))
        print("total horror books: {}".format(horror_count))
        print("total romance books: {}".format(romance_count))
        print("total satire books: {}".format(satire_count))
        print("total sci-fi books: {}".format(sci_fi_count))
        print("total speculative books: {}".format(speculative_count))
        print("total thriller books: {}".format(thriller_count))
        print("total isekai books: {}".format(isekai_count))
    
    def rate_book(self, title) :
        if title not in self.books.keys() :
                print("{} not found in collection.".format(title))
                return
        else :
             rating = int(input("Enter book rating 1-10: "))
             self.books[title].rating = rating
             print("Updated rating for: {}".format(self.books[title].title))

    def review_book(self, title) :
        if title not in self.books.keys() :
                print("{} not found in collection.".format(title))
                return
        else :
             review = input("Enter your review: ")
             self.books[title].review = review
             print("Updated review for: {}".format(self.books[title].title))
    
    def display_book_info(self, title) :
          if title not in self.books.keys() :
                print("{} not found in collection.".format(title))
                return
          else :
            self.books[title].display()
           
def main() :
    tracker = BookTracker()
    while True:
        print("\nBook Tracker")
        print("1. Add book")
        print("2. List books")
        print("3. Search books by genre")
        print("4. Rate a book")
        print("5. Delete book")
        print("6. Update book")
        print("7. Sort by rating")
        print("8. Count by genre")
        print("9. Add a review")
        print("10. Specific book details: ")
        print("11. Exit")
        try :    
            choice = int(input("Enter your choice: "))
        except :
            choice = -1

        if choice == 1:
         title = input("Enter book's title: ")
         print(GENRES)
         print("Enter only a number 1 - 13.")
         genre = int(input("Enter the genre: ")) # check for int input later
         rating = int(input("Enter book rating 1-10: "))
         tracker.add_book(Book(title, GENRES_MAPPING[genre], rating))
         print("Added {} to list of books.".format(title))

        elif choice == 2:
            print()
            tracker.list_books()

        elif choice == 3:
            print(GENRES)
            print("Enter only a number 1 - 13.")
            genre = GENRES_MAPPING[int(input("Enter genre: "))] # check for int input later
            tracker.list_books_by_genre(genre)

        elif choice == 4 :
           tracker.list_book_titles()
           title = input("Enter the book's title to rate it: ").lower()
           tracker.rate_book(title)

        elif choice == 5:
           tracker.list_book_titles()
           title = input("Enter book's title to remove: ").lower()
           tracker.remove(title)

        elif choice == 6:
            tracker.list_book_titles()
            title = input("Enter the title of the book you would like to update: ").lower()
            tracker.update_book(title)
        
        elif choice == 7:
            print("\nDisplaying books by rating:")
            tracker.sort_by_rating()
        
        elif choice == 8 :
            tracker.total_books_by_genre()
        
        elif choice == 9 :
            tracker.list_book_titles()
            title = input("Enter the title of the book you would like to review: ").lower()
            tracker.review_book(title)

        elif choice == 10 :
            tracker.list_book_titles()
            title = input("Enter the title of the book you would like to see the details of: ").lower()
            tracker.display_book_info(title)
        
        elif choice == 11 :
            print("Thank you for using book tracker, have a nice day.")
            break
        else:
            print("Invalid Selection.")
main()    