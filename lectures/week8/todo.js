"use strict";

// utility function to clone an object
function clone(obj) { return JSON.parse(JSON.stringify(obj)); }

// container for everything
var app = {};
// convenience function to make an item
app.make_item = function() {
    return {
        title: "",
        description: "",
        state: 0,        
    };
};
// The vue input config object    
app.config = {};
// The vue input setup() function returns the data to be exposed
app.config.setup = function() {
    return {
        new_item: Vue.ref(app.make_item()),
        items: Vue.ref([]),
        message: Vue.ref("")
    };
};
// the vue methods to be exposed
app.config.methods = {};
// method to mv a new item from the form into the list of items
app.config.methods.add_new_item = function() {
    if (app.vue.new_item.title.trim() !== "") {
        app.vue.items.push(clone(this.new_item));
        app.vue.new_item = app.make_item();
    }
    app.save();
};

// save and load methods (the save in the browser memory)
app.save = function() {
    window.localStorage.setItem("todo_items", JSON.stringify(app.vue.items));
}
app.load = function() {
    try {
        let items = JSON.parse(window.localStorage.getItem("todo_items"));
        if (items) app.vue.items = items;
    } catch(e) {};
}

// make the vue app
app.tmp = Vue.createApp(app.config);

// article component
app.tmp.component("my-article", {
    props: ["item"],
    setup: function(vars) {return {}; },
    emits: ['message'],
    methods: {
        // method to rotate (0->1->2->0) the state of an item (to change color)
        rotate: function(item) {
            item.state = (item.state + 1) % 3;
            app.save();
        },
        // method to remove the specified item
        remove: function(item_to_rm) {
            app.vue.items = app.vue.items.filter(function(item)
            {
                return item != item_to_rm;
            });
        
            app.save();
        }
    },
    template: `<article class="message"    
    v-bind:class="{'is-success':item.state==0, 'is-warning':item.state==1, 'is-danger':item.state==2}">
    <div class="message-header" v-on:click="rotate(item)">
    <p v-text="item.title"></p>
    <button class="delete" aria-label="delete" v-on:click="remove(item)"></button>
    </div>
    <div class="message-body" v-text="item.description"></div>
    </article>`
});
app.vue = app.tmp.mount("#myapp");
// then reload any saved data
app.load();