--スキーマ定義用SQLファイル

--ターゲット情報と共起の情報を格納するテーブル
CREATE TABLE IF NOT EXISTS co-occurrence(  -- テーブルの作成(取得したデータを入れるテーブル)
  id INTEGER PRIMARY KEY,  -- id
  time INTEGER,  -- タイムスタンプを格納
  data TEXT  -- 本文となる情報を格納
);
INSERT INTO co-occurrence(time, data) values(2000.10.10, "This is an example text.");  -- サンプルを1件格納