$(function(){
    $('[data-toggle="tooltip"]').tooltip();

    initElems($('body'));
});


(function( $ ) {
    function loadResults(resultsContainer, url){
        if (url == null || url == '' || url.startsWith('#')){
            return;
        }
        resultsContainer.addClass('loading-container');
        $.get(url, {}, function(data){
            resultsContainer.find('.results').html(data);
            resultsContainer.find('[data-toggle="tooltip"]').tooltip();
            resultsContainer.find(".link-row").click(function() {
                window.location = $(this).data("href");
            });
            resultsContainer.removeClass('loading-container');
            var preserveHistory = resultsContainer.attr('data-preservehistory');
            if (!preserveHistory || preserveHistory != 'true')
                window.history.replaceState({}, '', url);
        });
    }

    $.fn.ajaxLoader = function( url_or_action ) {
        var self = this;

        if ( url_or_action != null) {

            if (url_or_action === 'reload'){
                var current = self.find('.pagination .page-item.active > a').attr('href');
                loadResults(self, current);
                return self;
            }

            loadResults(self, url);
            return self;
        }

        var initialUrl = self.attr('data-initial');
        if ((initialUrl != null) && (initialUrl!='')){
            loadResults(self, initialUrl);
        }

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url);
        });

    };

     $.fn.ajaxFilter = function() {
        var self = this;
        var resultsTarget = self.attr('data-results') || '#results';
        var resultsContainer = $(resultsTarget);
        var initialUrl = resultsContainer.attr('data-initial');
        var filterUrl = ((initialUrl != null) && (initialUrl!=''))? initialUrl : '' + '?';

        self.on('submit', function(e){
            e.preventDefault();
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query)
        });

        self.on('change', 'select', function(e){
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query);
        });

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url);
        });

    };

}( jQuery ));

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function initDatePicker(container){
    var datePickerFormat = 'YYYY-MM-DD';
	container.find('.date-picker-selector').each(function(){
		var picker = $(this);
        var dropDirection = picker.attr('data-drop') || 'down';
        options = {
			cancelClass: 'btn-flat text-primary',
			applyClass: 'btn-light', drops:dropDirection,
			locale:{
				format:datePickerFormat,
				cancelLabel: 'Clear'
			}
		};

		if (picker.hasClass('single')){
		    options['singleDatePicker'] = true;
		    picker.daterangepicker(options);
		}
        else{
            options['autoUpdateInput'] = false;
            var startDate = picker.find('input[name="start_date"]');
            var endDate = picker.find('input[name="end_date"]');
            var dropDirection = picker.attr('data-drop');

            if (startDate.val()){
                options['startDate'] = startDate.val();
                startDate.val(moment(startDate.val(), datePickerFormat).format(datePickerFormat));
            }
            if (endDate.val()){
                options['endDate'] = endDate.val();
                endDate.val(moment(endDate.val(), datePickerFormat).format(datePickerFormat));
            }
            var daterange = picker.find('.daterange').daterangepicker(options, function(start, end, label){
                startDate.val(start.format(datePickerFormat));
                endDate.val(end.format(datePickerFormat));

            });
            picker.on('apply.daterangepicker', function(ev, picker) {
                  'from' + daterange.val(picker.startDate.format(datePickerFormat) + ' -- ' + picker.endDate.format(datePickerFormat));
            });

            picker.on('cancel.daterangepicker', function(ev, picker) {
                picker.setStartDate({})
                picker.setEndDate({})
                'from' + daterange.val('');
            });

            if (startDate.val() || endDate.val()){
                daterange.val(startDate.val() + ' -- ' + endDate.val())
            }

            picker.find('button').on('click', function(){ daterange.focus(); });
        }

	});
}

function initElems(container){
    container.find('.floating-label .form-control').floatinglabel();
    container.find('.show-at-load').modal('show');
    container.find('.datepicker').pickdate();
    container.find('.ajax-load').ajaxLoader();
    container.find('.ajax-filter').ajaxFilter();

    initDatePicker(container);

    container.find('[data-toggle="tooltip"]').tooltip();

    container.find(".link-row").click(function(e) {
        var target = $(e.target);
        if (!target.is('button') && !target.parents('button').length && !target.is('a') && !target.parents('a').length){
            window.location = $(this).data("href");
        }

    });


    container.find('.color-widget').each(function(){
        $(this).wrap('<div class="color-container"></div>').spectrum({ preferredFormat: "hex"}).show();
    });

    container.find('.enhanced-select').each(function(){
        var control = $(this);
        var select = control.find('select').addClass('form-control');
        control.find('.tags_declaration > li').each(function(){
            var tag = $(this);
            select.find('option[value="' + tag.attr('data-pk') + '"]').attr('data-color', tag.attr('data-color'));
        })

        select.select2({
            dropdownAutoWidth: true,
            templateResult: function formatSelect(tag){
                var selected = select.find('option[value="' + tag.id + '"]')
                var color = selected.attr('data-color');
                if (color){
                    return $('<span class="tag-bulleted"></span>').text(tag.text).prepend($('<span></span>').css('background-color', color));
                }

                var image = selected.attr('data-image');
                if (image){
                    return $('<span class="tag-image"></span>').text(tag.text).prepend($('<div class="profile-circle"><img src="'+image+'"></div>').css('background-color', color));
                }
            },
            templateSelection: function formatTag(tag){
                var color = select.find('option[value="' + tag.id + '"]').attr('data-color');
                if (color)
                    return $('<span class="tag-selected"></span>').text(tag.text).css('background-color', color);
                else return tag.text;
            }
        });

        control.find('.select2').addClass('form-control input-group').css('width','100%').css('height','auto');
        control.find('.select2-search__field').css('width', '100%');
        setTimeout( function(){ control.css('width', '500px;'); }, 200);
   });
}

function showToast(message, messageClasses){
    var toast = $('<div class="toast"></div>').text(message).addClass(messageClasses);
    toast.appendTo('#main-toasts');
    setTimeout(function(){ toast.fadeOut(); }, TOAST_DELAY);
}
