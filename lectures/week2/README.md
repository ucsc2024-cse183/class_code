# Javascript

Where to put JS code:

<div onclick="alert('hello world');">Click me</div>
<script>alert("hello world");</script>
<script src="myfile.js"></script>

## Useful links

- JS basics: https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics

- JS comprehensive guide: https://javascript.info/

## event handling example

```
<button id="mybutton">click me </button>
<script>
  const btn = document.querySelector("#mybutton");
  function greet(event) { alert("you clicked the button"); }
  btn.addEventListener("click", greet);
</script>
```

# Vue JS

## Example

## Example prototype app

```
<div id="myapp">{{ message }}</div>
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script>
  var app = {};
  app.config = {
    setup: function() {
      return {
        message: "hello world"        
      }
    },
    methods: {
      click: function() { alert("you clicked"); }
    }
  };
  app.vue = Vue.createApp(app.config).mount('#myapp');
</script>
```

<div v-text="expr"
     v-for="elem in array"
     v-if="expr"
     v-on:click="method()"
     v-on:keyup="method()"
     v-bind:class="{'selected':expr}"
     v-bind:style="{'color':expr}">...</div>     
<input v-model="variable"/>

## Useful links

Vue js quck start: https://vuejs.org/guide/quick-start.html