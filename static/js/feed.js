// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // review comments feature
        review_comments: {}, // This is an object that is kindof like a dictionary.
                             // The key will be the review id and the value is
                             // another object with the commenters user name and
                             // comment
        comment_box: "",
        editing_id: -1,      // Id of the movie listing to edit
        editing: false
        // end of review comments feature
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // Get a comment by review_comment id
    app.get_comment = function(comment_id, p_tag_id) {
        comment_row = app.vue.review_comments["" + comment_id];
        comment_string = comment_row.name + " says: " + comment_row.comment;
        document.getElementById(p_tag_id).innerHTML = comment_string;
    }

    // When a user hovers away from the commentors icon, clear the text
    app.hide_comment = function(p_tag_id) {
        document.getElementById(p_tag_id).innerHTML = "";
    }

    // When the user presses the comment button in the feed on a movie listing
    app.edit_comment = function(element_id) {
        app.vue.comment_box = "";
        app.vue.editing_id = element_id;
        app.vue.editing = true;
    }

    // Cancel the comment editing
    app.cancel_comment = function() {
        app.vue.comment_box = "";
        app.vue.editing_id = -1;
        app.vue.editing = false;
    }

    // Post the comment to the review_comment table
    app.post_comment = function() {
        axios.post(post_comment_url, 
            {
                listing_id: app.vue.editing_id,
                comment: app.vue.comment_box
            }).then(function (response) {
                app.vue.comment_box = "";
                app.vue.editing_id = -1;
                app.vue.editing = false;
            });
    }

    // This contains all the methods.
    app.methods = {
        get_comment: app.get_comment,   // Get comment of your review
        hide_comment: app.hide_comment, // clear the p tag of text

        edit_comment: app.edit_comment,
        cancel_comment: app.cancel_comment,
        post_comment: app.post_comment
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Populate the review comment object
        axios.get(get_comments_url)
            .then((result) => {
                comments = result.data.comments;
                for (let comment_id in comments) {
                    Vue.set(app.vue.review_comments, comment_id, comments["" + comment_id]);
                }
            });
        // End of review comment object population
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
