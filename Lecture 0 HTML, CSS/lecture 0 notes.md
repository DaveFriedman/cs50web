## Notes: Lecture 0 HTML, CSS


## Introduction
HTML5 and CSS3  
HTML: Structure, CSS: Style  
Git: Version control to keep track of changes, and allows multiple people to 
work on different parts then merge them back together.

Python, with Django framework to design and develop webapps.  
Django is good for webapps that interact with data.  
SQL: Language for interacting with data  
Django allows us to use models and migrations to interact with data  

Javascript: Make webpages more interactive. Used on UIs.

Testing & CI/CD:  
CI/CD: Continuous Integration and Continuous Development  
Tools & Software best practices to design and develop efficiently.  
Testing prevents us from breaking our webapp after updating it  

Scalability & Security:  
What do we need to change in order to allow lots of users to connnect at the
same time?  
How might an adversary attack our webapp, and what should we preemptively do to
stop them?  

## HTML  
Hyper-Text Markup Language: describes the structure of the webpage 

hello.html: Hello, World!  
```<!DOCTYPE html>```: "This page is written using html5"  
HTML elements: parents and children, have opening ```<tag>``` and closing ```</tag>```
elements can have attributes, Ex: ```<html lang="en">```

DOM: Document Object Model:  
A tree structure describing how the page's HTML elements relate to each other  
Important for modifying the page with JS


Headers: ```<h1>``` through ```<h6>```  
Comments: ```<!-- comment -->```  
```<strong>``` for bold, ```<em>``` "emphasis" for italics  
```<ol>``` ordered lists, ```<ul>``` unordered lists, ```<li>``` for list items  
Anchor tag for a link: ```<a href="http://example.com">A link to example.com</a>```  
Image tags for images ```<img src="a url or a file address" alt="alt text">```, note: no closing tag  
Tables:   
initialize with ```<table>```,  
column names in ```<thead>```,  
initialize data in ```<tbody>```,  
create a row with ```<trow>```,  
create cells within a row with ```<td>```

```<form>```: How users provide information to a webpage  
2 parts: input fields and submit button  
```<input type=text placeholder="username" name="username">```  
the form attribute ```name=``` is the variable name of the input of the form  
for input type ```<datalist>```: a searchable way to select from many options  
Ex: a ```<datalist id="countries"```, containing many elements, from ```<option
value="Afghanistan">``` through  ```<option value="united states"```,  where you
start typing ```uni...``` and ```united states``` will autocomplete  


## CSS
Cascading Style sheets, version 3 aka CSS3  
Color, spacing, justification, layout, padding, color etc.  

CSS inline: in some tag, include a Style attribute with a property and value  
```<tag style="property: value;></tag>```  
Ex: ```<h1 style="color: blue; text-align: center;">Hello World!</h1>```  

HTML elements will inherit the styles of thier parents, so a style applied to
```<body>``` will apply to all elements inside.  
Repeating styles (Ex: to make all ```<h1>``` elements look the same) gets clunky
fast though.  
Instead, maybe put all styles inside ```<head>```, add ```<style> h1 { color: blue; text-align: center }</style> ```  

Styling across multiple html page: styles.css  
In the styles.css file, write all your styling.   
Then, add ```<link rel="stylesheet" href="styles.css">``` in the head.  

Common CSS properties:  
text color: ```color: somecolor;```  
```background-color: somecolor;```

Controlling size:  
```width: ###px;```  
```height: ###px;```  
```margin: ##px;``` Add space around the exterior of an element  
```padding: ##px;``` move content inside an element away and inwards from element's
boundary. This is effectively margin, but for content within an element    
```border:##px solid black;``` Increase the size an element's boundary. Choose size, line pattern, and color 

Fonts:  
specify a font and a fallback font-family, Ex: ```font-family: Arial; sans-serif;```  
also, ```font-size: 20px; font-weight: bold;```

CSS Selectors:    
The style attribute's name, Ex: ```h1, h2 { color: blue; }```  
IDs: a unique name for an element, start with ```#```  
Ex: html ```<h1 id="foo">Hello, World</h1>```, css ```#foo { color: green; }```  
Classes: a non-unique name for a set of elements, start with ```.```  
Ex: html ```<h1 class="bar">"Hi again"</h1>``` and ```<h1 class="bar">"Hi
three"</h1>```,  
with ```.bar { color: orange; }```  

