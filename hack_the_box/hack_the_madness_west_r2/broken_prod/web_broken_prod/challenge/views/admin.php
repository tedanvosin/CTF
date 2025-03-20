<?php

$utilFile = "tickets.php";

if (isset($_GET['util']))
	$utilFile = $_GET['util'];
	$utilFile = str_replace("../","", $utilFile);

$fullPath = '/www/utils/'.$utilFile;

?>
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
	<link rel="stylesheet" type="text/css" href="/static/css/admin.css">
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
                        Admin Dashboard (Under Construction)
                    </a>
                </li>
                <div class="profile-sidebar">
                    <!-- SIDEBAR USERPIC -->
                    <div class="profile-userpic">
                        <img src="/static/images/makelaris.png" class="img-responsive" alt="">
                    </div>
                    <!-- END SIDEBAR USERPIC -->
                    <!-- SIDEBAR USER TITLE -->
                    <div class="profile-usertitle">
                        <div class="profile-usertitle-name">
                            <?php echo $username ?>
                        </div>
                        <div class="profile-usertitle-job">
                            Administrator
                        </div>
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
                <div class="row text-right mb-4">
	                <div class="col">
	                    <select class="custom-select" id="gotoPage">
	                    	<?php 
	                    		echo "<option value='$utilFile' selected='true'>$utilFile</option>";

	                    		$pages = array("logs.php", "tickets.php", "todo.php");
	                    		foreach ($pages as $page){
	                    			if($page != $utilFile){
	                    				echo "<option value='$page'>$page</option>";
	                    			}
	                    		}
	                    	?>
						</select>  
	                </div>    
	            </div>

                <div class="manage-box">
                	<?php include_once($fullPath); ?>
                </div>
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
	<script src="/static/js/admin.js"></script>

</html>