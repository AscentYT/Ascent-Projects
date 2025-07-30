import pickle
import neat
from snake_game import SnakeGame  

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = SnakeGame()
        fitness = 0
        frame = 0
        max_frames = 500

        while game.running and frame < max_frames:
            game.clock.tick(game.fps)
            inputs = game.get_inputs()

            output = net.activate(inputs)
            action = output.index(max(output))
            game.set_new_direction(action)

            game.update()
            fitness += 1 + (len(game.snake) - 1) * 10
            print(f"Output: {output}, Action: {action}")

            frame += 1

        genome.fitness = fitness


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    # Save the winner
    with open("best_snake_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Best genome saved to best_snake_genome.pkl")

def run_best_genome(config_file, genome_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    with open(genome_file, "rb") as f:
        genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    game = SnakeGame()
    fitness = 0
    frame = 0
    max_frames = 1000

    while game.running and frame < max_frames:
        game.clock.tick(game.fps)
        inputs = game.get_inputs()

        output = net.activate(inputs)
        action = output.index(max(output))
        game.set_new_direction(action)

        game.update()
        game.draw()
        fitness += 1 + (len(game.snake) - 1) * 10
        frame += 1

    print(f"Final fitness: {fitness}")
    print(f"Snake length: {len(game.snake)}")

train = False    

if __name__ == "__main__":
    if train:
        import os
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config-feedforward")
        run(config_path)
    else:
        import os
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config-feedforward")
        genome_path = os.path.join(local_dir, "best_snake_genome.pkl")
        run_best_genome(config_path, genome_path)