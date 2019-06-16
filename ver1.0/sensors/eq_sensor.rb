#!/usr/bin/ruby
# coding: utf-8
#元となったのはget_image.rb
#特定urlから画像を取得し、色を解析するプログラム
#参考資料: http://www.mk-mode.com/octopress/2013/09/05/ruby-compile-colors-by-rmagick/
#require 'pg'
require 'net/http'
require 'rmagick'
Net::HTTP.version_1_2
#データベース接続情報
host = "localhost"
user = "postgres"
pass = "Kensamavacation82"
db = "research"
port = "5432"

#データベース接続
#connection = PG::connect(host: host, user: user, password: pass, dbname: db, port: port)

#日付と時刻を取得
#day = Time.new
#day.to_s

#日付と時刻を自分で入力する場合
#puts "日付と時間を指定してください．(例:20161116180000)\n"
day = ARGV[0]

#-------------------------------------------------------------------------------
#特定のurlを指定して日付の画像を取得
Net::HTTP.start('realtime-earthquake-monitor.bosai.go.jp',80){ |http| #取得したい画像のあるurl
  path = "/seis/static/realtimeimg/jma_s/" + day + ".jma_s.gif" #取得したい画像のパスとファイル名.ファイル名に日付が含まれるため，あらかじめ取得しておいた変数dayを使う．
  response = http.get(path) #変数pathを用いてhttp.get
    File.write("a.gif", response.body)
}

#-------------------------------------------------------------------------------
#色の解析用のクラス定義
class RMagickCompileColor
#IMG_FILE = "/Users/KenHonda/ruby/sindo_example.gif" #画像ファイル
RATE_MIN = 0.05 #この百分率未満は非表示
def initialize #アニメーションGIFが考慮されて画像が読み込まれるので、その場合配列の先頭画像だけを取得する
@img = Magick::Image.read("a.gif").first
  @px_x = @img.columns #横
  @px_y = @img.rows #縦
  @px_total = @px_x * @px_y #トータル
end

#-------------------------------------------------------------------------------
#使用されている色を集計する関数(メソッド)を定義
def compile
  begin
    img_depth = @img.depth #画像のdepthを取得
    hist = @img.color_histogram.inject({}) do |hash, key_val| #カラーヒストグラムを取得してハッシュで集計
    color = key_val[0].to_color(Magick::AllCompliance, false, img_depth, true) #各ピクセルの色を16進数で取得
    hash[color] ||= 0 #Hashに格納
    hash[color] += key_val[1]
    hash
end

#-------------------------------------------------------------------------------
#ヒストグラムのハッシュを値の大きい順にソート
@hist = hist.sort{|a, b| b[1] <=> a[1]}
    rescue => e
      STDERR.puts "[ERROR][#{self.class.name}.compile] #{e}"
      exit 1
    end
  end

#-------------------------------------------------------------------------------
#結果を表示する関数(メソッド)の定義
def display
    begin
      color_array = ["#ff0000","#dc143c","#ff4500","#b22222","#a52a2a","#8b0000","#800000"] #配列redに赤系の色のコードを格納
      @hist.each do |color, count|
        rate = (count / @px_total.to_f) * 100
        break if rate < RATE_MIN
        #puts "#{color} => #{count} px ( #{sprintf("%2.4f", rate)} % )"

#-------------------------------------------------------------------------------
#特定の色(赤)があった場合にtrueの値を返す
        if color.include?("#FF0000") == true
          puts "True"
        elsif color.include?("#DC143C") == true
          puts "True"
        elsif color.include?("#FF4500") == true
          puts "True"
        elsif color.include?("#B22222") == true
          puts "True"
        elsif color.include?("#A52A2A") == true
          puts "True"
        elsif color.include?("#8B0000") == true
          puts "True"
        elsif color.include?("#800000") == true
          puts "True"
        elsif color.include?("#00D08B") == true #この行は実験用の赤以外の色(今回は震度1の緑)
          puts "True"
        elsif color.include?("#000000") == true #この行は実験用の赤以外の色
          puts "True"
        else
          puts "False"
        end

=begin
if color.include?(color_array) == true
  puts "True"
else
  puts "False"
end
=end

end
#puts "Image Size: #{@px_x} px * #{@px_y} px"
#puts "TOTAL     : #{@px_total} px, #{@hist.size} colors"
rescue => e
      STDERR.puts "[ERROR][#{self.class.name}.display] #{e}"
        exit 1
    end
  end
end

#-------------------------------------------------------------------------------
#先ほど定義したクラスの関数(メソッド)を使う
obj_main = RMagickCompileColor.new
obj_main.compile #画像内の使用色を集計
data = obj_main.display #表示する
