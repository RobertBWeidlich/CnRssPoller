<!DOCTYPE html>
<!--
  file:    index_basic.php
  author:  rbw
  date:    20120904.1900
  purpose: basic CN Current RSS Data
-->
<html>
  <head>
    <title>CN RT Data Feed</title>
  <head>

  <body>
<?php
  include("cn_rss_current.php");

  $base_dir = "/home/polyticker/polyticker.com/data/cn/rss_current";
  $n_items = 200;

  $crc = new CnRssCurrent($base_dir);

  $items = $crc->get_last_n_items($n_items);
  echo "  <table>\n";
  foreach ($items as $item) {
    echo "    <tr>\n";
    echo "      <td>", $item['tstamp'], "</td>\n";
    echo "      <td>", $item['src'], "</td>\n";
    //echo "      <td>", $item['url'], "</td>\n";
    echo "      <td>", $item['title'], "</td>\n";
    echo "      <td>", $item['text1'], "</td>\n";
    echo "    </tr>\n";
  }
  echo "  </table>\n";

  //phpinfo();
  //
  // check to see that we can read data both inside and outside
  // the httpd server subdirectory
  //
  //$path_name = '/tmp/abc.txt';
  //$path_name =
  //    '/home/polyticker/polyticker.com/data/cn/rss_current/hello.txt';
  //$path_name =
  //    '/home/polyticker/polyticker.com/data/cn/rss_current/' .
  //    '20121002.1625.13.txt';
  //$fh = fopen($path_name, 'r')
  //        or die("can't open file");
  //echo '<strong>';
  //while($line = fgets($fh)) {
  //  echo '<p>';
  //  echo $line;
  //}
  //echo '</strong>';
  //fclose($fh);
?>

  </body>
</html>
