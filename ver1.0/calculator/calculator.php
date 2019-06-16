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
#$date = $_POST['date'];
echo "Input : "."\"".$inp."\"";
echo "<br><br>";

# 前処理用のpythonスクリプトを実行--------------------------------------------------
$cmd = "python3 ./../nlp/preprocessing.py";
exec($cmd, $result);
echo($result);











# disconnect from database------------------------------------------------------
# pg_close($db);
?>

<br><br><br>
<div id="back">
<a href="./../index.html">Back</a>
</body>
</html>
