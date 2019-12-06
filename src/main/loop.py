def loop(game, fail):
    if fail.fail_loop():
        game.player.lifes = 3
        game.player.score = 0
        game.player.lost = False
        return
    if game.player.lost is True:
        return
    game.main_loop()
    loop(game, fail)
