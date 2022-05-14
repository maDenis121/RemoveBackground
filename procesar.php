<!DOCTYPE HTML PUBLIC >
<html> 
	<head> 
		<title>Remove Background</title> 
		<meta http-equiv="content-type" content="text/hyml"; charset="utf-8">
        <style type="text/css">
            html {font-family: Verdana, sans-serif}
            body {margin: auto; height: 100%; width: 60%;
                display: flex; justify-content: center; align-items: center}
        </style>
	</head> 
	<body> 
        <h2> Remove Background </h2>
        <br/><br/>
        <?php
            $imagenOriginal = $_FILES['imagenOriginal']['tmp_name'];
            echo "<img src='{$imagenOriginal}' />";
            if ($_POST['chkUsarNuevoFondo']){
                $imagenFondo = $_FILES['imagenFondo']['tmp_name'];
                echo "<img src='{$imagenFondo}' />";
            }
            echo $_POST['selectTipoFondo'];
            
		?>
	</body> 
</html>