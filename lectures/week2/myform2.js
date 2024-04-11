"use strict";

var app = {};
app.config = {};
app.config.setup = function() {
    return {
        message: Vue.ref(""),
        fruits: Vue.ref(["apple", "strawberry", "pineapple"])
    };
};
app.config.methods = {};
app.config.methods.reset = function() { this.message = ""; };
app.vue = Vue.createApp(app.config).mount("#myapp");