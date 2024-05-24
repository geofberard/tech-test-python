$(document).ready(function () {
  var currentFocus;

  $("#city-search-input").on("input", function (e) {
    var query = $(this).val();

    $('#city-search-submit').prop("disabled", true);
    $("#city-search-id").val("");

    if (!query) { return false; }

    currentFocus = -1;

    if (!$("#city-search-list").length) {
      $('body').append('<div id="city-search-list" class="autocomplete-items"></div>');
      $("#city-search-list").css("bottom", window.innerHeight - $("#city-search-input").offset().top + "px");
      $("#city-search-list").css("left", $("#city-search-input").offset().left + "px");
      $("#city-search-list").css("width", $("#city-search-input").outerWidth() + "px");
    }

    $.ajax({
      url: "/api/cities/search?name=" + query,
      success: function (data) {
        closeAllLists();
        data.forEach(function (city) {
          var name = city.name + " (" + city.admin_code + ")";
          var b = $("<div></div>")
            .html(name)
            .on("click", function (e) {
              $("#city-search-input").val(name);
              $("#city-search-id").val(city.id);
              $('#city-search-submit').removeAttr("disabled");
              $("#city-search-submit").focus();
              closeAllLists();
            });
          $("#city-search-list").append(b);
        });
      }
    });

  });

  $("#city-search-input").on("keydown", function (e) {
    var autocompleteItems = $("#city-search-list").find("div");
    if (e.keyCode === 40) {
      currentFocus++;
      addActive(autocompleteItems);
    } else if (e.keyCode === 38) {
      currentFocus--;
      addActive(autocompleteItems);
    } else if (e.keyCode === 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        autocompleteItems.eq(currentFocus).click();
      }
    }
  });

  function addActive(autocompleteItems) {
    removeActive(autocompleteItems);
    if (currentFocus >= autocompleteItems.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (autocompleteItems.length - 1);
    autocompleteItems.eq(currentFocus).addClass("autocomplete-active");
  }

  function removeActive(autocompleteItems) {
    autocompleteItems.removeClass("autocomplete-active");
  }

  function closeAllLists() {
    if ($("#city-search-list").length) {
      $("#city-search-list").empty();
    }
  }

});