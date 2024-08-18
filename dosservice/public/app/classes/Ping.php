<?

class Ping {
    public static function ping($host) {
        $command = "ping -c 1 " . $host;

        $output = shell_exec($command);

        if (preg_match('/time=([\d\.]+)\s*ms/', $output, $matches)) {
            return (float)$matches[1] . " ms";
        } else {
            return "Host não respondeu...";
        }
    }
}

?>