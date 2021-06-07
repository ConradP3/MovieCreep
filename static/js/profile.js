// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        selection_done: false,
        uploading: false,
        uploaded_file: "",
        uploaded: false,
        img_url: "",
        query: "",
        results: [],
        userrows: [],
        followingrows: [],
        followerrows: [],
    };

    // This is the file selected for upload.
    app.file = null;

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.upload_file = function (event, row_idx) {
        let input = event.target;
        let file = input.files[0];
        let row = app.vue.userrows[row_idx];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                // Sends the image to the server.
                axios.post(upload_thumbnail_url,
                    {
                        user_id: row.id,
                        thumbnail: reader.result,
                    })
                    .then(function () {
                        // Sets the local preview.
                        row.user_thumbnail = reader.result;

                    });
            });
            reader.readAsDataURL(file);
        }
    };

    /*
    app.upload_complete = function (file_name, file_type) {
        app.vue.uploading = false;
        app.vue.uploaded = true;
    };

    app.upload_file = function () {
        if (app.file) {
            let file_type = app.file.type;
            let file_name = app.file.name;
            let full_url = file_upload_url + "&file_name=" + encodeURIComponent(file_name)
                + "&file_type=" + encodeURIComponent(file_type);
            // Uploads the file, using the low-level streaming interface. This avoid any
            // encoding.
            app.vue.uploading = true;
            let req = new XMLHttpRequest();
            req.addEventListener("load", function () {
                app.upload_complete(file_name, file_type)
            });
            req.open("PUT", full_url, true);
            req.send(app.file);
        }
    };
     */

    app.search = function() {
        if (app.vue.query.length > 1) {
            axios.get(search_url, {params: {q: app.vue.query}
            }).then(function (result) {
                app.vue.results = result.data.results;
            });
        } else {
            app.vue.results = [];
        }
    };

    app.add_following = function(r) {
        //console.log(r);
        //console.log(r.email);
        //email = r.email;
        axios.post(add_following_url, {
            email: r.email,
        }).then(function () {
            followingrows.thumbnail = followingrows.thumbnail;
            followingrows.user_name = followingrows.user_name;
            followingrows.user_email = followingrows.user_email;
        });
    };

    app.delete_thumbnail = function(r) {
        //console.log(r);
        console.log(r.user_email);
        user_email = r.user_email;
        console.log(user_email);
        axios.post(delete_thumbnail_url, {
            email: user_email,
        }).then(function() {
            // Sets the local preview.
            r.user_thumbnail = "";
        });
    };

    app.delete_following = function(row_idx) {
        //console.log(r.user_email);
        //let email = r.user_email
        //console.log(email);
        let id = app.vue.followingrows[row_idx].id;
        axios.get(delete_following_url, {params: {id: id}}).then(function (response) {
            for(let i=0; i < app.vue.followingrows.length; i++) {
                if(app.vue.followingrows[i].id == id) {
                    app.vue.followingrows.splice(i, 1);
                    app.enumerate(app.vue.followingrows);
                    break;
                }
            }
        });
    };



    // This contains all the methods.
    app.methods = {
        //select_file: app.select_file,
        upload_file: app.upload_file,
        search: app.search,
        add_following: app.add_following,
        delete_thumbnail: app.delete_thumbnail,
        delete_following: app.delete_following,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(search_url).then(function (response) {
            app.vue.results = app.enumerate(response.data.results)
        });

        axios.get(load_user_url).then(function(response) {
            app.vue.userrows = app.enumerate(response.data.userrows)
        });
        axios.get(load_following_url).then(function(response) {
            app.vue.followingrows = app.enumerate(response.data.followingrows)
        });
        axios.get(load_follower_url).then(function(response) {
            app.vue.followerrows = app.enumerate(response.data.followerrows)
        });

    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);