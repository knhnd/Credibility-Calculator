<!DOCTYPE html>
<html>
　　　　<head>
　　　　　　　　<meta charset='utf-8'>
　　　　　　　　<title>Credibility Calculation System</title>
　　　　　　　　<link rel="stylesheet" href="./../style.css">
　　　　</head>

<body>
　　　　<header>
　　　　<div id="header">
　　　　<a href="./../index.html">Credibility Calculation System</a></div>
  　　　</header><br><br><br><br>
<h2>Result</h2><br>

<?php
# データベース情報-----------------------------------------------------------------
$user = 'postgres';  # postgreSQLのユーザ名
$pass = 'Kensamavacation82';  # PostgreSQLのパスワード
$database = 'research';  # 使用するデータベース名
$hostname = 'localhost';  # データベースサーバのアドレス
$port = '5432';  # データベースのポート番号

# フォームの入力を受け取る----------------------------------------------------------
$inp = $_POST['input'];
$date = $_POST['date'];
echo "Input : "."\"".$inp."\"";
echo "<br><br>";

# 入力されたテキストに対して言語処理を行う---------------------------------------------
$split_a = mb_str_split($inp); #入力された値を分解し、配列に格納
# var_dump($split_a);  # 表示
$length_a = strlen($inp); #入力された文字の長さを調べる
# マルチバイト文字列をsplitするためのfunction(日本語のみ)
function mb_str_split($str, $split_len = 1) {
    mb_internal_encoding('UTF-8');
    mb_regex_encoding('UTF-8');
    if ($split_len <= 0) {
        $split_len = 1;
    }
    $strlen = mb_strlen($str, 'UTF-8');
    $ret = array();
    for ($i = 0; $i < $strlen; $i += $split_len) {
        $ret[ ] = mb_substr($str, $i, $split_len);
    }
    return $ret;
}
echo "<hr>";
print "<br>";
print "・Sensors\n";
print "<br>";
print "<br>";

# 地震センサーを外部から実行(exec)し，結果を表示---------------------------------------
$cmd = "ruby ./../sensors/eq_sensor.rb ".$date;
exec($cmd, $result); #実行コマンドと結果を入れる配列
#preg_grepで配列の全要素にパターンマッチ
if (preg_grep("/True/",$result)){
    $eq_sensor = "True";
}else{
    $eq_sensor = "False";
}
echo "Eqrthquake_Sensor : ".$eq_sensor;
print "\n";
echo "<br><br>";

# 気象センサーを外部から実行し，結果を表示---------------------------------------------
$cmd2 = "php ./../sensors/rain_sensor.php";
exec($cmd2, $result2);
$rain_sensor = $result2[0];
for ($i2 = 0; $i2<count($result2); $i2++){
    $keywords2 = preg_split("/[\s,]+/", $result2[$i2]);
    for ($j2 = 0; $j2<count($keywords2); $j2++){
        if (preg_match('/http/', $keywords2[$j2])){
            print "<a href=".$keywords2[$j2].">".$keywords2[$j2]."</a>";
        }else{
            print $keywords2[$j2];
        }
    print "";
    }
    print "\n";
    echo "<br><br>";
}

# センサーの結果に応じて0,1を格納----------------------------------------------------
if ($eq_sensor == "True"){
    $eq_result = 1;
}else{
    $eq_result = 0;
}
if ($rain_sensor == "Weather_Sensor：Rain"||$rain_sensor == "Weather_Sensor：Clouds"){
    $rain_result = 1;
}else{
    $rain_result = 0;
}
echo "<hr>";
print "<br>";
print "・Text Processing (High Matching Level)";
print "<br><br>";

# databaseに接続-----------------------------------------------------------------
$db = pg_connect("host=$hostname dbname=$database user=$user password=$pass");
if(!$db) {
    die("cannot connect:" . pg_last_error());  # 接続できなかった時のエラー処理
}

