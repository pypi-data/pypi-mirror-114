
# デモ [demo.py]

import sys
# 複数エピソード実行
from ..episode import do_episodes

# デモ (DQN-catcher) [demo.py]
def dqn_catcher_demo():
	import resout as rout
	from relpath import add_import_path
	add_import_path("../")
	import catcher_game as game	# Catcherゲーム [catcher_game]
	from DQN_Agent import DQN_Agent	# Deep Q Network AI [DQN_Agent]
	rout.set_save_dir("./ezRL_demo_output/")	# 保存パスの設定 [resout]
	train_ai = DQN_Agent(action_ls = game.action_ls, ai_obs = game.ai_obs) # Deep Q Network AI
	do_episodes(game, train_ai, game_params_ls = [{} for _ in range(700)], save_reward_ls = True)	# 複数エピソード実行
	test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
	do_episodes(game, test_ai, game_params_ls = [{} for _ in range(3)], save_history = True)	# 複数エピソード実行
	print("demo finished! (results are in \"./ezRL_demo_output/\".)")

# デモ (Random-catcher) [demo.py]
def random_catcher_demo():
	import resout as rout
	from relpath import add_import_path
	add_import_path("../")
	import catcher_game as game	# Catcherゲーム [catcher_game]
	from debug_players import RandomPlayer	# ランダムAI
	rout.set_save_dir("./ezRL_demo_output/")	# 保存パスの設定 [resout]
	train_ai = RandomPlayer(action_ls = game.action_ls, ai_obs = game.ai_obs)	# ランダムAI
	do_episodes(game, train_ai, game_params_ls = [{} for _ in range(30)], save_reward_ls = True)	# 複数エピソード実行
	test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
	do_episodes(game, test_ai, game_params_ls = [{} for _ in range(5)], save_history = True)	# 複数エピソード実行
	print("demo finished! (results are in \"./ezRL_demo_output/\".)")

# デモ (Random-catcher-PeriodicTest) [demo.py]
def random_catcher_periodicTest_demo():
	import resout as rout
	from relpath import add_import_path, rel2abs
	add_import_path("../")
	import catcher_game as game	# Catcherゲーム [catcher_game]
	from debug_players import RandomPlayer	# ランダムAI
	rout.set_save_dir("./ezRL_demo_output/")	# 保存パスの設定 [resout]
	# 定期テスト
	def rcpd_periodicTest(train_ai, episode_idx):
		if episode_idx%5 != (-1%5): return
		test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
		prob_name_ls = [str(i) for i in range(2)]
		do_episodes(game, test_ai, save_history = True,
			episode_label_ls = ["episode_idx=%d,pt_name=%s"%(episode_idx, name) for name in prob_name_ls],
			game_params_ls = [{"specified_stage": rel2abs("./handmade_stages/catcher_game/%s.json"%name)} for name in prob_name_ls]
		)
	train_ai = RandomPlayer(action_ls = game.action_ls, ai_obs = game.ai_obs)	# ランダムAI
	do_episodes(game, train_ai, game_params_ls = [{} for _ in range(30)], callback = rcpd_periodicTest, save_reward_ls = True)	# 複数エピソード実行
	test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
	do_episodes(game, test_ai, game_params_ls = [{} for _ in range(5)], save_history = True)	# 複数エピソード実行
	print("demo finished! (results are in \"./ezRL_demo_output/\".)")

# デモ [demo.py]
def demo(demo_name = "DQN-catcher"):
	if demo_name == "DQN-catcher":
		dqn_catcher_demo()	# デモ (DQN-catcher) [demo.py]
	elif demo_name == "Random-catcher":
		random_catcher_demo()	# デモ (Random-catcher) [demo.py]
	elif demo_name == "Random-catcher-PeriodicTest":
		random_catcher_periodicTest_demo()	# デモ (Random-catcher-PeriodicTest) [demo.py]
	else:
		raise Exception("[ezRL error] invalid demo name.")
