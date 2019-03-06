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

function applySelectableBehaviour(selectable){

    function updateUserBtn(container, username_or_btn, enable){
        var btn;
        if (username_or_btn instanceof jQuery)
            btn = username_or_btn;
        else
            btn = container.find('[data-selectable-id="'+username_or_btn+'"] .btn-add');
        btn.toggleClass('disabled', enable)
            .find('.fa-check-circle').toggleClass('hidden', (!enable)).end()
            .find('.fa-plus').toggleClass('hidden', enable).end();
    }

    function updateSelectableItems(){

        var items = selectedItems.children();
        if (items.length > 0)
            //Update any user that is already added
            items.each(function(i, user){
                var selected = $(user).attr('data-selectable-id');
                updateUserBtn(availableItems, selected, true);
            });
        else{
            selectedTable.hide();
            explanation.show();
        }

    }

    var group;
    if (selectable instanceof HTMLElement) group = $(selectable);
    else if (selectable instanceof jQuery) group = selectable;
    else group = $(this);
    if(!group) return;

    var explanation = group.find('.explanation');
    var selectedTable = group.find('.selected-items-table');
    var availableItems = group.find('.available-items');
    var selectedItems = group.find('.selected-items');

    updateSelectableItems();

    availableItems.on('click', '.btn-add', function(){
        var btn = $(this);
        var itemRow = btn.parents('tr').first();
        if (btn.hasClass('disabled')) return;

        itemRow.clone().attr('data-selectable-id', itemRow.attr('data-selectable-id'))
            .removeAttr('id')
            .appendTo(selectedItems)
            .find('.btn-add').hide().end()
            .find('.removing').show();

        updateUserBtn(availableItems, btn, true);
        selectedTable.show();
        explanation.hide();
    });

    availableItems.on('click', '.pagination a, thead a', function(e){
        e.preventDefault();
        $.get(this.href, function(page){
            availableItems.html($(page));
            updateSelectableItems();
        });
    });

    selectedItems.on('click', '.btn-remove', function(){
        var selectedItem = $(this).parents('tr').first().remove();
        updateUserBtn(availableItems, selectedItem.attr('data-selectable-id'), false);
        updateSelectableItems();
    });
}

function getSelectableItemsSelected(selectable){
    var group;
    var results = [];
    if (selectable instanceof HTMLElement) group = $(selectable);
    else if (selectable instanceof jQuery) group = selectable;
    else group = $(this);
    if(!group) return results;

    var selectedItems = group.find('.selected-items');
    if (selectedItems.length > 0) group = selectedItems;

    return group
        .find('[data-selectable-id]')
        .map(function(){ return $(this).attr('data-selectable-id')}).get();

}