var Q = null;
var mQ = new mQuiz();

function mQuiz(){
	this.inQuiz = false;
	this.opts = {};
	this.onLogin = function(){};
	this.onLogout = function(){
		mQ.showPage("#login");
	};
	this.onRegister = function(){
		mQ.dataUpdate();
		var hash = $(location).attr('hash');
		mQ.showPage(hash);
	};
	this.store = null;
	
	this.initStore = function(){
		this.store = new Store();
		this.store.init();
	}
	
	this.init = function(opts){
		this.opts = opts;
		this.initStore();
		if(!this.opts.url){
			this.opts.url = "../api/v1/";
		}
		if(!this.opts.timeout){
			this.opts.timeout = 60000;
		}
		if(!this.opts.cacheexpire){
			this.opts.cacheexpire = 60;
		}
		this.showUsername();
		this.dataUpdate();
	}
	
	this.confirmExitQuiz = function(page){
		if(mQ.inQuiz){
			var endQuiz = confirm("Are you sure you want to leave this quiz?");
			if(endQuiz){
				mQ.inQuiz = false;
			} else {
				return;
			}
		}
		if (this.opts.home){
			document.location = this.opts.home;
		} else {
			document.location = '../';
		}
		
	};
	
	this.loadQuiz = function(id){
		
		$('#mq').empty();
		mQ.showLoading('quiz');
		
		// load from server
		$.ajax({
				url:this.opts.url + "quiz/"+id+"/",
			   	data:{'username':mQ.store.get('username'),'api_key':mQ.store.get('api_key')}, 
			   	success:function(data){
				   //save to local cache and then load
				   mQ.store.addArrayItem('quizzes', data);
				   mQ.showQuiz(id);
			   }, 
			   error:function(data,status){
				   // find if this quiz is already in the cache
				   var quiz = mQ.quizInCache(id);
				   if (quiz){
					   mQ.showQuiz(id);
				   } else {
					   alert("Quiz could not be loaded, please check your connection.");
					   document.location = "#select";
				   }
				   
			   }
			});
	};
	
	this.showRegister = function(){
		$('#mq').empty();
		var str = "<h2>Register";
		if(this.opts.allowregister){
			str += " (or <a href='#login' onclick='mQ.showLogin();'>Login</a>)";
		}
		str += "</h2>";
		$('#mq').append(str);
		var l = $('<div>').attr({'id':'loading'}).html("Registering...");
		$('#mq').append(l);
		l.hide();
		var form =  $('<form>').attr({'id':'register'});
		form.append("<div class='formblock'>" +
				"<div class='formlabel'>Username:</div>" +
				"<div class='formfield'><input type='text' name='username' id='username'></input></div>" +
				"</div>");
		form.append("<div class='formblock'>" +
			"<div class='formlabel'>Email address:</div>" +
			"<div class='formfield'><input type='text' name='email' id='email'></input></div>" +
			"</div>");
		form.append("<div class='formblock'>" +
				"<div class='formlabel'>Password:</div>" +
				"<div class='formfield'><input type='password' name='password' id='password'></input></div>" +
				"</div>");
		form.append("<div class='formblock'>" +
				"<div class='formlabel'>Password (confirm):</div>" +
				"<div class='formfield'><input type='password' name='passwordagain' id='passwordagain'></input></div>" +
				"</div>");
		form.append("<div class='formblock'>" +
				"<div class='formlabel'>First name:</div>" +
				"<div class='formfield'><input type='text' name='firstname' id='firstname'></input></div>" +
				"</div>");
		form.append("<div class='formblock'>" +
				"<div class='formlabel'>Surname:</div>" +
				"<div class='formfield'><input type='text' name='lastname' id='lastname'></input></div>" +
				"</div>");
		form.append("<div class='ctrl'><input type='button' name='submit' value='Register' onclick='mQ.register()' class='button'></input></div>");
		$('#mq').append(form);
		//data validation
		$('#register').validate({
			rules: {
				username: {
					required: true,
					minlength: 6
				},
				email: {
					required: true,
					email:true
				},
				password: {
					required: true,
					minlength: 6
				},
				passwordagain: {
					required: true,
					minlength: 6
				},
				firstname: {
					required: true
				},
				lastname: {
					required: true
				}
			}
			
		});
	};
	
	this.showHome = function(){
		$('#mq').empty();
		
		mQ.showMenu();
		
		var searchform = $('<div>').attr({'id':'searchform'});
		searchform.append($('<div>').attr({'id':'searchtitle'}).text("Search quizzes:"));
		var ff = $('<div>').attr({'class':'search'});
		var sterms = $('<input>').attr({'id':'searchterms'});
		var sbtn = $('<input>').attr({'type':'button','id':'searchbtn','value':'Go'});
		sbtn.click(function(){
				mQ.doSearch();
			});
		ff.append(sterms);
		ff.append(sbtn);
		searchform.append(ff);
		$('#mq').append(searchform);
		
		var searchresults = $('<div>').attr({'id':'searchresults','class':'formblock'}); 
		$('#mq').append(searchresults);
		
		
		this.updateSuggest();
		
		$('#searchterms').keypress(function (event) {
				if (event.keyCode == '13'){
					mQ.doSearch();
				}
			});
	};

	this.updateSuggest = function(){
		var suggest = $('<div>').attr({'id':'suggest','class':'formblock'});
		suggest.append($('<div>').attr({'id':'suggesttitle','class':'formlabel'}).text("or try one of these:"));
		$('#mq').append(suggest);
		var suggestresults = $('<div>').attr({'id':'suggestresults','class':'formblock'}); 
		$('#mq').append(suggestresults);
		
		var url = mQ.opts.url + "quiz/?limit=10&username=" + mQ.store.get('username') + "&api_key=" + mQ.store.get('api_key');
		$.ajax({
			type: "GET",
			timeout: mQ.opts.timeout,
			url: url,
			success:function(data){
				if(data){
					for(var q in data.quizzes){		   
						mQ.addQuizListItem(data.quizzes[q],'#suggestresults');
						mQ.cacheQuiz(data.quizzes[q]);
				   }
				}
			}, 
			error:function(data){ 
				// TODO - what should be displayed if suggestions don't load? (no connection?)
			}
		});	
	};
	
	this.showLocalQuizzes = function(){
		$('#mq').empty();
		mQ.showMenu();
		var localQuizzes = $('<div>').attr({'id':'localq'}); 
		if(this.opts.lang){
			localQuizzes.append(this.opts.lang.en.localquiz.title);
		}
		$('#mq').append(localQuizzes);
		var qs = mQ.store.get('quizzes');
		for (var q in qs){
			mQ.addQuizListItem(qs[q],'#localq');
		}
		if(!qs || qs.length == 0){
			$(localQuizzes).append("<br/>No quizzes");
		}
	};
	
	this.showLogin = function(hash){
		$('#mq').empty();
		var str = "<h2>Login";
		if(this.opts.allowregister){
			str += " (or <a href='#register' onclick='mQ.showRegister();'>Register</a>)";
		}
		str += "</h2>";
		$('#mq').append(str);
		var msg = $('<div>').attr({'id':'msg'});
		$('#mq').append(msg);
		msg.hide();
		var form = $('<form>')
		form.append("<div class='formblock'>" +
			"<div class='formlabel' name='lang' id='login_username'>Username:</div>" +
			"<div class='formfield'><input type='text' name='username' id='username'></input></div>" +
			"</div>");
		
		form.append("<div class='formblock'>"+
			"<div class='formlabel'name='lang' id='login_password'>Password:</div>" +
			"<div class='formfield'><input type='password' name='password' id='password'></input></div>" +
			"</div>");
		
		form.append("<div class='ctrl'><input type='button' name='submit' value='Login' class='button' id='loginbtn' onclick='mQ.login()'></input></div>");
		$('#mq').append(form);
	};
	
	this.showMenu = function(){
		if( this.opts.menu){
			var menu = $('#menu');
			if(menu.length == 0){
				menu = $('<div>').attr({'id':'menu'});
				$('#mq').append(menu);
			}
			menu.empty();
			for(var i=0;i < this.opts.menu.length;i++){
				menu.append($('<a>').attr({'href':this.opts.menu[i].link}).text(this.opts.menu[i].title));
				if( i+1 < this.opts.menu.length){
					menu.append(' | ');
				}
			}
		}
	};
	
	this.showQuiz = function(qref){
		$('#mq').empty();
		Q = new Quiz();
		Q.init(mQ.quizInCache(qref));
		
		var qhead = $('<div>').attr({'id':'quizheader'});
		$('#mq').append(qhead);
		
		var qs = $('<div>').attr({'id':'qs'});
		$('#mq').append(qs);
		
		var question = $('<div>').attr({'id':'question'});
		$('#qs').append(question);
		
		var notify = $('<div>').attr({'id':'notify','class':'warn'});
		$('#qs').append(notify);
		notify.hide();
		
		var response = $('<div>').attr({'id':'response'});
		$('#qs').append(response);
		
		var fb = $('<div>').attr({'id':'feedback'});
		$('#qs').append(fb);
		fb.hide();
		
		var quiznav = $('<div>').attr({'id':'quiznav'});
		
		var quiznavprev = $('<div>').attr({'id':'quiznavprev','tabindex':'0'}).html("&lt;&lt; Prev");
		quiznav.append(quiznavprev);
		
		var quiznavnext = $('<div>').attr({'id':'quiznavnext','tabindex':'0'}).html('Next &gt;&gt;');
		quiznav.append(quiznavnext);
		
		var clear = $('<div>').attr({'style':'clear:both'});
		quiznav.append(clear);
		
		$('#mq').append(quiznav);
		Q.loadQuestion();
	};
	
	this.login = function(hash){
		$('#msg').empty();
		$('#msg').show();
		var reqData = {};
		reqData.username = $('#username').val();
		reqData.password = $('#password').val();
		if(reqData.username == '' || reqData.password == ''){
			$('#msg').append("<span class='warn'>Please enter your username and password</span>");
			return false;
		}
		$('#msg').append("Logging in...");
		$('#username').attr('disabled','disabled');
		$('#password').attr('disabled','disabled');
		$('#loginbtn').attr('disabled','disabled');
		$.ajax({
				type: "POST",
	            contentType: "application/json; charset=utf-8",
	            data: JSON.stringify(reqData),
				timeout: this.opts.timeout,
				url: this.opts.url + "user/",
				success:function(data){
					mQ.store.set('username', reqData.username);
					mQ.store.set('displayname',data.first_name + " " + data.last_name);
					mQ.store.set('api_key',data.api_key);
					mQ.store.set('points',data.points);
					mQ.store.set('badges',data.badges);
					mQ.showUsername();
					mQ.onRegister();
				},
				statusCode: {
				    400: function(xhr) {
				    	$('#username').removeAttr('disabled');
						$('#password').removeAttr('disabled');
						$('#loginbtn').removeAttr('disabled');
						$('#msg').empty();
						$('#msg').append("<span class='warn'>"+xhr.responseText+"</span>");
				    }
				  },
				error:function(data){
					$('#username').removeAttr('disabled');
					$('#password').removeAttr('disabled');
					$('#loginbtn').removeAttr('disabled');
					$('#msg').empty();
					$('#msg').append("<span class='warn'>Connection error. Please check your internet connection, you need to be online to log in.</span>");
				}
			});
		return false;
	};
	
	this.logout = function(){
		var lo = confirm('Are you sure you want to log out?\n\nYou will need an active connection to log in again.');
		if(lo){
			mQ.inQuiz = false;
			mQ.store.clear();
			mQ.store.init();
			// send logout request to main site
			var url = this.opts.url + "../../profile/logout/";
			$.ajax({
				type: "GET",
				timeout: mQ.opts.timeout,
				url: url,
				success:function(data){
					$('#mquiz_username').val('');
					$('#mquiz_api_key').val('');
					mQ.showUsername();
					mQ.onLogout();
				}, 
				error:function(data){ 
					$('#mquiz_username').val('');
					$('#mquiz_api_key').val('');
					mQ.showUsername();
					mQ.onLogout();
				}
			});
		}
	};

	this.showPage = function(hash){
		if(!hash){
			hash = '#home';
		}
		var loggedin = mQ.loggedIn();
		if(!loggedin && hash != '#register' && hash != "#login"){
			this.showLogin(hash);
			return;
		} 
		$('#mq').empty();
		if (hash == '#register' && !loggedin){
			mQ.showRegister();
		} else if (hash == '#login' && !loggedin){
			this.showLogin();
		} else if($.isNumeric(hash.substring(1))){
			mQ.loadQuiz(hash.substring(1));
		} else if (hash == '#quizzes'){
			mQ.showLocalQuizzes();
		} else if (hash == '#results'){
			mQ.showResults();
		}  else {
			this.inQuiz = false;
			this.showHome();
		}
	};
	
	this.showResults = function(){
		$('#mq').empty();
		
		mQ.showMenu();
		var results = $('<div>').attr({'id':'results'}); 
		$('#mq').append(results);
		var qs = mQ.store.get('results');

		if(qs && qs.length>0){
			var result = $('<div>').attr({'class':'th'});
			result.append($('<div>').attr({'class':'thrt'}).text("Quiz"));
			result.append($('<div>').attr({'class':'thrs'}).text("Score"));
			result.append($('<div>').attr({'class':'thrr'}).text("Rank"));
			result.append("<div style='clear:both'></div>");
			results.append(result);
		} else {
			results.append("You haven't taken any quizzes yet");
			return;
		}
		qs.sort(sortresults);
		for (var q in qs){
			var q_result = $('<div>').attr({'class':'result'});
			var d = new Date(qs[q].attempt_date);
			var str = qs[q].title + "<br/><small>"+ dateFormat(d,'HH:MM d-mmm-yy')+"</small>";
			result.append($('<div>').attr({'class':'rest clickable','onclick':'document.location="#'+qs[q].quiz_id +'"','title':'try this quiz again'}).html(str));
			result.append($('<div>').attr({'class':'ress'}).text((qs[q].score*100/qs[q].maxscore).toFixed(0)+"%"));
			result.append($('<div>').attr({'class':'resr'}).text(qs[q].rank));
			result.append("<div style='clear:both'></div>");
			results.append(q_result);
		}
	};
	
	this.doSearch = function(){
		var q = $('#searchterms').val().trim();
		if(q.length > 1){
			$('#searchresults').text('Searching...');
			var url = mQ.opts.url + "quiz/search/?q="+q+"&limit=10&username=" + mQ.store.get('username') + "&api_key=" + mQ.store.get('api_key');
			$.ajax({
				type: "GET",
				timeout: mQ.opts.timeout,
				url: url,
				success:function(data){
					$('#searchresults').empty();
					if(data.quizzes && data.quizzes.length>0){
						for(var q in data.quizzes){		   
							mQ.addQuizListItem(data.quizzes[q],'#searchresults');
							mQ.cacheQuiz(data.quizzes[q]);
					   }
					} else {
						$('#searchresults').append("No results found");
					}
				}, 
				error:function(data){ 
					$('#searchresults').empty();
					$('#searchresults').append("Error or timeout in connection, please check you internet connection.");
				}
			});	
		}
	};
	
	this.showLoading = function(msg){
		var l = $('<div>').attr({'id':'loading'}).html("Loading "+msg+"...");
		$('#mq').append(l);
	};

	this.loggedIn = function(){
		if(mQ.store.get('username') == null || mQ.store.get('username') == ""){
			mQ.store.set('username',$('#mquiz_username').val());
			mQ.store.set('api_key',$('#mquiz_api_key').val());
			mQ.store.set('displayname',$('#mquiz_username').val());
			if(mQ.store.get('username') == null || mQ.store.get('username') == ""){
				return false;
			}
		} 
		return true;
	};
	
	this.track = function(obj){
		mQ.store.addArrayItem('tracker', obj);
	}
	
	this.dataUpdate = function(){
		if(!mQ.loggedIn()){
			return;
		}
		// check when last update made, return if too early
		var now = new Date();
		var lastupdate = new Date(mQ.store.get('lastupdate'));
		if(lastupdate > now.addMins(-this.opts.cacheexpire)){
			return;
		} 

		// send any unsubmitted responses
		var results = mQ.store.get('results');
		
		if(results){
			for(var r in results){
				if(results[r].sent == false){
					var url = mQ.opts.url + "quizattempt/?username=" + mQ.store.get('username') + "&api_key=" + mQ.store.get('api_key');
					$.ajax({
						type: "POST",
			            contentType: "application/json; charset=utf-8",
			            data: JSON.stringify(results[r]),
						timeout: mQ.opts.timeout,
						url: url,
						success:function(data){
								var cache = mQ.store.get('results');
								mQ.store.clearKey('results');
								
								results[r].sent = true;
								for (var c in cache){
									if(cache[c].quizdate == results[r].quizdate){
										mQ.store.addArrayItem('results', results[r]);
									} else {
										mQ.store.addArrayItem('results', cache[c]);
									}
								} 
								mQ.store.set('lastupdate',Date());
								mQ.store.set('points',data.points);
								mQ.store.set('badges',data.badges);
								mQ.showUsername();
								
						}, 
						error:function(data){ 
							// do nothing
						}
					});	
				}
			}
		}
	};
	
	this.cacheQuiz = function(quiz){
		var qs = mQ.store.get('quizzes');
		for(var q in qs){
			if (qs[q].id == quiz.id){
				return qs[q];
			}
		}
		mQ.store.addArrayItem('quizzes', quiz);
		return quiz;
	};
	
	this.register = function(){
		
		var postData = {};
		postData.username = $('#username').val();
		postData.email = $('#email').val();
		postData.password = $('#password').val();
		postData.passwordagain = $('#passwordagain').val();
		postData.firstname = $('#firstname').val();
		postData.lastname = $('#lastname').val();
		
		//check passwords match
		if(postData.password != postData.passwordagain){
			alert('Please check the passwords match');
			return;
		}
		
		if(!$('#register').valid()){
			alert('Please check you have fully completed the form');
			return;
		}
		
		$('#register').hide();
		
		$.ajax({
				type: "POST",
	            contentType: "application/json; charset=utf-8",
	            dataType: "json",
				timeout: this.opts.timeout,
				url: this.opts.url + "register/",
				data: JSON.stringify(postData), 
				success:function(data){
					// save username and password
					mQ.store.set('username',data.username);
					mQ.store.set('displayname',postData.firstname);
					mQ.store.set('api_key',data.api_key);
					mQ.store.set('points',data.points);
					mQ.store.set('badges',data.badges);
					mQ.showUsername();
					mQ.onRegister();		   
				}, 
				error:function(data){
					// TODO check the message gets displayed properly
					$('#loading').hide();
					$('#register').show();
				}
		});
		
		
	};
	
	this.showUsername = function(){
		$('#logininfo').empty();
		if(mQ.store.get('displayname') != null && mQ.store.get('displayname') != ""){
			$('#logininfo').text(mQ.store.get('displayname'));
			var points = $('<span>').attr({'class':'points'});
			points.text(mQ.store.get('points'));
			var badges = $('<span>').attr({'class':'badges'});
			var img = $('<img>').attr({'src':'/static/oppia/images/badge.png'});
			badges.append(img);
			badges.append(mQ.store.get('badges'));
		
			$('#logininfo').append(points);
			$('#logininfo').append(badges);
			$('#logininfo').append("<a onclick='mQ.logout()' name='lang' id='logout' href='#login'>Logout</a>");
		} 
	};
	
	this.addQuizListItem = function(q,list){
		var ql= $('<div>').attr({'class':'quizlist clickable','onclick':'document.location="#'+q.id +'"'});
		var quiz = $('<span>').attr({'class':'quiztitle'});
		quiz.append(q.title);
		$(list).append(ql.append(quiz));
		if(q.description != null && q.description != ""){
			var desc = $("<span>").attr({'class':'quizdesc'});
			desc.text(" - " + q.description);
			ql.append(desc);
		}
	};
	
	this.quizInCache = function(id){
		var qs = mQ.store.get('quizzes');
		for(var q in qs){
			if (qs[q].id == id){
				return qs[q];
			}
		}
		return false;
	};
}

