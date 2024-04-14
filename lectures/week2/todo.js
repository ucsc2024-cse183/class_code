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
        state: 0};
    };
// The vue input config object    
app.config = {};
// The vue input setup() function returns the data to be exposed
app.config.setup = function() {
    return {
        new_item: Vue.ref(app.make_item()),
        items: Vue.ref([])
    };
};
// the vue methods to be exposed
app.config.methods = {};
// method to mv a new item from the form into the list of items
app.config.methods.add_new_item = function() {
    if (this.new_item.title.trim() !== "") {
        this.items.push(clone(this.new_item));
        this.new_item = app.make_item();
    }
    app.save();
};
// method to remove the specified item
app.config.methods.remove = function(item_to_rm) {
    this.items = this.items.filter(function(item) { return item!=item_to_rm; });
    app.save();
};
// method to rotate (0->1->2->0) the state of an item (to change color)
app.config.methods.rotate = function(item) {
    item.state = (item.state + 1) % 3;
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
app.vue = Vue.createApp(app.config).mount("#myapp");
// then reload any saved data
app.load();