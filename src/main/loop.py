def loop(game, fail):
    fail.fail_loop()
    if game.player.lost is True:
        return
    game.main_loop()
    loop(game, fail)
