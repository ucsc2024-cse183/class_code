"use strict";

function clone(obj) { return JSON.parse(JSON.stringify(obj)); }

var app = {};
app.config = {};
app.config.setup = function() {
    return {
        new_item: Vue.ref({ title: "", description: ""}),
        items: Vue.ref([])
    };
};
app.config.methods = {};
app.config.methods.add_new_item = function() {
    this.items.push(clone(this.new_item));
    this.new_item.title = "";
    this.new_item.description = "";
};
app.vue = Vue.createApp(app.config).mount("#myapp");