CSS specificity: handling css styling conflicts.  
Highest to lowest precedence: Inline style, then id, then class, then attribute
type  
Precedence takes priority over linear order in the styles.css file

More CSS selectors:  
Multiple element selector ("a and b"): a, b  
Descendant selector ("b is a descendent (child, grandchild, etc.) of a"): a b  
Child selector ("b is the direct child of a"): a > b  
Adjacent sibling selector ("b is a sibling of a and also directly follows a"):  a + b  
Attribute selector ("all elements a that have attribute b"): [a=b]  
Psuedoclass selector ("all elements a that have psuedoclass (like :hover etc.) b"): a:b  
Psuedoelement selector ("b is a pseudoelment (a specific part"of a): a::b  


## Responsive Design  
Design for multiple devices. Multiple techniques: viewport, media queries,
flexbox, grids  

Viewport: the visual part of the screen that the viewer can actually see.  
Many websites assume the viewport is the same on any device, which causes the
website to just shrink the whole webpage so it fits, which makes the website too
small to view well.  
Instead, tell the device to use a viewport that is the same width as the actual
device being used, and not the viewport of a larger screen:  
```<meta name="viewport" content="width=divice-width, initial-scale=1.0">```  

Media queries: control how the site will look, depending on how the page is
being viewed  
If the size of the screen is some width X, style one way. If it's width Y, style
a different way  
This syntax will change the bkg color based on width:  
```@media (min-width: 600px) body { background-color: red; }```  
```@media (min-width: 599px) body { background-color: blue; }```  
Media queries are often used with the ```display: hidden;``` property, to control whether
some elements are visible based on screen size  

Flexbox: Wrap elements based on viewport width  
Helpful to prevent elements from overflowing  
Create a ```div class="container">``` that contains ```<div>``` boxes
that contain content.  
Then, add ```.container { display: flex; flex-wrap: wrap;}``` to have them
follow flexbox rules  

Grids: Manually define a grid's #cols, then let the cells responsively resize to fit the viewport  
Create a ```<div class="container">``` that contains ```<div>``` cells that contain
content.  
Then, add ```.container { display: grid; grid-template-columns: 50x auto
50px;}``` for 3 columns where the center column adjusts to viewport size.  
The ```<div>``` cells will distribute themselves, by default across all columns then
wrap to row #2


### Bootstrap  
A popular library to style webpages responsively  

http://www.getbootstrap.com, currently v5  
Include in a website with ```<link rel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
crossorigin="anonymous">```

Includes many elements, including alerts, breadcrumbs, carousels, etc.  
The Boostrap column model has 12 columns, and divs can be sized according to how
many columns they take up.  

Ex: ```<div class="col-3">``` takes up 3 columns,  
```<div class="col-6">``` would be twice as wide.  
Columns shold sum to 12  
Bootstrap can also specify column sizes based on screen size.  
Ex: ```<div class="col-lg-3 col-sm-6">```, this div will be 3 units wide on a large
screen, 6 units wide on a small screen.  
This keeps the div element large enough to comfortably view, even on small screens  


### SASS ("Syntactically Awesome StyleSheets")    
SASS is a preprocessor, which is a separate scripting language that extends CSS
to make it faster and less repetitive. It must be compiled to a .css file.
Files (by convention) end with .scss.  

SASS has variables, which begin with $  
Ex: ```$color: red;```.  
Then, use in place of the css value, ```body { background-color: $color; }```  

SASS also allows nested css attributes, impossible without classes in vanilla css:  
Ex: make all h1s inside a div lightblue, and all h2s red  
```div { background-color: blue; ```  
        ```h1 { color: lightblue; } ```  
        ```h2 {color: red;}```  
    ```}```

Finally, SASS has inheritance, which allows us to define a class of attributes
with a basic style which can be then shared to subclasses that inherit the class
properties and then extend or modify them.  
Ex: ```%message { font-family: sans-serif; font-size: 18px }```,  
and then ```.success { @extend %message; background-color: green;}```  
and also ```.error { @extend %message; background-color: red; }```

Browsers don't undestand SASS, so it must be compiled to css.  
Install the SASS compiler, then, in CLI, run ```sass styles.scss:styles.css```  
To compile SASS to css automatically, with a background process, use the Watch flag by running
```sass --watch styles.scss:styles.css```.  
There are a few SASS compilers, webpack is popular. 