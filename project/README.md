# Environ: Towards a greener future!

## Project title- Environ
## YoutTube link- https://youtu.be/rwb6cQoIqD4
#### Description: A project (site) that aims at acheiving a greener and cleaner future, by alerting/making people aware.

### Now let's see how the website works, it's functions and take a deep look at each files purpose:

#### First let's take a look at how the website works

You are first taken to the index page wich has a navbar with some options and has some headings in it's
body under which are the several pieces of advice, contributions, etc; shared by the users.

The navbar has a "Environ" logo which is a link in itself that allows you to reload the index page
or to come back to the index if you are on some other page. Then sepending on whether the user has
logged in, we see different options, lets look at those:

#### If not logged in:

- Register: Allows a new user to register.
- Login: You can login here.
- Developer: Information bout the developer.
- About: A brief description about the website.

#### If logged in:

- Your ideas: Shows all the content shared by you (and you only).
- Share idea: Allows the user to share their views with the user.
- Developer
- About
- Logout: User can logout from here.


The navbar also has a search bar using which the user can search for a particular content
by seaching for a specific word in the title, the description or the name of the author.
In addition to that the user can also search for shared types by either manually typing
in the type or by selecting and searching for a particular type in the dropdown menu
which appears only on the index page.

### To know what the other pages do, you'll have to visit the website for yourself.

### Now let's take a look at each of the files...

#### Static files:-
- There are a lot of images
- And there is the CSS styles file which has unique styles for almost all the elements on the website.


#### HTML Templates:-
All the templates required for the website.


#### application.py
It is where most of the logic takes place, it connects the templates with the database.


#### environ.db
The database, it has three tables, one storing the users information, another one for the shared content
and the last one for the quotes that appear as footers in the website.

#### helpers.py
It has a function to check if the user is logged in.

#### requirements.txt
List of all the components required for the making of the site


### Some features to look out for:
- Search bar
- Quotes
And everything else!

### You just have to register to save the world!