# Text Processing( 日本語 )------------------------------------------------------(ここからの処理が日本語版)
# 特定の列を取り出してresultに格納
$sql = "select text from system;";  # データベース内にある，systemテーブル
$db_result = pg_query($sql);
$final = 0;  # マッチングしたテキストとセンサーの数を数えるカウンター変数
$count=0;  # 入力された値と、テーブル内の文字列の比較

# テキスト処理のループここから-------------------------------------------------------
while ($colum = pg_fetch_array($db_result, NULL, PGSQL_ASSOC)){
    $r=$colum["text"];
    $length_b = strlen($r); #1行の文字の長さを調べる
    $split_b = mb_str_split($r); #1行の文字を１つ１つ分割
    $match=0;
      foreach($split_a as $a){
          foreach($split_b as $b){
# マッチングを繰り返し行う
              if(mb_ereg_match($a, $b)){
                  $match++;
              }
          }
      }
    $ratio = $match/($length_a * $length_b); #入力文字とデータの文字数を掛けてマッチ数を割って割合を算出

# センサーデータの値を統合----------------------------------------------------------
    $sensor = 0;  # 何のセンサーが反応しているかの値を入れる変数
    $credibility = 0;  # 信憑性の値を入れる変数
# センサーの切り替え(preg_splitで変数にパターンマッチを行い,特定の用語が来た時に参照するセンサーを変える)
    if (preg_match("/地震/",$inp)||preg_match("/震度/",$inp)||preg_match("/震源/",$inp)||preg_match("/震災/",$inp)||preg_match("/マグニチュード/",$inp)){
        $sensor = 1;  # 1なら地震センサー
    }elseif (preg_match("/雨/",$inp)||preg_match("/大雨/",$inp)||preg_match("/豪雨/",$inp)||preg_match("/洪水/",$inp)||preg_match("/氾濫/",$inp)){
        $sensor = 2;  # 2なら雨量センサー
    }
# 画面に値を表示し,最終的な信憑性を計測 (実験用に表示の仕方を変える時はif文を削除)
# 0.003という数字は信憑性の高さの閾値なので,ここを変える事で様々な実験ができる
    if ($ratio >= 0.002 && $ratio != 0){
        echo "Data : ".$r;
        echo "<br>";
        echo "Ratio : ".$ratio. "<br>";
# 地震センサーを統合するのはResourceからの情報が地震に関するものの時
    if ($sensor==1 && (preg_grep("/地震/",$colum)||preg_grep("/震度/",$colum)||preg_grep("/震源/",$colum)||preg_grep("/震災/",$colum)||preg_grep("/マグニチュード/",$colum))){
        $credibility = $ratio * $eq_result;
        echo "Sensor : Earthquake"."<br>";
# 雨量センサーを統合するのはResourceからの情報が天気に関するものの時
    }elseif($sensor==2 && (preg_grep("/雨/",$colum)||preg_grep("/大雨/",$colum)||preg_grep("/豪雨/",$colum)||preg_grep("/洪水/",$colum)||preg_grep("/氾濫/",$colum))){
        $credibility = $ratio * $rain_result;
        echo "Sensor : Weather"."<br>";
#それ以外の時はセンサーを参照しない
    }else{
        echo "Sensor : ---"."<br>";
    }
    echo "Credibility : ". $credibility;
    echo "<br><br>";
    $final++;
    }
}
echo "<hr>";
print "<br>";
print "・Final Credibility";
print "<br><br>";

# 結果の数によってFinal Credibilityを変える処理(仮)----------------------------------
if ($final == 0 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 0%";
}elseif($final == 3 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 30%";
}elseif($final == 4 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 60%";
}elseif($final == 5 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 90%";
}elseif($final > 6 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 99%";
}else{
    echo "Final Credibility : ---";
}

#-------------------------------------------------------------------------------(ここまでの処理が日本語版)
# databaseから切断---------------------------------------------------------------
pg_close($db);
?>

<br><br><br>
<div id="back">
<a href="./../index.html">Back</a>
</body>
</html>