function Store(){
	
	this.init = function(){
		if (!localStorage) {
			localStorage.setItem('username', null);
			localStorage.setItem('api_key', null);
			localStorage.setItem('quizzes', null);
			localStorage.setItem('results', null);
			localStorage.setItem('userlang', 'en');
			localStorage.setItem('points', 0);
			localStorage.setItem('badges', 0);
		}
	}
	
	this.get = function(key){
		var value = localStorage.getItem(key);
		try{
			return value && JSON.parse(value);
		} catch(err){
			return null;
		}
	}
	
	this.set = function(key,value){
		localStorage.setItem(key,JSON.stringify(value));
	}
	
	this.clear = function(){
		localStorage.clear();
	}
	
	this.clearKey = function(key){
		this.set(key,null);
	}
	
	this.addArrayItem = function(key,value){
		//get current array
		var c = this.get(key);
		//var count = 0;
		if(!c){
			c = [];
		} 
		c.unshift(value);
		this.set(key,c);
	}
	
}


function Quiz(){
	
	this.quiz = null;
	this.currentQuestion = 0;
	this.responses = [];
	this.matchingstate = [];
	this.matchingopt = [];
	this.feedback = "";
	this.opts = {};
	
	this.init = function(q,opts){
		this.quiz = q;
		mQ.inQuiz = true;
		this.opts = opts;
		if(this.quiz.props.randomselect){
			// generate a new question set
			this.quiz.questions = this.generateQuestionSet(q);
			//set the new max score
			var newMax = 0;
			for(var i=0; i<this.quiz.questions.length; i++){
				newMax += this.quiz.questions[i].question.props.maxscore;
			}
			this.quiz.props.maxscore = newMax;
		}
	}
	
	this.generateQuestionSet = function(q){
		var newQuestionSet = new Array();
		var setNo = 0;
		
		while(setNo < q.props.randomselect){
			var randomNum = Math.floor(Math.random() * q.questions.length);
			var found = false;
			//check if this question is already in the questions
			for(var i=0; i<newQuestionSet.length; i++){
				if (newQuestionSet[i].id == q.questions[randomNum].id){
					found = true;
				}
			}
			if(!found){
				newQuestionSet[setNo] = q.questions[randomNum];
				setNo++;
			}	
		}
		return newQuestionSet;
	}
	
	this.setHeader = function(){
		
		// find how many non-info questions there are
		var noquestions = this.quiz.questions.length;
		for(var q in this.quiz.questions){
			if(this.quiz.questions[q].question.type == 'info'){
				noquestions--;
			}
		}
		//check if current question is info one or not
		if(this.quiz.questions[this.currentQuestion].question.type == 'info'){
			$('#quizheader').html(this.quiz.title);
		} else {
			var currentq = 1;
			for(var q in this.quiz.questions){
				if(this.quiz.questions[q].question.type != 'info' && this.currentQuestion > q){
					currentq++;
				}
			}
			$('#quizheader').html(this.quiz.title + " Q" +currentq + " of "+ noquestions);
		}
	}
	
	this.loadNextQuestion = function(){
		if(this.saveResponse('next')){
			if(this.feedback != ""){
				$('#question').hide();
				$('#response').hide();
				$('#notify').hide();
				$('#notify').empty();
				$('#feedback').empty();
				$('#feedback').append("<h2>Feedback</h2><div id='fbtext'>"+this.feedback+"</div>");
				$('#feedback').show('blind',{},500);
				$('#quiznavnext').unbind('click');
				if(this.currentQuestion+1 == this.quiz.questions.length){
					$('#quiznavnext').bind('click',function(){
						Q.showResults();
					});
				} else {
					$('#quiznavnext').bind('click',function(){
						Q.currentQuestion++;
						Q.loadQuestion();
					});
				}
			} else {
				if(this.currentQuestion+1 == this.quiz.questions.length){
					Q.showResults();
				} else {
					this.currentQuestion++;
					this.loadQuestion();
				}
			}

		} else {
			$('#notify').text("Please answer this question before continuing.");
			$('#notify').show();
		}
	}
	
	this.loadPrevQuestion = function(){
		this.saveResponse('prev')
		this.currentQuestion--;
		this.loadQuestion();
	}
	
	this.loadQuestion = function(){
		this.setHeader();
		this.setNav();
		this.feedback = "";
			
		$('#question').html(this.quiz.questions[this.currentQuestion].question.title);
		this.loadResponses(this.quiz.questions[this.currentQuestion].question);
		$('#feedback').hide();
		$('#notify').empty();
		$('#notify').hide();
		$('#question').show('blind',{},500);
		$('#response').show('blind',{},500);
	}
	
	this.loadResponses = function(q){
		if(q.type == 'multichoice'){
			this.loadMultichoice(q.responses);
		} else if (q.type == 'shortanswer'){
			this.loadShortAnswer();
		} else if (q.type == 'matching'){
			this.loadMatching(q.responses);
		} else if (q.type == 'numerical'){
			this.loadNumerical(q.responses);
		} else if (q.type == 'essay'){
			this.loadEssay();
		} else if (q.type == 'multiselect'){
			this.loadMultiselect(q.responses);
		} else if (q.type == 'info'){
			this.loadInfo();
		} else {
			$('#response').empty();
		}
	}
	
	this.loadMultichoice = function(resp){
		$('#response').empty();
		
		$(function(){
			for(var i=0; i< resp.length; i++){
				(function(r){
					var d = $('<div>').attr({'class':'mcresponse','id':'div'+r.id}).click(function(event){
						$('#'+r.id).attr({'checked':'checked'});
						//remove class from all other responses
						var t = Q.quiz.questions[Q.currentQuestion].question.responses;
						for(var j in t){
							$('#div'+t[j].id).removeClass('selected');
						}
						$(this).addClass('selected');
					});
					var l = $('<label>').attr({'for':r.id});
					var o = $('<input>').attr({'type':'radio','value':r.id,'name':'response','id':r.id});
					if(Q.responses[Q.currentQuestion] && Q.responses[Q.currentQuestion].text == r.title){
						o.attr({'checked':'checked'});
						d.addClass('selected');
					}
					l.append(o);
					l.append(r.title);
					d.append(l);
					
					$('#response').append(d);
				})(resp[i]);
			}
		});
	}
	
	this.loadMultiselect = function(resp){
		$('#response').empty();
		
		$(function(){
			for(var i=0; i< resp.length; i++){
				(function(r){
					
					var od = $('<div>').attr({'class':'od','id':'div'+r.id});
					var mss = $('<div>').attr({'class':'mss'});
					var o = $('<input>').attr({'type':'checkbox','value':r.id,'name':'mcresponse','id':r.id});
					o.click(function(event){
						if ($('#'+r.id).is(':checked')) {
							$('#div'+r.id).addClass('selected');
					    } else {
					    	$('#div'+r.id).removeClass('selected');
					    }
					});
					mss.append(o);
					od.append(mss);
					
					var mst = $('<div>').attr({'class':'mst'}).text(r.title);
					mst.click(function(event){
						if ($('#'+r.id).is(':checked')) {
							$('#'+r.id).removeAttr('checked');
							$('#div'+r.id).removeClass('selected');
					    } else {
					    	$('#'+r.id).attr({'checked':'checked'});
					    	$('#div'+r.id).addClass('selected');
					    }
					});
					od.append(mst);
					od.append("<div style='clear:both'></div>");
					
					if(Q.responses[Q.currentQuestion]){
						var sel = Q.responses[Q.currentQuestion].text.split('||');
						for(var i in sel){
							if(sel[i] == r.title){
								o.attr({'checked':'checked'});
								od.addClass('selected');
							}
						}
					}					
					$('#response').append(od);
				})(resp[i]);
			}
		});
	}
	
	this.loadInfo = function(){
		$('#response').empty();
	}
	
	this.loadShortAnswer = function(){
		$('#response').empty();
		var o = $('<input>').attr({'type':'text','name':'response','id':'shortanswerresponse','class':'responsefield'});
		if(this.responses[this.currentQuestion]){
			o.attr({'value':this.responses[this.currentQuestion].text});
		}
		$('#response').append(o);
	}
	
	this.loadMatching = function(resp){
		$('#response').empty();
		
		this.matchingstate = [];
		this.matchingopt = [];
		for(var r in resp){
			var t = resp[r].title.split('|');
			if(t[0].trim() != ''){
				this.matchingstate[r] = t[0].trim();
			}
			if(t[1].trim() != ''){
				this.matchingopt[r] = t[1].trim();
			}
		}
		
		var curresp = [];
		if(this.responses[this.currentQuestion]){
			curresp = this.responses[this.currentQuestion].text.split('||');
		}
		for(var s in this.matchingstate){
			var d = $('<div>').attr({'class':'response'});
			var st = $('<span>').attr({'class':'matchingstate','name':'matching','id':'matchingstate'+s}).text(this.matchingstate[s]);
			d.append(st);
			
			var sel = $('<select>').attr({'class':'matchingopt','name':'matching','id':'matchingopt'+s}).append($('<option>'));
			for(var o in this.matchingopt){
				var ot = $('<option>').text(this.matchingopt[o]);
				// find if a current response for this answer
				for(var i in curresp){
					var r = curresp[i].split('|');
					if(r[0].trim() == this.matchingstate[s] && r[1].trim() == this.matchingopt[o]){
						ot.attr({'selected':'selected'});
					}
				}
				sel.append(ot);
			}
			d.append(sel);
			$('#response').append(d);
			$('#response').append('<div style="clear:both;"></div>');
		}
	}
	
	this.loadNumerical = function(){
		$('#response').empty();
		var o = $('<input>').attr({'type':'text','name':'response','id':'numericalresponse','class':'responsefield'});
		if(this.responses[this.currentQuestion]){
			o.attr({'value':this.responses[this.currentQuestion].text});
		}
		$('#response').append(o);
	}
	
	this.loadEssay = function(){
		$('#response').empty();
		var o = $('<textarea>').attr({'type':'text','name':'response','id':'essayresponse','class':'responsefield'});
		if(this.responses[this.currentQuestion]){
			o.text(this.responses[this.currentQuestion].text);
		}
		$('#response').append(o);
	}
	
	this.saveResponse = function(nav){
		var q = this.quiz.questions[this.currentQuestion].question;
		if(q.type == 'multichoice'){
			return this.saveMultichoice(nav);
		} else if(q.type == 'shortanswer'){
			return this.saveShortAnswer(nav);
		} else if(q.type == 'matching'){
			return this.saveMatching(nav);
		} else if(q.type == 'numerical'){
			return this.saveNumerical(nav);
		} else if(q.type == 'essay'){
			return this.saveEssay(nav);
		} else if(q.type == 'multiselect'){
			return this.saveMultiselect(nav);
		} else if(q.type == 'info'){
			return this.saveInfo(nav);
		} else {
			
		}
	}
	
	this.saveMultichoice = function(nav){
		var opt = $('input[name=response]:checked').val();
		if(opt){
			var o = Object();
			var q = this.quiz.questions[this.currentQuestion].question;
			o.question_id = q.id;
			o.score = 0;
			o.text = "";
			// mark question and get text
			for(var r in q.responses){
				if(q.responses[r].id == opt){
					o.score = q.responses[r].score;
					o.text = q.responses[r].title;
					// set feedback (if any)
					if (q.responses[r].props.feedback && q.responses[r].props.feedback != ''){
						this.feedback = q.responses[r].props.feedback;
					}
				}
			}
			o.score = Math.min(o.score,parseFloat(q.props.maxscore));
			this.responses[this.currentQuestion] = o;

			return true;
		} else {
			if(nav == 'next'){
				return false;
			} else {
				return true;
			}	
		}
	}
	
	this.saveShortAnswer = function(nav){
		var ans = $('#shortanswerresponse').val().trim();
		if(ans != ''){
			var o = Object();
			var q = this.quiz.questions[this.currentQuestion].question;
			o.question_id = q.id;
			o.score = 0;
			o.text = ans;
			// mark question and get text
			for(var r in q.responses){
				if(q.responses[r].title.toLowerCase() == ans.toLowerCase()){
					o.score = q.responses[r].score;
					// set feedback (if any)
					if (q.responses[r].props.feedback && q.responses[r].props.feedback != ''){
						this.feedback = q.responses[r].props.feedback;
					}
				}
			}
			o.score = Math.min(o.score,parseFloat(q.props.maxscore));
			this.responses[this.currentQuestion] = o;
			return true;
		} else {
			if(nav == 'next'){
				return false;
			} else {
				return true;
			}	
		}
	}
	
	this.saveInfo = function(nav){
		var o = Object();
		var q = this.quiz.questions[this.currentQuestion].question;
		o.question_id = q.id;
		o.score = 0;
		o.text = "";
		this.responses[this.currentQuestion] = o;
		return true;
	}
	
	this.saveMatching = function(nav){
		//check an answer given for all options
		for(var s in this.matchingstate){
			if($('#matchingopt'+s+' :selected').text() == ''){
				if(nav == 'next'){
					return false;
				} else {
					return true;
				}
			}
		}
		//now mark and save the answers
		var o = Object();
		var q = this.quiz.questions[this.currentQuestion].question;
		o.question_id = q.id;
		o.score = 0;
		o.text = '';
		for(var s in this.matchingstate){
			var resp = this.matchingstate[s] + "|" +  $('#matchingopt'+s+' :selected').text();
			for(var r in q.responses){
				if(q.responses[r].title == resp){
					o.score += parseFloat(q.responses[r].score);
				}
			}
			o.text += resp + "||";
			
		}
		o.score = Math.min(o.score,parseFloat(q.props.maxscore));
		this.responses[this.currentQuestion] = o;
		return true;
	}
	

	this.saveNumerical = function(nav){
		var ans = $('#numericalresponse').val().trim();
		if(ans != ''){
			var o = Object();
			var q = this.quiz.questions[this.currentQuestion].question;
			o.question_id = q.id;
			o.score = 0;
			o.text = ans;
			var bestans = -1;
			// mark question and get text
			for(var r in q.responses){
				if(parseFloat(q.responses[r].title) - parseFloat(q.responses[r].props.tolerance) <= ans && ans <= parseFloat(q.responses[r].title) + parseFloat(q.responses[r].props.tolerance) ){
					if(parseFloat(q.responses[r].score) > parseFloat(o.score)){
						o.score = q.responses[r].score;
						bestans = r;
					}
				}
			}
			if(bestans != -1){
				o.score = q.responses[bestans].score;
				// set feedback (if any)
				if (q.responses[bestans].props.feedback && q.responses[bestans].props.feedback != ''){
					this.feedback = q.responses[bestans].props.feedback;
				}
			}
			
			o.score = Math.min(o.score,parseFloat(q.props.maxscore));
			this.responses[this.currentQuestion] = o;
			return true;
		} else {
			if(nav == 'next'){
				return false;
			} else {
				return true;
			}	
		}
	}
	
	this.saveEssay = function(nav){
		var ans = $('#essayresponse').val().trim();
		if(ans != ''){
			var o = Object();
			var q = this.quiz.questions[this.currentQuestion].question;
			o.question_id = q.id;
			o.score = 0;
			o.text = ans;
			// mark question and get text
			for(var r in q.responses){
				if(q.responses[r].title == ans){
					o.score = q.responses[r].score;
					// set feedback (if any)
					if (q.responses[r].props.feedback && q.responses[r].props.feedback != ''){
						this.feedback = q.responses[r].props.feedback;
					}
				}
			}
			o.score = Math.min(o.score,parseFloat(q.props.maxscore));
			this.responses[this.currentQuestion] = o;

			return true;
		} else {
			if(nav == 'next'){
				return false;
			} else {
				return true;
			}	
		}
	}
	
	this.saveMultiselect = function(nav){
		var q = this.quiz.questions[this.currentQuestion].question;
		var c = false;
		for(var r in q.responses){
			if($('#'+q.responses[r].id).attr('checked')){
				c = true;
			}
		}
		if(!c){
			if(nav == 'next'){
				return false;
			} else {
				return true;
			}
		}
		var o = Object();
		o.question_id = q.id;
		o.score = 0;
		o.text = "";
		var countsel = 0;
		// mark question and get text
		for(var r in q.responses){
			if($('#'+q.responses[r].id).attr('checked')){
				o.score += parseFloat(q.responses[r].score);
				o.text += q.responses[r].title + "||";
				countsel++;
				if(q.responses[r].props.feedback && q.responses[r].props.feedback != ''){
					this.feedback += q.responses[r].title+": "+ q.responses[r].props.feedback + "<br/>";
				}
			}
		}
		//set score back to 0 if any incorrect options selected
		for(var r in q.responses){
			if($('#'+q.responses[r].id).attr('checked') && parseFloat(q.responses[r].score) == 0){
				o.score = 0;
			}
		}
		o.score = Math.min(o.score,parseFloat(q.props.maxscore));
		this.responses[this.currentQuestion] = o;
		return true;
	}
	
	this.showResults = function(){
		if(!this.saveResponse('next')){
			$('#notify').text("Please answer this question before getting your results.");
			$('#notify').show();
			return;
		} 
		
		mQ.inQuiz = false;
		$('#mq').empty();
		
		$('#mq').append("<h2 name='lang' id='page_title_results'>Your results for:<br/> '"+ this.quiz.title +"':</h2>");
		// calculate score
		var total = 0;
		for(var r in this.responses){
			total += this.responses[r].score;
		}
		total = Math.min(total,this.quiz.props.maxscore);
		if(this.quiz.props.maxscore && this.quiz.props.maxscore > 0){
			var percent = total*100/this.quiz.props.maxscore;
		} else {
			var percent = 0;
		}
		
		// find if any essay questions (so can't be marked)
		var hasessay = false;
		for(var q in this.quiz.questions){
			if(this.quiz.questions[q].question.type == 'essay'){
				hasessay = true;
			}
		}

		if(hasessay){
			var scorestring = percent.toFixed(0) + "% *";
		} else {
			var scorestring = percent.toFixed(0) + "%";
		}
		
		$('#mq').append("<div id='quizresults'>"+ scorestring +"</div>");
		
		if(hasessay){
			var essay = $('<div>').attr({'class': 'centre'}).text("* this quiz contained essay questions which will need to be manually marked. Your score will be updated when these questions have been marked");
			$('#mq').append(essay);
		}
		
		var rank = $('<div>').attr({'id':'rank','class': 'rank'});
		$('#mq').append(rank);
		rank.hide();
		
		var next = $('<div>').attr({'id':'next','class': 'next centre'});
		$('#mq').append(next);
		next.hide();
		
		var d = $('<div>').attr({'class': 'resultopt clickable centre'});
		var l = $('<a>').text("Retry '"+ this.quiz.title +"'");
		d.append(l);
		var id = this.quiz.id;
		l.click(function(){
			mQ.loadQuiz(id);
		});
		$('#mq').append(d);
		
		if(mQ.opts.finallinks){
			for(var i in mQ.opts.finallinks){
				var d = $('<div>').attr({'class': 'resultopt clickable centre'});
				var l = $('<a>').attr({'href': mQ.opts.finallinks[i].link}).text(mQ.opts.finallinks[i].title);
				d.append(l);
				$('#mq').append(d);
			}
			
		}
	
		//save for submission to server
		var content = Object();
		content.quiz_id = this.quiz.id;
		content.maxscore = this.quiz.props.maxscore;
		content.score = total;
		content.attempt_date = dateFormat(Date().now,"isoDateTime", true);
		content.responses = this.responses;
		content.title = this.quiz.title;
		content.sent = false;
	
		mQ.store.addArrayItem('results', content);
		
		var url = mQ.opts.url + "quizattempt/?username=" + mQ.store.get('username') + "&api_key=" + mQ.store.get('api_key');
		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(content),
			timeout: mQ.opts.timeout,
			url: url,
			success:function(data){
				//check for any error messages
				if(data && !data.error){
					content.rank = data.rank;
					// show ranking 
					if($('#rank') && data.rank){
						$('#rank').empty();
						$('#rank').append("Your ranking: " + data.rank);
						$('#rank').show();
					}
					if($('#next') && data.next){
						if(data.next.length > 0){
							$('#next').empty();
							$('#next').append("We suggest you take '<a href='#"+ data.next[0].id+"'>"+ data.next[0].title+"</a>' next");
						   	$('#next').show('blind');
						}
					}
					// loop through results and update rank & sent status
					var cache = mQ.store.get('results');
					mQ.store.clearKey('results');
					content.sent = true;
					for (var c in cache){
						if(cache[c].quizdate == content.quizdate){
							mQ.store.addArrayItem('results', content);
						} else {
							mQ.store.addArrayItem('results', cache[c]);
						}
					} 
					mQ.store.set('points',data.points);
					mQ.store.set('badges',data.badges);
					mQ.showUsername();
				}
			}, 
			error:function(data){ 
				// do nothing
			}
		});	
	}
	
	this.setNav = function(){
		$('#quiznavprev').unbind('click');
		$('#quiznavprev').bind('click',function(event){
			Q.loadPrevQuestion();
		});
		if(this.currentQuestion == 0){
			$('#quiznavprev').hide();
		} else {
			$('#quiznavprev').show();
		}
		
		$('#quiznavnext').unbind('click');
		if(this.currentQuestion+1 == this.quiz.questions.length){
			$('#quiznavnext').html('Get results');
		} else {
			$('#quiznavnext').html('Next &gt;&gt;');
			
		}
		$('#quiznavnext').bind('click',function(){
			Q.loadNextQuestion();
		});
	}
	
}

Date.prototype.addMins= function(m){
    this.setTime(this.getTime() + (m*60000));
    return this;
}

Date.prototype.addHours= function(h){
    this.setHours(this.getHours()+h);
    return this;
}

Date.prototype.addDays= function(d){
    this.setDate(this.getDate()+d);
    return this;
}

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function sortresults(a, b){
	if(a.attempt_date >= b.attempt_date){
		return -1;
	} else {
		return 1;
	}
}