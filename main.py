import tkinter as tk
from tkinter import messagebox, ttk
import oracledb

# Oracle connection parameters
DB_USER = "system"
DB_PASSWORD = "k6g1i34z" 
DB_DSN = "localhost/XE"

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.show_login_screen()
    
    def show_login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create login frame
        login_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        login_frame.pack(expand=True)
        
        # Title
        login_title = tk.Label(
            login_frame, 
            text="Library Management System", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        login_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        username_label = tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        username_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Password
        password_label = tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Login button
        login_button = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.login
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Register button
        register_button = tk.Button(
            login_frame,
            text="Register",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
            command=self.show_register_screen
        )
        register_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            # Check admin credentials
            cursor.execute(
                "SELECT admin_id FROM Admin WHERE username = :1 AND password = :2",
                [username, password]
            )
            
            result = cursor.fetchone()
            
            if result:
                cursor.close()
                connection.close()
                self.admin_id = result[0]
                self.admin_username = username
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def show_register_screen(self):
        # Create a simple dialog for registration
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New Admin")
        register_window.geometry("300x200")
        register_window.configure(bg="#f0f0f0")
        register_window.grab_set()  # Make window modal
        
        # Register frame
        register_frame = tk.Frame(register_window, bg="#f0f0f0", padx=20, pady=20)
        register_frame.pack(expand=True)
        
        # Username
        username_label = tk.Label(register_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        username_label.grid(row=0, column=0, sticky="w", pady=5)
        
        username_entry = tk.Entry(register_frame, font=("Arial", 12), width=20)
        username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Password
        password_label = tk.Label(register_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        password_label.grid(row=1, column=0, sticky="w", pady=5)
        
        password_entry = tk.Entry(register_frame, font=("Arial", 12), width=20, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Register function
        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password")
                return
                
            try:
                connection = get_connection()
                cursor = connection.cursor()
                
                # Call the insert_admin procedure
                cursor.callproc("insert_admin", [username, password])
                connection.commit()
                
                messagebox.showinfo("Success", "Admin registered successfully")
                register_window.destroy()
                
                cursor.close()
                connection.close()
                
            except oracledb.Error as error:
                messagebox.showerror("Database Error", str(error))
        
        # Register button
        register_button = tk.Button(
            register_frame,
            text="Register",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=register
        )
        register_button.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    
    def show_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create navbar
        navbar = tk.Frame(self.root, bg="#333333", height=50)
        navbar.pack(fill="x")
        
        title_label = tk.Label(
            navbar,
            text="Library Management System",
            font=("Arial", 16, "bold"),
            bg="#333333",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        welcome_label = tk.Label(
            navbar,
            text=f"Welcome, {self.admin_username}",
            font=("Arial", 12),
            bg="#333333",
            fg="white"
        )
        welcome_label.pack(side="right", padx=20, pady=10)
        
        # Create tabs
        tab_control = ttk.Notebook(self.root)
        
        books_tab = ttk.Frame(tab_control)
        members_tab = ttk.Frame(tab_control)
        borrow_tab = ttk.Frame(tab_control)
        return_tab = ttk.Frame(tab_control)
        
        tab_control.add(books_tab, text="Books")
        tab_control.add(members_tab, text="Members")
        tab_control.add(borrow_tab, text="Borrow Books")
        tab_control.add(return_tab, text="Return Books")
        
        tab_control.pack(expand=1, fill="both", padx=20, pady=20)
        
        # Setup each tab
        self.setup_books_tab(books_tab)
        self.setup_members_tab(members_tab)
        self.setup_borrow_tab(borrow_tab)
        self.setup_return_tab(return_tab)
        
        # Logout button
        logout_button = tk.Button(
            navbar,
            text="Logout",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            command=self.show_login_screen
        )
        logout_button.pack(side="right", padx=10, pady=10)
    
    def setup_books_tab(self, tab):
        # Create search frame at the top
        search_frame = tk.Frame(tab, pady=10)
        search_frame.pack(fill="x")
        
        # Author search
        author_search_label = tk.Label(search_frame, text="Search by Author:")
        author_search_label.pack(side="left", padx=5)
        
        self.author_search_entry = tk.Entry(search_frame, width=25)
        self.author_search_entry.pack(side="left", padx=5)
        
        # Search button
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.search_books_by_author
        )
        search_button.pack(side="left", padx=5)
        
        # Reset button to show all books
        reset_button = tk.Button(
            search_frame,
            text="Show All",
            command=self.load_books
        )
        reset_button.pack(side="left", padx=5)
        
        # Create frame for book list
        list_frame = tk.Frame(tab)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for books
        columns = ("ISBN", "Title", "Author", "Total Copies", "Available Copies")
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=100)
        
        self.books_tree.pack(fill="both", expand=True, side="left")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = tk.Frame(tab)
        button_frame.pack(fill="x", pady=10)
        
        # Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_books
        )
        refresh_button.pack(side="left", padx=5)
        
        # Add book button
        add_button = tk.Button(
            button_frame,
            text="Add Book",
            command=self.show_add_book_dialog
        )
        add_button.pack(side="left", padx=5)
        
        # Load books initially
        self.load_books()
    
    def search_books_by_author(self):
        author_query = self.author_search_entry.get().strip()
        
        if not author_query:
            messagebox.showinfo("Info", "Please enter an author name to search")
            return
            
        try:
            # Clear existing data
            for row in self.books_tree.get_children():
                self.books_tree.delete(row)
                
            connection = get_connection()
            cursor = connection.cursor()
            
            # Search for books by author (using LIKE for partial matching)
            cursor.execute(
                "SELECT isbn, title, author, total_copies, available_copies FROM Books WHERE UPPER(author) LIKE UPPER(:1)",
                ['%' + author_query + '%']
            )
            
            results = cursor.fetchall()
            
            if not results:
                messagebox.showinfo("Search Results", "No books found for this author")
            else:
                # Insert found books
                for row in results:
                    self.books_tree.insert("", "end", values=row)
                    
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def setup_members_tab(self, tab):
        # Create frame for member list
        list_frame = tk.Frame(tab)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for members
        columns = ("ID", "Name", "Email", "Total Fine")
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=100)
        
        self.members_tree.pack(fill="both", expand=True, side="left")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.members_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = tk.Frame(tab)
        button_frame.pack(fill="x", pady=10)
        
        # Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_members
        )
        refresh_button.pack(side="left", padx=5)
        
        # Add member button
        add_button = tk.Button(
            button_frame,
            text="Add Member",
            command=self.show_add_member_dialog
        )
        add_button.pack(side="left", padx=5)
        
        top_borrowers_button = tk.Button(
            button_frame,
            text="Top Borrowers",
            command=self.show_top_borrowers
        )
        top_borrowers_button.pack(side="left", padx=5)
        
        # Load members initially
        self.load_members()
    
    def setup_borrow_tab(self, tab):
        # Create input frame
        input_frame = tk.Frame(tab, pady=20)
        input_frame.pack(fill="x")
        
        # Member ID input
        member_label = tk.Label(input_frame, text="Member ID:")
        member_label.grid(row=0, column=0, padx=5, pady=5)
        self.borrow_member_id = tk.Entry(input_frame, width=10)
        self.borrow_member_id.grid(row=0, column=1, padx=5, pady=5)
        
        # ISBN input
        isbn_label = tk.Label(input_frame, text="Book ISBN:")
        isbn_label.grid(row=0, column=2, padx=5, pady=5)
        self.borrow_isbn = tk.Entry(input_frame, width=15)
        self.borrow_isbn.grid(row=0, column=3, padx=5, pady=5)
        
        # Borrow button
        borrow_button = tk.Button(
            input_frame,
            text="Borrow Book",
            command=self.borrow_book
        )
        borrow_button.grid(row=0, column=4, padx=20, pady=5)
        
        # Create frame for borrowed books list
        list_frame = tk.Frame(tab)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for borrowed books
        columns = ("Borrow ID", "Member ID", "ISBN", "Title", "Borrow Date", "Due Date")
        self.borrowed_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=100)
        
        self.borrowed_tree.pack(fill="both", expand=True, side="left")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.borrowed_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.borrowed_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button
        refresh_button = tk.Button(
            tab,
            text="Refresh",
            command=self.load_borrowed_books
        )
        refresh_button.pack(pady=10)
        
        # Load borrowed books initially
        self.load_borrowed_books()
    
    def setup_return_tab(self, tab):
        # Create input frame
        input_frame = tk.Frame(tab, pady=20)
        input_frame.pack(fill="x")
        
        # Borrow ID input
        borrow_id_label = tk.Label(input_frame, text="Borrow ID:")
        borrow_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.return_borrow_id = tk.Entry(input_frame, width=10)
        self.return_borrow_id.grid(row=0, column=1, padx=5, pady=5)
        
        # Return button
        return_button = tk.Button(
            input_frame,
            text="Return Book",
            command=self.return_book
        )
        return_button.grid(row=0, column=2, padx=20, pady=5)
        
        # Create frame for borrowed books list (not yet returned)
        list_frame = tk.Frame(tab)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for books to return
        columns = ("Borrow ID", "Member ID", "Member Name", "ISBN", "Title", "Borrow Date", "Due Date")
        self.returns_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.returns_tree.heading(col, text=col)
            self.returns_tree.column(col, width=100)
        
        self.returns_tree.pack(fill="both", expand=True, side="left")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.returns_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.returns_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button
        refresh_button = tk.Button(
            tab,
            text="Refresh",
            command=self.load_books_to_return
        )
        refresh_button.pack(pady=10)
        
        # Load books to return initially
        self.load_books_to_return()
    
    def load_books(self):
        try:
            # Clear existing data
            for row in self.books_tree.get_children():
                self.books_tree.delete(row)
                
            connection = get_connection()
            cursor = connection.cursor()
            
            # Get all books
            cursor.execute("SELECT isbn, title, author, total_copies, available_copies FROM Books")
            for row in cursor:
                self.books_tree.insert("", "end", values=row)
                
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def load_members(self):
        try:
            # Clear existing data
            for row in self.members_tree.get_children():
                self.members_tree.delete(row)
                
            connection = get_connection()
            cursor = connection.cursor()
            
            # Get all members
            cursor.execute("SELECT member_id, name, email, total_fine FROM Members")
            for row in cursor:
                self.members_tree.insert("", "end", values=row)
                
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def load_borrowed_books(self):
        try:
            # Clear existing data
            for row in self.borrowed_tree.get_children():
                self.borrowed_tree.delete(row)
                
            connection = get_connection()
            cursor = connection.cursor()
            
            # Get all borrowed books
            cursor.execute("""
                SELECT b.borrow_id, b.member_id, b.isbn, bk.title, 
                       TO_CHAR(b.borrow_date, 'YYYY-MM-DD'), 
                       TO_CHAR(b.due_date, 'YYYY-MM-DD')
                FROM Borrowed b
                JOIN Books bk ON b.isbn = bk.isbn
                WHERE b.return_date IS NULL
            """)
            for row in cursor:
                self.borrowed_tree.insert("", "end", values=row)
                
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def load_books_to_return(self):
        try:
            # Clear existing data
            for row in self.returns_tree.get_children():
                self.returns_tree.delete(row)
                
            connection = get_connection()
            cursor = connection.cursor()
            
            # Get all books to return
            cursor.execute("""
                SELECT b.borrow_id, b.member_id, m.name, b.isbn, bk.title,
                       TO_CHAR(b.borrow_date, 'YYYY-MM-DD'), 
                       TO_CHAR(b.due_date, 'YYYY-MM-DD')
                FROM Borrowed b
                JOIN Books bk ON b.isbn = bk.isbn
                JOIN Members m ON b.member_id = m.member_id
                WHERE b.return_date IS NULL
            """)
            for row in cursor:
                self.returns_tree.insert("", "end", values=row)
                
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def show_add_book_dialog(self):
        # Create a dialog for adding a book
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("300x250")
        dialog.grab_set()  # Make window modal
        
        # Form fields
        tk.Label(dialog, text="ISBN:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        isbn_entry = tk.Entry(dialog, width=20)
        isbn_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Title:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        title_entry = tk.Entry(dialog, width=20)
        title_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Author:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        author_entry = tk.Entry(dialog, width=20)
        author_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Total Copies:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        copies_entry = tk.Entry(dialog, width=20)
        copies_entry.grid(row=3, column=1, padx=10, pady=5)
        copies_entry.insert(0, "1")
        
        # Add function
        def add_book():
            isbn = isbn_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            
            try:
                total_copies = int(copies_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Total copies must be a number")
                return
            
            if not isbn or not title or not author:
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                connection = get_connection()
                cursor = connection.cursor()
                
                # Call the insert_book procedure
                cursor.callproc("insert_book", [isbn, title, author, total_copies])
                connection.commit()
                
                messagebox.showinfo("Success", "Book added successfully")
                dialog.destroy()
                self.load_books()  # Refresh the book list
                
                cursor.close()
                connection.close()
                
            except oracledb.Error as error:
                messagebox.showerror("Database Error", str(error))
        
        # Add button
        add_button = tk.Button(dialog, text="Add Book", command=add_book)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    def show_add_member_dialog(self):
        # Create a dialog for adding a member
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Member")
        dialog.geometry("300x200")
        dialog.grab_set()  # Make window modal
        
        # Form fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = tk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        email_entry = tk.Entry(dialog, width=20)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Add function
        def add_member():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            
            if not name or not email:
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                connection = get_connection()
                cursor = connection.cursor()
                
                # Call the insert_member procedure
                cursor.callproc("insert_member", [name, email])
                connection.commit()
                
                messagebox.showinfo("Success", "Member added successfully")
                dialog.destroy()
                self.load_members()  # Refresh the member list
                
                cursor.close()
                connection.close()
                
            except oracledb.Error as error:
                messagebox.showerror("Database Error", str(error))
        
        # Add button
        add_button = tk.Button(dialog, text="Add Member", command=add_member)
        add_button.grid(row=2, column=0, columnspan=2, pady=20)
    
    def borrow_book(self):
        member_id = self.borrow_member_id.get().strip()
        isbn = self.borrow_isbn.get().strip()
        
        if not member_id or not isbn:
            messagebox.showerror("Error", "Member ID and ISBN are required")
            return
            
        try:
            member_id = int(member_id)
        except ValueError:
            messagebox.showerror("Error", "Member ID must be a number")
            return
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            # Check if member exists
            cursor.execute("SELECT COUNT(*) FROM Members WHERE member_id = :1", [member_id])
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Error", "Member not found")
                cursor.close()
                connection.close()
                return
            
            # Check if book exists and is available
            cursor.execute("SELECT available_copies FROM Books WHERE isbn = :1", [isbn])
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Book not found")
                cursor.close()
                connection.close()
                return
            
            if result[0] <= 0:
                messagebox.showerror("Error", "No copies available for borrowing")
                cursor.close()
                connection.close()
                return
            
            # Call the insert_borrowed procedure
            cursor.callproc("insert_borrowed", [member_id, isbn])
            connection.commit()
            
            messagebox.showinfo("Success", "Book borrowed successfully")
            self.borrow_member_id.delete(0, tk.END)
            self.borrow_isbn.delete(0, tk.END)
            
            # Refresh the borrowed books list
            self.load_borrowed_books()
            self.load_books_to_return()
            self.load_books()
            
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def return_book(self):
        borrow_id = self.return_borrow_id.get().strip()
        
        if not borrow_id:
            messagebox.showerror("Error", "Borrow ID is required")
            return
            
        try:
            borrow_id = int(borrow_id)
        except ValueError:
            messagebox.showerror("Error", "Borrow ID must be a number")
            return
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            # Check if borrow record exists and is not returned
            cursor.execute(
                "SELECT COUNT(*) FROM Borrowed WHERE borrow_id = :1 AND return_date IS NULL", 
                [borrow_id]
            )
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Error", "Borrow record not found or already returned")
                cursor.close()
                connection.close()
                return
            
            # Call the return_book procedure
            cursor.callproc("return_book", [borrow_id])
            connection.commit()
            
            messagebox.showinfo("Success", "Book returned successfully")
            self.return_borrow_id.delete(0, tk.END)
            
            # Refresh the lists
            self.load_books_to_return()
            self.load_borrowed_books()
            self.load_books()
            self.load_members()  # To refresh fines
            
            cursor.close()
            connection.close()
            
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
    
    def show_top_borrowers(self):
        try:
        # Clear existing data
            for row in self.members_tree.get_children():
                self.members_tree.delete(row)
            connection = get_connection()
            cursor = connection.cursor()        
        # SQL query to get the maximum number of books borrowed
            cursor.execute("""
                SELECT m.member_id, m.name, COUNT(b.borrow_id) AS borrow_count
                FROM Members m
                LEFT JOIN Borrowed b ON m.member_id = b.member_id
                GROUP BY m.member_id, m.name
                HAVING COUNT(b.borrow_id) = (
                    SELECT MAX(borrow_count)
                    FROM (
                        SELECT COUNT(borrow_id) AS borrow_count
                        FROM Borrowed
                        GROUP BY member_id
                    )
                )
            """)
            results = cursor.fetchall()
            if not results:
                messagebox.showinfo("Top Borrowers", "No borrow records found.")
            else:
                # Insert found members into the treeview
                for row in results:
                    self.members_tree.insert("", "end", values=(row[0], row[1], "", row[2]))  
            cursor.close()
            connection.close()
        except oracledb.Error as error:
            messagebox.showerror("Database Error", str(error))
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()