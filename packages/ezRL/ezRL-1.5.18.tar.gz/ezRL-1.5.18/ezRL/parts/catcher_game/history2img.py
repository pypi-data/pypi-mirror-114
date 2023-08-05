
import sys
import ezpip
ezRL = ezpip.load_develop("ezRL", "../"*3)

history_filename = input("history_filename>")

# 棋譜の画像化 (デフォルトは入力棋譜と同じディレクトリに置かれる)
ezRL.history2img(
	history_filename,	# 棋譜ファイル名
	game = ezRL.catcher_game,	# ゲーム
	output_file_flag = True	# ファイル出力フラグ
)
