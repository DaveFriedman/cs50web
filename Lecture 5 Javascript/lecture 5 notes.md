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
