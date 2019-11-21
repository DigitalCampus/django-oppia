$(function(){
    $('[data-toggle="tooltip"]').tooltip();
    if ($('.device-lg').css('display') == 'block'){
        $('.navdrawer-persistent-lg').navdrawer('show')
    }

    var datePickerFormat = 'YYYY-MM-DD';
	$('.date-picker-selector').each(function(){
		var picker = $(this);
        var dropDirection = picker.attr('data-drop') || 'down';
        options = {
			cancelClass: 'btn-flat text-primary',
			applyClass: 'btn-light', drops:dropDirection,
			autoApply: true,
			locale:{
				format:datePickerFormat
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
            daterange.on('apply.daterangepicker', function(ev, picker) {
                  'from' + $(this).val(picker.startDate.format(datePickerFormat) + ' -- ' + picker.endDate.format(datePickerFormat));
            });

            if (startDate.val() || endDate.val()){
                daterange.val(startDate.val() + ' -- ' + endDate.val())
            }

            picker.find('button').on('click', function(){ daterange.focus(); });
        }


	});

});