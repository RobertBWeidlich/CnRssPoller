<?php
////////////////////////////////////////////////////////////////////////
// file:     ut_cn_rss_current.php
// author:   rbw
// date:     20120904.2000
// purpose:  unit test for CnRssCurrent class
// synopsis: php ./ut_cn_rss_current.php
////////////////////////////////////////////////////////////////////////
include("cn_rss_current.php");

$base_dir = "/home/polyticker/polyticker.com/data/cn/rss_current";

$crc = new CnRssCurrent($base_dir);

$run_test_2 = false;
$run_test_3 = false;
$run_test_4 = false;
$run_test_5 = true;

if ($run_test_2) {
  $file_list = $crc->get_cn_rss_filenames();
  foreach($file_list as $file) {
    print $file . "\n";
  }
  print "\n";
}

if ($run_test_3) {
  $items = $crc->get_items_from_file('20121003.2313.13.txt');
  print_items($items);
}

if ($run_test_4) {
  $file_list = $crc->get_cn_rss_filenames();
  $n_total;
  foreach($file_list as $file) {
    $n = $crc->get_number_items_in_file($file);
    print $file . "  " . $n . "\n";
    $n_total += $n;
  }
  print "\n";
  print "  total: " . $n_total . "\n";
  print "\n";
}

if ($run_test_5) {
  //$items = $crc->get_last_n_items(500);
  $n = 5;
  print "n: " . $n . "\n";
  $items = $crc->get_last_n_items($n);
  print "\n";
  print_items($items);
}

function print_item($item) {
  print 'path:    ' . $item['path'] .    "\n";
  print 'src:     ' . $item['src'] .     "\n";
  print 'tstamp:  ' . $item['tstamp'] .  "\n";
  print 'pubdate: ' . $item['pubdate'] . "\n";
  print 'author:  ' . $item['author'] .  "\n";
  print 'guid:    ' . $item['guid'] .    "\n";
  print 'url:     ' . $item['url'] .     "\n";
  print 'title:   ' . $item['title'] .   "\n";
  print 'summary: ' . $item['summary'] . "\n";
  print 'text1:   ' . $item['text1'] .   "\n";
  print "\n";
}

function print_items($items) {
  print "print_items() - " . sizeof($items) . " items\n";
  $i = 0;
  foreach($items as $item) {
    ++$i;
    print "item " . $i . "\n";
    print_item($item);
  }
  print "\n";
}

?>

