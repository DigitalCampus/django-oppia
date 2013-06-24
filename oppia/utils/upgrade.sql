-- script to migrate from previous version of mquiz.oppia to current version

INSERT INTO oppia_course SELECT * FROM learning_modules_module;
INSERT INTO oppia_section SELECT * FROM learning_modules_section;  
INSERT INTO oppia_activity SELECT * FROM learning_modules_activity;
INSERT INTO oppia_media SELECT * FROM learning_modules_media;
INSERT INTO oppia_tag SELECT * FROM learning_modules_tag;
INSERT INTO oppia_coursetag SELECT * FROM learning_modules_moduletag;
INSERT INTO oppia_coursedownload SELECT * FROM learning_modules_moduledownload;
INSERT INTO oppia_schedule SELECT * FROM learning_modules_schedule;
INSERT INTO oppia_activityschedule SELECT * FROM learning_modules_activityschedule;
INSERT INTO oppia_cohort SELECT * FROM learning_modules_cohort;
INSERT INTO oppia_participant SELECT * FROM learning_modules_participant;
INSERT INTO oppia_message SELECT * FROM learning_modules_message;
INSERT INTO oppia_tracker SELECT * FROM learning_modules_tracker;

INSERT INTO oppia_points (id, user_id, points,date,description,data,type,course_id,cohort_id) SELECT id, user_id, points,date,description,data,type,module_id,cohort_id FROM badges_points;
INSERT INTO oppia_badge SELECT * FROM badges_badge;
INSERT INTO oppia_award SELECT * FROM badges_award;
INSERT INTO oppia_awardcourse SELECT * FROM badges_awardmodule;

INSERT INTO quiz_quiz SELECT * FROM mquiz_quiz;
INSERT INTO quiz_quizprops SELECT * FROM mquiz_quizprops;
INSERT INTO quiz_question SELECT * FROM mquiz_question;
INSERT INTO quiz_questionprops SELECT * FROM mquiz_questionprops;
INSERT INTO quiz_response SELECT * FROM mquiz_response;
INSERT INTO quiz_responseprops SELECT * FROM mquiz_responseprops;
INSERT INTO quiz_quizquestion SELECT * FROM mquiz_quizquestion;
INSERT INTO quiz_quizattempt SELECT * FROM mquiz_quizattempt;
INSERT INTO quiz_quizattemptresponse SELECT * FROM mquiz_quizattemptresponse;