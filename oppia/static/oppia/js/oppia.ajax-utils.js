function getCookieValue(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

$.postWithCSRF = function postWithCSRF(url, data, callback){

    var csrfToken = getCookieValue('csrftoken');
    return $.ajax({
        type: "POST",
        url : url,
        data: data,
        beforeSend: function(xhr) { xhr.setRequestHeader("X-CSRFToken", csrfToken); },
        success: callback
    });
};
