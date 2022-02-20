## Notes: Lecture 5 Javascript

Javascript runs on the client side
This can be faster
THis allows us to manipulate the Document Object Model to create interactivity

Include javascript with <script></script>

helloworld.html:

```
<!DOCTYPE html>
<head>
    <title>Hello</title>
</head>
<body>
    <script>
        alert("hello, world!")
    </script>
</body>
```

### Events

Event-driven programming:

Thinking about things that happen on the web as events that happen
An event is a user action, like clicking a button or selecting from a dropdown

Javascript allows you to have event listners and event handlers: "When user does
x, do y"

Javascript functions:

```
function hello() {
    alert("Hello, World!");
}
<button onclick="hello()">click here</button>
```

### variables:

```
let counter = 0;
function count() {
    counter +=1; (or counter++)
    alert(counter);
}
button onclick="counter()">click here</button>
```

### querySelector

document.querySelector(): look through a page and extract an html element to manipulate
querySelector returns only 1 element, the first one it finds that matches

Javascript uses `===` to check for strict equality, uses `==` for looser equality
where types are ignored

`if (condition === value) {expression1} else {expression2};`

javascript has multiple ways to create a variable:
user `let` to define a variable whose value might change
use `const` to define a variable whose value that won't change

### DOM Manipulation

Template literal: string that can hold variables.  
Formatted (inside a fn) as `` alert(`This will print a ${variable}`) ``

functions can be treated as variables (this is called functional programming)
replace onclick="counter()" attribte with:
`document.querySelector("button").onclick=count;`

Use the javascript console in browser to troubleshoot and debug

Javascript will throw an error if a script refers to an html object because the
browser reads code from top to bottom and the scripts are above the html. Solve
by 1) move the script to the bottom, 2) add a event lister to the document
itself:
`document.addEventListener('DOMContentLoaded', function() {some function});`

Working with forms:

<script>
document.addEventListener('DomContentLoaded', function() {
    document.querySelector('form').onsubmit = function() {
        const name = document.querySelector('#name').value;
        alert(`Hello, ${name}`);
    }
})
</script>
<body>
<form>
    <input id="name" placeholder="What's your name?" type="text">
    <input type="submit">
</form>
</body>

Working with CSS & using data attributes

<script>
document.addEventListener('DomContentLoaded', function() {

    document.querySelectorAll('button').forEach(function(button) {
        button.onclick = function() {
            document.querySelector('#hello').style.color = button.dataset.color;
        }
    })
</script>
<body>
<h1 id="hello">Hello!</h1>
<button data-color="red">Red</button>
<button data-color="blue">Blue</button>
<button data-color="green">Green</button>
</body>

`data-<name>` (here, `data-color`) creates an array variable for a set of values
called by the method `dataset.name`

Arrow notation for functions in JS:
.forEach(button => {somefunction});
