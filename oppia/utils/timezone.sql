UPDATE oppia_tracker SET 
submitted_date = CONVERT_TZ( submitted_date, 'GMT', 'UTC' ) ,
tracker_date = CONVERT_TZ( tracker_date, 'GMT', 'UTC' );

 