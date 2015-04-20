noise = {

    initialize_noise_form: function () {

        // Activate JSForms for client side form validation
        $(".noise-form").jsf({
            selectInput: function (elt) {
                return elt.parent();
            }
        });

    },

    initialize_email_noise_form: function () {
        $(".noise #email-texts").on("change", function () {
            var txt = $("#email_heading").text() + "\n" + $("option:selected", this).text();
            $(".noise #email-text-div").text(txt);
        });

        $(".noise .email_noise").on("click", function (e) {
            e.preventDefault();
            $("#email_body").val($("#email-text-div").text());
            $("#email_noise_form").submit();
        });
    },

    initialize_twitter_noise_form: function () {

        $(".noise #twitter-texts").on("change", function () {

            var txt = $(".noise #tweet-text-div").text();
            var url = "";
            if (txt.indexOf("http:") != -1) {
                url = txt.match(/http:[^\s]* /) + " ";
            }

            $(".noise #tweet-text-div").text("." + $("#twitter_rcpt").text() + " " + $("option:selected", this).text() + url);
            $('#tweet-text-div').trigger("keyup");
        });

        $(".noise .images .clickable-image").on("click", function (e) {

            e.preventDefault();
            var txt = $("#tweet-text-div").text();
            var url = $(this).find("img").attr("src").replace("/image_thumb", "");

            if (txt.indexOf("http://") != -1) {
                txt = txt.replace(/http:[^\s]* /, url + " ");
                $("#tweet-text-div").text(txt);
            } else {
                $("#tweet-text-div").text(txt + url + " ");
            }
            $('#tweet-text-div').trigger("keyup");
        });

        $('#tweet-text-div').on("keyup", function () {

            var txt = $(this).text();
            var url = txt.match(/http:[^\s\n]*/) + " ";
            var tweet_length = 0;

            // tweet can only be 140 characters minus a shortened url's length (max. 20)
            if (url.length > 20) {
                tweet_length = txt.length - url.length + 20;
            } else {
                tweet_length = txt.length;
            }

            if (tweet_length > 119) {
                $(this).addClass("exceeds_limit");
            } else {
                $(this).removeClass("exceeds_limit");
            }

            $("#tweet-counter").text(tweet_length);
        });
    },

    initialize_twitter_web_intent: function () {

        // Bind to tweet event and submit the noise form
        twttr.events.bind(
            'tweet',
            function (event) {
                console.log("Tweet tweet tweet...");
                $("#twitter_noise_form").submit();
            }
        );

        $(".tweet_noise").on("click", function (e) {
            // Compose the tweet
            $("#tweet-text").val($("#tweet-text-div").text().substring(0, 119) + " " + $("#absolute_url").text());
            $(this).attr("href", "https://twitter.com/intent/tweet?text=" + $("#tweet-text").val());
        });
    },

    initialize_tabs: function () {
        $(".noise-menu a").click(function (event) {
            event.preventDefault();
            $(this).parent().addClass("current");
            $(this).parent().siblings().removeClass("current");
            var tab = $(this).attr("href");
            $(".tab-content").not(tab).css("display", "none");
            $(tab).fadeIn();
        });
    },

    initialize_readmore: function () {

        $("#noise-container a.readmore").on("click", function (e) {
            e.preventDefault();
            $(this).parent().animate({"height": $(this).parent()[0].scrollHeight});
            $(this).fadeOut();
        });
    }
};

$(document).ready(function () {

    noise.initialize_noise_form();

    noise.initialize_twitter_noise_form();
    noise.initialize_twitter_web_intent();

    noise.initialize_email_noise_form();

    noise.initialize_tabs();

    noise.initialize_readmore();
});