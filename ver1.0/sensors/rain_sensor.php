<?php
#openweathermapから取得した特定の値を抽出
#元となったプログラムはrain.php

$url = 'http://api.openweathermap.org/data/2.5/weather?q=Tokyo,jp&units=metric&appid=88addf0338d7540b217b2276484345d9';
$weather = json_decode(file_get_contents($url), true);

/*
echo "<pre>"; #<pre>タグは，このタグで囲んだ範囲にあるソースに記述されたスペースや改行をそのまま表示するためのタグ．
var_dump($weather["weather"][0]["main"]); #var_dumpは引数として指定した変数の内容や命令の返り値を画面に出力する．
echo "----------------------------------------------\n";
var_dump($weather[rain]);
echo "</pre>";
*/

echo "Weather_Sensor：" . $weather["weather"][0]["main"] . "\n";

?>
