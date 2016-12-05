<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--
  file:  index_exp_01.php
  purpose: JS CB - 7.2 - simple mouse click processing
-->
<html>
  <head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=UTF-8" />
          
    <title>CN NRT Data Feed</title>

    <meta name="description" content="Near-realtime analysis of textual data"/>
    <meta name="Keywords" content="realtime, NLP, Big Data"/>

    <link rel="stylesheet" type="text/css" href="/cn/cn_rtfeed/main.css"/>

    <script type="text/javascript">
      function cnProcessClick(evt) {
        evt = evt || window.event;
        var x = 0;
        var y = 0;
        // ...

        alert("Hello!");
      }
    </script>
  <head>

  <body>
  <script type="text/javascript">
    document.onclick=cnProcessClick;
  </script>
  <h1> Near Real Time Data Feed </h1>
<?php
  include("cn_rss_current.php");

  $base_dir = "/home/polyticker/polyticker.com/data/cn/rss_current";
  $n_items = 1000;

  $crc = new CnRssCurrent($base_dir);

  $items = $crc->get_last_n_items($n_items);
  echo "  <table border=\"1\">\n";
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
