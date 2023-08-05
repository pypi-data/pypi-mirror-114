<?php
header("X-Frame-Options: SAMEORIGIN");
header("X-Content-Type-Options: nosniff");
header("X-XSS-Protection: 1; mode=block");
session_start();
function main($file){
    ob_get_clean();
    ob_start();
    include $file;
    return ob_get_clean();
}
echo implode(" ",explode("\n",main("site.php")));
?>