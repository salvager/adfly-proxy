<?php
// Just call this script with the 3-5 trailing characters of an adf.ly url in the code GET variable and it will redirect you to the proper location.

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
if (!preg_match("/^[A-Za-z0-9]{3,5}$/", $code)) {
    pdie("That's not a valid code.");
}

$file = file_get_contents('http://adf.ly/' . $code);

if (!$file)
    pdie("Couldn't connect to adfly.");

$matched = preg_match("/var url = '(.*?)';/", $file, $matches);

if (!$matched) 
    pdie("Invalid response from adfly.");

$gourl = $matches[1];

$prefix = "https://adf.ly";
$prefixlen = strlen($prefix);

// remove the https://adf.ly/ prefix at the beginning of the url in the intermediate page
if (!strncmp($gourl, $prefix, $prefixlen))
    $gourl = substr($gourl, $prefixlen);

$gourl = "http://adf.ly" . $gourl;

$headers = get_headers($gourl, 1);

if (!$headers)
    pdie("Couldn't connect to adfly to find the destination of the /go/ url");

if (!isset($headers["Location"])) 
    pdie("Invalid response from adfly when finding the destination of the /go/ url.");

$url = $headers["Location"];

header("Location: " . $url);

?>
