from game import Game # importamos o "game class" do game, acho que é assim que se fala

g = Game() # chamamos por aqui

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()