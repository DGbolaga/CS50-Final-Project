# MyBook  

#### Video Demo: <https://youtu.be/up3oyNeJb40?si=zcCUAgc3r_UUVa5l>  

## Description  

### Vision  
**MyBOOK** is more than just a book-sharing platform—it’s a community-driven initiative that keeps knowledge flowing, reduces waste, and makes learning more accessible by lowering the cost of textbooks. This is my **MVP**, and I plan to enhance it in the near future.  


### Tools and Thought Process  
I built **MyBOOK** using **Python (Flask), SQL, HTML, CSS,** and a bit of **JavaScript**. I integrated **Google’s Books API** and the **Open Library API** to fetch cover images for certain books. I also used the **Google Maps API** to display the location of users who enlisted a book for sale.  


- **Flask**: I used Flask for the backend because it's the web framework I'm most familiar with—I used it in week 9 to complete the problem set. It's also quick to set up and beginner-friendly.  

- **SQL**: For the database, I used SQLite3. Again, it's what I was most acquainted with. Also, it allowed me to make subtle changes to my database quickly. I made use of CS50's library to avoid SQL injection attacks.  

- **JavaScript**: A bit of JavaScript to dynamically show the "other" category input, allowing users to input a suitable tag if it's not already there.  

- **Pandas**: The database was populated with dummy data. I outlined certain books from different categories in `books.txt` and used the Google Books API to get the relevant details for them. Some cover images from Google Books weren't good enough, which led me to use the Open Library API. I received help from Claude AI in doing this. The bulk of my time was spent cleaning the data, and the Pandas library played a huge role in accomplishing that.  

- **WTForms**: The login, sign-up, and book listing forms were created using WTForms—it allowed me to set constraints and validate web forms.  

### Features  
- Book searches can be done via the search bar. E.g., users can search by title using the search bar.  
- Added a filter by book categories option.
- Addition of new books: Users can enlist a book for sale by filling out the book form.  
- Implemented Sign-in feature: User authentication was enforced.  
- Implemented Sign-up feature (Creating new users).  
- Restricted the delete feature to the admin profile.  
- Implemented Log-out feature.  

### Folders  
- **csv_file**: Contains the books added by users, as well as books deleted by the admin.  
- **static**: Contains the CSS file and the background image.  
- **templates**: Contains the HTML files.  
- **testing_folder**: Contains the Python script used to fetch image URLs, descriptions, and other details needed to populate the bookshelf. It isn't complete, as I had to do a lot of manual cleaning to get the correct data.  
- **text_file**: Contains `books.txt`, which lists books to fetch using the Google Books API and Open Library API. The `requirements.txt` file includes the necessary packages to run the program. The `steps` file documents the steps I took while creating the program.  

### Python Files  
- The entry point for my Python script is **main.py**.  
- My database can be created using the **created_db.py** script. It consists of the user table (`id`, `name`, `password`, `email`) and the books table (`id`, `title`, `authors`, `description`, `category`, `cover_image`, `location_of_seller`, `format_of_book`, `ratings`, `user_who_added_the_file`). Drawing from concepts learned during the course, I implemented password hashing for security measures.  
- All the forms used in the app were created in **forms.py**.  
- **helpers.py** contains the `User` class, which helps track users in the app.  

### Issues I Faced  
I had some issues fetching images using the **Google Books API**, so I used the **Open Library API** to supplement the missing images. 

I created two CSS files—one for styling the **welcome page** and another for the rest of the HTML files. I wanted it to look like what I had in my Figma design, though I made some adjustments.  

To debug and improve certain parts of my code, I used **Claude AI** and **ChatGPT**. I made sure to cite AI-generated sections with comments in my code.  

### Future Plans  
- MyBOOK could be improved with pricing features, comment sections, transaction history for user profiles, and real-time info on seller status (online or offline).  
- I'll look into efficient databases for scaling the program.  
- A recommendation system will definitely enhance user experience by connecting students with similar interests in the same or different universities.  
- At the time of building this, my programming skills are insufficient to fully actualize the project. I'll be taking advanced courses and enlisting in developer programs that will equip me to completely build and deploy the project.  

### About the Developer  
Omogbolaga Daramola is a first-year Computer Science student at the University of Lagos, Nigeria. He is an optimist who thrives on solving challenges both within and beyond his environment.  
