$(function(){
    $('[data-toggle="tooltip"]').tooltip();

    var datePickerFormat = 'YYYY-MM-DD';
	$('.date-picker-selector').each(function(){
		var picker = $(this);
        var dropDirection = picker.attr('data-drop') || 'down';
        options = {
			cancelClass: 'btn-flat text-primary',
			applyClass: 'btn-light', drops:dropDirection,
			locale:{
				format:datePickerFormat
			}
		};

		if (picker.hasClass('single')){
		    options['singleDatePicker'] = true;
		    picker.daterangepicker(options);

		}
        else{
            var startDate = picker.find('input[name="start_date"]');
            var endDate = picker.find('input[name="end_date"]');
            var dropDirection = picker.attr('data-drop');

            if (startDate.val()){ options['startDate'] = startDate.val(); }
            if (endDate.val()){ options['endDate'] = endDate.val(); }

            startDate.val(moment(startDate.val(), datePickerFormat).format(datePickerFormat));
            endDate.val(moment(endDate.val(), datePickerFormat).format(datePickerFormat));

            var daterange = picker.find('.daterange').daterangepicker(options, function(start, end, label){
                startDate.val(start.format(datePickerFormat));
                endDate.val(end.format(datePickerFormat));
            });

            picker.find('button').on('click', function(){ daterange.focus(); });
        }


	});

});