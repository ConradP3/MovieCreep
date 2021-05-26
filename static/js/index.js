// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
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
                app.vue.results = result.data.results;
            });
        } else {
            app.vue.results = [];
        }
    }


    // Toggle gallery view
    app.set_view = function (new_status) {
        app.vue.view_mode = new_status;
    };

    // This contains all the methods.
    app.methods = {
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
        // First we get the images.
        axios.get(get_images_url)
            .then((result) => {
                // We set them
                let images = result.data.images;
                app.enumerate(images);
                app.complete(images);
                app.vue.images = images;
            })
            .then(() => {
                // Then we get the star ratings for each image.
                // These depend on the user.
                for (let img of app.vue.images) {
                    axios.get(get_rating_url, {params: {"image_id": img.id}})
                        .then((result) => {
                            img.rating = result.data.rating;
                            img.num_stars_display = result.data.rating;
                        });
                }
            });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
