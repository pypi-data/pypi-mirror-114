
# エピソード関係処理 [episode.py]

import sys
import copy
import json
import resout as rout
import matplotlib.pyplot as plt
# 棋譜をjson形式で保存 [history.py]
from .history import save_history_json

# エピソードを実行 [episode.py]
def do_episode(game, ai, game_params, save_history = False, episode_label = None):
	# defaultのepisode_label
	if episode_label is None: episode_label = "no_name_episode"
	# state, actionの初期化
	action, state = "initial_action", game.gen_init_state(game_params)
	# 棋譜追記
	history_ls = []
	def add_history(state, action, reward):
		if save_history is True: state = copy.deepcopy(state)
		history_ls.append({"state": state, "action": action, "reward": reward})
	# ゲーム進行
	add_history(state, action, reward = None)	# 棋譜追記
	while state["finished"] is False:
		state, reward = game.game_step(state, action)
		action = ai.think(state, reward) # 行動決定
		add_history(state, action, reward)	# 棋譜追記
	# 棋譜の保存
	if save_history is True:
		save_history_json(history_ls, rout.gen_save_path(".json", label = episode_label))	# 棋譜をjson形式で保存 [history.py]
	return history_ls

# 棋譜から報酬合計値を算出
def reward_sum(history_ls):
	# reward一覧
	reward_ls = [step["reward"] for step in history_ls]
	# Noneを除く
	non_none_r_ls = [r for r in reward_ls if r is not None]
	# 合計を返す
	return sum(non_none_r_ls)

# episode結果・進捗の表示
def show_episode_result(episode_idx, episode_label, reward):
	if episode_label is None:
		episode_label_str = ""
	else:
		episode_label_str = " (%s)"%episode_label
	print("Episode #%d%s, Reward: %.1f"%(episode_idx, episode_label_str, reward))

# 複数エピソード実行 [episode.py]
def do_episodes(game, train_ai, game_params_ls, episode_label_ls = None, callback = None, save_history = False, save_reward_ls = False):
	if episode_label_ls is None: episode_label_ls = [None for _ in game_params_ls]
	total_reward_ls = []
	for episode_idx, game_params in enumerate(game_params_ls):
		history_ls = do_episode(game, train_ai, game_params, save_history, episode_label = episode_label_ls[episode_idx])	# エピソードを実行
		total_reward_ls.append(reward_sum(history_ls))	# 棋譜から報酬合計値を算出
		show_episode_result(episode_idx, episode_label_ls[episode_idx], total_reward_ls[-1])	# episode結果・進捗の表示
		# コールバック関数の実行
		if callback is not None: callback(train_ai, episode_idx)
	# 獲得報酬の推移を表示
	if save_reward_ls is True:
		plt.plot(total_reward_ls)
		plt.savefig(rout.gen_save_path(".png"))	# 保存ファイル名の生成(自動で連番になる) [resout]
