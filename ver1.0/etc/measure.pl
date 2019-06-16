#! /usr/bin/perl
use: strict;
use: warnings;
use: DBI;
#DB内にある情報と入力された情報を比較するプログラム

my $measure = $_POST['measure'];
#DB情報
my $user = 'postgres'; #postgreSQLのユーザ名
my $pass = 'Kensamavacation82'; #PostgreSQLのパスワード
my $database = 'research'; #使用するデータベース名
my $hostname = 'localhost'; #データベースサーバのアドレス
my $port = '5432'; #データベースサーバに接続する
#DB接続
my $db = DBI->connect("dbi:Pg:dbname=$database;host=$hostname;port=$port; ","$user","$pass") or die "cannot connect to MySWL: $DBI::errstr";
if (!$db) {exit ('データベースに接続できません。');} #DBに接続できなかった時の処理



#DBから切断
$db->disconnect;
