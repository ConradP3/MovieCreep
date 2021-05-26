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

        // Ratings
        add_mode: false,
        add_post_text: "",
        add_user_name: "",
        
        rows: [],

        username: username,
        useremail: useremail,

        haters: "",
        likers: "",

        rating: -1,
        temp: 0,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;
            // e.rating = -1;
            e.temp = 0;
        });
        return a;
    };

    app.reset_form = function () {
        app.vue.add_post_text = "";
    };

    app.add_post = function () {
        axios.post(add_post_url,
            {
                post_text: app.vue.add_post_text,
                post_user: app.vue.add_user_name,
                likers: app.vue.likers,
                dislikers: app.vue.haters,
                rating: app.vue.rating

            }).then(function (response) {
            app.vue.rows.push({
                id: response.data.id,
                post_text: app.vue.add_post_text,
                post_user: app.vue.add_user_name,
                likers: app.vue.likers,
                dislikers: app.vue.haters,
                email: response.data.email,
                rating: -1,
                temp: response.data.temp,
                name: app.data.username,
                curremail: app.data.useremail


            });
            app.enumerate(app.vue.rows);
            app.set_add_status(false);
            Vue.set(app.data.rows[length - 1], 'rating', -1);
            // Vue.set(app.data.rows[length - 1], 'rating', -1);
            app.reset_form();
            console.log(app.vue.rows);
        });
    };


    app.delete_post = function(row_idx) {
        let id = app.vue.rows[row_idx].id;
        axios.get(delete_post_url, {params: {id: id}}).then(function (response) {
            for (let i = 0; i < app.vue.rows.length; i++) {
                if (app.vue.rows[i].id === id) {
                    app.vue.rows.splice(i, 1);
                    app.enumerate(app.vue.rows);
                    break;
                }
            }
            });
    };

    app.set_add_status = function (new_status) {
        app.vue.add_mode = new_status;
    };

    app.complete = (rows) => {
        // Initializes useful fields of post
        rows.map((post) => {
            // post.rating = -1;
            post.temp= 0;
        })
    };

    app.set_rating = (post_idx, post_like) => {
        let post = app.vue.rows[post_idx];
        post.rating = post_like;
        // app.vue.rating = post_like;
        // Sets the rating on the server.
        axios.post(set_rating_url, {rating: post.rating,
                                    id: post.id});
        // let rows = response.data.rows;
        // app.vue.rows = rows;
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
        // Posts and Ratings
        add_post: app.add_post,
        set_add_status: app.set_add_status,
        delete_post: app.delete_post,
        set_rating: app.set_rating,
        reset_form: app.reset_form,


        // Search
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
        axios.get(load_post_url).then(function (response) {
            app.vue.rows = app.enumerate(response.data.rows);
            console.log(app.vue.rows);
            //     // get ratings for each post. These depend on the user.
                for (let post of app.vue.rows) {
                    axios.get(get_rating_url, {params: {"post_id": post.id}})
                        .then((result) => {
                            post.rating = result.data.rating;
                            console.log(post);
                        });
                }
        });
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
