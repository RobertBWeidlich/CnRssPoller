<?php
////////////////////////////////////////////////////////////////////////
// file:    cn_rss_current.php
// author:  rbw
// date:    20120904.2000
// purpose: Access to the CN RSS Current data
////////////////////////////////////////////////////////////////////////

class CnRssCurrent {
  private $base_dir_cndata;

  public function __construct($base_dir_arg) {
    $this->base_dir_cndata = $base_dir_arg;
    $i = strlen($this->base_dir_cndata) - 1;
    if ($this->base_dir_cndata[$i] != '/') {
      $this->base_dir_cndata .= "/";
    }
  }

  //
  // return sorted list of CN RSS files in the form
  //
  //   "20121002.2102.13.txt"
  //
  public function get_cn_rss_filenames() {
    $file_list = array();

    // 1. get files that match naming convention
    $d = opendir($this->base_dir_cndata);
    while ($f = readdir($d)) {
      // match '20121002.2135.13.txt'
      if (preg_match('/^\d{8}\.\d{4}\.\d{2}\.txt$/', $f)) {
        $file_list[] = $f;
      }
      //echo $f . "\n";
    }

    // 2. sort
    sort($file_list);

    // 3. return array
    return $file_list;
  }

  public function get_items_from_file($filename_arg) {
    $pathname = $this->base_dir_cndata . $filename_arg;
    $if = fopen($pathname, 'r') or die("can't open file");

    $item = array();
    $item_list = array();
    $tag = '';
    $data = '';

    $inside_item = false;

    while ($line_wnl = fgets($if)) {
      $line = preg_replace("/\r\n|\r|\n$/", '', $line_wnl);

      if (preg_match('/^start-item:/', $line)) {
        $inside_item = true;
        //echo "\n";
        //echo "INSIDE\n";
        continue;
      }
      if (preg_match('/^end-item:/', $line)) {
        $inside_item = false;
        if (sizeof($item) > 0) {
          // append $item to $item_list
          //echo "  appending to item_list\n";
          //echo "  A item_list size: " . sizeof($item_list) . "\n";
          $item_list[] = $item;
          //echo "  B item_list size: " . sizeof($item_list) . "\n";
        }
        //echo "OUTSIDE\n";
        //echo "  item size: " .      sizeof($item) . "\n";
        //echo "  item_list size: " . sizeof($item_list) . "\n";

        // reset
        $item = array();
        $tag = '';
        $data = '';
      }
      if (!$inside_item) {
        continue;
      }

      //
      // we are inside an item
      //
      // look for tag line which indicates the start of a new
      // sub-item, in the form:
      //
      //   "tstamp:  20121002.2327.13"
      //
      $tag_line_re = '/^(\w+\-?\w+):\s*(\S*.*)$/';
      if (preg_match($tag_line_re, $line, $groups)) {
        $g_len = sizeof($groups);
        //echo "MATCH\n";
        //echo "GROUPS: " . $g_len . "\n";
        $g1 = "";
        $g2 = "";
        if ($g_len > 1) {
          $g1 = $groups[1];
        }
        if ($g_len > 2) {
          $g2 = $groups[2];
        }
        //echo " g0: >>>" . $groups[0] . "<<<" . "\n";
        //echo " g1: >>>" . $g1 . "<<<" . "\n";
        //echo " g2: >>>" . $g2 . "<<<" . "\n";
        $tag = $g1;
        $data = '';
        if (sizeof($g2) > 0) {
          $data = $g2;
          $item[$tag] = $data;
        }
      }
      else { // no tag in line, just a continuation of the previous tag
        if (array_key_exists($tag, $item)) {
          //echo "HERE >>>" . $tag . "<<<" . ">>>" . $line . "<<<" . "\n";
          $item[$tag] .= "\n";
          $item[$tag] .= $line;
        }
      }
    }

    fclose($if);
    return $item_list;
  }

  public function get_number_items_in_file($file_name) {
    $item_count = 0;
    $path_name = $this->base_dir_cndata . $file_name;

    $if = fopen($path_name, 'r') or die("can not open file");
    while($line_wnl = fgets($if)) {
      //echo ">>>" . $line_wnl . "<<<";
      if (preg_match('/^start-item:/', $line_wnl)) {
        ++$item_count;
      }
    }

    fclose($if);

    return $item_count;
  }

  public function get_last_n_items($n) {
    $items = array();

    $p_file_list_rev = array(); // minimal list to get $n items

    //
    // 1. get ordered list of current rss data files
    //
    $file_list = $this->get_cn_rss_filenames();

    //
    // 2. reverse the list
    //
    $file_list_rev = array_reverse($file_list);

    //
    // 3. find which files need to be read to get those n items using
    //
    $pl_item_count = 0; // number of items in partial list
    foreach($file_list_rev as $file) {
      $count = $this->get_number_items_in_file($file);
      $pl_item_count += $count;
      //print $file . "  " . $pl_item_count . "  " . $count . "\n";
      $p_file_list_rev[] = $file;
      if ($pl_item_count >= $n) {
        break;
      }
    }
    $p_file_list = array_reverse($p_file_list_rev);

    //
    // 4. get the items
    // 
    //print "\n";
    //print "4. partial list of files\n";
    foreach($p_file_list as $p_file) {
      //print "  " . $p_file . "\n";
      $p_items = $this->get_items_from_file($p_file);
      $items = array_merge($items, $p_items);
    }
    //print "\n";
    //print 'size of $items: ' . sizeof($items) . "\n";

    //
    // 5. truncate the list
    // 
    // use array_slice() - see p. 111 of PHP Cookbook
    $items_n = array_slice($items, -$n);

    return $items_n;
  }

}


?>
