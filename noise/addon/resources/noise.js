noise = {

    initialize_noise_form: function () {

        $("#no-javascript").hide();
        $("#noise-container").show();

        // Activate JSForms for client side form validation
        $(".noise-form").jsf();

        // Landingpages

        if( $(".noise-menu li").length == 1 ) {
            $(".noise-menu").hide();
        }

        var lp = $("#current_tab").text();

        if( $("#current_tab").text() && $(".noise-menu .noise-menu-" + lp).length > 0 ) {
            $(".noise-menu .noise-menu-" + lp).addClass("current");
            $("#" + lp + "-tab").show();
        } else {
            $(".noise-menu li").first().addClass("current");
            $(".tab").first().show();
        }

        $(".image.thumb").on("mouseenter", function() {
            var image_id = $(this).attr("id");
            var idx = image_id.substring(image_id.lastIndexOf('-')+1);
            $("#t-popup-" + idx).show({"effect": "blind"}).on("mouseout", function() {
                $(this).hide();
            });
        })
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

    initialize_hardcopy_noise_form: function () {
        $(".noise #hardcopy-texts").on("change", function () {
            var txt = $("#hardcopy_heading").text() + "<br/>" + $("option:selected", this).text();
            $(".noise #hardcopy-text-div").html(txt);
        });

        $(".noise .hardcopy_noise").on("click", function (e) {
            e.preventDefault();
            $("#hardcopy_body").val($("#hardcopy-text-div").text());

            $("#printme #pr-rcpt").html($("#hardcopy_rcpt").html());
            $("#printme #pr-body").html($("#hardcopy-text-div").html());
            $("#printme #pr-firstname").text($("#hardcopy_noise_form #firstname").val());
            $("#printme #pr-lastname").text($("#hardcopy_noise_form #lastname").val());
            $("#printme #pr-address").text($("#hardcopy_noise_form #address").val());
            $("#printme #pr-zipcode").text($("#hardcopy_noise_form #zipcode").val());
            $("#printme #pr-city").text($("#hardcopy_noise_form #city").val());
            $("#printme #pr-phonenumber").text($("#hardcopy_noise_form #phonenumber").val());

            $("#hardcopy_noise_form").submit();

            if( $("#hardcopy_noise_form .error").length + $("#hardcopy_noise_form .constraint-violation").not(".irrelevant").length == 0 ) {
                window.print();
            }

        });
    },

    initialize_twitter_noise_form: function () {

        $(".noise #twitter-texts").on("change", function () {

            var txt = $(".noise #tweet-text-div").text();
            var url = "";
            if (txt.indexOf("http") != -1) {
                url = txt.match(/http[^\s]* /) + " ";
            }

            $(".noise #tweet-text-div").text("." + $("#twitter_rcpt").text() + " " + $("option:selected", this).text() + url);
            $('#tweet-text-div').trigger("keyup");
        });

        $(".noise .images .clickable-image").on("click", function (e) {

            e.preventDefault();
            var txt = $("#tweet-text-div").text();
            var url = $(this).find("img").attr("src").replace("/image_thumb", "");

            if (txt.indexOf("http") != -1) {
                txt = txt.replace(/http[^\s]* /, url + " ");
                $("#tweet-text-div").text(txt);
            } else {
                $("#tweet-text-div").text(txt + url + " ");
            }
            $('#tweet-text-div').trigger("keyup");
        });

        $('#tweet-text-div').on("keyup", function () {

            var txt = $(this).text();
            var url = txt.match(/http[^\s\n]*/) + " ";
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

            $("#tweet-counter").text(120 - tweet_length);
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

            // Trigger change event when trying to submit
            $("#twitter_noise_form .required input, #twitter_noise_form .required select").each(function() {
                $(this).trigger("change");
            });

            // Compose the tweet if there are no errors
            if( ($("#twitter_noise_form .error").length + $("#twitter_noise_form .constraint-violation").not(".irrelevant").length) == 0 ) {
                $("#tweet-text").val($("#tweet-text-div").text().substring(0, 119) + " " + $("#absolute_url").text());
                $(this).attr("href", "https://twitter.com/intent/tweet?text=" + $("#tweet-text").val());
            } else {
                e.preventDefault();
            }
        });
    },

    initialize_tabs: function () {
        $(".noise-menu a").click(function (event) {
            event.preventDefault();
            $(this).parent().addClass("current");
            $(this).parent().siblings().removeClass("current");
            var tab = $(this).attr("href");
            $(".tab-content").not(tab).parent().css("display", "none");
            $(tab).fadeIn();
        });
    },

    initialize_readmore: function () {

        $("#noise-container a.readmore").on("click", function (e) {
            e.preventDefault();
            var noise_body = $(this).parent().find(".noise-body");
            noise_body.animate({"height": noise_body[0].scrollHeight}).css("background", "none");
            $(this).fadeOut();
        });
    }
};

$(document).ready(function () {

    noise.initialize_noise_form();
    noise.initialize_twitter_noise_form();
    noise.initialize_twitter_web_intent();
    noise.initialize_email_noise_form();
    noise.initialize_hardcopy_noise_form();
    noise.initialize_tabs();
    noise.initialize_readmore();
});