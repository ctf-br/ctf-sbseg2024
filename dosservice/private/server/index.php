<?php
require 'vendor/autoload.php';
require 'classes/Ping.php';

use Smarty\Smarty;

$smarty = new Smarty();
$smarty->setTemplateDir(__DIR__ . '/templates');

$smarty->enableSecurity();

$request = urldecode($_SERVER['REQUEST_URI']);
$baseDir = __DIR__ . $request;

$allowList = array_merge(
    range(0x61, 0x7A),
    range(0x41, 0x5A),
    range(0x30, 0x39),
    [0x7B, 0x7D, 0x3A, 0x22, 0x27, 0x3D, 0x2F, 0x20]
);

for ($i = 0; $i < strlen($request); $i++) {
    $char = ord($request[$i]);
    if (!in_array($char, $allowList, true)) {
        $request = "";
        break;
    }
}

if (!file_exists($baseDir) && !is_dir($baseDir)) {

    $processed = $smarty->fetch('string:'.$request);

    $smarty->assign('not_found', $processed);

    header("HTTP/1.0 404 Not Found");
    $smarty->display('not_found.tpl');
    exit();
}

$pingResult = Ping::ping("hackersdobem.org.br");
$smarty->assign('pingResult', $pingResult);
$smarty->display('ping_result.tpl');
?>
