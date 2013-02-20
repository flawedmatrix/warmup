ERR_BAD_CREDENTIALS = (-1);
ERR_USER_EXISTS = (-2);
ERR_BAD_USERNAME = (-3);
ERR_BAD_PASSWORD = (-4);

$(document).ready(function() {
    show_login_page();
});

function json_request(page, dict, success, failure) {
    $.ajax({
        type: 'POST',
        url: page,
        data: JSON.stringify(dict),
        contentType: "application/json",
        dataType: "json",
        success: success,
        error: failure
    });
}

function get_err_message(code) {
    if (code == ERR_BAD_CREDENTIALS) {
        return ("Invalid username and password combination. Please try again.");
    } else if (code == ERR_BAD_USERNAME) {
        return ("The user name should not be empty and must be at most 128 characters long. Please try again.");
    } else if (code== ERR_USER_EXISTS) {
        return ("This user name already exists. Please try again.");
    } else if (code == ERR_BAD_PASSWORD) {
        return ("The password should be at most 128 characters long. Please try again.");
    } else {
        return ("Something wrong happened with the backend.");
}

$('#login-button').click(function() {
    username = $('#login-username').val();
    password = $('#login-password').val();
    json_request("/user/login", {
        user : username,
        password : password
        },
        function(data) {
            return handle_login_response(data, username);
        },
        function(err) {
            console.log("Something wrong happened with the backend.");
        }
    );
    return false;
});

$('#add-user-button').click(function() {
    username = $('#login-username').val();
    password = $('#login-password').val();
    json_request("/users/add", {
        user : username,
        password : password
        },
        function(data) {
            return handle_add_user_response(data, username);
        },
        function(err) {
            console.log("Something wrong happened with the backend.");
        }
    );
    return false;
});

$('#logout-button').click(function() {
    show_login_page();
    return false;
});

function show_login_page(message) {
    if (!message) {
        message = "Please enter your credentials below";
    }
    $('#welcome-page').hide();
    $('#login-username').val("");
    $('#login-password').val("");
    $('#login-message').html(message)
    $('#login-page').show()
}

function show_welcome_page(user, count) {
    $('#login-page').hide();
    $('#welcome-page').show();
    $('#welcome-message').html("Welcome " + user + ", you have logged in "+ count + " times.");
}

function handle_login_response(data, user) {
    if (data.errCode > 0) {
        count = data.count;
        show_welcome_page(user, count);
    } else {
        show_login_page( get_err_message(data.errCode) );
    }
}

function handle_add_user_response(data, user) {
    if (data.errCode > 0) {
        count = data.count;
        show_welcome_page(user, count);
    } else {
        show_login_page( get_err_message(data.errCode) );
    }
}
