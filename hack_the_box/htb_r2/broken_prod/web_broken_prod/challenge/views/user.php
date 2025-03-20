
<!DOCTYPE html>
<html lang="en">
<head>
	<title>Broken Production</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="/static/images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="/static/vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="/static/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="/static/vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="/static/vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="/static/vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="/static/css/util.css">
	<link rel="stylesheet" type="text/css" href="/static/css/user.css">
<!--===============================================================================================-->
</head>
<body>
	
	<body>
    <div id="wrapper">
        <!-- Sidebar -->
        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <li class="sidebar-brand">
                    <a href="#">
                        User Dashboard
                    </a>
                </li>
                <div class="profile-sidebar">
                    <!-- SIDEBAR USERPIC -->
                    <div class="profile-userpic">
                        <img src="/static/images/avatar.png" class="img-responsive" alt="">
                    </div>
                    <!-- END SIDEBAR USERPIC -->
                    <!-- SIDEBAR USER TITLE -->
                    <div class="profile-usertitle">
                        <div class="profile-usertitle-name">
                            Username: <?php echo $username ?>
                        </div>
                        <div class="profile-usertitle-job">
                            Roll: Employee
                        </div>
                        <p class="text-white font-weight-bold">Admin: False</p>
                    </div>
                    <!-- END SIDEBAR USER TITLE -->
                    <!-- SIDEBAR BUTTONS -->
                    <div class="profile-userbuttons">
                        <a href="/logout" class="btn btn-danger btn-xs">Log Out</a>
                    </div>
                </div>
            </ul>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <!----------- index page ------------>

                <div class="manage-box">
                    <div class="row">
                        <div class="col text-center">
                            <div class="box">
                                <i class="bl fa fa-line-chart fa-5x" aria-hidden="true"></i>
                                <div class="box-title">
                                    <h3>Performance</h3>
                                </div>
                                <div class="box-text">
                                    <span>Check Your Yearly Performance Details</span>
                                </div>
                                <div class="box-btn">
                                    <a href="#">Learn More</a>
                                </div>
                            </div>
                        </div>

                        <div class="col  text-center">
                            <div class="box">
                                <i class="bl fa fa-trophy fa-5x" aria-hidden="true"></i>
                                <div class="box-title">
                                    <h3>Achievements</h3>
                                </div>
                                <div class="box-text">
                                    <span>Check Your Lifetime Achievements & Awards Details</span>
                                </div>
                                <div class="box-btn">
                                    <a href="#">Learn More</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                    	<div class="col text-center">
                            <div class="box">
                                <i class="bl fa fa-calendar-minus-o fa-5x" aria-hidden="true"></i>
                                <div class="box-title">
                                    <h3>Mark Absent</h3>
                                </div>
                                <div class="box-text">
                                    <span>Mark yourself absent today</span>
                                </div>
                                <div class="box-btn">
                                    <a href="#">Learn More</a>
                                </div>
                            </div>
                        </div>

                        <div class="col text-center">
                            <div class="box">
                                <i class="bl fa fa-calendar fa-5x" aria-hidden="true"></i>
                                <div class="box-title">
                                    <h3>Take Leave</h3>
                                </div>
                                <div class="box-text">
                                    <span>Take paid time off from work</span>
                                </div>
                                <div class="box-btn">
                                    <a href="#">Learn More</a>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
            <div class="row justify-content-center">
                <p class="alert alert-info">User dashboard development is currently paused as we are working on new features for admin.</p>
            </div>
        </div>
        <!-- /#page-content-wrapper -->

    </div>
</body>
<!--===============================================================================================-->	
	<script src="/static/vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="/static/vendor/bootstrap/js/popper.js"></script>
	<script src="/static/vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="/static/vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="/static/vendor/tilt/tilt.jquery.min.js"></script>
	<script >
		$('.js-tilt').tilt({
			scale: 1.1
		})
	</script>
<!--===============================================================================================-->
	<script src="/static/js/main.js"></script>

</html>