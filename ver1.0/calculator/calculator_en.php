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
$split_a = preg_split("/[\s,]+/",$inp);  #入力された値を空白で分解し、配列に格納
#var_dump($split_a);  # 表示
$length_a = strlen($inp);  #入力された文字の長さを調べる
echo "<hr>";
print "<br>";
print "・Sensors\n";
print "<br>";
print "<br>";

# 地震センサーを外部から実行(exec)し，結課を表示---------------------------------------
$cmd = "ruby ./../sensors/eq_sensor.rb ".$date;
exec($cmd, $result);
# preg_grepで配列の全要素にパターンマッチ
if (preg_grep("/True/",$result)){
    $eq_sensor = "True";
}else{
    $eq_sensor = "False";
}
echo "Eqrthquake_Sensor : ".$result[0];
print "\n";
echo "<br><br>";

# 雨量センサーを外部から実行し，結果を表示---------------------------------------------
$cmd2 = "php ./../sensors/rain_sensor.php";
exec($cmd2, $result2);
$rain_sensor = $result2[0];
for ($i = 0; $i<count($result2); $i++){
    $keywords = preg_split("/[\s,]+/", $result2[$i]);
    for ($j = 0; $j<count($keywords); $j++){
    if (preg_match('/http/', $keywords[$j])){
        print "<a href=".$keywords[$j].">".$keywords[$j]."</a>";
    }else{
        print $keywords[$j];
    }
        print "";
    }
    print "\n";
    echo "<br><br>";
}

# センサーの値に応じて0,1を格納------------------------------------------------------
if ($eq_sensor == "True"){
    $eq_result = 1;
}else{
    $eq_result = 0;
}
if ($rain_sensor == "Weather_Sensor：Rain"||$rain_sensor == "Weather_Sensor：Clear"){
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
    die("cannot connect:" . pg_last_error()); #接続できなかった時のエラー処理
}

# Text Processing( 英語 )--------------------------------------------------------(ここからの処理が英語版)
# 特定の列を取り出してresultに格納
$sql = "select text from systemE;"; #データベース内にある，systemテーブル
$db_result = pg_query($sql);
$final = 0; #マッチングしたテキストとセンサーの数を数えるカウンター変数
$count=0; #入力された値と、テーブル内の文字列の比較

# Text Processingのループここから--------------------------------------------------
while ($colum = pg_fetch_array($db_result, NULL, PGSQL_ASSOC)){
    $r=$colum["text"];
    $length_b = strlen($r);  # 1行の文字の長さを調べる
    $split_b = preg_split("/[\s,]+/",$r);  # 1行の文字をスペースで分割
    $match=0;
    foreach($split_a as $a){
        foreach($split_b as $b){  # マッチングを繰り返し行う
            if($a==$b){
                $match++;
            }
        }
    }
    $ratio = $match/($length_a * $length_b);  #入力文字とデータの文字数を掛けてマッチ数を割って割合を算出

# センサーデータの値を統合----------------------------------------------------------
    $sensor = 0;  # 何のセンサーが反応しているかの値を入れる変数
    $credibility = 0;  # 信憑性の値を入れる変数
# センサーの切り替え(preg_splitで変数にパターンマッチを行い,特定の用語が来た時に参照するセンサーを変える)
    if (preg_match("/earthquake/i",$inp)||preg_match("/seismic/i",$inp)||preg_match("/intensity/i",$inp)||preg_match("/aftershocks/i",$inp)){
        $sensor = 1;  # 1なら地震センサー
    }elseif (preg_match("/rain/i",$inp)||preg_match("/RAIN/i",$inp)||preg_match("/CLEAR/i",$inp)||preg_match("/torrential/i",$inp)||preg_match("/downpower/i",$inp)||preg_match("/CLOUDY/i",$inp)||preg_match("/flood/i",$inp)||preg_match("/SNOW/i",$inp)){
        $sensor = 2;  # 2なら雨量センサー
    }
# 画面に表示し最終的な信憑性を計測 (実験用に表示の仕方を変える時はif文を削除)
# 0.003という数字は信憑性の高さの閾値なので、ここを変える事で様々な実験ができる
    if ($ratio > 0.001 && $ratio != 0){
        echo "Data : ".$r;
        echo "<br>";
        echo "Ratio : ".$ratio. "<br>";
# 地震センサーを統合するのはResourceからの情報が地震に関するものの時
    if ($sensor==1 && (preg_grep("/earthquake/",$colum)||preg_grep("/intensity/",$colum)||preg_grep("/seismic/",$colum)||preg_grep("/aftershocks/",$colum))){
        $credibility = $ratio * $eq_result;
        echo "Sensor : Earthquake"."<br>";
# 雨量センサーを統合するのはResourceからの情報が天気に関するものの時
    }elseif($sensor==2 && (preg_grep("/rain/",$colum)||preg_grep("/RAIN/",$colum)||preg_grep("/CLEAR/",$colum)||preg_grep("/torrential/",$colum)||preg_grep("/downpower/",$colum)||preg_grep("/CLOUDY/",$colum)||preg_grep("/flood/",$colum)||preg_grep("/SNOW/",$colum))){
        $credibility = $ratio * $rain_result;
        echo "Sensor : Weather"."<br>";
# それ以外の時はセンサーを参照しない
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
}elseif($final == 1 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 30%";
}elseif($final == 2 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 60%";
}elseif($final == 3 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 90%";
}elseif($final > 4 && ($eq_result == 1||$rain_result == 1)){
    echo "Final Credibility : 99%";
}else{
    echo "Final Credibility : ---";
}

#-------------------------------------------------------------------------------(ここまでの処理が英語版)
# disconnect from database------------------------------------------------------
pg_close($db);
?>

<br><br><br>
<div id="back">
<a href="./../index.html">Back</a>
</body>
</html>
