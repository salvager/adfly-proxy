<?php
// Just call this script with the 5 trailing characters of an adf.ly url and it will redirect you to the proper location.

function pdie ($msg) {
    header("Content-type: text/plain");
    die($msg);
}

if (isset($_GET["code"])) {
    $code = $_GET["code"];
} else {
    pdie("No code specified!");
}

// FIXME: If they specify a huge GET parameter for code, it could take a while to parse, right?
if (!preg_match("/^[A-Za-z0-9]{5}$/", $code)) {
    pdie("That's not a valid code.");
}

$file = file_get_contents('http://adf.ly/' . $code);

if (!$file)
    pdie("Couldn't connect to adfly.");

$matched = preg_match("/var url = '(.*?)';/", $file, $matches);

if (!$matched) 
    pdie("Invalid response from adfly.");

header("Location: " . $matches[1]);

?>
