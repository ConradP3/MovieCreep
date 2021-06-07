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
        // end of review comments feature
        images: [],
        query: "",
        results: [],
        delete_edit_mode: false,
        view_mode: 0,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.complete = (images) => {
        // Initializes useful fields of images.
        images.map((img) => {
            img.rating = 0;
            img.num_stars_display = 0;
        })
    };


    app.set_stars = (img_idx, num_stars) => {
        let img = app.vue.images[img_idx];
        img.rating = num_stars;
        // Sets the stars on the server.
        axios.post(set_rating_url, {image_id: img.id, rating: num_stars});
    };

    app.stars_out = (img_idx) => {
        let img = app.vue.images[img_idx];
        img.num_stars_display = img.rating;
    };

    app.stars_over = (img_idx, num_stars) => {
        let img = app.vue.images[img_idx];
        img.num_stars_display = num_stars;
    };


    app.set_delete_edit_status = function (new_status) {
        app.vue.delete_edit_mode = new_status;
    };

    app.add_movie = function () {
        axios.post(add_movie_url,
            {
                post_text: app.vue.add_post_text
            }).then(function () {
            app.set_delete_edit_status(false);
        });
    };


  
    app.search = function() {
        if (app.vue.query.length > 1) {
            axios.get(search_url, {params: {q: app.vue.query}
            }).then(function (result) {
                app.vue.results = enumerate(result.data.results);
            });
        } else {
            app.vue.results = [];
        }
    }


    // Toggle gallery view
    app.set_view = function (new_status) {
        app.vue.view_mode = new_status;
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

    // This contains all the methods.
    app.methods = {
        get_comment: app.get_comment, // Get comment of your review
        hide_comment: app.hide_comment, // clear the p tag of text

        set_stars: app.set_stars,
        stars_out: app.stars_out,
        stars_over: app.stars_over,
        set_delete_edit_status: app.set_delete_edit_status,
        add_movie: app.add_movie,
        search: app.search,

        set_view: app.set_view,
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
