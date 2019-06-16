<?php
//phpからセンサー(雨量)のプログラムを実行．

$cmd = "php ./rain_sensor.php";
exec($cmd, $result);

for ($i = 0; $i<count($result); $i++){
    $keywords = preg_split("/[\s,]+/", $result[$i]);
    for ($j = 0; $j<count($keywords); $j++){
      if (preg_match('/http/', $keywords[$j])){
        print "<a href=".$keywords[$j].">".$keywords[$j]."</a>";
      }else{
        print $keywords[$j];
       }
       print "";
    }
    print "\n";
}


 ?>
