<div class="container">
	<p>Viewing log file : /var/log/nginx/access.log</p>
<pre style="height:600px">
<?php
	echo file_get_contents("/var/log/nginx/access.log");
?>
</pre>
</div>